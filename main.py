import pygame
from images import*
from constants import WIDTH, HEIGHT
from sprites  import*
from menu import Menu, transition
from game import Game
from audio_manager import AudioManager

pygame.init()

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MUMMY MAZE")

icon_img = pygame.image.load("images/icon.png")
pygame.display.set_icon(icon_img)

audio_manager = AudioManager()
audio_manager.play_background_music()

#Tạo đối tượng Menu
menu = Menu(SCREEN)
game = Game(SCREEN, audio_manager)

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

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            print(pygame.mouse.get_pos())

        #Chuyển trạng thái game dựa vào sự kiện
        if game_state == "menu":
            game_state = menu.handled_event(event)
        if game_state == "play":
            game_state = game.handled_event(event)
        
    #Hiển thị màn hình theo trạng thái game
    if game_state == "menu":
        menu.draw_menu(title_y, mummy_y)
    elif game_state == "play":
        game.draw_game()

    
    pygame.display.flip()

    clock.tick(30) #Giới hạn FPS

pygame.quit()