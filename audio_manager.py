import pygame

class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        self.music_volume = 0.5
        self.sfx_volume = 0.5

        try:
            self.background_music = pygame.mixer.Sound("sounds/Title.mp3")
        except pygame.error:
            print("Background music file not found! Please add 'background_music.mp3' to the 'sounds' folder.")
            self.background_music = None
        
        try:
            self.button_click = pygame.mixer.Sound("sounds/button_click.wav")
        except pygame.error:
            print("Button click sound file not found! Please add 'button_click.wav' to the 'sounds' folder.")
            self.button_click = None

        if self.background_music:
            self.background_music.set_volume(self.music_volume) 
        if self.button_click:
            self.button_click.set_volume(self.sfx_volume)

    def play_background_music(self):
        """Play the background music on loop."""
        if self.background_music:
            self.background_music.play(-1)

    def stop_background_music(self):
        """Stop the background music."""
        if self.background_music:
            self.background_music.stop()

    def set_music_volume(self, volume):
        """Set the music volume (0.0 to 1.0)."""
        self.music_volume = volume / 100
        if self.background_music:
            self.background_music.set_volume(self.music_volume)

    def set_sfx_volume(self, volume):
        """Set the sound effects volume (0.0 to 1.0)."""
        self.sfx_volume = volume / 100
        if self.button_click:
            self.button_click.set_volume(self.sfx_volume)

    def play_button_click(self):
        """Play the button click sound effect."""
        if self.button_click:
            self.button_click.play()