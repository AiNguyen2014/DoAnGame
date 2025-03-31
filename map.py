import pygame
from images import *

class Map:
    def __init__(self, map_screen):
        self.map_screen = map_screen
        self.adventure_map = pygame.image.load("images/adventuremap.jpg")
        