import pygame
from constants import CELL_SIZE, WIDTH, HEIGHT

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, wall_type):
        super().__init__()
        if wall_type == "W_h":
            self.image = pygame.image.load("images/wall_horizontal.png")
        elif wall_type == "W_v":
            self.image = pygame.image.load("images/wall_vertical.png")
        else:
            raise ValueError(f"Loại tường không hợp lệ: {wall_type}")
        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))
        self.rect = self.image.get_rect(topleft=(x, y))

class Stair(pygame.sprite.Sprite):
    def __init__(self, x, y, stair_type):
        super().__init__()
        if stair_type == "S_r":
            self.image = pygame.image.load("images/stairs_right.png")
        elif stair_type == "S_l":
            self.image = pygame.image.load("images/stairs_left.png")
        elif stair_type == "S_t":
            self.image = pygame.image.load("images/stairs_top.png")
        elif stair_type == "S_b":
            self.image = pygame.image.load("images/stairs_bottom.png")
        else:
            raise ValueError(f"Loại cầu thang không hợp lệ: {stair_type}")
        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.grid_x = (y - 80) // CELL_SIZE
        self.grid_y = (x - 215) // CELL_SIZE

class Key(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("images/key6.png")
        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.grid_x = (y - 80) // CELL_SIZE
        self.grid_y = (x - 215) // CELL_SIZE

class Trap(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("images/trap_skull.png")
        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.grid_x = (y - 80) // CELL_SIZE
        self.grid_y = (x - 215) // CELL_SIZE

class Gate(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("images/gate6.png")
        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.grid_x = (y - 80) // CELL_SIZE
        self.grid_y = (x - 215) // CELL_SIZE
        self.is_closed = True

class Character(pygame.sprite.Sprite):
    def __init__(self, x, y, images):
        super().__init__()
        self.images = images
        self.direction = "down"
        self.image = self.images[self.direction][0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.row = (y - 80) // CELL_SIZE
        self.col = (x - 215) // CELL_SIZE
        self.grid_x = self.row
        self.grid_y = self.col
        self.moving = False
        self.move_speed = 2
        self.target_pos = (x, y)
        self.current_pos = [float(x), float(y)]
        self.frame_index = 0
        self.last_update = pygame.time.get_ticks()
        self.move_queue = []  # Hàng đợi lưu trữ các bước di chuyển

    def update_image(self):
        if self.moving:
            now = pygame.time.get_ticks()
            if now - self.last_update > 100:
                self.frame_index = (self.frame_index + 1) % len(self.images[self.direction])
                self.last_update = now
            self.image = self.images[self.direction][int(self.frame_index)]
        else:
            self.frame_index = 0
            self.image = self.images[self.direction][0]

    def update(self):
        if self.moving:
            target_x, target_y = self.target_pos
            dx = target_x - self.current_pos[0]
            dy = target_y - self.current_pos[1]
            distance = (dx**2 + dy**2)**0.5
            if distance <= self.move_speed:
                self.current_pos = [target_x, target_y]
                self.rect.topleft = (target_x, target_y)
                self.moving = False
                self.frame_index = 0
                # Sau khi hoàn thành một bước, kiểm tra hàng đợi
                if self.move_queue:
                    next_move = self.move_queue.pop(0)
                    self.direction = next_move[0]
                    new_row, new_col = next_move[1], next_move[2]
                    self.row, self.col = new_row, new_col
                    self.grid_x, self.grid_y = self.row, self.col
                    self.target_pos = (215 + self.col * CELL_SIZE, 80 + self.row * CELL_SIZE)
                    self.moving = True
                    self.update_image()
            else:
                move_x = (dx / distance) * self.move_speed
                move_y = (dy / distance) * self.move_speed
                self.current_pos[0] += move_x
                self.current_pos[1] += move_y
                self.rect.topleft = (self.current_pos[0], self.current_pos[1])
                self.update_image()

    def eligible_move(self, maze, gate, new_row, new_col, is_player=False, stairs_positions=None):
        max_row = len(maze)
        max_col = len(maze[0])

        # Cho phép người chơi di chuyển ra ngoài mê cung đến ô đích
        if is_player and stairs_positions:
            for stair in stairs_positions:
                if new_row == stair["row"] and new_col == stair["col"]:
                    return True

        # Xác ướp không được di chuyển ra ngoài mê cung
        if not is_player and not (0 <= new_row < max_row and 0 <= new_col < max_col):
            print(f"Move to ({new_row}, {new_col}) is out of bounds for mummy!")
            return False

        # Người chơi có thể di chuyển ra ngoài mê cung, nhưng cần kiểm tra tường và cổng
        if not (0 <= new_row < max_row and 0 <= new_col < max_col):
            if not is_player:
                return False
            # Nếu người chơi di chuyển ra ngoài nhưng không phải ô đích, chặn lại
            if not any(stair["row"] == new_row and stair["col"] == new_col for stair in stairs_positions):
                print(f"Move to ({new_row}, {new_col}) is out of bounds and not a stair!")
                return False

        current_cell = maze[self.row][self.col]
        target_cell = maze[new_row][new_col] if (0 <= new_row < max_row and 0 <= new_col < max_col) else {}
        direction = None
        if new_row < self.row:
            direction = "top"
        elif new_row > self.row:
            direction = "bottom"
        elif new_col < self.col:
            direction = "left"
        elif new_col > self.col:
            direction = "right"

        if "walls" in current_cell and direction in current_cell["walls"]:
            print(f"Blocked by wall in current cell at ({self.row}, {self.col}) in direction {direction}")
            return False

        opposite = {"top": "bottom", "bottom": "top", "left": "right", "right": "left"}
        if "walls" in target_cell and opposite[direction] in target_cell["walls"]:
            print(f"Blocked by wall in target cell at ({new_row}, {new_col}) from direction {opposite[direction]}")
            return False

        if gate.get("isClosed", False):
            if direction == "up" and self.row > 0 and maze[self.row - 1][self.col].get("gate"):
                print(f"Blocked by closed gate at ({self.row - 1}, {self.col})")
                return False
            if direction == "down" and self.row < len(maze) - 1 and maze[self.row + 1][self.col].get("gate"):
                print(f"Blocked by closed gate at ({self.row + 1}, {self.col})")
                return False
            if direction == "left" and self.col > 0 and maze[self.row][self.col - 1].get("gate"):
                print(f"Blocked by closed gate at ({self.row}, {self.col - 1})")
                return False
            if direction == "right" and self.col < len(maze[0]) - 1 and maze[self.row][self.col + 1].get("gate"):
                print(f"Blocked by closed gate at ({self.row}, {self.col + 1})")
                return False
        return True

    def add_to_move_queue(self, direction, new_row, new_col):
        self.move_queue.append((direction, new_row, new_col))
        if not self.moving:
            next_move = self.move_queue.pop(0)
            self.direction = next_move[0]
            self.row, self.col = next_move[1], next_move[2]
            self.grid_x, self.grid_y = self.row, self.col
            self.target_pos = (215 + self.col * CELL_SIZE, 80 + self.row * CELL_SIZE)
            self.moving = True
            self.update_image()

class Player(Character):
    def __init__(self, x, y):
        images = {
            "up": [],
            "down": [],
            "left": [],
            "right": []
        }
        for direction in ["up", "down", "left", "right"]:
            sheet = pygame.image.load(f"images/player/move_{direction}.png")
            frame_width = sheet.get_width() // 5
            for i in range(5):
                frame = sheet.subsurface((i * frame_width, 0, frame_width, sheet.get_height()))
                frame = pygame.transform.scale(frame, (CELL_SIZE, CELL_SIZE))
                images[direction].append(frame)
        super().__init__(x, y, images)

    def move(self, direction, maze, gate, stairs_positions):
        if self.moving:
            return False
        
        self.direction = direction
        new_row, new_col = self.row, self.col
        if direction == "up":
            new_row -= 1
        elif direction == "down":
            new_row += 1
        elif direction == "left":
            new_col -= 1
        elif direction == "right":
            new_col += 1

        if self.eligible_move(maze, gate, new_row, new_col, is_player=True, stairs_positions=stairs_positions):
            self.add_to_move_queue(direction, new_row, new_col)
            return True
        return False

class Mummy(Character):
    def __init__(self, x, y, color="white"):
        images = {
            "up": [],
            "down": [],
            "left": [],
            "right": []
        }
        for direction in ["up", "down", "left", "right"]:
            sheet = pygame.image.load(f"images/mummy/{color}{direction}.png")
            frame_width = sheet.get_width() // 5
            for i in range(5):
                frame = sheet.subsurface((i * frame_width, 0, frame_width, sheet.get_height()))
                frame = pygame.transform.scale(frame, (CELL_SIZE, CELL_SIZE))
                images[direction].append(frame)
        super().__init__(x, y, images)
        self.color = color.lower()

    def manhattan_distance(self, row1, col1, row2, col2):
        return abs(row1 - row2) + abs(col1 - col2)

    def auto_move(self, maze, gate, player_row, player_col):
        if self.moving or self.move_queue:
            return False

        moved = False
        for _ in range(2):  # Tối đa 2 bước di chuyển
            current_distance = self.manhattan_distance(self.row, self.col, player_row, player_col)
            possible_moves = []

            directions = ["up", "down", "left", "right"]
            for direction in directions:
                new_row, new_col = self.row, self.col
                if direction == "up": new_row -= 1
                elif direction == "down": new_row += 1
                elif direction == "left": new_col -= 1
                elif direction == "right": new_col += 1

                if self.eligible_move(maze, gate, new_row, new_col):
                    new_distance = self.manhattan_distance(new_row, new_col, player_row, player_col)
                    if new_distance < current_distance:  # Chỉ chọn hướng giảm khoảng cách
                        possible_moves.append((new_distance, direction, new_row, new_col))

            if not possible_moves:
                break

            # Sắp xếp theo khoảng cách nhỏ nhất
            possible_moves.sort(key=lambda x: x[0])
            min_distance = possible_moves[0][0]
            best_moves = [move for move in possible_moves if move[0] == min_distance]

            # Ưu tiên di chuyển theo màu
            if self.color == "white":
                priority = ["left", "right", "up", "down"]
            else:  # red
                priority = ["up", "down", "left", "right"]

            selected_move = min(best_moves, key=lambda x: priority.index(x[1]))
            direction, new_row, new_col = selected_move[1], selected_move[2], selected_move[3]

            self.add_to_move_queue(direction, new_row, new_col)
            moved = True

        return moved

    def update(self):
        super().update()