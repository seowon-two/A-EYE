from src.model_connector import detect_medicine
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
RAW_DIR = BASE_DIR / "data" / "raw_photos"

CLASSES = [
    "band", "bearse", "eyedrop-multi", "eyedrop-single", "ezen6",
    "festal", "fusidin", "geborin", "madecassol", "pancol",
    "panpirin", "patch", "tylenol",
]

results = []

for class_name in CLASSES:
    class_dir = RAW_DIR / class_name
    if not class_dir.exists():
        print(f"[건너뜀] {class_name} 폴더 없음")
        continue

    images = sorted(class_dir.glob("*.jpg"))
    if not images:
        print(f"[건너뜀] {class_name} 사진 없음")
        continue

    img_path = images[0]
    result = detect_medicine(str(img_path))

    is_correct = (result["class_name"] == class_name)
    results.append({
        "기대": class_name,
        "결과": result["class_name"],
        "confidence": round(result["confidence"], 3),
        "detected": result["detected"],
        "정답여부": "✅" if is_correct else "❌",
    })

print("\n" + "=" * 70)
print(f"{'기대':<16}{'결과':<16}{'confidence':<12}{'detected':<10}{'정답여부'}")
print("=" * 70)
for r in results:
    print(f"{r['기대']:<16}{str(r['결과']):<16}{r['confidence']:<12}{str(r['detected']):<10}{r['정답여부']}")

correct_count = sum(1 for r in results if r["정답여부"] == "✅")
print("=" * 70)
print(f"전체 {len(results)}개 중 {correct_count}개 정답 ({correct_count/len(results)*100:.1f}%)")