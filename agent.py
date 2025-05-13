import random
import pygame
import heapq
import copy
from collections import deque
from sprites import Mummy, Player, Trap
from constants import CELL_SIZE

def manhattan_distance(row1, col1, row2, col2):
    return abs(row1 - row2) + abs(col1 - col2)

def predict_mummy_moves(mummy, maze, gate, player_row, player_col, steps=2):
    """Giảm số bước dự đoán và vùng đệm của xác ướp"""
    possible_positions = {(mummy.row, mummy.col)}
    current_row, current_col = mummy.row, mummy.col
    directions = ["up", "down", "left", "right"]
    priority = ["left", "right", "up", "down"] if mummy.color == "white" else ["up", "down", "left", "right"]

    # Chỉ thêm vùng đệm 1 ô xung quanh xác ướp
    buffer_positions = set()
    for dr, dc in [(0,1), (0,-1), (1,0), (-1,0)]:  # Chỉ thêm 4 ô kề cạnh
        new_row, new_col = mummy.row + dr, mummy.col + dc
        if 0 <= new_row < len(maze) and 0 <= new_col < len(maze[0]):  # Kiểm tra giới hạn bản đồ
            buffer_positions.add((new_row, new_col))

    for _ in range(steps):  # Tăng số bước dự đoán
        current_distance = manhattan_distance(current_row, current_col, player_row, player_col)
        possible_moves = []
        
        for direction in directions:
            new_row, new_col = current_row, current_col
            if direction == "up": new_row -= 1
            elif direction == "down": new_row += 1
            elif direction == "left": new_col -= 1
            elif direction == "right": new_col += 1
            
            if mummy.eligible_move(maze, gate, new_row, new_col):
                new_distance = manhattan_distance(new_row, new_col, player_row, player_col)
                possible_moves.append((new_distance, direction, new_row, new_col))
        
        if not possible_moves:
            break
            
        possible_moves.sort(key=lambda x: x[0])
        min_distance = possible_moves[0][0]
        best_moves = [move for move in possible_moves if move[0] == min_distance]
        selected_move = min(best_moves, key=lambda x: priority.index(x[1]))
        current_row, current_col = selected_move[2], selected_move[3]
        possible_positions.add((current_row, current_col))
        
        # Thêm vùng đệm cho vị trí mới
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                buffer_positions.add((current_row + dr, current_col + dc))

    return possible_positions.union(buffer_positions)

