import json

def load_db(path="../DB/medications.json"):  # src 기준 상대경로
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data["medicine_db"]

def get_medicine_info(class_name: str):
    db = load_db()
    for item in db:
        if item["class_name"] == class_name:
            return item
    return None
