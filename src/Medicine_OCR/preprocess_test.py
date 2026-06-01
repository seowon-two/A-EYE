import cv2
import easyocr

img = cv2.imread("images/tylenol_01.jpg")

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.resize(gray, None, fx=2, fy=2)

cv2.imwrite("gray_tylenol.jpg", gray)

reader = easyocr.Reader(['ko'])

result = reader.readtext(
    gray,
    detail=0,
    paragraph=True
)

print(result)
