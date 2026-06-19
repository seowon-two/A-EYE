# Confidence Threshold 분석 가이드

## 배경
지금 `model_connector.py`는 13개 클래스 모두 동일한 confidence threshold(0.80)와 margin threshold(0.06)를 쓰고 있음
하지만 클래스별로 모델 성능이 다르기 때문에(어떤 모델은 confidence가 전반적으로 낮게 나오거나, 다른 클래스와 잘 헷갈림),
실제 사진 데이터로 클래스별 적정 threshold를 찾아서 오인식을 줄이는 작업임.

---

## 새로 추가된 함수 역할

### `src/model_connector.py` — `detect_medicine_with_logging(image_path, true_label)`
기존 `detect_medicine()`은 실제 서비스(Streamlit 앱)에서 쓰는 함수이고, 이건 **평가/분석 전용 함수**임.

- 입력: 이미지 경로, 그 이미지의 정답 클래스명(`true_label`)
- 동작: 13개 모델 전체를 이미지에 돌려서, 각 모델이 낸 confidence를 전부 기록
- 결과: `logs/detection_log.csv`에 한 줄씩 누적 저장 (timestamp, 이미지경로, 정답라벨, 순위, 예측라벨, confidence)
- **앱 동작에는 영향 없음** — 평가할 때만 따로 호출하는 함수.

### `split_dataset.py`
클래스별 폴더(`data/raw_photos/<클래스명>/`)에 있는 사진을 80%(train) / 20%(val)로 무작위 분리해서 `test_images/train/`, `test_images/val/`에 복사함.
- train: threshold를 찾는 데 사용
- val: 찾은 threshold가 실제로 맞는지 마지막에 검증하는 데 사용 (train에 쓴 사진으로 검증하면 그 사진들에만 잘 맞는 threshold가 나올 위험이 있어서 분리함)

### `run_eval.py`
`test_images/train/` 안의 모든 클래스 폴더를 돌면서, 폴더 안 사진들을 전부 `detect_medicine_with_logging()`에 넣어 `logs/detection_log.csv`를 생성함.

### `analyze_thresholds.py`
쌓인 `detection_log.csv`를 읽어서 클래스별로:
- 정답 사진에서 나온 confidence 분포
- 다른 약품 사진에서 나온(오인식) confidence 분포
- precision-recall 기반 추천 threshold (F1 최대 지점)

를 계산해서 출력함.

---

## 각자 자기 클래스 threshold 분석하는 방법 (단계별)

### 1. 본인이 맡은 클래스 사진을 폴더에 넣기
폴더 이름은 `model_connector.py`의 `MODEL_PATHS` 키 이름과 정확히 일치해야 함.
(band, bearse, eyedrop-multi, eyedrop-single, ezen6, festal, fusidin, geborin, madecassol, pancol, panpirin, patch, tylenol)

### 2. 데이터 train/val 분리
```bash
python split_dataset.py
```

### 3. 평가 실행 (13개 모델 전체에 돌림 — 시간 좀 걸림)
```bash
python run_eval.py
```
완료되면 `logs/detection_log.csv`가 생성/누적됨.

### 4. 분석 실행
```bash
python analyze_thresholds.py
```
본인이 맡은 클래스 결과를 확인함. (다른 사람이 안 올린 클래스는 정답 데이터가 없어서 분석이 불완전하게 나오는 게 정상)

### 5. 결과 확인 및 판단
- `정답 confidence`와 `다른 약품 confidence` 분포가 잘 분리되어 있는지 확인
- `추천 threshold`의 precision/recall이 납득할만한 수준인지 확인
  - precision이 너무 낮으면(0.5 이하) → 모델이 다른 클래스와 심하게 헷갈리고 있다는 뜻, 추가 분석 필요
  - 정답 사진의 confidence 자체가 매번 너무 낮으면 → 모델 재학습 필요할 수 있음

### 6. 결과 공유
- 각자 생성된 `logs/detection_log.csv`를 깃헙에 push
- 모두 합치면 13개 클래스 전체에 대한 분석이 완성됨 (한 명이 `pd.concat`으로 머지 후 `analyze_thresholds.py` 다시 실행)

### 7. 최종 적용
분석 결과로 나온 클래스별 threshold를 `model_connector.py`의 `CONFIDENCE_THRESHOLDS` 딕셔너리에 반영