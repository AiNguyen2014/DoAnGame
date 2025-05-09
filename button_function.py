import pygame
from audio_manager import *
from images import IMAGES
def undo_move(audio_manager):
    print("Undo Move clicked!")
    audio_manager.play_button_click()

def reset_maze(audio_manager):
    print("Reset Maze clicked!")
    audio_manager.play_button_click()

def show_world_map(game, audio_manager):
    print("World Map clicked!")
    audio_manager.play_button_click()

def quit_to_main(audio_manager):
    print("Quit to Main clicked!")
    audio_manager.play_button_click()

class Slider:
    def __init__(self, x, y, width, value=50):
        self.rect = pygame.Rect(x, y, width, 10)
        self.value = value
        self.handle_rect = pygame.Rect(x + (width * value // 100) - 5, y - 5, 10, 20)  
        self.dragging = False

    def draw(self, screen):
        pygame.draw.rect(screen, (128, 128, 128), self.rect)
        pygame.draw.rect(screen, (255, 215, 0), self.handle_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.handle_rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            mouse_x = event.pos[0]
            if mouse_x < self.rect.left:
                mouse_x = self.rect.left
            elif mouse_x > self.rect.right:
                mouse_x = self.rect.right
            self.handle_rect.x = mouse_x - self.handle_rect.width // 2
            self.value = ((self.handle_rect.x - self.rect.x) / self.rect.width) * 100
            
class OptionsMenu:
    def __init__(self, audio_manager):
        self.active = False
        self.audio_manager = audio_manager

        self.options_image = IMAGES["options"]
        self.options_image = pygame.transform.scale(self.options_image, (400, 400))
        self.image_rect = self.options_image.get_rect(topleft=(150, 50))
        
        self.music_slider = Slider(270, 120, 250)
        self.sound_slider = Slider(270, 150, 250)
        
        self.done_button = pygame.Rect(180, 377, 338, 35)

    def draw(self, screen):
        if not self.active:
            return

        screen.blit(self.options_image, self.image_rect)

        self.music_slider.draw(screen)
        self.sound_slider.draw(screen)

    def handle_event(self, event):
        if not self.active:
            return False

        self.music_slider.handle_event(event)
        self.sound_slider.handle_event(event)

        self.audio_manager.set_music_volume(self.music_slider.value)
        self.audio_manager.set_sfx_volume(self.sound_slider.value)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.done_button.collidepoint(event.pos):
                self.active = False
                print("DONE button clicked, closing options menu")
                self.audio_manager.play_button_click()
                return True
        return False

def show_options(options_menu, audio_manager):
    options_menu.active = True
    print("Options clicked!")
    audio_manager.play_button_click()