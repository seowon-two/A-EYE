from ultralytics import YOLO
import json
from pathlib import Path
import streamlit as st
import csv
from datetime import datetime

# 프로젝트 루트 경로: A-EYE
BASE_DIR = Path(__file__).resolve().parent.parent

# models 폴더 경로
MODEL_DIR = BASE_DIR / "models"

# DB 경로
DB_PATH = BASE_DIR / "DB" / "medicine_db.json"

# 모든 YOLO 모델 로드
MODEL_PATHS = {
    "band": MODEL_DIR / "band_best.pt",
    "bearse": MODEL_DIR / "bearse_best.pt",
    "eyedrop-multi": MODEL_DIR / "eyedrop_multi_best.pt",
    "eyedrop-single": MODEL_DIR / "eyedrop_single_best.pt",
    "ezen6": MODEL_DIR / "ezen6_best.pt",
    "festal": MODEL_DIR / "festal_best.pt",
    "fusidin": MODEL_DIR / "fusidin_best.pt",
    "geborin": MODEL_DIR / "geborin_best.pt",
    "madecassol": MODEL_DIR / "madecassol_best.pt",
    "pancol": MODEL_DIR / "pancol_best.pt",
    "panpirin": MODEL_DIR / "panpirin_best.pt",
    "patch": MODEL_DIR / "patch_best.pt",
    "tylenol": MODEL_DIR / "tylenol_best.pt",
}

# YOLO 모델 캐싱 (최초 1회 로드 후 재사용)
@st.cache_resource
def load_models():
    return {
        class_name: YOLO(model_path)
        for class_name, model_path in MODEL_PATHS.items()
    }

# DB 로드
@st.cache_data
def load_db():
    with open(DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

# 약품 정보 조회
def get_medicine_info(class_name):
    db = load_db()

    for medicine in db["medicine_db"]:
        if medicine["class_name"] == class_name:
            return medicine

    return None

# AI 모델 + DB 연결 함수
def detect_medicine(image_path):
    models = load_models()

    results_list = []  

    for class_name, model in models.items():
        results = model(image_path)

        if len(results[0].boxes) > 0:
            confidence = float(results[0].boxes.conf.max())
            results_list.append((class_name, confidence))

    # 검출된 게 하나도 없으면 바로 실패
    if len(results_list) == 0:
        return {
            "detected": False,
            "class_name": None,
            "confidence": 0,
            "medicine_info": None
        }

    # confidence 높은 순으로 정렬
    results_list.sort(key=lambda x: x[1], reverse=True)
    print("DEBUG results_list:", results_list)

    best_class_name, best_confidence = results_list[0]

    # 클래스별 margin threshold (patch는 다른 클래스와 헷갈림이 심해 더 낮은 기준 적용)
    DEFAULT_MARGIN_THRESHOLD = 0.06
    CLASS_MARGIN_OVERRIDES = {
        "patch": 0.04,
    }
    margin_threshold = CLASS_MARGIN_OVERRIDES.get(best_class_name, DEFAULT_MARGIN_THRESHOLD)

    # 2위가 있으면 margin 계산, 없으면 margin 조건 생략
    if len(results_list) >= 2:
        second_class_name, second_confidence = results_list[1]
        margin = best_confidence - second_confidence
    else:
        second_class_name, second_confidence = None, 0
        margin = 1.0  # 경쟁자가 없으니 margin 통과시킴

    detected = (best_confidence >= 0.80) and (margin >= margin_threshold)

    if detected:
        info = get_medicine_info(best_class_name)
        return {
            "detected": True,
            "class_name": best_class_name,
            "confidence": best_confidence,
            "medicine_info": info
        }

    return {
        "detected": False,
        "class_name": None,
        "confidence": best_confidence,
        "medicine_info": None
    }

LOG_PATH = BASE_DIR / "logs" / "detection_log.csv"

def detect_medicine_with_logging(image_path, true_label):
    """
    평가용 함수. true_label(정답 클래스명)을 받아서
    13개 모델 전체의 결과를 CSV에 기록한다.
    실제 서비스(detect_medicine)에는 영향 없음.
    """
    models = load_models()
    results_list = []

    for class_name, model in models.items():
        results = model(image_path)
        if len(results[0].boxes) > 0:
            confidence = float(results[0].boxes.conf.max())
            results_list.append((class_name, confidence))

    results_list.sort(key=lambda x: x[1], reverse=True)

    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    file_exists = LOG_PATH.exists()

    with open(LOG_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "image_path", "true_label", "rank", "pred_label", "confidence"])

        if len(results_list) == 0:
            writer.writerow([datetime.now().isoformat(), str(image_path), true_label, 0, None, 0.0])
        else:
            for rank, (label, conf) in enumerate(results_list, start=1):
                writer.writerow([datetime.now().isoformat(), str(image_path), true_label, rank, label, conf])

    return results_list