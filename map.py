import pygame
import os
from constants import WIDTH, HEIGHT

class Map:
    def __init__(self, map_screen, level_manager):
        self.map_screen = map_screen
        self.level_manager = level_manager

        # Đường dẫn chung đến thư mục images
        BASE_IMAGES_PATH = os.path.join(os.path.dirname(__file__), "images")

        # Tải các hình ảnh sử dụng đường dẫn chung
        self.adventure_map = pygame.image.load(os.path.join(BASE_IMAGES_PATH, "adventuremap.jpg"))
        self.save_quit_button = pygame.image.load(os.path.join(BASE_IMAGES_PATH, "save_and_quit.png")).convert_alpha()
        self.enter_pyramid_button = pygame.image.load(os.path.join(BASE_IMAGES_PATH, "enter_pyramid.png")).convert_alpha()

        self.active = False
        self.previous_state = None

        # Center the map image on the screen
        self.image_rect = self.adventure_map.get_rect(center=(WIDTH // 2, HEIGHT // 2))

        self.save_quit_button = pygame.transform.scale(
            self.save_quit_button,
            (int(self.save_quit_button.get_width() * 0.6), int(self.save_quit_button.get_height() * 0.6))
        )
        self.enter_pyramid_button = pygame.transform.scale(
            self.enter_pyramid_button,
            (int(self.enter_pyramid_button.get_width() * 0.6), int(self.enter_pyramid_button.get_height() * 0.6))
        )
        
        # Định nghĩa các nút cho các cấp độ
        self.level_buttons = [
            {"rect": pygame.Rect(150, 100, 40, 40), "level": 0},  # Pyramid 1 (top-left)
            {"rect": pygame.Rect(220, 90, 40, 40), "level": 1},   # Pyramid 2
            {"rect": pygame.Rect(280, 110, 40, 40), "level": 2},  # Pyramid 3
            {"rect": pygame.Rect(340, 90, 40, 40), "level": 3},   # Pyramid 4
            {"rect": pygame.Rect(400, 110, 40, 40), "level": 4},  # Pyramid 5
            {"rect": pygame.Rect(460, 90, 40, 40), "level": 5},   # Pyramid 6
            {"rect": pygame.Rect(150, 200, 40, 40), "level": 6},  # Pyramid 7
            {"rect": pygame.Rect(220, 180, 40, 40), "level": 7},  # Pyramid 8
            {"rect": pygame.Rect(280, 200, 40, 40), "level": 8},  # Pyramid 9
            {"rect": pygame.Rect(340, 180, 40, 40), "level": 9},  # Pyramid 10
            {"rect": pygame.Rect(400, 200, 40, 40), "level": 10}, # Pyramid 11
            {"rect": pygame.Rect(460, 180, 40, 40), "level": 11}, # Pyramid 12
            {"rect": pygame.Rect(220, 280, 40, 40), "level": 12}, # Pyramid 13
            {"rect": pygame.Rect(340, 280, 40, 40), "level": 13}, # Pyramid 14 (bottom-right)
        ]

        self.selected_level = None  # Lưu trữ mức đã chọn
        self.save_quit_rect = self.save_quit_button.get_rect(topleft=(self.image_rect.x + 5, self.image_rect.y + self.image_rect.height - 80))
        self.enter_pyramid_rect = self.enter_pyramid_button.get_rect(topleft=(self.image_rect.x + 5, self.image_rect.y + self.image_rect.height - 40))

    def toggle(self, current_state=None):
        """Toggle the visibility of the map."""
        if self.active:  # Nếu bản đồ đang mở, đóng nó
            self.active = False
            self.selected_level = None
        else:  # Nếu bản đồ đang đóng, mở nó và lưu trạng thái trước đó
            self.active = True
            self.previous_state = current_state

    def draw(self):
        """Draw the map if active."""
        if not self.active:
            return
        self.map_screen.blit(self.adventure_map, self.image_rect)
        self.map_screen.blit(self.save_quit_button, self.save_quit_rect)
        self.map_screen.blit(self.enter_pyramid_button, self.enter_pyramid_rect)

    def handle_event(self, event):
        """Handle events for the map (e.g., clicking on a pyramid)."""
        if not self.active:
            return False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            if self.save_quit_rect.collidepoint(mouse_pos):
                print("Save and Quit clicked!")
                self.active = False
                return self.previous_state

            if self.enter_pyramid_rect.collidepoint(mouse_pos):
                print("Enter Pyramid clicked!")
                if self.selected_level is not None:
                    self.active = False
                    return "play"
                return None
                 
            for button in self.level_buttons:
                adjusted_rect = button["rect"].copy()
                adjusted_rect.x += self.image_rect.x
                adjusted_rect.y += self.image_rect.y
                if adjusted_rect.collidepoint(mouse_pos):
                    self.selected_level = button["level"]
                    print(f"Selected level {self.selected_level + 1}")
                    return None
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.active = False
            return self.previous_state
        return None
