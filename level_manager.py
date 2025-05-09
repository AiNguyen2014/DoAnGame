import json
import os

LEVELS_PATH = r"./levels.json"
class LevelManager:
    def __init__(self):
        self.levels = []
        self.current_level = 0  # Bắt đầu ở cấp độ 1 (chỉ số 0)
        # Tải dữ liệu levels từ file JSON
        self.load_levels()

    def load_levels(self):
        """Tải toàn bộ dữ liệu levels từ file JSON."""
        try:
            with open(LEVELS_PATH, "r", encoding="utf-8") as file:
                data = json.load(file)
                self.levels = data.get("levels", [])
        except FileNotFoundError:
            print(f"Lỗi: Không tìm thấy tệp '{LEVELS_PATH}'!")
            self.levels = []
        except json.JSONDecodeError:
            print(f"Lỗi: Định dạng JSON không hợp lệ trong '{LEVELS_PATH}'!")
            self.levels = []

    def load_level(self, level_number):
        """Đọc dữ liệu level cụ thể từ file JSON."""
        try:
            with open(LEVELS_PATH, "r", encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError:
            print(f"Error: File '{LEVELS_PATH}' not found! Please ensure the file exists in the correct directory.")
            return None, None, None, None, None
        except json.JSONDecodeError:
            print(f"Error: File '{LEVELS_PATH}' contains invalid JSON format!")
            return None, None, None, None, None

        for level in data.get("levels", []):
            if level["level"] == level_number:
                return (
                    level["maze"],
                    level["stairs"],
                    level.get("player_start", {"row": 0, "col": 0}),
                    level.get("mummies", []),
                    level.get("traps", [])
                )
        return None, None, None, None, None

    def get_current_level_data(self):
        """Trả lại dữ liệu cho cấp độ hiện tại."""
        if 0 <= self.current_level < len(self.levels):
            return self.load_level(self.current_level + 1)
        return None, None, None, None, None

    def next_level(self):
        if self.current_level < len(self.levels) - 1:
            self.current_level += 1
            return True
        return False

    def reset_level(self):
        self.current_level = 0

    def get_level_count(self):
        return len(self.levels)