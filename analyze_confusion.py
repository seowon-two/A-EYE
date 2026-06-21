import pandas as pd

df = pd.read_csv("logs/detection_log.csv")

all_classes = df["true_label"].unique()

for target_class in all_classes:
    confused = df[(df["pred_label"] == target_class) & (df["true_label"] != target_class)]
    
    if confused.empty:
        print(f"\n=== {target_class} 모델이 헷갈리는 클래스 ===\n오인식 케이스 없음")
        continue
    
    summary = confused.groupby("true_label")["confidence"].agg(["count", "mean", "max"]).sort_values("mean", ascending=False)
    
    print(f"\n=== {target_class} 모델이 헷갈리는 클래스 ===")
    print(summary)