from ultralytics import YOLO

model = YOLO("models/band_best.pt")

# conf를 0.01까지 낮춰서 강제로 detection 시켜봄
results = model("test_images/train/band/band_01.jpg", conf=0.01)

print("=== boxes (conf=0.01) ===")
print(results[0].boxes)