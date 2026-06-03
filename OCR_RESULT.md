# OCR_RESULT

## OCR Model

- EasyOCR
- PaddleOCR 2.7.3

Language: Korean

---

### Test Image

Image : tylenol_01.jpg

Expected:
타이레놀

---

## EasyOCR Test:

EasyOCR Output:
디 (이레뜰

Result:
Fail

---

## Preprocessing Test

Applied :
- GrayScale
- 2x Resize

OCR Output:
'", "{ '0 5 [ 놀

Result:
Fail

---

## paddleOCR Test

PaddleOCR Output:
정
목하교링
균레모호
룩리103
정
00
물디름
지시가
복용하지마십시오
O0
저
릉유9링
긍을융
웅요퓨공8
메
복

Result:
Partial Success

Observation:

- 약품명 "타이레놀"을 전혀 인식하지 못함
- 패키지 내 일반 한글 문구는 일부 인식 가능

---

## Analysis

약품 패키지 이미지에는 입체 로고, 그림자, 반사광, 다양한 글꼴 및 디자인 요소가 포함되어 있어 OCR 인식에 어려움이 있었다.

EasyOCR은 약품명을 포함한 주요 텍스트를 정확하게 인식하지 못했으며, Grayscale 변환 및 이미지 확대 전처리를 적용한 후에도 유의미한 성능 향상은 확인되지 않았다.

PaddleOCR은 일부 안내 문구를 읽어낼 수 있었지만, 약품명을 정확하게 식별하는 수준에는 도달하지 못하였다.

## Conclusion

EasyOCR과 PaddleOCR을 이용하여 약품 패키지 이미지에 대한 OCR 성능을 비교하였다.

EasyOCR은 약품명 인식에 실패하였으며, 전처리 적용 후에도 성능 향상이 크지 않았다. PaddleOCR은 일부 한글 문구를 인식하는 데 성공하였으나, 약품명을 정확하게 추출하지는 못하였다.

최종 시스템에서는 YOLO 기반 객체 탐지를 1차 분류 수단으로 사용하고, OCR은 YOLO가 탐지하지 못한 경우를 보완하는 보조 수단으로 활용할 계획이다
