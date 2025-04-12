import pygame
import sys
from images import*
from constants import WIDTH, HEIGHT

class LevelComplete:
    def __init__(self, level_complete_screen):
        self.level_complete_screen = level_complete_screen
        self.level_complete_img = pygame.image.load("images/levelcomplete.jpg")

    def draw_levelcomplete_screen(self):
        """Vẽ màn hình level complete lên screen"""
        self.level_complete_screen.blit(self.level_complete_img, (0, 0))