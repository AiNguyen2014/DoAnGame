import pygame
import sys
from images import*
from constants import WIDTH, HEIGHT


class Menu:
    def __init__(self, menu_screen):
        self.menu_screen = menu_screen
        self.menu_bg = pygame.image.load("images/menuback.jpg")
        self.menu_logo = pygame.image.load("images/menulogo.png")
        self.menu_front = pygame.image.load("images/menufront.png")
        self.play_button = pygame.image.load("images/playgame_button.png")
        self.menu_quitgame = pygame.image.load("images/menu_quitgame.png")
        self.menu_map = pygame.image.load("images/menu_map.png")

        #Giữ nguyên tỷ lệ ảnh nhưng thu nhỏ 70% kích thước gốc của ảnh
        self.play_button = pygame.transform.scale(self.play_button, 
                                                (int(self.play_button.get_width() * 0.7),
                                                int(self.play_button.get_height() * 0.7)))
        self.menu_map = pygame.transform.scale(self.menu_map,
                                               (int(self.menu_map.get_width()* 0.7),
                                                int(self.menu_map.get_height() * 0.7)))
        self.menu_quitgame = pygame.transform.scale(self.menu_quitgame,
                                               (int(self.menu_quitgame.get_width()* 0.7),
                                                int(self.menu_quitgame.get_height() * 0.7)))
        
        #Lấy kích thước menu_front
        img_width, img_height = self.menu_front.get_size()
        self.x = (WIDTH - img_width) // 2
        self.y = (HEIGHT - img_height) // 2   #Canh giữa theo chiều ngang


        #Vị trí của button PLAY GAME
        self.btn_play_x = 205
        self.btn_play_y = 320
        self.play_rect_btn = self.play_button.get_rect(topleft=(self.btn_play_x, self.btn_play_y))

        #Vị trí của button MENU MAP
        self.btn_map_x = 205
        self.btn_map_y = 360
        self.map_rect_btn = self.menu_map.get_rect(topleft=(self.btn_map_x, self.btn_map_y)) 

        #Vị trí của button QUIT GAME
        self.btn_quit_x = 205
        self.btn_quit_y = 400
        self.quit_rect_btn = self.menu_quitgame.get_rect(topleft=(self.btn_quit_x, self.btn_quit_y))

    def draw_menu(self, title_y, mummy_y):
        """Vẽ màn hình menu lên screen"""
        self.menu_screen.blit(self.menu_bg, (0, 0))  #Vẽ menu background
        self.menu_screen.blit(self.menu_front, (self.x, mummy_y))  #Vẽ menu front
        self.menu_screen.blit(self.menu_logo, (98, title_y))  #Vẽ menu logo "MUMMY MAZE"
        
        #Cập nhật vị trí nút theo menu_front
        self.play_rect_btn.topleft = (self.btn_play_x, mummy_y + 300)
        self.map_rect_btn.topleft = (self.btn_map_x + 10, mummy_y + 340)  
        self.quit_rect_btn.topleft = (self.btn_quit_x + 5, mummy_y + 380)

        self.menu_screen.blit(self.play_button, self.play_rect_btn)  #Vẽ PLAY GAME button
        self.menu_screen.blit(self.menu_map, self.map_rect_btn) #Vẽ MENU MAP button
        self.menu_screen.blit(self.menu_quitgame, self.quit_rect_btn) #Vẽ MENU QUIT GAME button


    def handled_event(self, event):
        """Xử lý sự kiện trong menu"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.play_rect_btn.collidepoint(mouse_pos):
                return "play"
            #if self.map_rect_btn.collidepoint(mouse_pos):
               #return ""
            if self.quit_rect_btn.collidepoint(mouse_pos):
                pygame.quit()
                sys.exit()

        return "menu"

def transition(menu_screen, menu):
    """Hiệu ứng chuyển động khi xuất hiện màn hình menu"""
    # Vị trí ban đầu (ngoài màn hình)
    title_y = - 50 #Bắt đầu từ ngoài màn hình trên
    mummy_y = HEIGHT + 50 #Bắt đầu từ ngoài màn hình dưới

    target_y_title = 25 #Vì trí cuối cùng của chữ
    target_y_mummy = HEIGHT - 470 #Vị trí cuối cùng của Mummy
    
    #Tốc độ di chuyển của ảnh
    speed = 2
    
    running = True
    while running:
        menu_screen.fill((0, 0, 0))  # Xóa màn hình
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
        # Di chuyển title xuống
        if title_y < target_y_title:
            title_y += speed
        else:
            title_y = target_y_title  # Đảm bảo không đi quá
        
        # Di chuyển menu mummy lên
        if mummy_y > target_y_mummy:
            mummy_y -= speed
        else:
            mummy_y = target_y_mummy  # Đảm bảo không đi quá
        
        # Vẽ menu với các giá trị vị trí thay đổi
        menu.draw_menu(title_y, mummy_y)

        pygame.display.update()

        # Nếu cả 2 đã đến vị trí đích thì thoát khỏi hiệu ứng chuyển động
        if title_y == target_y_title and mummy_y == target_y_mummy:
            running = False
