"""
Module Tuile
Définition de la classe Tuile représentant les éléments de la grille dans CircuLab.
Contient les types de tuiles, leur orientation, leur rendu visuel et leur position logique.
"""

import pygame

# Classe représentant une tuile dans la grille de jeu (route, maison, signalisation, etc.)
class Tuile(pygame.sprite.Sprite):
    
    # Dictionnaires statiques définissant les types de tuiles et leurs orientations selon le contexte du jeu
    empty_tile = pygame.image.load("assets/tile_images/none.png")
    
    BUILD_TILE_TYPES = {
        1: "Road",
        2: "Grass",
        3: "Sidewalk",
        4: "Intersection",
        5: "House1",
        6: "House2",
        7: "House3",
        8: "House4"
    }
    
    SIGNALISATION_TILE_TYPES = {
        1: "Traffic Light",
        2: "Stop Sign",
        3: "",
        4: "",
        5: "",
        6: "",
        7: "",
        8: ""
    }
    
    TILE_TYPES = {
        0: BUILD_TILE_TYPES,
        1: SIGNALISATION_TILE_TYPES
    }
    
    BUILD_ORIENTATIONS = {
        0: "UP",
        1: "LEFT",
        2: "DOWN",
        3: "RIGHT"
    }
    
    def __init__(self, size: int, image:pygame.Surface, orientation:int = 0, tile_type: str=None,sprite_group=None):
        """
        Constructeur de la classe Tuile.

        Parameters
        ----------
        size : int
            Taille de la tuile.
        image : pygame.Surface
            Image de la tuile.
        orientation : int
            Orientation de la tuile (0: UP, 1: LEFT, 2: DOWN ou 3: RIGHT).
        tile_type : str, optional
            Type de la tuile. Par défaut, None.
        sprite_group : pygame.sprite.Group, optional
            Groupe de sprites auquel la tuile sera ajout e.
        """
        super().__init__()
        self.image = image
        self.tile_type = tile_type
        self.orientation = orientation
        self.image = pygame.transform.scale(image, (size, size))
        self.rect = image.get_rect()
    
    def rotate_clockwise(self):
        # Tourne l’image de la tuile de 90° dans le sens horaire
        self.image = pygame.transform.rotate(self.image, 90)

    def draw(self, surface):
        # Affiche l’image de la tuile sur la surface donnée, selon son orientation
        image_a_draw = self.image.copy()
        image_a_draw = pygame.transform.scale(image_a_draw, (self.rect.width, self.rect.height))
        image_a_draw = pygame.transform.rotate(self.image, self.orientation * 90)
        surface.blit(image_a_draw, self.rect)
    
    def change_size(self, new_size):
        # Redimensionne la tuile à la nouvelle taille spécifiée
        self.rect.width = new_size
        self.rect.height = new_size
    
    def get_x_tile(self, tile_size):
        # Retourne la position X (ou Y) de la tuile dans la grille en unités de tuiles
        return self.rect.x // tile_size

    def get_y_tile(self, tile_size):
        # Retourne la position X (ou Y) de la tuile dans la grille en unités de tuiles
        return self.rect.y // tile_size

    def __repr__(self):
        # Représentation textuelle utile pour le débogage : type et orientation
        return f"{self.tile_type} ({self.BUILD_ORIENTATIONS[self.orientation]})"