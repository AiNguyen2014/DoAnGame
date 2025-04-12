import json
import os
def load_level(level_number):
    """Đọc dữ liệu level từ file JSON"""

def load_level(level_number):
    with open("levels.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    for level in data["levels"]:
        if level["level"] == level_number:
            return (
                level["maze"],
                level["stairs"],
                level.get("player_start", {"row": 0, "col": 0}),
                level.get("mummies", []),
                level.get("scorpions", []),
                level.get("traps", []),
                level.get("keys", [])
            )

    return None, None, None, None, None, None, None
