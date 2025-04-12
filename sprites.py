import pygame
from constants import *
from images_manager import IMAGES

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, wall_type):
        super().__init__()
        if wall_type == "W_h":
            self.image = IMAGES["wall_horizontal"]
        elif wall_type == "W_v":
            self.image = IMAGES["wall_vertical"]
        else:
            raise ValueError(f"Loại tường không hợp lệ: {wall_type}")
        
        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))
        self.rect = self.image.get_rect(topleft=(x, y))

class Stair(pygame.sprite.Sprite):
    def __init__(self, x, y, stair_type):
        super().__init__()
        if stair_type == "S_r":
            self.image = IMAGES["stairs_right"]
        elif stair_type == "S_l":
            self.image = IMAGES["stairs_left"]
        elif stair_type == "S_t":
            self.image = IMAGES["stairs_top"]
        elif stair_type == "S_b":
            self.image = IMAGES["stairs_bottom"]
        else:
            raise ValueError(f"Loại cầu thang không hợp lệ: {stair_type}")

        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))
        self.rect = self.image.get_rect(topleft=(x, y))

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.direction = "right"  # Hướng mặc định
        self.image = IMAGES["player"][self.direction]
        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))
        self.rect = self.image.get_rect(topleft=(x, y))
        # Tính row, col dựa trên vị trí lưới, loại bỏ offset
        self.row = (y - 80) // CELL_SIZE
        self.col = (x - 215) // CELL_SIZE
        print(f"Player init: row={self.row}, col={self.col}, x={x}, y={y}")  # Debug

    def move(self, direction, maze, walls):
        new_row, new_col = self.row, self.col
        if direction == "up":
            new_row -= 1
        elif direction == "down":
            new_row += 1
        elif direction == "left":
            new_col -= 1
        elif direction == "right":
            new_col += 1

        print(f"Attempting move {direction}: new_row={new_row}, new_col={new_col}")  # Debug

        if 0 <= new_row < len(maze) and 0 <= new_col < len(maze[0]):
            # Kiểm tra ô mới trong maze
            cell = maze[new_row][new_col]
            # Kiểm tra va chạm với walls
            walls_block = False
            new_x = 215 + new_col * CELL_SIZE
            new_y = 80 + new_row * CELL_SIZE
            for wall in walls:
                if wall.rect.colliderect(pygame.Rect(new_x, new_y, CELL_SIZE, CELL_SIZE)):
                    walls_block = True
                    print(f"Blocked by wall at x={wall.rect.x}, y={wall.rect.y}")  # Debug
                    break
            # Kiểm tra tường trong maze
            if not walls_block and ("walls" not in cell or not self.is_blocked(direction, cell["walls"])):
                self.row = new_row
                self.col = new_col
                self.rect.topleft = (new_x, new_y)
                self.direction = direction
                self.image = pygame.transform.scale(IMAGES["player"][self.direction], (CELL_SIZE, CELL_SIZE))
                print(f"Move successful: row={self.row}, col={self.col}, x={new_x}, y={new_y}")  # Debug
                return True
            else:
                print(f"Blocked by maze walls: {cell.get('walls', [])}")  # Debug
        else:
            print(f"Out of bounds: new_row={new_row}, new_col={new_col}")  # Debug
        return False

    def is_blocked(self, direction, walls):
        """Kiểm tra xem hướng di chuyển có bị chặn bởi tường không"""
        if direction == "up" and "bottom" in walls:
            return True
        if direction == "down" and "top" in walls:
            return True
        if direction == "left" and "right" in walls:
            return True
        if direction == "right" and "left" in walls:
            return True
        return False

