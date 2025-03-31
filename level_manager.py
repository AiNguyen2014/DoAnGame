import json
import os
def load_level(level_number):
    """Đọc dữ liệu level từ file JSON"""
    import json

def load_level(level_number):
    with open("levels.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    for level in data["levels"]:
        if level["level"] == level_number:
            return level["maze"], level["stairs"]

    return None, None  # Trả về None nếu không tìm thấy level