class GameState:
    def __init__(self, game):
        self.player_pos = (game.player.row, game.player.col)
        self.maze = game.maze
        self.gate = game.gate
        self.mummies = [(m.row, m.col, m.color, m.direction) for m in game.mummies]
        self.traps = [((t.rect.y - 80) // CELL_SIZE, (t.rect.x - 215) // CELL_SIZE) for t in game.traps]
        self.goals = [(stair["row"], stair["col"]) for stair in game.stairs_positions]
        self.max_row = len(game.maze)
        self.max_col = len(game.maze[0]) if self.max_row > 0 else 0

    def get_mummy_positions(self):
        return [(m[0], m[1]) for m in self.mummies]

    def is_position_safe(self, row, col):
        if (row, col) in self.get_mummy_positions():
            return False
        if (row, col) in self.traps:
            return False
        return True

    def is_goal(self, row, col):
        return (row, col) in self.goals

def is_valid_move(game, game_state, current_row, current_col, new_row, new_col):
    if (new_row, new_col) in game_state.goals:
        return True

    max_row = game_state.max_row
    max_col = game_state.max_col
    if new_row < 0 or new_row >= max_row or new_col < 0 or new_col >= max_col:
        return False

    dr = new_row - current_row
    dc = new_col - current_col
    direction = None
    if dr == -1: direction = "top"
    elif dr == 1: direction = "bottom"
    elif dc == -1: direction = "left"
    elif dc == 1: direction = "right"

    current_cell = game_state.maze[current_row][current_col]
    if "walls" in current_cell and direction in current_cell["walls"]:
        return False

    target_cell = game_state.maze[new_row][new_col]
    opposite = {"top": "bottom", "bottom": "top", "left": "right", "right": "left"}
    if "walls" in target_cell and opposite[direction] in target_cell["walls"]:
        return False

    return True

def predict_mummy_moves_auto(game, game_state, mummy, player_row, player_col):
    """
    Dự đoán các di chuyển có thể của một mummy.
    Returns: List of tuples (direction, new_row, new_col)
    """
    # Handle different mummy data formats
    if hasattr(mummy, 'row'):
        current_row = mummy.row
        current_col = mummy.col
    elif isinstance(mummy, dict):
        current_row = mummy['row']
        current_col = mummy['col']
    else:
        current_row, current_col = mummy[0], mummy[1]
    
    current_distance = abs(current_row - player_row) + abs(current_col - player_col)
    possible_moves = []
    directions = [("up", -1, 0), ("down", 1, 0), ("left", 0, -1), ("right", 0, 1)]
    
    for direction_name, dr, dc in directions:
        new_row, new_col = current_row + dr, current_col + dc

        max_row = game_state.max_row
        max_col = game_state.max_col
        if not (0 <= new_row < max_row and 0 <= new_col < max_col):
            continue

        direction = None
        if dr == -1: direction = "top"
        elif dr == 1: direction = "bottom"
        elif dc == -1: direction = "left"
        elif dc == 1: direction = "right"

        current_cell = game_state.maze[current_row][current_col]
        if "walls" in current_cell and direction in current_cell["walls"]:
            continue

        target_cell = game_state.maze[new_row][new_col]
        opposite = {"top": "bottom", "bottom": "top", "left": "right", "right": "left"}
        if "walls" in target_cell and opposite[direction] in target_cell["walls"]:
            continue

        if game_state.gate.get("isClosed", False):
            if direction == "up" and current_row > 0 and game_state.maze[current_row - 1][current_col].get("gate"):
                continue
            if direction == "down" and current_row < max_row - 1 and game_state.maze[current_row + 1][current_col].get("gate"):
                continue
            if direction == "left" and current_col > 0 and game_state.maze[current_row][current_col - 1].get("gate"):
                continue
            if direction == "right" and current_col < max_col - 1 and game_state.maze[current_row][current_col + 1].get("gate"):
                continue

        new_distance = abs(new_row - player_row) + abs(new_col - player_col)
        if new_distance < current_distance:
            possible_moves.append((direction_name, new_row, new_col))

    return possible_moves

def is_mummy_blocked(game, game_state, mummy):
    """Kiểm tra xem mummy có bị chặn bởi tường không"""
    mummy_row, mummy_col = mummy[0], mummy[1]
    
    directions = [
        ("up", -1, 0, "top"),
        ("down", 1, 0, "bottom"),
        ("left", 0, -1, "left"),
        ("right", 0, 1, "right")
    ]
    
    blocked_count = 0
    for _, dr, dc, wall_dir in directions:
        new_row, new_col = mummy_row + dr, mummy_col + dc
        
        if new_row < 0 or new_row >= game_state.max_row or \
           new_col < 0 or new_col >= game_state.max_col:
            blocked_count += 1
            continue
            
        current_cell = game_state.maze[mummy_row][mummy_col]
        if "walls" in current_cell and wall_dir in current_cell["walls"]:
            blocked_count += 1
            continue
            
        target_cell = game_state.maze[new_row][new_col]
        opposite = {"top": "bottom", "bottom": "top", "left": "right", "right": "left"}
        if "walls" in target_cell and opposite[wall_dir] in target_cell["walls"]:
            blocked_count += 1
            
    return blocked_count >= 3

def calculate_safety_score(state):
    """Tính điểm an toàn với trọng số mới"""
    player_row, player_col = state.player_pos
    safety_score = 0
    
    if hasattr(state, 'previous_positions') and len(state.previous_positions) > 0:
        if (player_row, player_col) in state.previous_positions[-4:]:
            safety_score -= 1000

    for mummy in state.mummies:
        distance = abs(player_row - mummy[0]) + abs(player_col - mummy[1])
        
        if is_mummy_blocked(None, state, mummy):
            safety_score += 500
        else:
            if distance <= 1:
                safety_score -= 2000
            elif distance <= 2:
                safety_score -= 1000
            elif distance <= 3:
                safety_score -= 500
            else:
                safety_score += distance * 10

    min_goal_dist = min(abs(player_row - goal[0]) + abs(player_col - goal[1]) 
                       for goal in state.goals)
    goal_weight = 10 if any(is_mummy_blocked(None, state, m) for m in state.mummies) else 5
    safety_score -= min_goal_dist * goal_weight

    return safety_score

def find_alternative_path(game, game_state):
    """Tìm đường đi thay thế khi phát hiện loop"""
    start = game_state.player_pos
    goals = game_state.goals
    
    goal = min(goals, key=lambda g: abs(g[0] - start[0]) + abs(g[1] - start[1]))
    dr = goal[0] - start[0]
    dc = goal[1] - start[1]
    
    directions = []
    if abs(dr) > abs(dc):
        if dc > 0:
            directions.extend(["right", "up", "down", "left"])
        else:
            directions.extend(["left", "up", "down", "right"])
    else:
        if dr > 0:
            directions.extend(["down", "left", "right", "up"])
        else:
            directions.extend(["up", "left", "right", "down"])

    for direction in directions:
        new_row, new_col = start
        if direction == "up": new_row -= 1
        elif direction == "down": new_row += 1
        elif direction == "left": new_col -= 1
        elif direction == "right": new_col += 1

        if not is_valid_move(game, game_state, start[0], start[1], new_row, new_col):
            continue

        safe = True
        for mummy in game_state.mummies:
            distance = abs(new_row - mummy[0]) + abs(new_col - mummy[1])
            if distance <= 1:
                safe = False
                break

        if safe and (new_row, new_col) not in game.blocked_positions:
            return direction

    return None

def analyze_situation(game, game_state):
    start = game_state.player_pos
    goals = game_state.goals

    if any(abs(start[0] - goal[0]) + abs(start[1] - goal[1]) <= 1 for goal in goals):
        return "can_reach_goal_safely"

    mummy_blocked = all(is_mummy_blocked(game, game_state, mummy) 
                       for mummy in game_state.mummies)
    
    if mummy_blocked:
        path = find_path_to_goal(game, game_state)
        if path:
            return "can_reach_goal_safely"
    
    path = find_safe_path_to_goal(game, game_state)
    if path:
        return "can_reach_goal_safely"

    return "find_safe_path"

def find_path_to_goal(game, game_state):
    start = game_state.player_pos
    goals = game_state.goals

    for goal in goals:
        dr = goal[0] - start[0]
        dc = goal[1] - start[1]
        if abs(dr) + abs(dc) == 1:
            if dr == 1: return "down"
            if dr == -1: return "up"
            if dc == 1: return "right"
            if dc == -1: return "left"

    path = bfs_search(game, game_state, start, goals)
    return path if path else None

def bfs_search(game, game_state, start, goals, max_depth=10):
    queue = deque([(copy.deepcopy(game_state), [], 0)])
    visited = set()

    while queue:
        state, actions, depth = queue.popleft()
        
        state_key = (state.player_pos, tuple(sorted((m[0], m[1]) for m in state.mummies)))
        if state_key in visited:
            continue
        visited.add(state_key)

        if depth > max_depth:
            continue

        if state.is_goal(state.player_pos[0], state.player_pos[1]):
            return actions[0] if actions else None

        if (state.player_pos in [(m[0], m[1]) for m in state.mummies]) or (state.player_pos in state.traps):
            continue

        directions = ["up", "down", "left", "right"]
        for direction in directions:
            new_row, new_col = state.player_pos
            if direction == "up": new_row -= 1
            elif direction == "down": new_row += 1
            elif direction == "left": new_col -= 1
            elif direction == "right": new_col += 1

            if not is_valid_move(game, game_state, state.player_pos[0], state.player_pos[1], new_row, new_col):
                continue

            new_state = copy.deepcopy(state)
            new_state.player_pos = (new_row, new_col)

            new_mummies = []
            mummy_positions = []
            
            for mummy in new_state.mummies:
                mummy_data = {
                    'row': mummy[0],
                    'col': mummy[1],
                    'color': mummy[2],
                    'direction': mummy[3]
                }
                
                moves = predict_mummy_moves_auto(game, new_state, mummy_data, new_row, new_col)
                if moves:
                    new_pos = (moves[0][1], moves[0][2])
                    new_mummies.append((new_pos[0], new_pos[1], mummy[2], moves[0][0]))
                    mummy_positions.append(new_pos)
                else:
                    new_mummies.append(mummy)
                    mummy_positions.append((mummy[0], mummy[1]))

            position_counts = {}
            for pos in mummy_positions:
                position_counts[pos] = position_counts.get(pos, 0) + 1
            new_mummies = [m for m in new_mummies if position_counts[(m[0], m[1])] <= 1]
            new_state.mummies = new_mummies

            queue.append((new_state, actions + [direction], depth + 1))

    return None

def find_safe_path_to_goal(game, game_state):
    start = game_state.player_pos
    goals = game_state.goals
    queue = deque([(copy.deepcopy(game_state), [], 0)])
    visited = set()
    best_path = None
    best_safety_score = float('-inf')

    while queue:
        state, actions, depth = queue.popleft()
        
        if depth > 10:
            continue

        state_key = (state.player_pos, tuple(sorted((m[0], m[1]) for m in state.mummies)))
        if state_key in visited:
            continue
        visited.add(state_key)

        if state.is_goal(state.player_pos[0], state.player_pos[1]):
            return actions[0] if actions else None

        if (state.player_pos in [(m[0], m[1]) for m in state.mummies]) or (state.player_pos in state.traps):
            continue

        current_safety = calculate_safety_score(state)
        if best_path is None or current_safety > best_safety_score:
            if state.is_goal(state.player_pos[0], state.player_pos[1]):
                best_path = actions[0] if actions else None
                best_safety_score = current_safety

        for direction in ["up", "down", "left", "right"]:
            new_row, new_col = state.player_pos
            if direction == "up": new_row -= 1
            elif direction == "down": new_row += 1
            elif direction == "left": new_col -= 1
            elif direction == "right": new_col += 1

            if not is_valid_move(game, state, state.player_pos[0], state.player_pos[1], new_row, new_col):
                continue

            new_state = copy.deepcopy(state)
            new_state.player_pos = (new_row, new_col)

            new_mummies = []
            mummy_positions = []
            for mummy in new_state.mummies:
                mummy_data = {
                    'row': mummy[0],
                    'col': mummy[1],
                    'color': mummy[2],
                    'direction': mummy[3]
                }
                
                moves = predict_mummy_moves_auto(game, new_state, mummy_data, new_row, new_col)
                if moves:
                    new_pos = (moves[0][1], moves[0][2])
                    new_mummies.append((new_pos[0], new_pos[1], mummy[2], moves[0][0]))
                    mummy_positions.append(new_pos)
                else:
                    new_mummies.append(mummy)
                    mummy_positions.append((mummy[0], mummy[1]))

            position_counts = {}
            for pos in mummy_positions:
                position_counts[pos] = position_counts.get(pos, 0) + 1
            new_mummies = [m for m in new_mummies if position_counts[(m[0], m[1])] <= 1]
            new_state.mummies = new_mummies

            queue.append((new_state, actions + [direction], depth + 1))

    return best_path

def stall_safely(game, game_state):
    directions = ["up", "down", "left", "right"]
    safe_directions = []

    for direction in directions:
        player_row, player_col = game_state.player_pos
        new_row, new_col = player_row, player_col
        if direction == "up": new_row -= 1
        elif direction == "down": new_row += 1
        elif direction == "left": new_col -= 1
        elif direction == "right": new_col += 1

        if not is_valid_move(game, game_state, player_row, player_col, new_row, new_col):
            continue

        trap_penalty = 50 if (new_row, new_col) in game_state.traps else 0

        mummy_danger = 0
        min_goal_dist = min(abs(new_row - g[0]) + abs(new_col - g[1]) for g in game_state.goals)
        for mummy in game_state.mummies:
            distance = abs(new_row - mummy[0]) + abs(new_col - mummy[1])
            if min_goal_dist > 1:
                if distance <= 1:
                    mummy_danger += 200
                elif distance <= 2:
                    mummy_danger += 80
                elif distance <= 3:
                    mummy_danger += 20

        nearest_goal = min(game_state.goals, key=lambda g: abs(g[0] - new_row) + abs(g[1] - new_col))
        goal_distance = abs(new_row - nearest_goal[0]) + abs(new_col - nearest_goal[1])
        goal_score = 100 - goal_distance

        final_score = goal_score * 0.7 - mummy_danger * 0.3 - trap_penalty
        safe_directions.append((final_score, direction))

    if safe_directions:
        safe_directions.sort(reverse=True)
        return safe_directions[0][1]

    least_dangerous = find_least_dangerous_move(game, game_state)
    return least_dangerous

def find_least_dangerous_move(game, game_state):
    directions = ["up", "down", "left", "right"]
    moves_with_scores = []

    for direction in directions:
        player_row, player_col = game_state.player_pos
        new_row, new_col = player_row, player_col
        if direction == "up": new_row -= 1
        elif direction == "down": new_row += 1
        elif direction == "left": new_col -= 1
        elif direction == "right": new_col += 1

        if not is_valid_move(game, game_state, player_row, player_col, new_row, new_col):
            continue

        if (new_row, new_col) in game_state.traps:
            continue

        danger_score = 0
        min_goal_dist = min(abs(new_row - g[0]) + abs(new_col - g[1]) for g in game_state.goals)
        for mummy in game_state.mummies:
            distance = abs(new_row - mummy[0]) + abs(new_col - mummy[1])
            if min_goal_dist > 1:
                if distance == 0:
                    danger_score += 10000
                elif distance == 1:
                    danger_score += 2000
                elif distance == 2:
                    danger_score += 500
                else:
                    danger_score += 100 / max(1, distance)

        trapped_score = 0
        exit_count = 0
        temp_directions = [("up", -1, 0), ("down", 1, 0), ("left", 0, -1), ("right", 0, 1)]
        for _, dr, dc in temp_directions:
            if is_valid_move(game, game_state, new_row, new_col, new_row + dr, new_col + dc):
                exit_count += 1
        if exit_count <= 1:
            trapped_score = 500
        elif exit_count == 2:
            trapped_score = 200

        goal_distance = min(abs(new_row - goal[0]) + abs(new_col - goal[1]) for goal in game_state.goals)
        goal_score = goal_distance * 5

        total_danger = danger_score + trapped_score + goal_score
        moves_with_scores.append((total_danger, direction))

    if moves_with_scores:
        return min(moves_with_scores, key=lambda x: x[0])[1]

    for direction in random.sample(directions, len(directions)):
        player_row, player_col = game_state.player_pos
        new_row, new_col = player_row, player_col
        if direction == "up": new_row -= 1
        elif direction == "down": new_row += 1
        elif direction == "left": new_col -= 1
        elif direction == "right": new_col += 1
        if is_valid_move(game, game_state, player_row, player_col, new_row, new_col):
            return direction

    return None

def search_no_observation(game, game_state):
    """Search with No Observation algorithm implementation"""
    start = game_state.player_pos
    goals = game_state.goals
    
    # Initialize exploration grid
    explored = set()
    frontier = [(0, start, [])]  # (cost, position, path)
    heapq.heapify(frontier)
    
    while frontier:
        cost, current, path = heapq.heappop(frontier)
        
        if current in explored:
            continue
            
        explored.add(current)
        
        # Check if goal reached
        if current in goals:
            return path[0] if path else None
            
        # Generate possible moves
        directions = ["up", "down", "left", "right"]
        for direction in directions:
            new_row, new_col = current
            if direction == "up": new_row -= 1
            elif direction == "down": new_row += 1
            elif direction == "left": new_col -= 1
            elif direction == "right": new_col += 1
            
            new_pos = (new_row, new_col)
            
            if not is_valid_move(game, game_state, current[0], current[1], new_row, new_col):
                continue
                
            # Calculate heuristic cost
            min_goal_dist = min(manhattan_distance(new_row, new_col, g[0], g[1]) 
                              for g in goals)
            
            # Calculate safety score
            safety = 0
            for mummy in game_state.mummies:
                mummy_dist = manhattan_distance(new_row, new_col, mummy[0], mummy[1])
                if mummy_dist <= 1:
                    safety -= 1000
                elif mummy_dist <= 2:
                    safety -= 500
                    
            # Total cost combines distance and safety
            new_cost = min_goal_dist - safety
            
            # Add to frontier
            new_path = path + [direction] if path else [direction]
            heapq.heappush(frontier, (new_cost, new_pos, new_path))
    
    return None

def auto_play_step(game):
    """Thực hiện một bước tự động với logic từ auto_agent"""
    if not hasattr(game, 'blocked_positions'):
        game.blocked_positions = set()
    if not hasattr(game, 'reset_counter'):
        game.reset_counter = 0
    if not hasattr(game, 'previous_positions'):
        game.previous_positions = []

    if game.game_over:
        print(f"Game over! Reason: {'Collision with mummy' if pygame.sprite.spritecollide(game.player, game.characters, False) else 'Trap or other'}")
        game.blocked_positions.clear()
        return "auto_play"

    if game.player.moving or game.player.move_queue or any(mummy.moving or mummy.move_queue for mummy in game.mummies):
        return "auto_play"

    game_state = GameState(game)

    current_pos = (game.player.row, game.player.col)
    game.previous_positions.append(current_pos)
    if len(game.previous_positions) > 6:
        game.previous_positions.pop(0)

    if len(game.previous_positions) >= 4:
        last_4_pos = game.previous_positions[-4:]
        if len(set(last_4_pos)) <= 2:
            print("Detected short loop pattern, forcing path recalculation")
            game.blocked_positions.clear()
            game.previous_positions.clear()
            return find_alternative_path(game, game_state)

    position_counts = {}
    for pos in game.previous_positions:
        position_counts[pos] = position_counts.get(pos, 0) + 1

    for pos, count in position_counts.items():
        if count >= 3:
            print(f"Detected loop at {pos}, resetting nearby blocked positions")
            game.blocked_positions = {
                move for move in game.blocked_positions
                if abs(move[0] - current_pos[0]) > 2 or abs(move[1] - current_pos[1]) > 2
            }
            game.previous_positions.clear()
            break

    mummies_data = [{"row": m.row, "col": m.col, "color": m.color, "direction": m.direction} for m in game.mummies]
    traps_data = [{"row": (t.rect.y - 80) // CELL_SIZE, "col": (t.rect.x - 215) // CELL_SIZE} for t in game.traps]
    game.move_history.append({
        "player_pos": (game.player.row, game.player.col),
        "mummies": mummies_data,
        "traps": traps_data
    })

    if game_state.is_goal(game.player.row, game.player.col):
        print(f"Reached goal at {current_pos}!")
        return "auto_play"

    situation = analyze_situation(game, game_state)
    mummy_positions = [(m.row, m.col) for m in game.mummies]
    print(f"Level {game.level_manager.current_level + 1}, Situation: {situation}, Player at {current_pos}, Mummies at {mummy_positions}")

    next_move = None
    if hasattr(game.player, 'current_algorithm') and game.player.current_algorithm == "search_no_observation":
        next_move = search_no_observation(game, game_state)
    else:
        if situation == "can_reach_goal_safely":
            next_move = find_path_to_goal(game, game_state)
        else:
            next_move = search_no_observation(game, game_state)
            if not next_move:
                next_move = find_safest_path(game, game_state)

    if game.player.current_algorithm == "search_no_observation":
        next_move = search_no_observation(game, game_state)

    if next_move:
        print(f"Attempting move: {next_move}")
        player_move_success = game.player.move(next_move, game.maze, game.gate, game.stairs_positions)
        if not player_move_success:
            new_row, new_col = game.player.row, game.player.col
            if next_move == "up": new_row -= 1
            elif next_move == "down": new_row += 1
            elif next_move == "left": new_col -= 1
            elif next_move == "right": new_col += 1
            game.blocked_positions.add((game.player.row, game.player.col, new_row, new_col))
            print(f"Move {next_move.upper()} blocked! Added to blocked list.")
            return "auto_play"

        for mummy in game.mummies:
            mummy.auto_move(game.maze, game.gate, game.player.row, game.player.col)

        game.reset_counter = 0
        return game.check_collisions()

    print("No valid move found, stalling")
    return "auto_play"

def find_safest_path(game, game_state):
    start = game_state.player_pos
    goals = game_state.goals
    path = bfs_search(game, game_state, start, goals)
    return path if path else stall_safely(game, game_state)