class Mummy(pygame.sprite.Sprite):
    def __init__(self, x, y, color="white"):
        super().__init__()
        self.color = color
        self.direction = "right"
        self.image = IMAGES["mummy"][f"{color}_{self.direction}"]
        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.row = (y - 80) // CELL_SIZE
        self.col = (x - 215) // CELL_SIZE
        print(f"Mummy init: row={self.row}, col={self.col}, x={x}, y={y}")  # Debug

    def auto_move(self, player_row, player_col, maze, walls):
        directions = ["down", "up", "right", "left"]
        for direction in directions:
            if direction == "down" and self.row < player_row and self.move(direction, maze, walls):
                return
            if direction == "up" and self.row > player_row and self.move(direction, maze, walls):
                return
            if direction == "right" and self.col < player_col and self.move(direction, maze, walls):
                return
            if direction == "left" and self.col > player_col and self.move(direction, maze, walls):
                return

    def move(self, direction, maze, walls):
        new_row, new_col = self.row, self.col
        if direction == "up":
            new_row -= 1
        elif direction == "down":
            new_row += 1
        elif direction == "left":
            new_col -= 1
        elif direction == "right":
            new_col += 1

        if 0 <= new_row < len(maze) and 0 <= new_col < len(maze[0]):
            cell = maze[new_row][new_col]
            walls_block = False
            new_x = 215 + new_col * CELL_SIZE
            new_y = 80 + new_row * CELL_SIZE
            for wall in walls:
                if wall.rect.colliderect(pygame.Rect(new_x, new_y, CELL_SIZE, CELL_SIZE)):
                    walls_block = True
                    break
            if not walls_block and ("walls" not in cell or not self.is_blocked(direction, cell["walls"])):
                self.row = new_row
                self.col = new_col
                self.rect.topleft = (new_x, new_y)
                self.direction = direction
                self.image = pygame.transform.scale(IMAGES["mummy"][f"{self.color}_{self.direction}"], (CELL_SIZE, CELL_SIZE))
                return True
        return False

    def is_blocked(self, direction, walls):
        if direction == "up" and "bottom" in walls:
            return True
        if direction == "down" and "top" in walls:
            return True
        if direction == "left" and "right" in walls:
            return True
        if direction == "right" and "left" in walls:
            return True
        return False

class Key(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = IMAGES["key"]
        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))
        self.rect = self.image.get_rect(topleft=(x, y))

class Trap(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = IMAGES["trap_skull"]
        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))
        self.rect = self.image.get_rect(topleft=(x, y))

class Scorpion(pygame.sprite.Sprite):
    def __init__(self, x, y, color="black"):
        super().__init__()
        self.color = color
        self.direction = "right"
        self.image = IMAGES["scorpion"][f"{color}_{self.direction}"]
        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.row = (y - 80) // CELL_SIZE
        self.col = (x - 215) // CELL_SIZE
        print(f"Scorpion init: row={self.row}, col={self.col}, x={x}, y={y}")  # Debug

    def auto_move(self, player_row, player_col, maze, walls):
        directions = ["down", "up", "right", "left"]
        for direction in directions:
            if direction == "down" and self.row < player_row and self.move(direction, maze, walls):
                return
            if direction == "up" and self.row > player_row and self.move(direction, maze, walls):
                return
            if direction == "right" and self.col < player_col and self.move(direction, maze, walls):
                return
            if direction == "left" and self.col > player_col and self.move(direction, maze, walls):
                return

    def move(self, direction, maze, walls):
        new_row, new_col = self.row, self.col
        if direction == "up":
            new_row -= 1
        elif direction == "down":
            new_row += 1
        elif direction == "left":
            new_col -= 1
        elif direction == "right":
            new_col += 1

        if 0 <= new_row < len(maze) and 0 <= new_col < len(maze[0]):
            cell = maze[new_row][new_col]
            walls_block = False
            new_x = 215 + new_col * CELL_SIZE
            new_y = 80 + new_row * CELL_SIZE
            for wall in walls:
                if wall.rect.colliderect(pygame.Rect(new_x, new_y, CELL_SIZE, CELL_SIZE)):
                    walls_block = True
                    break
            if not walls_block and ("walls" not in cell or not self.is_blocked(direction, cell["walls"])):
                self.row = new_row
                self.col = new_col
                self.rect.topleft = (new_x, new_y)
                self.direction = direction
                self.image = pygame.transform.scale(IMAGES["scorpion"][f"{self.color}_{self.direction}"], (CELL_SIZE, CELL_SIZE))
                return True
        return False

    def is_blocked(self, direction, walls):
        if direction == "up" and "bottom" in walls:
            return True
        if direction == "down" and "top" in walls:
            return True
        if direction == "left" and "right" in walls:
            return True
        if direction == "right" and "left" in walls:
            return True
        return False