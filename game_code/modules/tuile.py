import pygame

class Tuile(pygame.sprite.Sprite):
    def __init__(self, size: int, image:pygame.Surface, orientation:int, tile_type: str=None,sprite_group=None):
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
            Type de la tuile. Par d faut, None.
        sprite_group : pygame.sprite.Group, optional
            Groupe de sprites auquel la tuile sera ajout e.
        """
        super().__init__()
        self.image = image
        self.tile_type = tile_type
        self.orientation = orientation
        self.image = pygame.transform.scale(image, (size, size))
        self.image = pygame.transform.rotate(self.image, self.orientation * 90)
        self.rect = image.get_rect()
    
    def rotate_clockwise(self):
        self.image = pygame.transform.rotate(self.image, 90)

    def update(self):
        pass