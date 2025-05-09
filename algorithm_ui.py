import pygame
from constants import WIDTH

class AlgorithmUI:
    def __init__(self, screen):
        self.screen = screen
        # Thêm thuật toán local_search vào danh sách
        self.algorithms = ["a_star", "q_learning", "min_conflict", "bfs", "local_search"]
        # Tên hiển thị cho người dùng
        self.algorithm_names = {
            "a_star": "A* Search",
            "q_learning": "Q-Learning",
            "min_conflict": "Min-Conflict",
            "bfs": "BFS",
            "local_search": "Local Search"
        }
        self.selected_algorithm = "a_star"  # Mặc định là A*
        self.is_expanded = False
        self.button_rect = pygame.Rect(WIDTH - 150, 10, 140, 30)
        self.dropdown_rects = []
        self.font = pygame.font.Font(None, 24)
        self.update_dropdown_rects()

    def update_dropdown_rects(self):
        self.dropdown_rects = []
        for i, algo in enumerate(self.algorithms):
            rect = pygame.Rect(
                self.button_rect.x,
                self.button_rect.y + (i + 1) * 30,
                self.button_rect.width,
                30
            )
            self.dropdown_rects.append(rect)

    def draw(self):
        # Draw main button
        pygame.draw.rect(self.screen, (50, 50, 50), self.button_rect)
        pygame.draw.rect(self.screen, (200, 200, 200), self.button_rect, 2)
        
        # Draw selected algorithm text
        text = self.font.render(self.algorithm_names[self.selected_algorithm], True, (255, 255, 255))
        text_rect = text.get_rect(center=self.button_rect.center)
        self.screen.blit(text, text_rect)

        # Draw dropdown if expanded
        if self.is_expanded:
            for i, rect in enumerate(self.dropdown_rects):
                pygame.draw.rect(self.screen, (50, 50, 50), rect)
                pygame.draw.rect(self.screen, (200, 200, 200), rect, 1)
                
                text = self.font.render(self.algorithm_names[self.algorithms[i]], True, (255, 255, 255))
                text_rect = text.get_rect(center=rect.center)
                self.screen.blit(text, text_rect)

    def handle_click(self, pos):
        if self.button_rect.collidepoint(pos):
            self.is_expanded = not self.is_expanded
            return None
        
        if self.is_expanded:
            for i, rect in enumerate(self.dropdown_rects):
                if rect.collidepoint(pos):
                    self.selected_algorithm = self.algorithms[i]
                    self.is_expanded = False
                    return self.selected_algorithm
        
        return None

    def get_selected_algorithm(self):
        return self.selected_algorithm