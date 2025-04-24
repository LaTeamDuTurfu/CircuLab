import pygame_gui
import json

class Settings:
    def __init__(self, manager, configs: dict):
        self.manager = manager
        self.configs = configs
    
    