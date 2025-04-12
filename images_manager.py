import pygame
import os

# Đường dẫn đến thư mục images
BASE_PATH = os.path.join(os.path.dirname(__file__), "images")

def load_images():
    """Load tất cả hình ảnh từ thư mục images và các thư mục con"""
    images = {}

    # Load hình ảnh cho Player
    player_path = os.path.join(BASE_PATH, "player")
    images["player"] = {}
    for file_name in os.listdir(player_path):
        if file_name.endswith(".png"):
            # Ví dụ: file_name = "player_up.png" -> key = "up"
            direction = file_name.replace("player_", "").replace(".png", "")
            images["player"][direction] = pygame.image.load(os.path.join(player_path, file_name))

    # Load hình ảnh cho Mummy
    mummy_path = os.path.join(BASE_PATH, "mummy")
    images["mummy"] = {}
    for file_name in os.listdir(mummy_path):
        if file_name.endswith(".png"):
            # Ví dụ: file_name = "mummy_white_up.png" -> key = "white_up"
            key = file_name.replace("mummy_", "").replace(".png", "")
            images["mummy"][key] = pygame.image.load(os.path.join(mummy_path, file_name))

    # Load hình ảnh cho Scorpion
    scorpion_path = os.path.join(BASE_PATH, "scorpion")
    images["scorpion"] = {}
    for file_name in os.listdir(scorpion_path):
        if file_name.endswith(".png"):
            # Ví dụ: file_name = "scorpion_white_up.png" -> key = "white_up"
            key = file_name.replace("scorpion_", "").replace(".png", "")
            images["scorpion"][key] = pygame.image.load(os.path.join(scorpion_path, file_name))

    # Load các hình ảnh khác (Trap, Key, Fence, v.v.)
    images["trap_skull"] = pygame.image.load(os.path.join(BASE_PATH, "trap_skull.png"))
    images["key"] = pygame.image.load(os.path.join(BASE_PATH, "key6.png"))

    # Load hình ảnh giao diện
    images["backdrop"] = pygame.image.load(os.path.join(BASE_PATH, "backdrop.png"))
    images["floor"] = pygame.image.load(os.path.join(BASE_PATH, "floor.jpg"))
    images["mumlogo"] = pygame.image.load(os.path.join(BASE_PATH, "mumlogo.png"))
    images["wall_horizontal"] = pygame.image.load(os.path.join(BASE_PATH, "wall_horizontal.png"))
    images["wall_vertical"] = pygame.image.load(os.path.join(BASE_PATH, "wall_vertical.png"))
    images["stairs_right"] = pygame.image.load(os.path.join(BASE_PATH, "stairs_right.png"))
    images["stairs_left"] = pygame.image.load(os.path.join(BASE_PATH, "stairs_left.png"))
    images["stairs_top"] = pygame.image.load(os.path.join(BASE_PATH, "stairs_top.png"))
    images["stairs_bottom"] = pygame.image.load(os.path.join(BASE_PATH, "stairs_bottom.png"))

    # Load hình ảnh menu
    images["menuback"] = pygame.image.load(os.path.join(BASE_PATH, "menuback.jpg"))
    images["menulogo"] = pygame.image.load(os.path.join(BASE_PATH, "menulogo.png"))
    images["menufront"] = pygame.image.load(os.path.join(BASE_PATH, "menufront.png"))
    images["playgame_button"] = pygame.image.load(os.path.join(BASE_PATH, "playgame_button.png"))
    images["menu_quitgame"] = pygame.image.load(os.path.join(BASE_PATH, "menu_quitgame.png"))
    images["menu_map"] = pygame.image.load(os.path.join(BASE_PATH, "menu_map.png"))
    images["options"] = pygame.image.load(os.path.join(BASE_PATH, "options.png"))
    images["icon"] = pygame.image.load(os.path.join(BASE_PATH, "icon.png"))

    return images

IMAGES = load_images()