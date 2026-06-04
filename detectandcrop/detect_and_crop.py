from ultralytics import YOLO
import cv2

def detect_and_crop(model_path, image_path):
    # YOLO 모델 로드 (학습된 best.pt 등)
    model = YOLO(model_path)

    # 입력 이미지에 대해 객체 탐지 수행
    results = model(image_path)

    # 원본 이미지 읽기
    img = cv2.imread(image_path)

    # 저장된 crop 이미지 파일명을 담을 리스트
    saved_files = []

    # 탐지된 모든 객체의 bbox(x1, y1, x2, y2) 순회
    for i, box in enumerate(results[0].boxes.xyxy.cpu().numpy()):

        # bbox 좌표를 정수형으로 변환
        x1, y1, x2, y2 = map(int, box)

        # bbox 영역만 잘라내기 (crop)
        crop = img[y1:y2, x1:x2]

        # 저장할 파일명 생성
        # 예: crop_0.jpg, crop_1.jpg ...
        filename = f"crop_{i}.jpg"

        # crop 이미지 저장
        cv2.imwrite(filename, crop)

        # 저장된 파일명을 리스트에 추가
        saved_files.append(filename)

    # 저장된 crop 이미지 파일명 목록 반환
    return saved_files
