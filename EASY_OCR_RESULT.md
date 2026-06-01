# EASY_OCR_RESULT

## OCR Model

-EasyOCR
-Language:Korean

---

### Test Image

Image : tylenol_01.jpg

Expected:
타이레놀

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

## Conclusion

EasyOCR을 이용하여 약품 패키지 이미지를 대상으로 OCR 실험을 수행하였다.

약품 로고의 입체 효과, 그림자, 색상 대비 등의 영향으로 인해 문자를 정확하게 인식하지 못하는 사례가 다수 발생하였다. 또한 Grayscale 변환 및 이미지 확대와 같은 전처리를 적용하였으나 인식 성능의 유의미한 향상은 확인되지 않았다.

다만 OCR 모델에 따라 인식 성능이 달라질 수 있기에, PaddleOCR을 적용해 성능을 확인해볼 예정이다.

최종 시스템에서는 YOLO 기반 객체 탐지를 1차 분류 수단으로 사용하고, OCR은 YOLO가 탐지하지 못한 경우를 보완하는 보조 수단으로 활용할 계획이다
