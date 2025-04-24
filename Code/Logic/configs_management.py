import json
import os

class ConfigsManager:
    def __init__(self, config_file_path: str="data/config/config.json"):
        self.config_file_path = config_file_path
        self.config = {}
        self.load_config()

    def load_config(self):
        if os.path.exists(self.config_file_path):
            with open(self.config_file_path, "r") as file:
                self.config = json.load(file)
    
    def save_config(self):
        with open(self.config_file_path, "w") as file:
            json.dump(self.config, file, indent=4)