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
        self.building_data = save_data["building_data"]
        self.car_data = None
        self.signalisation_data = None
        self.font = pygame.font.Font("freesansbold.ttf", 32)
        
        self.game_data = {
            0: self.building_data,
            1: self.signalisation_data
        }
        
    
    def check_correct_path(self):
        print("Chemin Valide")
        return os.path.exists(self.path)

    def update_save(self):
        """
        Met à jour la sauvegarde en cours.

        Crée un dictionnaire `save_data` contenant les données de la partie, puis vérifie si le chemin de sauvegarde est valide.
        Si le chemin est valide, la méthode stocke les données de la partie dans un fichier .clab à l'emplacement spécifié.
        Si le chemin est invalide, un message d'erreur est affiché et la méthode renvoie False.
        Sinon, la méthode renvoie True.

        :return: True si la sauvegarde a réussi, False sinon.
        :rtype: bool
        """
        
        save_data = {
            "name": self.name,
            "cols": self.columns,
            "rows": self.rows,
            "tile_size": self.TILE_SIZE,
            "scroll_x": self.scrollx,
            "scroll_y": self.scrolly,
            "path": self.path,
            "building_data": self.building_data,
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

        for y, row in enumerate(self.building_data):
                for x, tile in enumerate(row):
                    if tile.tile_type != "@empty":
                        tile.rect = pygame.Rect(x * self.TILE_SIZE - self.scrollx, y * self.TILE_SIZE - self.scrolly, self.TILE_SIZE, self.TILE_SIZE)
                        tile.draw(surface)
                        print(f"{tile.tile_type}({tile.orientation}) X:{tile.rect.x // self.TILE_SIZE} Y:{tile.rect.y // self.TILE_SIZE}")

    def change_scroll(self, surface):
        """
        Adjusts the scroll position based on the current scroll direction and speed.

        This method updates the horizontal and vertical scroll positions (`scrollx` and `scrolly`)
        of the game display. The scrolling is controlled by the `horizontal_scroll` and `vertical_scroll`
        attributes, which determine the direction of scrolling. The scroll speed is determined by the
        `scroll_speed` attribute.

        The method ensures that scrolling does not exceed the boundaries of the game area defined 
        by the total number of columns and rows times the tile size (`TILE_SIZE`), minus the dimensions
        of the visible surface.

        :param surface: The surface to which the scrolling constraints are applied.
        :type surface: pygame.Surface
        """

        if self.horizontal_scroll == 1 and self.scrollx < (self.columns * self.TILE_SIZE) - surface.get_width():
            self.scrollx += 5 * self.scroll_speed
        elif self.horizontal_scroll == -1 and self.scrollx > 0:
            self.scrollx -= 5 * self.scroll_speed
        
        if self.vertical_scroll == 1 and self.scrolly < (self.rows * self.TILE_SIZE) - surface.get_height():
            self.scrolly += 5 * self.scroll_speed
        elif self.vertical_scroll == -1 and self.scrolly > 0: 
            self.scrolly -= 5 * self.scroll_speed
    
    def draw_grid(self, surface):
        """
        Dessine un quadrillage sur la surface.
        
        Cette methode dessine un quadrillage sur la surface en fonction de la
        taille des tuiles (`TILE_SIZE`) et de la position actuelle du scroll.
        """
        for c in range(self.columns + 1):
            pygame.draw.line(surface, "#FFFFFF", (c * self.TILE_SIZE - self.scrollx, 0), (c * self.TILE_SIZE - self.scrollx, surface.get_height()))
        for c in range(self.rows + 1):
            pygame.draw.line(surface, "#FFFFFF", (0, c * self.TILE_SIZE - self.scrolly), (surface.get_width(), c * self.TILE_SIZE - self.scrolly))
    
    def zoom(self, modificateur):
        """
        Modifie la taille des tuiles de la partie.

        Cette methode modifie la taille des tuiles (`TILE_SIZE`) de la partie en fonction du modificateur fourni.
        Ensuite, elle met à jour la taille de chaque tuile non vide en appelant la methode `change_size` de la classe `Tuile`.
        """
        self.TILE_SIZE += modificateur
        
        for y, row in enumerate(self.building_data):
                for x, tile in enumerate(row):
                    if tile.tile_type != "@empty":
                        tile.change_size(self.TILE_SIZE)
    