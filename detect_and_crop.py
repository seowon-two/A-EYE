from ultralytics import YOLO
import cv2

def detect_and_crop(model_path, image_path):
    model = YOLO(model_path)

    results = model(image_path)

    img = cv2.imread(image_path)

    saved_files = []

    for i, box in enumerate(results[0].boxes.xyxy.cpu().numpy()):
        x1, y1, x2, y2 = map(int, box)

        crop = img[y1:y2, x1:x2]

        filename = f"crop_{i}.jpg"

        cv2.imwrite(filename, crop)

        saved_files.append(filename)

    return saved_files