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

        self.music_playlist = [
            pygame.mixer.Sound("assets/audio/music/music1.mp3"),
            pygame.mixer.Sound("assets/audio/music/music2.mp3"),
            ]  # Liste des chemins de fichiers musicaux
        self.current_track_index = 0
        
        # Dictionnaire accessible par le nom de l'effet sonore
        self.sound_effects = {
            "tile_placed": pygame.mixer.Sound("assets/audio/sfx/tile_placed.mp3"),
            "tile_removed": pygame.mixer.Sound("assets/audio/sfx/tile_removed.mp3"),
            "button_click": pygame.mixer.Sound("assets/audio/sfx/button_click.mp3"),
        }

        self.load_config()
    
    def play_current_track(self):
        if self.music_playlist:
            track_path = self.music_playlist[self.current_track_index]
            try:
                self.music_channel.set_volume(self.music_volume)
                self.music_channel.play(track_path)
                print(f"Playing: {track_path}")
            except pygame.error as e:
                print(f"Error loading {track_path}: {e}")
        else:
            print("No music loaded in the playlist.")
    
    def play_next_track(self):
        if self.music_playlist:
            self.current_track_index = (self.current_track_index + 1) % len(self.music_playlist)
            self.play_current_track()
    
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
    