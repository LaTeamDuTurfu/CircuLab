"""
Module de gestion de la configuration utilisateur pour CircuLab.
Permet de charger, sauvegarder et réinitialiser les paramètres de volume et de comportement au démarrage.
"""

import json
import os

# Classe pour la gestion des configurations utilisateur (volumes, options, etc.)
class ConfigsManager:

    # Valeurs par défaut utilisées si le fichier de configuration n'existe pas
    default_config = {
        "music_volume": 0.5,
        "sfx_volume": 0.5,
        "save_on_exit": True
    }

    def __init__(self, config_file_path: str="data/config/config.json"):
        """
        Initialise le gestionnaire avec le chemin du fichier de configuration.

        Args:
            config_file_path (str): Chemin vers le fichier de configuration JSON.
        """
        self.config_file_path = config_file_path
        self.config = {}
        self.load_config()

    def load_config(self):
        """
        Charge la configuration à partir du fichier JSON.
        Si le fichier n'existe pas, initialise avec les valeurs par défaut et sauvegarde.
        """
        if os.path.exists(self.config_file_path):
            with open(self.config_file_path, "r") as file:
                self.config = json.load(file)
        else:
            self.config = self.default_config.copy()
            self.save_config()
    
    def save_config(self):
        """
        Sauvegarde la configuration actuelle dans le fichier JSON.
        """
        with open(self.config_file_path, "w") as file:
            json.dump(self.config, file, indent=4)