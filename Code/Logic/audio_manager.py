import pygame
import pygame.mixer
import pygame_gui

class AudioManager:
    def __init__(self, config_manager):
        pygame.mixer.init()
        self.music_volume = 0
        self.sfx_volume = 0
        self.config_manager = config_manager

        self.music_channel = pygame.mixer.Channel(0)
        self.sfx_channel = pygame.mixer.Channel(1)

        # Dictionnaire accessible par le nom de l'effet sonore
        self.sound_effects = {
            "tile_placed": pygame.mixer.Sound("assets/audio/sfx/tile_placed.mp3"),
            "button_click": pygame.mixer.Sound("assets/audio/sfx/button_click.mp3"),
        }

        self.load_config()


    def load_config(self):
        self.music_volume = self.config_manager.config["music_volume"]
        self.sfx_volume = self.config_manager.config["sfx_volume"]

        self.apply_config()
    
    def apply_config(self):
        self.music_channel.set_volume(self.music_volume)
        self.sfx_channel.set_volume(self.sfx_volume)

        print(f"Music volume set to {self.music_volume}")
        print(f"SFX volume set to {self.sfx_volume}")
    
    def play_sfx(self, sound_name:str):
        if sound_name in self.sound_effects:
            self.sound_effects[sound_name].set_volume(self.sfx_volume)
            self.sfx_channel.play(self.sound_effects[sound_name])
        else:
            print(f"Sound effect '{sound_name}' not found.")
    