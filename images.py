import pygame
import os
from constants import CELL_SIZE

BASE_PATH = "./images"

def load_images():
    images = {}
    
    def split_sprite_sheet(sheet, frame_width, frame_count):
        frames = []
        for i in range(frame_count):
            frame = sheet.subsurface((i * frame_width, 0, frame_width, sheet.get_height()))
            frames.append(pygame.transform.scale(frame, (CELL_SIZE, CELL_SIZE)))
        return frames

    # Load Player images
    player_path = os.path.join(BASE_PATH, "player")
    images["player"] = {}
    directions = ["up", "down", "left", "right"]
    player_sprite_sheets = {
        "up": "move_up.png",
        "down": "move_down.png",
        "left": "move_left.png",
        "right": "move_right.png"
    }
    
    if os.path.exists(player_path):
        for direction in directions:
            images["player"][direction] = []
            file_name = player_sprite_sheets.get(direction, f"player_{direction}.png")
            file_path = os.path.join(player_path, file_name)
            try:
                if os.path.exists(file_path):
                    sprite_sheet = pygame.image.load(file_path)
                    frames = split_sprite_sheet(sprite_sheet, sprite_sheet.get_width() // 5, 5)
                    images["player"][direction].extend(frames)
                else:
                    print(f"Warning: Player sprite sheet {file_path} not found.")
                    placeholder = pygame.Surface((CELL_SIZE, CELL_SIZE))
                    placeholder.fill((0, 255, 0))
                    images["player"][direction] = [placeholder] * 4
            except pygame.error as e:
                print(f"Error loading player sprite sheet {file_path}: {e}")
                placeholder = pygame.Surface((CELL_SIZE, CELL_SIZE))
                placeholder.fill((0, 255, 0))
                images["player"][direction] = [placeholder] * 4
    else:
        print(f"Warning: Player image directory not found: {player_path}")
        for direction in directions:
            images["player"][direction] = [pygame.Surface((CELL_SIZE, CELL_SIZE)) for _ in range(4)]
            for frame in images["player"][direction]:
                frame.fill((0, 255, 0))
    
    # Load Mummy images
    mummy_path = os.path.join(BASE_PATH, "mummy")
    images["mummy"] = {}
    colors = ["white", "red"]
    mummy_sprite_sheets = {
        "white_up": "whiteup.png",
        "white_down": "whitedown.png",
        "white_left": "whiteleft.png",
        "white_right": "whiteright.png",
        "red_up": "redup.png",
        "red_down": "reddown.png",
        "red_left": "redleft.png",
        "red_right": "redright.png"
    }
    
    if os.path.exists(mummy_path):
        for color in colors:
            for direction in directions:
                key = f"{color}_{direction}"
                images["mummy"][key] = []
                file_name = mummy_sprite_sheets.get(key, f"{color}{direction}.png")
                file_path = os.path.join(mummy_path, file_name)
                try:
                    if os.path.exists(file_path):
                        sprite_sheet = pygame.image.load(file_path)
                        frames = split_sprite_sheet(sprite_sheet, sprite_sheet.get_width() // 5, 5)
                        images["mummy"][key].extend(frames)
                    else:
                        print(f"Warning: Mummy sprite sheet {file_path} not found.")
                        placeholder = pygame.Surface((CELL_SIZE, CELL_SIZE))
                        placeholder.fill((255, 165, 0))
                        images["mummy"][key] = [placeholder] * 4
                except pygame.error as e:
                    print(f"Error loading mummy sprite sheet {file_path}: {e}")
                    placeholder = pygame.Surface((CELL_SIZE, CELL_SIZE))
                    placeholder.fill((255, 165, 0))
                    images["mummy"][key] = [placeholder] * 4
    else:
        print(f"Error: Mummy image directory not found: {mummy_path}")
        for color in colors:
            for direction in directions:
                key = f"{color}_{direction}"
                images["mummy"][key] = [pygame.Surface((CELL_SIZE, CELL_SIZE)) for _ in range(4)]
                for frame in images["mummy"][key]:
                    frame.fill((255, 165, 0))
    
    # Load other images
    try:
        images["trap_skull"] = pygame.image.load(os.path.join(BASE_PATH, "trap_skull.png"))
        images["backdrop"] = pygame.image.load(os.path.join(BASE_PATH, "backdrop.png"))
        images["floor"] = pygame.image.load(os.path.join(BASE_PATH, "floor.jpg"))
        images["mumlogo"] = pygame.image.load(os.path.join(BASE_PATH, "mumlogo.png"))
        images["wall_horizontal"] = pygame.image.load(os.path.join(BASE_PATH, "wall_horizontal.png"))
        images["wall_vertical"] = pygame.image.load(os.path.join(BASE_PATH, "wall_vertical.png"))
        images["stairs_right"] = pygame.image.load(os.path.join(BASE_PATH, "stairs_right.png"))
        images["stairs_left"] = pygame.image.load(os.path.join(BASE_PATH, "stairs_left.png"))
        images["stairs_top"] = pygame.image.load(os.path.join(BASE_PATH, "stairs_top.png"))
        images["stairs_bottom"] = pygame.image.load(os.path.join(BASE_PATH, "stairs_bottom.png"))
        images["menuback"] = pygame.image.load(os.path.join(BASE_PATH, "menuback.jpg"))
        images["menulogo"] = pygame.image.load(os.path.join(BASE_PATH, "menulogo.png"))
        images["menufront"] = pygame.image.load(os.path.join(BASE_PATH, "menufront.png"))
        images["playgame_button"] = pygame.image.load(os.path.join(BASE_PATH, "playgame_button.png"))
        images["menu_quitgame"] = pygame.image.load(os.path.join(BASE_PATH, "menu_quitgame.png"))
        images["menu_map"] = pygame.image.load(os.path.join(BASE_PATH, "menu_map.png"))
        images["options"] = pygame.image.load(os.path.join(BASE_PATH, "options.png"))
        images["icon"] = pygame.image.load(os.path.join(BASE_PATH, "icon.png"))
        images["game_over"] = pygame.image.load(os.path.join(BASE_PATH, "game_over.png"))
    except pygame.error as e:
        print(f"Error loading image: {e}")
    
    return images

IMAGES = load_images()