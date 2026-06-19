import pandas as pd
import numpy as np
from sklearn.metrics import precision_recall_curve
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
LOG_PATH = BASE_DIR / "logs" / "detection_log.csv"

df = pd.read_csv(LOG_PATH)
df = df[df["pred_label"].notna()]

print("=== 클래스별 confidence 분포 (정답 vs 오답) ===\n")

for class_name in sorted(df["true_label"].unique()):
    subset = df[df["pred_label"] == class_name].copy()
    if subset.empty:
        continue

    subset["is_correct"] = (subset["true_label"] == class_name)

    tp_conf = subset[subset["is_correct"]]["confidence"]
    fp_conf = subset[~subset["is_correct"]]["confidence"]

    print(f"[{class_name}]")
    if len(tp_conf) > 0:
        print(f"  정답 사진 confidence  : mean={tp_conf.mean():.3f}, min={tp_conf.min():.3f}, max={tp_conf.max():.3f} (n={len(tp_conf)})")
    else:
        print("  정답 사진에서 검출된 적 없음")

    if len(fp_conf) > 0:
        print(f"  다른 약품 사진 confidence: mean={fp_conf.mean():.3f}, min={fp_conf.min():.3f}, max={fp_conf.max():.3f} (n={len(fp_conf)})")
    else:
        print("  다른 약품 사진에서는 검출된 적 없음 (오인식 위험 적음)")

    # precision-recall 기반 최적 threshold
    y_true = subset["is_correct"].astype(int)
    y_score = subset["confidence"]

    if y_true.nunique() == 2:
        precision, recall, thresholds = precision_recall_curve(y_true, y_score)
        f1 = 2 * precision * recall / (precision + recall + 1e-9)
        best_idx = np.argmax(f1[:-1])
        print(f"  >> 추천 threshold: {thresholds[best_idx]:.3f} (precision={precision[best_idx]:.2f}, recall={recall[best_idx]:.2f})")
    else:
        print("  >> 정답/오답이 한 쪽만 있어서 threshold 계산 불가 (현재 데이터로는 안전하다고 봐도 됨)")

    print()