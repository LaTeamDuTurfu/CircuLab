import json
import os

class ConfigsManager:

    default_config = {
        "music_volume": 0.5,
        "sfx_volume": 0.5,
        "save_on_exit": True
    }

    def __init__(self, config_file_path: str="data/config/config.json"):
        self.config_file_path = config_file_path
        self.config = {}
        self.load_config()

    def load_config(self):
        if os.path.exists(self.config_file_path):
            with open(self.config_file_path, "r") as file:
                self.config = json.load(file)
        else:
            self.config = self.default_config.copy()
            self.save_config()
    
    def save_config(self):
        with open(self.config_file_path, "w") as file:
            json.dump(self.config, file, indent=4)