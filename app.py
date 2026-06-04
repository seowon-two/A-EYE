import time
import re
from difflib import SequenceMatcher

import streamlit as st
from PIL import Image

# 기본 설정
st.set_page_config(
    page_title="AI 비상약품 안내 서비스",
    page_icon="💊",
    layout="wide",
)

# CSS 
st.markdown(
    """
    <style>
    .main {
        background-color: #F5F7FA;
    }

    .header-card {
        background-color: white;
        padding: 24px 30px;
        border-radius: 18px;
        border: 1px solid #DDE3EA;
        margin-bottom: 10px;
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

    .result-card {
        background-color: #F9FBFD;
        padding: 18px 20px;
        border-radius: 16px;
        border: 1px solid #E1E7EF;
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

    header[data-testid="stHeader"] {
        display: none;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    [data-testid="stToolbar"] {
        display: none;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1000px;
    }

    .tip-box-large {
    background-color: #1E3554;
    color: #9CC3FF;
    padding: 18px 24px;
    border-radius: 12px;
    font-size: 18px;
    line-height: 1.8;
    font-weight: 500;
    margin-top: 12px;
    margin-bottom: 16px;
    }

    .tip-box-large ul {
        margin: 0;
        padding-left: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# 세션 상태 초기화
if "state" not in st.session_state:
    # input / loading / success / fail
    st.session_state.state = "input"

if "uploaded_image" not in st.session_state:
    st.session_state.uploaded_image = None

if "result" not in st.session_state:
    st.session_state.result = None


# 더미 약품 DB (나중에 삭제)
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

# 유틸 함수
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

    # TODO: 실제 연결 시 이 부분 교체
    yolo_detected = True
    cropped_image = image

    # EasyOCR 결과라고 가정한 더미 텍스트
    dummy_ocr_text = "Ty1enol!!"
    # 실패 화면 테스트 시 값을 0.6 미만으로 낮추면 됨
    ocr_confidence = 0.92

    cleaned_text, best, candidates = match_medicine(dummy_ocr_text)


    if not yolo_detected or ocr_confidence < 0.6:
        # YOLO 탐지에 실패했거나 OCR 신뢰도가 기준값보다 낮으면 실패 결과를 반환
        return {
            "status": "fail",
            "reason": "OCR 신뢰도가 낮습니다.",
            "ocr_text": dummy_ocr_text,
            "confidence": ocr_confidence,
            "candidates": candidates,
            "cropped_image": cropped_image,
        }

    # OCR 신뢰도가 기준값 이상이면 성공 결과를 반환
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
            <div class="main-title">💊 A-EYE</div>
            <div class="sub-title">
            약품 사진을 업로드하면 약 이름과 복용법, 주의사항을 음성으로 안내해드립니다.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# 1. 메인 / 이미지 입력 화면
def show_input_screen():
    st.subheader("약품 이미지 입력")
    st.write("카메라로 약품을 촬영하거나 이미지 파일을 업로드하세요.")
    
    left_space, input_area, right_space = st.columns([0.3, 3.4, 0.3])

    with input_area:
        camera_image = st.camera_input("📸 약품 촬영")

        st.markdown(
            """
            <div style='color:#D32F2F; font-size:14px; font-weight:600; margin-top:6px; margin-bottom:18px;'>
                사진을 다시 찍으려면 Clear photo를 누른 뒤 다시 촬영해주세요.
            </div>
            """,
            unsafe_allow_html=True,
        )

        uploaded_file = st.file_uploader(
            "이미지 파일 업로드",
            type=["jpg", "jpeg", "png"],
        )

        selected_image = camera_image or uploaded_file

        if selected_image is not None:
            image = Image.open(selected_image)
            st.session_state.uploaded_image = image

            st.image(
                image,
                caption="입력된 약품 이미지",
                use_container_width=True,
            )

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
    st.subheader("약품 정보 분석")
    st.write("약품명과 복용 정보를 확인할 준비가 되었습니다.")

    if st.session_state.uploaded_image is not None:
        st.image(
            st.session_state.uploaded_image,
            caption="분석 대상 이미지",
            width=420,
        )

    st.info("아래 버튼을 누르면 약품 정보 분석을 시작합니다.")

    if st.button("약품 정보 분석 실행", use_container_width=True):
        progress = st.progress(0)
        status_text = st.empty()

        steps = [
            "약품 사진을 확인하고 있습니다...",
            "약품명을 인식하고 있습니다...",
            "복용 정보를 찾고 있습니다...",
            "주의사항을 확인하고 있습니다...",
            "음성 안내를 준비하고 있습니다...",
        ]

        for i, step in enumerate(steps):
            status_text.info(step)
            progress.progress((i + 1) / len(steps))
            time.sleep(0.8)

        result = run_ai_pipeline(st.session_state.uploaded_image)
        st.session_state.result = result

        status_text.success("분석이 완료되었습니다.")
        progress.progress(1.0)
        time.sleep(0.8)

        if result["status"] == "success":
            st.session_state.state = "success"
        else:
            st.session_state.state = "fail"

        st.rerun()

# 3. 분석 결과 / 음성 안내 화면
def show_success_screen():
    result = st.session_state.result
    medicine = result["medicine"]

    left, right = st.columns([1, 1.5], gap="large")

    with left:
        st.subheader("입력 이미지 미리보기")
        st.write("탐지된 약품 이미지를 확인합니다.")

        img_l, img_c, img_r = st.columns([0.1, 1.3, 0.1])
        with img_c:
            st.image(
                result["cropped_image"],
                caption="탐지된 약품 영역",
                use_container_width=True,
            )

        st.markdown(
            f"""
            <div class="result-card">
                <div class="label">인식된 글자</div>
                <div class="value">{result["ocr_text"]}</div>
            </div>

            <div class="result-card">
                <div class="label">확인한 약품명</div>
                <div class="value">{medicine["name_ko"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        confidence_percent = int(result["confidence"] * 100)

        guide_text = (
            f"{medicine['name_ko']}입니다. "
            f"{medicine['dosage']} "
            f"주의사항으로 {medicine['warning']}"
        )

        st.subheader("분석 결과")
        st.write("약품 이미지 분석을 통해 확인된 정보입니다.")

        st.success(f"인식된 약품: {medicine['name_ko']} / {medicine['name_en']}")
        st.write(f"정확도: {confidence_percent}%")

        st.markdown("### 복용법")
        st.info(medicine["dosage"])

        st.markdown("### 주의사항")
        st.warning(medicine["warning"])

        st.markdown("### 음성 안내 문장")
        st.write(guide_text)

        st.caption("현재 코드는 화면 구성용입니다. (TTS 음성 모듈과 연결 전)")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("음성으로 다시 듣기", use_container_width=True):
                st.success("음성 안내를 실행합니다.")
                st.write(guide_text)

        with col2:
            if st.button("다른 약품 분석하기", use_container_width=True):
                reset_app()
                st.rerun()

# 4. 인식 실패 / 복수 후보 화면
def show_fail_screen():
    result = st.session_state.result

    left, right = st.columns([1, 1.5], gap="large")

    with left:
        st.subheader("입력 이미지 미리보기")
        st.write("인식이 불안정했던 이미지를 확인합니다.")

        if result and result.get("cropped_image") is not None:
            img_l, img_c, img_r = st.columns([0.1, 1.3, 0.1])

            with img_c:
                st.image(
                    result["cropped_image"],
                    caption="인식 실패 이미지",
                    use_container_width=True,
                )
        st.markdown(
            """
            <div class="tip-box-large">
                <ul>
                    <li>약품명이 화면 중앙에 오게<br>해주세요.</li>
                    <li>흔들리지 않게 촬영해주세요.</li>
                    <li>빛 반사를 피해주세요.</li>
                    <li>포장지의 글자가 잘 보이게<br>해주세요.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        confidence_percent = int(result["confidence"] * 100) if result else 0

        st.subheader("인식 실패 또는 복수 후보")
        st.write("약품명이 선명하게 인식되지 않았습니다. 아래 후보를 확인하거나 다시 촬영해주세요.")

        st.error(f"약품 정보를 정확히 확인하지 못했습니다.")
        st.write(f"정확도: {confidence_percent}%")

        st.error("다시 촬영하거나 아래 후보 약품을 확인해주세요.")

        if result and result.get("candidates"):
            st.markdown("### 유사 약품 후보")

            for candidate in result["candidates"]:
                info = candidate["info"]
                score = int(candidate["score"] * 100)

                st.warning(
                    f"후보 약품: {info['name_ko']} / {info['name_en']}\n\n"
                    f"문자열 유사도: {score}%"
                )

        col1, col2 = st.columns(2)

        with col1:
            if st.button("다시 촬영하기", use_container_width=True):
                reset_app()
                st.rerun()

        # TODO: 후보 약품 선택 시 해당 약품 정보를 최종 안내 화면으로 전달,
        # Web Speech API 또는 TTS 모듈과 연결하여 복용법과 주의사항을 음성으로 출력
        with col2:
            if st.button("후보 확인하기", use_container_width=True):
                st.warning("선택한 후보의 복용법과 주의사항 안내 기능은 추후 연결 예정입니다.")

# 메인 실행
show_header()

if st.session_state.state == "input":
    show_input_screen()

elif st.session_state.state == "loading":
    show_loading_screen()

elif st.session_state.state == "success":
    show_success_screen()

elif st.session_state.state == "fail":
    show_fail_screen()