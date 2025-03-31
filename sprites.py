import pygame
from images import*
from constants import*

class Wall(pygame.sprite.Sprite):
    def __init__(self, x , y , wall_type):
        super().__init__()
        if wall_type == "W_h":
             self.image = pygame.image.load("images/wall_horizontal.png")
        elif wall_type == "W_v":
            self.image = pygame.image.load("images/wall_vertical.png")
        else:
            raise ValueError(f"Loại tường không hợp lệ: {wall_type}")
        
        # Chuyển đổi kích thước hình ảnh tường
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

        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))
        self.rect = self.image.get_rect(topleft=(x, y))