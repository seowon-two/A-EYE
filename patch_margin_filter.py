import pandas as pd

def is_confident_patch(predictions, margin_threshold=0.18):
    """
    predictions: [(label, confidence), ...] 1등부터 내림차순 정렬된 리스트
    patch가 1등일 때, 2등과의 margin이 충분히 클 때만 patch로 확정
    """
    if not predictions:
        return False, None
    best_label, best_conf = predictions[0]
    if best_label != "patch":
        return True, best_label  # patch가 아니면 그대로 통과
    if len(predictions) < 2:
        return True, "patch"
    second_label, second_conf = predictions[1]
    margin = best_conf - second_conf
    if margin < margin_threshold:
        return False, "uncertain"  # patch로 확정 안 함, 재확인 필요
    return True, "patch"


def evaluate_margin_threshold(csv_path, margin_threshold=0.18):
    """detection_log.csv를 읽어서 margin 필터링 적용 전/후 비교"""
    df = pd.read_csv(csv_path)

    results = []
    for image_path, group in df.groupby("image_path"):
        group = group.sort_values("rank")
        true_label = group["true_label"].iloc[0]
        preds = list(zip(group["pred_label"], group["confidence"]))

        confirmed, final_label = is_confident_patch(preds, margin_threshold)
        results.append({
            "image_path": image_path,
            "true_label": true_label,
            "raw_top1": preds[0][0] if preds else None,
            "filtered_label": final_label,
            "confirmed": confirmed,
        })

    return pd.DataFrame(results)


if __name__ == "__main__":
    CSV_PATH = "logs/detection_log.csv"  # 실제 경로로 수정

    for threshold in [0.00, 0.02, 0.04, 0.06, 0.08, 0.10]:
        result_df = evaluate_margin_threshold(CSV_PATH, threshold)

        # patch가 정답인 케이스 중 raw로 patch를 맞춘 비율
        patch_true = result_df[result_df["true_label"] == "patch"]
        raw_recall = (patch_true["raw_top1"] == "patch").mean()
        filtered_recall = (patch_true["filtered_label"] == "patch").mean()

        # 다른 클래스인데 patch로 잘못 예측된 케이스 (false positive)
        non_patch_true = result_df[result_df["true_label"] != "patch"]
        raw_fp_rate = (non_patch_true["raw_top1"] == "patch").mean()
        filtered_fp_rate = (non_patch_true["filtered_label"] == "patch").mean()

        print(f"\n=== margin_threshold = {threshold} ===")
        print(f"patch recall: raw={raw_recall:.3f} -> filtered={filtered_recall:.3f}")
        print(f"non-patch false positive: raw={raw_fp_rate:.3f} -> filtered={filtered_fp_rate:.3f}")