from pathlib import Path
from src.model_connector import detect_medicine_with_logging

BASE_DIR = Path(__file__).resolve().parent
TRAIN_DIR = BASE_DIR / "test_images" / "train"

image_extensions = ["*.jpg", "*.jpeg", "*.png"]

for class_folder in TRAIN_DIR.iterdir():
    if not class_folder.is_dir():
        continue

    true_label = class_folder.name
    image_paths = []
    for ext in image_extensions:
        image_paths.extend(class_folder.glob(ext))

    for img_path in image_paths:
        detect_medicine_with_logging(img_path, true_label)
        print(f"[{true_label}] {img_path.name} 처리 완료")

print("전체 평가 완료. logs/detection_log.csv 확인하세요.")