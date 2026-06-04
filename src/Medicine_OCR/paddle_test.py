from paddleocr import PaddleOCR

ocr = PaddleOCR(
    use_angle_cls=True,
    lang="korean"
)

result = ocr.ocr(
    "OCR_images/tylenol_01.jpg",
    cls=True
)

for line in result[0]:
    print(line[1][0])
