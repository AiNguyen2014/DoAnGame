import pygame
from constants import CELL_SIZE, WIDTH, HEIGHT
import heapq
import random
import numpy as np

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
        self.grid_x = (y - 80) // CELL_SIZE
        self.grid_y = (x - 215) // CELL_SIZE

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

        # Allow player to move to stairs even if outside maze
        if is_player and stairs_positions:
            for stair in stairs_positions:
                if new_row == stair["row"] and new_col == stair["col"]:
                    return True

        # Check if move is within maze bounds
        if not (0 <= new_row < max_row and 0 <= new_col < max_col):
            if not is_player:
                print(f"Move to ({new_row}, {new_col}) is out of bounds for mummy!")
                return False
            # If player moves out of bounds but not to stairs, block it
            if not any(stair["row"] == new_row and stair["col"] == new_col for stair in stairs_positions):
                print(f"Move to ({new_row}, {new_col}) is out of bounds and not a stair!")
                return False

        # Determine movement direction
        direction = None
        if new_row < self.row:
            direction = "top"
        elif new_row > self.row:
            direction = "bottom" 
        elif new_col < self.col:
            direction = "left"
        elif new_col > self.col:
            direction = "right"
        
        # If no direction change, move is invalid
        if direction is None:
            return False

        current_cell = maze[self.row][self.col]
        target_cell = maze[new_row][new_col] if (0 <= new_row < max_row and 0 <= new_col < max_col) else {}

        # Check walls in current cell
        if "walls" in current_cell and direction in current_cell["walls"]:
            print(f"Blocked by wall in current cell at ({self.row}, {self.col}) in direction {direction}")
            return False

        # Check walls in target cell
        opposite = {"top": "bottom", "bottom": "top", "left": "right", "right": "left"}
        if "walls" in target_cell and opposite[direction] in target_cell["walls"]:
            print(f"Blocked by wall in target cell at ({new_row}, {new_col}) from direction {opposite[direction]}")
            return False

        # Check gates
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
        self.algorithm = "manual"  # Default algorithm
        self.q_table = {}  # For Q-learning
        self.learning_rate = 0.1
        self.discount_factor = 0.9
        self.epsilon = 0.1  # For exploration

    def manhattan_distance(self, row1, col1, row2, col2):
        return abs(row1 - row2) + abs(col1 - col2)

    def get_state_key(self, row, col):
        return f"{row},{col}"

    def get_q_value(self, state, action):
        if state not in self.q_table:
            self.q_table[state] = {"up": 0, "down": 0, "left": 0, "right": 0}
        return self.q_table[state][action]

    def update_q_value(self, state, action, reward, next_state):
        if state not in self.q_table:
            self.q_table[state] = {"up": 0, "down": 0, "left": 0, "right": 0}
        if next_state not in self.q_table:
            self.q_table[next_state] = {"up": 0, "down": 0, "left": 0, "right": 0}
        
        current_q = self.q_table[state][action]
        next_max_q = max(self.q_table[next_state].values())
        new_q = current_q + self.learning_rate * (reward + self.discount_factor * next_max_q - current_q)
        self.q_table[state][action] = new_q

    def a_star_search(self, maze, start, goal, gate, stairs_positions):
        def heuristic(a, b):
            return self.manhattan_distance(a[0], a[1], b[0], b[1])

        frontier = []
        heapq.heappush(frontier, (0, start))
        came_from = {start: None}
        cost_so_far = {start: 0}

        while frontier:
            current = heapq.heappop(frontier)[1]

            if current == goal:
                break

            for direction in ["up", "down", "left", "right"]:
                next_row, next_col = current
                if direction == "up": next_row -= 1
                elif direction == "down": next_row += 1
                elif direction == "left": next_col -= 1
                elif direction == "right": next_col += 1

                next_pos = (next_row, next_col)
                if self.eligible_move(maze, gate, next_row, next_col, is_player=True, stairs_positions=stairs_positions):
                    new_cost = cost_so_far[current] + 1
                    if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                        cost_so_far[next_pos] = new_cost
                        priority = new_cost + heuristic(goal, next_pos)
                        heapq.heappush(frontier, (priority, next_pos))
                        came_from[next_pos] = current

        # Reconstruct path
        path = []
        current = goal
        while current != start:
            path.append(current)
            current = came_from.get(current)
            if current is None:
                return []
        path.append(start)
        path.reverse()
        return path

    def min_conflict_search(self, maze, start, goal, gate, stairs_positions):
        def get_conflicts(pos):
            conflicts = 0
            row, col = pos
            for direction in ["up", "down", "left", "right"]:
                next_row, next_col = row, col
                if direction == "up": next_row -= 1
                elif direction == "down": next_row += 1
                elif direction == "left": next_col -= 1
                elif direction == "right": next_col += 1
                
                if not self.eligible_move(maze, gate, next_row, next_col, is_player=True, stairs_positions=stairs_positions):
                    conflicts += 1
            return conflicts

        current = start
        path = [current]
        visited = {current}

        while current != goal:
            best_next = None
            min_conflicts = float('inf')
            
            for direction in ["up", "down", "left", "right"]:
                next_row, next_col = current
                if direction == "up": next_row -= 1
                elif direction == "down": next_row += 1
                elif direction == "left": next_col -= 1
                elif direction == "right": next_col += 1

                next_pos = (next_row, next_col)
                if (next_pos not in visited and 
                    self.eligible_move(maze, gate, next_row, next_col, is_player=True, stairs_positions=stairs_positions)):
                    conflicts = get_conflicts(next_pos)
                    if conflicts < min_conflicts:
                        min_conflicts = conflicts
                        best_next = next_pos

            if best_next is None:
                return path

            current = best_next
            path.append(current)
            visited.add(current)

        return path

    def local_search(self, maze, start, goal, gate, stairs_positions, mummy_row, mummy_col):
        def evaluate_position(pos, goal, mummy_pos):
            goal_distance = self.manhattan_distance(pos[0], pos[1], goal[0], goal[1])
            mummy_distance = self.manhattan_distance(pos[0], pos[1], mummy_row, mummy_col)
            # Heuristic: minimize distance to goal, maximize distance from mummy
            return goal_distance - 0.5 * mummy_distance

        current = start
        best_move = None
        best_score = float('inf')

        for direction in ["up", "down", "left", "right"]:
            next_row, next_col = current
            if direction == "up": next_row -= 1
            elif direction == "down": next_row += 1
            elif direction == "left": next_col -= 1
            elif direction == "right": next_col += 1

            next_pos = (next_row, next_col)
            if self.eligible_move(maze, gate, next_row, next_col, is_player=True, stairs_positions=stairs_positions):
                score = evaluate_position(next_pos, goal, (mummy_row, mummy_col))
                if score < best_score:
                    best_score = score
                    best_move = (direction, next_row, next_col)

        if best_move:
            return [start, best_move[1:]]  # Return path with start and next position
        return []

    def auto_move(self, maze, gate, mummy_row, mummy_col, stairs_positions, goal_row, goal_col):
        if self.moving or self.move_queue:
            return False

        if self.algorithm == "a_star":
            path = self.a_star_search(maze, (self.row, self.col), (goal_row, goal_col), gate, stairs_positions)
            if path and len(path) > 1:
                next_pos = path[1]
                direction = None
                if next_pos[0] < self.row: direction = "up"
                elif next_pos[0] > self.row: direction = "down"
                elif next_pos[1] < self.col: direction = "left"
                elif next_pos[1] > self.col: direction = "right"
                
                if direction:
                    self.add_to_move_queue(direction, next_pos[0], next_pos[1])
                    return True

        elif self.algorithm == "q_learning":
            state = self.get_state_key(self.row, self.col)
            if random.random() < self.epsilon:
                # Exploration: choose random action
                direction = random.choice(["up", "down", "left", "right"])
            else:
                # Exploitation: choose best action
                direction = max(self.q_table.get(state, {"up": 0, "down": 0, "left": 0, "right": 0}).items(), 
                              key=lambda x: x[1])[0]

            new_row, new_col = self.row, self.col
            if direction == "up": new_row -= 1
            elif direction == "down": new_row += 1
            elif direction == "left": new_col -= 1
            elif direction == "right": new_col += 1

            if self.eligible_move(maze, gate, new_row, new_col, is_player=True, stairs_positions=stairs_positions):
                next_state = self.get_state_key(new_row, new_col)
                reward = -1  # Default reward
                if (new_row, new_col) == (goal_row, goal_col):
                    reward = 100  # Goal reached
                elif self.manhattan_distance(new_row, new_col, mummy_row, mummy_col) < 2:
                    reward = -50  # Too close to mummy

                self.update_q_value(state, direction, reward, next_state)
                self.add_to_move_queue(direction, new_row, new_col)
                return True

        elif self.algorithm == "min_conflict":
            path = self.min_conflict_search(maze, (self.row, self.col), (goal_row, goal_col), gate, stairs_positions)
            if path and len(path) > 1:
                next_pos = path[1]
                direction = None
                if next_pos[0] < self.row: direction = "up"
                elif next_pos[0] > self.row: direction = "down"
                elif next_pos[1] < self.col: direction = "left"
                elif next_pos[1] > self.col: direction = "right"
                
                if direction:
                    self.add_to_move_queue(direction, next_pos[0], next_pos[1])
                    return True

        elif self.algorithm == "local_search":
            path = self.local_search(maze, (self.row, self.col), (goal_row, goal_col), gate, stairs_positions, mummy_row, mummy_col)
            if path and len(path) > 1:
                next_pos = path[1]
                direction = None
                if next_pos[0] < self.row: direction = "up"
                elif next_pos[0] > self.row: direction = "down"
                elif next_pos[1] < self.col: direction = "left"
                elif next_pos[1] > self.col: direction = "right"
                
                if direction:
                    self.add_to_move_queue(direction, next_pos[0], next_pos[1])
                    return True

        return False

    def set_algorithm(self, algorithm):
        self.algorithm = algorithm
        if algorithm == "q_learning":
            self.q_table = {}  # Reset Q-table when switching to Q-learning

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