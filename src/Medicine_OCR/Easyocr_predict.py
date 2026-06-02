import easyocr
from difflib import get_close_matches

reader = easyocr.Reader(['ko'])

medicine_dict = {
    "타이레놀": "tylenol",
    "게보린": "geborin",
    "이지엔": "ezen6",
    "판콜": "pancol",
    "판피린": "panpirin",
    "베아제": "bearse",
    "훼스탈": "festal",
    "후시딘": "fusidin",
    "마데카솔": "madecassol"
}

def ocr_predict(image_path):

    result = reader.readtext(
        image_path,
        detail=0,
        paragraph=True
    )

    text = " ".join(result)

    candidates = get_close_matches(
        text,
        list(medicine_dict.keys()),
        n=1,
        cutoff=0.3
    )

    if candidates:
        return medicine_dict[candidates[0]]

    return "unknown"
