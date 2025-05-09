import pygame
from images import IMAGES
from constants import WIDTH, HEIGHT
from sprites import *
from menu import Menu, transition
from game import Game
from audio_manager import AudioManager
from map import Map
from level_manager import LevelManager

pygame.init()

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MUMMY MAZE")

pygame.display.set_icon(IMAGES["icon"])

audio_manager = AudioManager()
audio_manager.play_background_music()

level_manager = LevelManager()
map_instance = Map(SCREEN, level_manager)

menu = Menu(SCREEN, map_instance)
game = Game(SCREEN, audio_manager, level_manager, map_instance)

transition(SCREEN, menu)

game_state = "menu"

title_y = 25
mummy_y = HEIGHT - 470
target_y_title = 25
target_y_mummy = HEIGHT - 470
speed = 0

clock = pygame.time.Clock()
running = True


while running:
    SCREEN.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            print(pygame.mouse.get_pos())

        if game_state == "menu":
            game_state = menu.handled_event(event)
            if game_state == "map":
                map_instance.toggle(game_state)
            elif game_state in ["play", "auto_play"]:
                game.load_level()
        elif game_state == "map":
            result = map_instance.handle_event(event)
            if result is not None:
                game_state = result
                if game_state in ["play", "auto_play"] and map_instance.selected_level is not None:
                    level_manager.current_level = map_instance.selected_level
                    game.load_level()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                map_instance.toggle(game_state)
                game_state = map_instance.previous_state
        elif game_state in ["play", "auto_play"]:
            game_state = game.handled_event(event, game_state)
            if game_state == "map":
                map_instance.toggle(game_state)
            elif game_state == "load_level":
                game.load_level()
                game_state = "play"
        
    if game_state == "menu":
        menu.draw_menu(title_y, mummy_y)
    elif game_state == "map":
        map_instance.active = True
        map_instance.draw()
    elif game_state in ["play", "auto_play"]:
        game.draw_game()

    pygame.display.flip()

    clock.tick(50)
pygame.quit()