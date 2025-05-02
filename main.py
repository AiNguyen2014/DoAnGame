import pygame
from constants import WIDTH, HEIGHT
from sprites  import*
from menu import Menu, transition
from game import Game
from map import Map
from levelcomplete import LevelComplete
from audio_manager import AudioManager
from level_manager import *
from images_manager import *

pygame.init()

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MUMMY MAZE")

pygame.display.set_icon(IMAGES["icon"])

#Tạo đối tượng AudioManager
audio_manager = AudioManager()
audio_manager.play_background_music()

#Tạo đối tượng LevelManager
level_manager = LevelManager()

#Tạo đối tượng Map
map_instance = Map(SCREEN, level_manager)

#Tạo đối tượng Menu và Game
menu = Menu(SCREEN, map_instance)
game = Game(SCREEN, audio_manager, level_manager, map_instance)

#Gọi hiệu ứng transition trước khi hiển thị menu
transition(SCREEN, menu)

#Trạng thái game
game_state = "menu"

# Khai báo biến cho vị trí menu
title_y = 25  # Sau khi transition xong
mummy_y = HEIGHT - 470
target_y_title = 25
target_y_mummy = HEIGHT - 470
speed = 0

#Vòng lặp game
clock = pygame.time.Clock()
running = True

while running:
    SCREEN.fill((0,0,0))   #Xóa màn hình

    #Xử lý các sự kiện
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            print(pygame.mouse.get_pos())

        # Chuyển trạng thái game dựa vào sự kiện
        if game_state == "menu":
            game_state = menu.handled_event(event)
            if game_state == "map":
                map_instance.toggle(game_state)
        elif game_state == "map":
            result = map_instance.handle_event(event)
            if result is not None:
                game_state = result
                if game_state == "play" and map_instance.selected_level is not None:
                    level_manager.current_level = map_instance.selected_level
                    game.load_level()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                map_instance.toggle(game_state)
                game_state = map_instance.previous_state
        elif game_state == "play":
            result = game.handled_event(event)
            if result is not None:
                game_state = result
            if game_state == "map":
                map_instance.toggle(game_state)
            elif game_state == "load_level":
                game.load_level()
                game_state = "play"

    #Vẽ giao diện dựa vào trạng thái 
    if game_state == "menu":
        menu.draw_menu(title_y, mummy_y)
    elif game_state == "map":
        map_instance.active = True
        map_instance.draw()
    elif game_state == "play":
        game.draw_game()

    pygame.display.flip()

    clock.tick(50)
pygame.quit()