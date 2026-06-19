import shutil
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SRC_DIR = BASE_DIR / "data" / "raw_photos"
TRAIN_DIR = BASE_DIR / "test_images" / "train"
VAL_DIR = BASE_DIR / "test_images" / "val"

random.seed(42)

for class_folder in SRC_DIR.iterdir():
    if not class_folder.is_dir():
        continue

    images = list(class_folder.glob("*.jpg")) + list(class_folder.glob("*.jpeg")) + list(class_folder.glob("*.png"))
    random.shuffle(images)
    split_idx = int(len(images) * 0.8)

    for i, img_path in enumerate(images):
        target_dir = (TRAIN_DIR if i < split_idx else VAL_DIR) / class_folder.name
        target_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy(img_path, target_dir / img_path.name)

    print(f"{class_folder.name}: train {split_idx}장, val {len(images) - split_idx}장")