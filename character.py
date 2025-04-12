import pygame
from constants import CELL_SIZE
from images_manager import IMAGES

class Character(pygame.sprite.Sprite):
    def __init__(self, x, y, images):
        super().__init__()
        # Danh sách các hình ảnh theo hướng (lên, xuống, trái, phải), mỗi hướng chỉ có 1 frame
        self.images = images
        self.direction = "down"  # Hướng mặc định
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.row = (y - 80) // CELL_SIZE  # Điều chỉnh tọa độ y
        self.col = (x - 215) // CELL_SIZE  # Điều chỉnh tọa độ x

    def update_image(self):
        """Cập nhật hình ảnh dựa trên hướng di chuyển"""
        self.image = self.images[self.direction]

    def can_move(self, row, col, maze, walls):
        """Kiểm tra xem ô có thể di chuyển được không"""
        # Kiểm tra giới hạn lưới
        if not (0 <= row < 7 and 0 <= col < 7):
            return False

        # Kiểm tra tường
        cell = maze[row][col]
        if "walls" in cell:
            for wall in cell["walls"]:
                if (wall == "top" and self.direction == "up") or \
                   (wall == "bottom" and self.direction == "down") or \
                   (wall == "left" and self.direction == "left") or \
                   (wall == "right" and self.direction == "right"):
                    return False

        return True

class Player(Character):
    def __init__(self, x, y):
        images = {
            "up": pygame.transform.scale(IMAGES["player"]["up"], (CELL_SIZE, CELL_SIZE)),
            "down": pygame.transform.scale(IMAGES["player"]["down"], (CELL_SIZE, CELL_SIZE)),
            "left": pygame.transform.scale(IMAGES["player"]["left"], (CELL_SIZE, CELL_SIZE)),
            "right": pygame.transform.scale(IMAGES["player"]["right"], (CELL_SIZE, CELL_SIZE))
        }
        super().__init__(x, y, images)

    def move(self, direction, maze, walls):
        """Di chuyển người chơi bằng phím mũi tên"""
        new_row, new_col = self.row, self.col

        if direction == "up":
            new_row -= 1
            self.direction = "up"
        elif direction == "down":
            new_row += 1
            self.direction = "down"
        elif direction == "left":
            new_col -= 1
            self.direction = "left"
        elif direction == "right":
            new_col += 1
            self.direction = "right"

        # Kiểm tra xem có thể di chuyển không (không va vào tường)
        if self.can_move(new_row, new_col, maze, walls):
            self.row, self.col = new_row, new_col
            self.rect.topleft = (215 + self.col * CELL_SIZE, 80 + self.row * CELL_SIZE)
            self.update_image()
            return True
        return False

class Mummy(Character):
    def __init__(self, x, y, color="white"):
        images = {
            "up": pygame.transform.scale(IMAGES["mummy"][f"white_up"], (CELL_SIZE, CELL_SIZE)),
            "down": pygame.transform.scale(IMAGES["mummy"][f"white_down"], (CELL_SIZE, CELL_SIZE)),
            "left": pygame.transform.scale(IMAGES["mummy"][f"white_left"], (CELL_SIZE, CELL_SIZE)),
            "right": pygame.transform.scale(IMAGES["mummy"][f"white_right"], (CELL_SIZE, CELL_SIZE))
        }
        super().__init__(x, y, images)
        self.color = color  # "white" hoặc "red" để xác định ưu tiên di chuyển

    def auto_move(self, player_row, player_col, maze, walls):
        """Xác ướp di chuyển 2 ô theo hướng ưu tiên"""
        for _ in range(2):  # Di chuyển 2 lần
            if self.color == "white":
                directions = ["left", "right", "up", "down"]  # Ưu tiên ngang
            else:  # red
                directions = ["up", "down", "left", "right"]  # Ưu tiên dọc

            for direction in directions:
                new_row, new_col = self.row, self.col
                if direction == "up":
                    new_row -= 1
                elif direction == "down":
                    new_row += 1
                elif direction == "left":
                    new_col -= 1
                elif direction == "right":
                    new_col += 1

                if self.can_move(new_row, new_col, maze, walls):
                    self.row, self.col = new_row, new_col
                    self.direction = direction
                    self.rect.topleft = (215 + self.col * CELL_SIZE, 80 + self.row * CELL_SIZE)
                    self.update_image()
                    break

class Scorpion(Character):
    def __init__(self, x, y, color="white"):
        images = {
            "up": pygame.transform.scale(IMAGES["scorpion"][f"{color}_up"], (CELL_SIZE, CELL_SIZE)),
            "down": pygame.transform.scale(IMAGES["scorpion"][f"{color}_down"], (CELL_SIZE, CELL_SIZE)),
            "left": pygame.transform.scale(IMAGES["scorpion"][f"{color}_left"], (CELL_SIZE, CELL_SIZE)),
            "right": pygame.transform.scale(IMAGES["scorpion"][f"{color}_right"], (CELL_SIZE, CELL_SIZE))
        }
        super().__init__(x, y, images)
        self.color = color  # "white" hoặc "red" để xác định ưu tiên di chuyển

    def auto_move(self, player_row, player_col, maze, walls):
        """Bò cạp di chuyển 1 ô theo hướng ưu tiên"""
        if self.color == "white":
            directions = ["left", "right", "up", "down"]  # Ưu tiên ngang
        else:  # red
            directions = ["up", "down", "left", "right"]  # Ưu tiên dọc

        for direction in directions:
            new_row, new_col = self.row, self.col
            if direction == "up":
                new_row -= 1
            elif direction == "down":
                new_row += 1
            elif direction == "left":
                new_col -= 1
            elif direction == "right":
                new_col += 1

            if self.can_move(new_row, new_col, maze, walls):
                self.row, self.col = new_row, new_col
                self.direction = direction
                self.rect.topleft = (215 + self.col * CELL_SIZE, 80 + self.row * CELL_SIZE)
                self.update_image()
                break

class Trap(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(IMAGES["trap_skull"], (CELL_SIZE, CELL_SIZE))
        self.rect = self.image.get_rect(topleft=(x, y))

class Key(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(IMAGES["key"], (CELL_SIZE, CELL_SIZE))
        self.rect = self.image.get_rect(topleft=(x, y))