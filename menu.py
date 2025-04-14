import pygame
import sys
from images import IMAGES
from constants import WIDTH, HEIGHT

class Menu:
    def __init__(self, menu_screen, map_instance):
        self.menu_screen = menu_screen
        self.map = map_instance
        self.menu_bg = IMAGES["menuback"]
        self.menu_logo = IMAGES["menulogo"]
        self.menu_front = IMAGES["menufront"]
        self.play_button = IMAGES["playgame_button"]
        self.menu_quitgame = IMAGES["menu_quitgame"]
        self.menu_map = IMAGES["menu_map"]

        self.play_button = pygame.transform.scale(self.play_button, 
                                                (int(self.play_button.get_width() * 0.7),
                                                int(self.play_button.get_height() * 0.7)))
        self.menu_map = pygame.transform.scale(self.menu_map,
                                               (int(self.menu_map.get_width() * 0.7),
                                                int(self.menu_map.get_height() * 0.7)))
        self.menu_quitgame = pygame.transform.scale(self.menu_quitgame,
                                               (int(self.menu_quitgame.get_width() * 0.7),  
                                                int(self.menu_quitgame.get_height() * 0.7)))
        
        img_width, img_height = self.menu_front.get_size()
        self.x = (WIDTH - img_width) // 2
        self.y = (HEIGHT - img_height) // 2

        self.btn_play_x = 205
        self.btn_play_y = 320
        self.play_rect_btn = self.play_button.get_rect(topleft=(self.btn_play_x, self.btn_play_y))

        self.btn_map_x = 205
        self.btn_map_y = 360
        self.map_rect_btn = self.menu_map.get_rect(topleft=(self.btn_map_x, self.btn_map_y)) 

        self.btn_quit_x = 205
        self.btn_quit_y = 400
        self.quit_rect_btn = self.menu_quitgame.get_rect(topleft=(self.btn_quit_x, self.btn_quit_y))

    def draw_menu(self, title_y, mummy_y):
        self.menu_screen.blit(self.menu_bg, (0, 0))
        self.menu_screen.blit(self.menu_front, (self.x, mummy_y))
        self.menu_screen.blit(self.menu_logo, (98, title_y))
        
        self.play_rect_btn.topleft = (self.btn_play_x, mummy_y + 300)
        self.map_rect_btn.topleft = (self.btn_map_x + 10, mummy_y + 340)  
        self.quit_rect_btn.topleft = (self.btn_quit_x + 5, mummy_y + 380)

        self.menu_screen.blit(self.play_button, self.play_rect_btn)
        self.menu_screen.blit(self.menu_map, self.map_rect_btn)
        self.menu_screen.blit(self.menu_quitgame, self.quit_rect_btn)

    def handled_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.play_rect_btn.collidepoint(mouse_pos):
                return "play"
            if self.map_rect_btn.collidepoint(mouse_pos):
                self.map.toggle("menu")
                return "map"
            if self.quit_rect_btn.collidepoint(mouse_pos):
                pygame.quit()
                sys.exit()

        return "menu"

def transition(menu_screen, menu):
    title_y = -50
    mummy_y = HEIGHT + 50

    target_y_title = 25
    target_y_mummy = HEIGHT - 470
    
    speed = 2
    
    running = True
    while running:
        menu_screen.fill((0, 0, 0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
        if title_y < target_y_title:
            title_y += speed
        else:
            title_y = target_y_title
        
        if mummy_y > target_y_mummy:
            mummy_y -= speed
        else:
            mummy_y = target_y_mummy
        
        menu.draw_menu(title_y, mummy_y)

        pygame.display.update()

        if title_y == target_y_title and mummy_y == target_y_mummy:
            running = False