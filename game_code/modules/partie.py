import pickle
import os, sys
import pygame

# Permet de charger les modules dans le dossier game_code
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(project_root, "game_code"))

from modules.tuile import Tuile

class Partie():
    
    empty_tile = pygame.image.load("assets/tile_images/none.png")
    vertical_scroll = 0
    horizontal_scroll = 0
    scroll_speed = 1
    
    def __init__(self, save_data: dict):
        self.name = save_data["name"]
        self.columns = save_data["cols"]
        self.rows = save_data["rows"]
        self.scrollx = save_data["scroll_x"]
        self.scrolly = save_data["scroll_y"]
        self.path = save_data["path"]
        self.TILE_SIZE = save_data["tile_size"]
        self.road_data = save_data["road_data"]
        self.car_data = None
        self.signalisation_data = None
        
    
    def check_correct_path(self):
        print("Chemin Valide")
        return os.path.exists(self.path)

    def update_save(self):
        save_data = {
            "name": self.name,
            "cols": self.columns,
            "rows": self.rows,
            "tile_size": self.TILE_SIZE,
            "scroll_x": self.scrollx,
            "scroll_y": self.scrolly,
            "path": self.path,
            "road_data": self.road_data,
            "car_data": self.car_data,
            "signalisation_data": self.signalisation_data
        }

        if self.check_correct_path():
            with open(self.path + f"/{self.name}.clab", "wb") as file:
                pickle.dump(str(save_data), file)
                return True
        
        print("Le chemin de sauvegarde n'est pas correct")
        return False
    
    def draw_tuiles(self, surface):
        """
        Dessine les tuiles sur l'écran, en fonction de la
        position actuelle du scroll.
        """

        for y, row in enumerate(self.road_data):
                for x, tile in enumerate(row):
                    if tile.tile_type != "@empty":
                        tile.rect = pygame.Rect(x * self.TILE_SIZE - self.scrollx, y * self.TILE_SIZE - self.scrolly, self.TILE_SIZE, self.TILE_SIZE)
                        tile.draw(surface)

    def change_scroll(self, surface):
        if self.horizontal_scroll == 1 and self.scrollx < (self.columns * self.TILE_SIZE) - surface.get_width():
            self.scrollx += 5 * self.scroll_speed
        elif self.horizontal_scroll == -1 and self.scrollx > 0:
            self.scrollx -= 5 * self.scroll_speed
        
        if self.vertical_scroll == 1 and self.scrolly < (self.rows * self.TILE_SIZE) - surface.get_height():
            self.scrolly += 5 * self.scroll_speed
        elif self.vertical_scroll == -1 and self.scrolly > 0: 
            self.scrolly -= 5 * self.scroll_speed
    
    def draw_grid(self, surface):
        for c in range(self.columns + 1):
            pygame.draw.line(surface, "#FFFFFF", (c * self.TILE_SIZE - self.scrollx, 0), (c * self.TILE_SIZE - self.scrollx, surface.get_height()))
        for c in range(self.rows + 1):
            pygame.draw.line(surface, "#FFFFFF", (0, c * self.TILE_SIZE - self.scrolly), (surface.get_width(), c * self.TILE_SIZE - self.scrolly))
    
    def zoom(self, multiplicateur):
        self.TILE_SIZE *= multiplicateur
        
        for _, row in enumerate(self.road_data):
                for _, tile in enumerate(row):
                    if tile.tile_type != "@empty":
                        tile.change_size(multiplicateur)
    