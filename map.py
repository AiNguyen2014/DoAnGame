import pygame
from constants import WIDTH, HEIGHT

class Map:
    def __init__(self, map_screen, level_manager):
        self.map_screen = map_screen
        self.level_manager = level_manager
        self.adventure_map = pygame.image.load("images/adventuremap.jpg")
        self.active = False
        self.previous_state = None

        # Center the map image on the screen
        self.image_rect = self.adventure_map.get_rect(center=(WIDTH // 2, HEIGHT // 2))

        self.save_quit_button = pygame.image.load("images/save_and_quit.png").convert_alpha()
        self.enter_pyramid_button = pygame.image.load("images/enter_pyramid.png").convert_alpha()

        self.save_quit_button = pygame.transform.scale(
            self.save_quit_button,
            (int(self.save_quit_button.get_width() * 0.6), int(self.save_quit_button.get_height() * 0.6))
        )
        self.enter_pyramid_button = pygame.transform.scale(
            self.enter_pyramid_button,
            (int(self.enter_pyramid_button.get_width() * 0.6), int(self.enter_pyramid_button.get_height() * 0.6))
        )
        self.level_buttons = [
            {"rect": pygame.Rect(329, 351, 37, 36), "level": 0},  # Pyramid 1
            {"rect": pygame.Rect(416, 371, 36, 38), "level": 1},  # Pyramid 2
            {"rect": pygame.Rect(400, 291, 39, 40), "level": 2},  # Pyramid 3
            {"rect": pygame.Rect(354, 226, 39, 34), "level": 3},  # Pyramid 4
            {"rect": pygame.Rect(416, 163, 38, 37), "level": 4},  # Pyramid 5
            {"rect": pygame.Rect(352, 108, 38, 38), "level": 5},  # Pyramid 6
            {"rect": pygame.Rect(275, 141, 38, 37), "level": 6},  # Pyramid 7
            #{"rect": pygame.Rect(257, 271, 38, 38), "level": 7},  # Pyramid 8
            #{"rect": pygame.Rect(150, 319, 40, 39), "level": 8},  # Pyramid 9
            #{"rect": pygame.Rect(183, 212, 37, 39), "level": 9},  # Pyramid 10
            #{"rect": pygame.Rect(68, 272, 39, 39), "level": 10}, # Pyramid 11
            #{"rect": pygame.Rect(96, 177, 37, 37), "level": 11}, # Pyramid 12
            #{"rect": pygame.Rect(87, 81, 38, 40), "level": 12},  # Pyramid 13
            #{"rect": pygame.Rect(188, 121, 39, 38), "level": 13}, # Pyramid 14
        ]

        self.selected_level = None
        self.save_quit_rect = self.save_quit_button.get_rect(topleft=(self.image_rect.x + 5, self.image_rect.y + self.image_rect.height - 80))
        self.enter_pyramid_rect = self.enter_pyramid_button.get_rect(topleft=(self.image_rect.x + 5, self.image_rect.y + self.image_rect.height - 40))

        # Initialize font for level numbers
        self.font = pygame.font.Font(None, 24)  # Use default font, size 24

    def toggle(self, current_state=None):
        """Toggle the visibility of the map."""
        if self.active:  # Nếu bản đồ đang mở, đóng nó
            self.active = False
            self.selected_level = None
        else:  # Nếu bản đồ đang đóng, mở nó và lưu trạng thái trước đó
            self.active = True
            self.previous_state = current_state

    def draw(self):
        """Draw the map if active with level numbers on pyramids."""
        if not self.active:
            return
        self.map_screen.blit(self.adventure_map, self.image_rect)
        self.map_screen.blit(self.save_quit_button, self.save_quit_rect)
        self.map_screen.blit(self.enter_pyramid_button, self.enter_pyramid_rect)

        # Draw level numbers on each pyramid
        for button in self.level_buttons:
            # Calculate triangular vertices for the pyramid
            rect = button["rect"]
            center_x = rect.centerx
            center_y = rect.centery
            height = rect.height * 0.8  # Slightly less than full height to match pyramid shape
            width = rect.width * 0.6    # Narrower base to match pyramid width
            # Apex is at the top center, base is at the bottom with adjusted width
            apex_x = center_x
            apex_y = rect.top + (rect.height - height) // 2  # Center the triangle vertically
            base_left_x = center_x - width // 2
            base_right_x = center_x + width // 2
            base_y = apex_y + height
            triangle_points = [
                (apex_x, apex_y),
                (base_left_x, base_y),
                (base_right_x, base_y)
            ]

            # Highlight selected level with a filled triangle
            if self.selected_level == button["level"]:
                adjusted_points = [(x + self.image_rect.x, y + self.image_rect.y) for x, y in triangle_points]
                pygame.draw.polygon(self.map_screen, (255, 255, 0, 0), adjusted_points)  # Semi-transparent yellow

            # Draw level number
            level_number = str(button["level"] + 1)
            text_surface = self.font.render(level_number, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=button["rect"].center)
            adjusted_text_rect = text_rect.move(self.image_rect.x, self.image_rect.y)
            self.map_screen.blit(text_surface, adjusted_text_rect)

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
                    return self.previous_state
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