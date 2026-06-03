import time
import re
from difflib import SequenceMatcher

import streamlit as st
from PIL import Image


# =========================
# 기본 설정
# =========================
st.set_page_config(
    page_title="AI 비상약품 안내 서비스",
    page_icon="💊",
    layout="wide",
)

# =========================
# CSS 스타일
# =========================
st.markdown(
    """
    <style>
    .main {
        background-color: #F5F7FA;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }

    .header-card {
        background-color: white;
        padding: 28px 34px;
        border-radius: 20px;
        border: 1px solid #DDE3EA;
        margin-bottom: 24px;
    }

    .main-title {
        font-size: 34px;
        font-weight: 800;
        color: #1F2937;
        margin-bottom: 8px;
    }

    .sub-title {
        font-size: 17px;
        color: #5B6778;
    }

    .section-card {
        background-color: white;
        padding: 26px;
        border-radius: 20px;
        border: 1px solid #DDE3EA;
        min-height: 520px;
    }

    .section-title {
        font-size: 22px;
        font-weight: 700;
        color: #1F2937;
        margin-bottom: 8px;
    }

    .section-desc {
        font-size: 15px;
        color: #667085;
        margin-bottom: 18px;
    }

    .result-card {
        background-color: #F9FBFD;
        padding: 18px 20px;
        border-radius: 16px;
        border: 1px solid #E1E7EF;
        margin-bottom: 16px;
    }

    .success-card {
        background-color: #EBF7EC;
        padding: 18px 20px;
        border-radius: 16px;
        border: 1px solid #BFDCC4;
        margin-bottom: 16px;
    }

    .warning-card {
        background-color: #FFF8E1;
        padding: 18px 20px;
        border-radius: 16px;
        border: 1px solid #E8D99B;
        margin-bottom: 16px;
    }

    .error-card {
        background-color: #FFEBEE;
        padding: 18px 20px;
        border-radius: 16px;
        border: 1px solid #F0B8BE;
        margin-bottom: 16px;
    }

    .label {
        font-size: 14px;
        color: #667085;
        margin-bottom: 4px;
    }

    .value {
        font-size: 22px;
        font-weight: 700;
        color: #1F2937;
    }

    .big-value {
        font-size: 30px;
        font-weight: 800;
        color: #2E7D32;
    }

    .flow-box {
        background-color: white;
        padding: 20px;
        border-radius: 18px;
        border: 1px solid #DDE3EA;
        margin-top: 22px;
    }

    .flow-step {
        background-color: #EBF3FC;
        padding: 14px;
        border-radius: 14px;
        text-align: center;
        font-weight: 700;
        color: #1F4E79;
        border: 1px solid #C8DAED;
    }

    .tip {
        font-size: 14px;
        color: #667085;
        background-color: #F9FBFD;
        padding: 14px 16px;
        border-radius: 12px;
        border: 1px solid #E1E7EF;
        margin-top: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================
# 세션 상태 초기화
# =========================
if "state" not in st.session_state:
    # input / loading / success / fail
    st.session_state.state = "input"

if "uploaded_image" not in st.session_state:
    st.session_state.uploaded_image = None

if "result" not in st.session_state:
    st.session_state.result = None


# =========================
# 더미 약품 DB
# =========================
MEDICINE_DB = {
    "tylenol": {
        "name_ko": "타이레놀",
        "name_en": "Tylenol",
        "dosage": "하루 3회 식후 복용하세요.",
        "warning": "공복 복용을 피하고, 정해진 복용량을 초과하지 마세요.",
    },
    "tacenol": {
        "name_ko": "타세놀",
        "name_en": "Tacenol",
        "dosage": "성인 기준 1회 1정을 복용하세요.",
        "warning": "다른 해열진통제와 중복 복용하지 마세요.",
    },
    "fucidin": {
        "name_ko": "후시딘",
        "name_en": "Fucidin",
        "dosage": "상처 부위에 하루 1~2회 얇게 바르세요.",
        "warning": "눈이나 입 주변에 들어가지 않도록 주의하세요.",
    },
}


# =========================
# 유틸 함수
# =========================
def clean_text(text: str) -> str:
    """
    OCR 결과 문자열을 정제하는 함수.
    예: Ty1enol!! -> tylenol
    """
    text = text.lower()
    text = text.replace("1", "l")
    text = re.sub(r"[^a-z가-힣0-9]", "", text)
    return text


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()


def match_medicine(ocr_text: str):
    """
    OCR 텍스트와 약품 DB를 비교해서 가장 유사한 약품을 찾는 함수.
    """
    cleaned = clean_text(ocr_text)

    candidates = []
    for key, info in MEDICINE_DB.items():
        score = similarity(cleaned, key)
        candidates.append(
            {
                "key": key,
                "score": score,
                "info": info,
            }
        )

    candidates.sort(key=lambda x: x["score"], reverse=True)
    best = candidates[0]

    return cleaned, best, candidates[:2]


def run_ai_pipeline(image):
    """
    나중에 YOLO/OCR 실제 코드가 들어갈 자리.

    현재 흐름:
    1. YOLOv8 객체 탐지
    2. 약품 영역 Crop
    3. EasyOCR 문자 인식
    4. RegEx 정제
    5. DB 매칭
    6. 결과 반환
    """

    # 분석 진행처럼 보이기 위한 대기
    time.sleep(1)

    # =========================
    # TODO: 실제 연결 시 이 부분 교체
    # =========================
    yolo_detected = True
    cropped_image = image

    # EasyOCR 결과라고 가정한 더미 텍스트
    dummy_ocr_text = "Ty1enol!!"
    ocr_confidence = 0.92

    cleaned_text, best, candidates = match_medicine(dummy_ocr_text)

    # 실패 상황 테스트하고 싶으면 아래 값을 낮춰보면 됨
    # ocr_confidence = 0.45

    if not yolo_detected or ocr_confidence < 0.6:
        return {
            "status": "fail",
            "reason": "OCR 신뢰도가 낮습니다.",
            "ocr_text": dummy_ocr_text,
            "confidence": ocr_confidence,
            "candidates": candidates,
            "cropped_image": cropped_image,
        }

    return {
        "status": "success",
        "ocr_text": dummy_ocr_text,
        "cleaned_text": cleaned_text,
        "confidence": ocr_confidence,
        "medicine": best["info"],
        "candidates": candidates,
        "cropped_image": cropped_image,
    }


def reset_app():
    st.session_state.state = "input"
    st.session_state.uploaded_image = None
    st.session_state.result = None


def show_header():
    st.markdown(
        """
        <div class="header-card">
            <div class="main-title">AI 비상약품 안내 서비스</div>
            <div class="sub-title">
                약품 이미지를 업로드하거나 촬영하면 YOLOv8, EasyOCR 기반 분석을 통해 약품명, 복용법, 주의사항을 안내합니다.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================
# 상태 1. 메인 / 이미지 입력 화면
# =========================
def show_input_screen():
    st.subheader("약품 이미지 입력")
    st.write("카메라로 약품을 촬영하거나 이미지 파일을 업로드하세요.")

    camera_image = st.camera_input("카메라로 촬영하기")

    uploaded_file = st.file_uploader(
        "이미지 파일 업로드",
        type=["jpg", "jpeg", "png"],
    )

    selected_image = camera_image or uploaded_file

    if selected_image is not None:
        image = Image.open(selected_image)
        st.session_state.uploaded_image = image
        st.image(image, caption="입력된 약품 이미지", use_container_width=True)

    st.info(
        "촬영 팁: 약품명과 복용법이 잘 보이도록 정면에서 촬영하고, "
        "빛 반사와 흔들림을 피해주세요."
    )

    if st.button("분석 시작하기", use_container_width=True):
        if st.session_state.uploaded_image is None:
            st.warning("먼저 약품 이미지를 촬영하거나 업로드해주세요.")
        else:
            st.session_state.state = "loading"
            st.rerun()

# 2. 분석 진행 화면
def show_loading_screen():
    left, right = st.columns([1, 1.2], gap="large")

    with left:
        st.markdown(
            """
            <div class="section-card">
                <div class="section-title">업로드된 이미지</div>
                <div class="section-desc">현재 분석 중인 약품 이미지입니다.</div>
            """,
            unsafe_allow_html=True,
        )

        if st.session_state.uploaded_image is not None:
            st.image(
                st.session_state.uploaded_image,
                caption="분석 대상 이미지",
                use_container_width=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown(
            """
            <div class="section-card">
                <div class="section-title">AI 분석 진행 중</div>
                <div class="section-desc">
                    YOLOv8, Crop, EasyOCR, DB 매칭 단계를 순차적으로 수행합니다.
                </div>
            """,
            unsafe_allow_html=True,
        )

        progress = st.progress(0)
        status = st.empty()

        steps = [
            "YOLOv8 객체 탐지 중...",
            "약품 영역 Crop 생성 중...",
            "EasyOCR 문자 인식 중...",
            "OCR 결과 정제 및 DB 매칭 중...",
            "음성 안내 문장 생성 중...",
        ]

        for i, step in enumerate(steps):
            status.info(step)
            progress.progress((i + 1) / len(steps))
            time.sleep(0.5)

        result = run_ai_pipeline(st.session_state.uploaded_image)
        st.session_state.result = result

        if result["status"] == "success":
            st.session_state.state = "success"
        else:
            st.session_state.state = "fail"

        st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)


# 3. 분석 결과 / 음성 안내 화면
def show_success_screen():
    result = st.session_state.result
    medicine = result["medicine"]

    left, right = st.columns([1, 1.3], gap="large")

    with left:
        st.markdown(
            """
            <div class="section-card">
                <div class="section-title">입력 이미지 미리보기</div>
                <div class="section-desc">
                    YOLOv8이 탐지한 약품 이미지를 확인합니다.
                </div>
            """,
            unsafe_allow_html=True,
        )

        st.image(
            result["cropped_image"],
            caption="탐지된 약품 영역",
            use_container_width=True,
        )

        st.markdown(
            f"""
            <div class="result-card">
                <div class="label">OCR 원문</div>
                <div class="value">{result["ocr_text"]}</div>
            </div>

            <div class="result-card">
                <div class="label">정제된 문자열</div>
                <div class="value">{result["cleaned_text"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        confidence_percent = int(result["confidence"] * 100)

        guide_text = (
            f"{medicine['name_ko']}입니다. "
            f"{medicine['dosage']} "
            f"주의사항으로 {medicine['warning']}"
        )

        st.markdown(
            f"""
            <div class="section-card">
                <div class="section-title">분석 결과</div>
                <div class="section-desc">
                    OCR 결과와 약품 데이터베이스를 매칭한 최종 결과입니다.
                </div>

                <div class="success-card">
                    <div class="label">인식된 약품</div>
                    <div class="big-value">{medicine["name_ko"]}</div>
                    <p>{medicine["name_en"]} · 신뢰도 {confidence_percent}%</p>
                </div>

                <div class="result-card">
                    <div class="label">복용법</div>
                    <div class="value">{medicine["dosage"]}</div>
                </div>

                <div class="result-card">
                    <div class="label">주의사항</div>
                    <div class="value">{medicine["warning"]}</div>
                </div>

                <div class="result-card">
                    <div class="label">음성 안내 문장</div>
                    <p>{guide_text}</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.info("현재 코드는 화면 구성용입니다. 실제 TTS는 팀원이 만든 음성 모듈과 연결하면 됩니다.")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("음성으로 다시 듣기", use_container_width=True):
                st.success("음성 안내를 실행합니다. 실제 구현 시 TTS 함수와 연결하세요.")
                st.write(guide_text)

        with col2:
            if st.button("다른 약품 분석하기", use_container_width=True):
                reset_app()
                st.rerun()


# =========================
# 상태 4. 인식 실패 / 복수 후보 화면
# =========================
def show_fail_screen():
    result = st.session_state.result

    left, right = st.columns([1, 1.3], gap="large")

    with left:
        st.markdown(
            """
            <div class="section-card">
                <div class="section-title">입력 이미지</div>
                <div class="section-desc">
                    인식이 불안정했던 이미지입니다.
                </div>
            """,
            unsafe_allow_html=True,
        )

        if result and result.get("cropped_image") is not None:
            st.image(
                result["cropped_image"],
                caption="인식 실패 이미지",
                use_container_width=True,
            )

        st.markdown(
            """
            <div class="tip">
                재촬영 팁<br>
                - 약품명이 화면 중앙에 오도록 촬영<br>
                - 흔들리지 않게 촬영<br>
                - 빛 반사 피하기<br>
                - 약품 포장지의 글자가 잘 보이게 촬영
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        confidence_percent = int(result["confidence"] * 100) if result else 0

        st.markdown(
            f"""
            <div class="section-card">
                <div class="section-title">인식 실패 또는 복수 후보</div>
                <div class="section-desc">
                    OCR 신뢰도가 낮거나 유사 약품이 여러 개 존재하는 경우입니다.
                </div>

                <div class="error-card">
                    <div class="label">오류 원인</div>
                    <div class="value">약품 인식 정확도가 낮습니다.</div>
                    <p>현재 OCR 신뢰도: {confidence_percent}%</p>
                </div>

                <div class="warning-card">
                    <div class="label">안내</div>
                    <div class="value">다시 촬영하거나 후보 약품을 확인해주세요.</div>
                </div>
            """,
            unsafe_allow_html=True,
        )

        if result and result.get("candidates"):
            st.markdown("#### 유사 약품 후보")

            for candidate in result["candidates"]:
                info = candidate["info"]
                score = int(candidate["score"] * 100)

                st.markdown(
                    f"""
                    <div class="result-card">
                        <div class="label">후보 약품</div>
                        <div class="value">{info["name_ko"]} / {info["name_en"]}</div>
                        <p>문자열 유사도: {score}%</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.markdown("</div>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            if st.button("다시 촬영하기", use_container_width=True):
                reset_app()
                st.rerun()

        with col2:
            if st.button("후보 선택 후 안내", use_container_width=True):
                st.warning("실제 구현 시 선택한 후보의 복용법과 주의사항을 안내하도록 연결하세요.")


# =========================
# 메인 실행
# =========================
show_header()

if st.session_state.state == "input":
    show_input_screen()

elif st.session_state.state == "loading":
    show_loading_screen()

elif st.session_state.state == "success":
    show_success_screen()

elif st.session_state.state == "fail":
    show_fail_screen()