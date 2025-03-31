import sys
import os

# Permet de charger les modules dans le dossier game_code
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(project_root, "game_code"))

class Graphe:
    def __init__(self, current_save):
        self.current_save = current_save
        self.name = current_save["name"]
        self.building_data = current_save["building_data"]
        self.tile_size = current_save["tile_size"]
        self.scrollx = current_save["scrollx"]
        self.scrolly = current_save["scrolly"]
        
        """
        Building_data = [
            [Tuile, Tuile, Tuile],
            [Tuile, Tuile, Tuile],
            [Tuile, Tuile, Tuile]
        ]
        
        Tuile --> 
        self.image = image
        self.tile_type = tile_type --> @empty, @road
        self.orientation = orientation --> 0, 1, 2, 3
        self.rect = image.get_rect() --> width, height, x, y
        """