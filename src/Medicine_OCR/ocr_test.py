import easyocr

reader = easyocr.Reader(['ko'])

result = reader.readtext(
    "images/tylenol_01.jpg",
    detail=0,
    paragraph=True
)

print(result)
