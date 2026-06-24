from src.model_connector import detect_medicine
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
RAW_DIR = BASE_DIR / "data" / "raw_photos"

CLASSES = ["bearse", "ezen6", "madecassol", "pancol", "patch"]

for class_name in CLASSES:
    img_path = sorted((RAW_DIR / class_name).glob("*.jpg"))[0]
    result = detect_medicine(str(img_path))
    print(f"{class_name}: 결과={result['class_name']}, confidence={result['confidence']:.3f}, detected={result['detected']}")