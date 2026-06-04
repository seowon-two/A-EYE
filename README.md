<YOLO 기반 약품 객체 탐지 및 Crop 프로젝트>

1. 프로젝트 개요

본 프로젝트는 YOLOv8 모델을 활용하여 약품 패키지 이미지에서 객체를 탐지하고,
탐지된 영역을 Bounding Box 기반으로 분리하여 Crop 이미지로 저장하는 기능을 구현한다.

추후 OCR 시스템과 연계하여 약품명 인식 성능을 향상시키는 것을 목표로 한다.

2. 사용 모델

YOLOv8 (Ultralytics)
Custom trained model: best.pt

3. 주요 기능
✔ 1) 객체 탐지 (Object Detection)
입력 이미지에서 약품 객체 탐지
Bounding Box 좌표(x1, y1, x2, y2) 추출
✔ 2) Bounding Box 시각화
탐지된 객체를 이미지에 박스로 표시
✔ 3) Crop 기능
Bounding Box 영역만 잘라서 개별 이미지로 저장
✔ 4) 결과 저장
bbox 이미지 저장
crop 이미지 개별 저장

4. 구현 함수
detect_and_crop()
def detect_and_crop(model_path, image_path):
->
YOLO 모델 로드
이미지 객체 탐지 수행
bbox 좌표 추출
객체 영역 crop
crop 이미지 저장
저장된 파일 리스트 반환

5. 실행 방법
1) 필수 라이브러리 설치
pip install ultralytics opencv-python

2) 실행 코드
from detect_and_crop import detect_and_crop

saved_files = detect_and_crop(
    "best.pt",
    "test.jpg"
)

print(saved_files)

6. 결과 예시
✔ Bounding Box Detection
약품 패키지 영역 정상 탐지 확인
✔ Crop Result
탐지된 객체만 잘라서 저장 성공

7. 테스트 이미지

총 13개 약품 이미지에 대해 테스트 수행:

band_01.jpg
bearse_01.jpg
eyedrop_multi_01.jpg
eyedrop_single_17.jpg
ezen6_01.jpg
festal_01.jpg
fusidin_01.jpg
madecassol_01.jpg
pancol_01.jpg
panpirin_01.jpg
patch_01.jpg
geborin_02.jpg

8. 분석 (Analysis)

YOLO 모델을 이용하여 다양한 약품 패키지 이미지를 테스트한 결과,
대부분의 이미지에서 약품 객체가 정확하게 탐지되었다.

Bounding Box 기반 Crop 기능 또한 정상적으로 동작하여
OCR 입력 전처리 단계로 활용 가능함을 확인하였다.

특히 복잡한 배경이나 다양한 조명 조건에서도
약품 영역을 안정적으로 탐지하는 것을 확인하였다.

9. 결론 (Conclusion)

YOLOv8 기반 객체 탐지 모델을 활용하여
약품 이미지에서 객체 탐지 및 Crop 기능을 성공적으로 구현하였다.

본 결과는 OCR 시스템과 결합하여
약품명 인식 성능을 향상시키는 전처리 단계로 활용될 수 있다.
