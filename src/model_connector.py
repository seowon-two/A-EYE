from ultralytics import YOLO
import json

# 모든 YOLO 모델 로드
models = {
    "band": YOLO("best.pt/band_best.pt"),
    "bearse": YOLO("best.pt/bearse_best.pt"),
    "eyedrop-multi": YOLO("best.pt/eyedrop_multi_best.pt"),
    "eyedrop-single": YOLO("best.pt/eyedrop_single_best.pt"),
    "ezen6": YOLO("best.pt/ezen6_best.pt"),
    "festal": YOLO("best.pt/festal_best.pt"),
    "fusidin": YOLO("best.pt/fusidin_best.pt"),
    "geborin": YOLO("best.pt/geborin_best.pt"),
    "madecassol": YOLO("best.pt/madecassol_best.pt"),
    "pancol": YOLO("best.pt/pancol_best.pt"),
    "panpirin": YOLO("best.pt/panpirin_best.pt"),
    "patch": YOLO("best.pt/patch_best.pt"),
    "tylenol": YOLO("best.pt/tylenol_best.pt")
}

# DB 로드
def load_db():
    with open("medicine_db.json", "r", encoding="utf-8") as f:
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

    for class_name, model in models.items():

        results = model(image_path)

        # 약품 검출 성공
        if len(results[0].boxes) > 0:

            info = get_medicine_info(class_name)

            return {
                "detected": True,
                "class_name": class_name,
                "medicine_info": info
            }

    # 어떤 약품도 검출되지 않음
    return {
        "detected": False,
        "class_name": None,
        "medicine_info": None
    }
