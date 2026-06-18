import time
import streamlit as st
from PIL import Image
import tempfile

from src.model_connector import detect_medicine
from src.tts import speak_medicine_info

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

def run_ai_pipeline(image):
    
    """
    실제 AI 모델 + DB + TTS 연결 함수

    흐름:
    1. Streamlit에서 받은 PIL 이미지를 임시 파일로 저장
    2. YOLO 모델에 이미지 경로 전달
    3. 약품 인식 결과 확인
    4. DB에서 가져온 약품 정보 확인
    5. TTS 음성 파일 생성
    6. app.py 화면에서 사용할 결과 반환
    """

    # 1. PIL 이미지를 임시 jpg 파일로 저장
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        image = image.convert("RGB")
        image.save(tmp.name)
        image_path = tmp.name

    # 2. AI 모델 실행
    detection_result = detect_medicine(image_path)

    # 3. 약품 인식 실패
    if not detection_result["detected"]:
        return {
            "status": "fail",
            "reason": "약품을 인식하지 못했습니다.",
            "confidence": detection_result.get("confidence", 0),
            "medicine": None,
            "audio_path": None,
            "cropped_image": image,
        }

    # 4. 약품 정보 가져오기
    medicine = detection_result["medicine_info"]

    # 5. DB 정보가 없을 때
    if medicine is None:
        return {
            "status": "fail",
            "reason": "DB에서 약품 정보를 찾지 못했습니다.",
            "confidence": detection_result.get("confidence", 0),
            "medicine": None,
            "audio_path": None,
            "cropped_image": image,
        }

    # 6. TTS 음성 파일 생성
    audio_path = speak_medicine_info(medicine)

    # 7. 성공 결과 반환
    return {
        "status": "success",
        "class_name": detection_result["class_name"],
        "medicine": medicine,
        "audio_path": audio_path,
        "cropped_image": image,
        "confidence": detection_result["confidence"],
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
                <div class="label">인식된 약품 클래스</div>
                <div class="value">{result["class_name"]}</div>
            </div>

            <div class="result-card">
                <div class="label">확인한 약품명</div>
                <div class="value">{medicine["ko_name"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        guide_text = (
            f"{medicine['ko_name']}입니다. "
            f"{medicine['guide']} "
            f"{medicine['usage']} "
            f"주의사항: {medicine['warning']}"
        )

        st.subheader("분석 결과")
        st.write("약품 이미지 분석을 통해 확인된 정보입니다.")

        st.success(f"인식된 약품: {medicine['ko_name']}")

        st.markdown("### 안내")
        st.info(medicine["guide"])

        st.markdown("### 복용법")
        st.info(medicine["usage"])

        st.markdown("### 주의사항")
        st.warning(medicine["warning"])

        st.markdown("### 음성 안내 문장")
        st.write(guide_text)

        st.markdown("### 음성 안내")
        st.audio(result["audio_path"], format="audio/mp3")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("음성으로 다시 듣기", use_container_width=True):
                st.audio(result["audio_path"], format="audio/mp3")

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
        st.subheader("인식 실패")
        st.error("약품 정보를 정확히 확인하지 못했습니다.")

        if result and result.get("reason"):
            st.write(f"실패 이유: {result['reason']}")

        st.warning("다시 촬영하거나 더 선명한 이미지를 업로드해주세요.")

        if st.button("다시 촬영하기", use_container_width=True):
            reset_app()
            st.rerun()

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