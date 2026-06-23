import pandas as pd

DEFAULT_MARGIN_THRESHOLD = 0.06
CLASS_MARGIN_OVERRIDES = {
    "patch": 0.04,
}
CONFIDENCE_THRESHOLD = 0.80


def apply_detect_logic(preds, default_margin=DEFAULT_MARGIN_THRESHOLD,
                        overrides=None, conf_threshold=CONFIDENCE_THRESHOLD):
    """
    detect_medicine()와 동일한 로직.
    preds: [(label, confidence), ...] confidence 내림차순 정렬된 리스트
    반환: detected(bool), predicted_label(str or None)
    """
    if overrides is None:
        overrides = {}

    if len(preds) == 0:
        return False, None

    best_label, best_conf = preds[0]
    margin_threshold = overrides.get(best_label, default_margin)

    if len(preds) >= 2:
        second_label, second_conf = preds[1]
        margin = best_conf - second_conf
    else:
        margin = 1.0

    detected = (best_conf >= conf_threshold) and (margin >= margin_threshold)

    if detected:
        return True, best_label
    return False, None


def evaluate(csv_path):
    df = pd.read_csv(csv_path)

    rows = []
    for image_path, group in df.groupby("image_path"):
        group = group.sort_values("rank")
        true_label = group["true_label"].iloc[0]
        preds = list(zip(group["pred_label"], group["confidence"]))
        preds = [p for p in preds if pd.notna(p[0])]  # None 제거
        rows.append({"image_path": image_path, "true_label": true_label, "preds": preds})

    eval_df = pd.DataFrame(rows)

    results = {}

    # ===== RAW (margin 적용 안 한 기존 방식: 그냥 top1) =====
    eval_df["raw_pred"] = eval_df["preds"].apply(lambda p: p[0][0] if p else None)
    raw_correct = (eval_df["raw_pred"] == eval_df["true_label"]).sum()
    raw_total = len(eval_df)
    results["raw_top1"] = {
        "accuracy": raw_correct / raw_total,
        "correct": raw_correct,
        "total": raw_total,
    }

    # ===== 기존 로직 (모든 클래스 margin=0.06, confidence>=0.80) =====
    def old_logic(preds):
        return apply_detect_logic(preds, default_margin=0.06, overrides={})

    eval_df["old_detected"], eval_df["old_pred"] = zip(*eval_df["preds"].apply(old_logic))
    old_correct = ((eval_df["old_pred"] == eval_df["true_label"]) & eval_df["old_detected"]).sum()
    old_undetected = (~eval_df["old_detected"]).sum()
    old_wrong = eval_df["old_detected"].sum() - ((eval_df["old_pred"] == eval_df["true_label"]) & eval_df["old_detected"]).sum()
    results["old_logic (margin=0.06 전체)"] = {
        "accuracy": old_correct / len(eval_df),
        "correct": old_correct,
        "wrong": old_wrong,
        "undetected": old_undetected,
        "total": len(eval_df),
    }

    # ===== 새 로직 (patch만 margin=0.04, 나머지 0.06) =====
    def new_logic(preds):
        return apply_detect_logic(preds, default_margin=0.06, overrides=CLASS_MARGIN_OVERRIDES)

    eval_df["new_detected"], eval_df["new_pred"] = zip(*eval_df["preds"].apply(new_logic))
    new_correct = ((eval_df["new_pred"] == eval_df["true_label"]) & eval_df["new_detected"]).sum()
    new_undetected = (~eval_df["new_detected"]).sum()
    new_wrong = eval_df["new_detected"].sum() - new_correct
    results["new_logic (patch=0.04)"] = {
        "accuracy": new_correct / len(eval_df),
        "correct": new_correct,
        "wrong": new_wrong,
        "undetected": new_undetected,
        "total": len(eval_df),
    }

    return results, eval_df


if __name__ == "__main__":
    CSV_PATH = "logs/detection_log.csv"  # 실제 경로로 수정

    results, eval_df = evaluate(CSV_PATH)

    print("=" * 60)
    print("전체 정확도 비교 (13클래스 전체 기준)")
    print("=" * 60)
    for name, r in results.items():
        print(f"\n[{name}]")
        for k, v in r.items():
            if k == "accuracy":
                print(f"  accuracy: {v:.3f}")
            else:
                print(f"  {k}: {v}")

    # 클래스별로도 한번 보기 (특히 patch)
    print("\n" + "=" * 60)
    print("클래스별 accuracy 비교 (old_logic vs new_logic)")
    print("=" * 60)
    for true_label, group in eval_df.groupby("true_label"):
        old_acc = ((group["old_pred"] == true_label) & group["old_detected"]).sum() / len(group)
        new_acc = ((group["new_pred"] == true_label) & group["new_detected"]).sum() / len(group)
        marker = "  <-- 변경됨" if true_label == "patch" else ""
        print(f"{true_label:18s}  old={old_acc:.3f}  new={new_acc:.3f}{marker}")