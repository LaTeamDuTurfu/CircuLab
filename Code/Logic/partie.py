"""
Module Partie
Représente une instance de partie dans CircuLab, avec la gestion des tuiles, du défilement, du zoom,
des modifications sur la grille, et la sauvegarde/chargement des données du jeu.
"""

import dill
import os, sys
import pygame
import copy
from Code.Logic.états import ÉtatJeu

# Permet de charger les modules dans le dossier game_code
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(project_root, "Code"))

from Tiles.tuile import Tuile

# Classe Partie — gère l'état courant d'une partie, les interactions avec la grille, et la persistance des données.
class Partie():
    
    empty_tile = pygame.image.load("assets/tile_images/none.png")
    vertical_scroll = 0
    horizontal_scroll = 0
    scroll_speed = 1
    DEFAULT_TILE_SIZE = 64
    
    def __init__(self, save_data: dict):
        """
        Initialise une nouvelle instance de Partie à partir d'un dictionnaire de sauvegarde.

        Args:
            save_data (dict): Données sérialisées provenant d'une sauvegarde de partie.
        """
        self.last_tuile_checked = None
        self.name = save_data["name"]
        self.columns = save_data["cols"]
        self.rows = save_data["rows"]
        self.scrollx = save_data["scroll_x"]
        self.scrolly = save_data["scroll_y"]
        self.path = save_data["path"]
        self.TILE_SIZE = save_data["tile_size"]
        self.building_data = save_data["building_data"]
        self.signalisation_data = save_data["signalisation_data"]
        self.intersections = save_data["intersections"]
        self.inter_points = save_data["inter_points"]
        self.ordered_points = save_data["ordered_points"]
        
        self.font = pygame.font.Font("freesansbold.ttf", 32)
        
        self.game_data = {
            2: self.building_data,
            7: self.signalisation_data
        }
        
    
    def check_correct_path(self):
        # Vérifie si le chemin de sauvegarde est valide
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
        copy_building_data = copy.deepcopy(self.building_data)
        serialized_building_data = self.tiles_data_to_bytes(copy_building_data)
        print(f"[1/3] {self.name}.clab : Données de construction sérialisées")
        
        copy_signalisation_data = copy.deepcopy(self.signalisation_data)
        serialized_signalisation_data = self.tiles_data_to_bytes(copy_signalisation_data)
        print(f"[2/3] {self.name}.clab : Données de signalisation sérialisées")

        save_data = {
            "name": self.name,
            "cols": self.columns,
            "rows": self.rows,
            "tile_size": self.TILE_SIZE,
            "scroll_x": self.scrollx,
            "scroll_y": self.scrolly,
            "path": self.path,
            "building_data": serialized_building_data,
            "signalisation_data": serialized_signalisation_data,
            "intersections": self.intersections,
            "inter_points": self.inter_points,
            "ordered_points": self.ordered_points
        }

        print(f"[3/3] {self.name}.clab : Enregistrement des données...")
        if self.check_correct_path():
            with open(self.path + f"/{self.name}.clab", "wb") as file:
                dill.dump(save_data, file)
                print(f"[Succès]: {self.name}.clab a été sauvegardé ✅")
                return True
        
        print("[Erreur]: Le chemin de sauvegarde est incorrect ❌")
        return False
    
    # Dessine les tuiles de construction et de signalisation visibles à l'écran.
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
                        # print(f"{tile.tile_type}({tile.orientation}) X:{tile.rect.x // self.TILE_SIZE} Y:{tile.rect.y // self.TILE_SIZE}")
        
        for y, row in enumerate(self.signalisation_data):
                for x, tile in enumerate(row):
                    if tile.tile_type != "@empty":
                        tile.rect = pygame.Rect(x * self.TILE_SIZE - self.scrollx, y * self.TILE_SIZE - self.scrolly, self.TILE_SIZE, self.TILE_SIZE)
                        tile.draw(surface)
                        # print(f"{tile.tile_type}({tile.orientation}) X:{tile.rect.x // self.TILE_SIZE} Y:{tile.rect.y // self.TILE_SIZE}")

    def change_scroll(self, surface):
        # Met à jour les positions de défilement horizontal et vertical selon la direction et la vitesse
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
        # Trace les lignes du quadrillage sur la surface de jeu
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
        # Change la taille des tuiles et ajuste leur rendu
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
                        print("New Tile Size:", self.TILE_SIZE)
    
    def change_tuiles(self, screen, toolbar, pos, window_border, state_manager, road_orientation_manager, build_orientation, graphe):
        # Gère le placement ou la suppression de tuiles via les clics souris selon l'état actif
        """
        Updates the tile at the current mouse position to the selected tile
        image from the toolbar, but only if the left mouse button is pressed
        and the current tile at the mouse position is not the same as the
        selected tile. If the right mouse button is pressed, the tile is reset
        to an empty tile.

        This function is used in the game loop to update the tiles on the grid
        based on the user's input. It is called every frame when the game is in
        the game editor state.
        """
        if window_border.thickness < pos[0] < (screen.get_width() - window_border.thickness) and toolbar.TOOL_BAR_HEIGHT < pos[1] < (screen.get_height() - window_border.bottom_thickness):
            x_pos = int((pos[0] + self.scrollx) // self.TILE_SIZE)
            y_pos = int((pos[1] + self.scrolly) // self.TILE_SIZE)
            try:
                bouton_actif = toolbar.get_selected_btn()
                id_bouton_actif = bouton_actif.object_ids[-1][-1]
            except AttributeError:
                pass
            if pygame.mouse.get_pressed()[0] == 1:
                try:
                    if (state_manager.état_courant == 2 and self.building_data[y_pos][x_pos].tile_type != Tuile.BUILD_TILE_TYPES[int(id_bouton_actif)]) or (state_manager.état_courant == 7 and self.signalisation_data[y_pos][x_pos].tile_type != Tuile.SIGNALISATION_TILE_TYPES[int(id_bouton_actif)]):
                        print(state_manager.état_courant)
                        if state_manager.état_courant == 2:
                            
                            new_tile = Tuile(self.TILE_SIZE, toolbar.building_tile_images[int(id_bouton_actif[-1])], orientation=build_orientation, tile_type=Tuile.BUILD_TILE_TYPES[int(id_bouton_actif)])
                            print("Placé dans building")
                            self.building_data[y_pos][x_pos] = new_tile
                            
                            road_orientation_manager.set_game_data(self.building_data)
                            road_orientation_manager.check_tile_change(x_pos, y_pos)

                            return True, "placed"

                        elif state_manager.état_courant == 7:
                            new_tile = Tuile(self.TILE_SIZE, toolbar.signalisation_tile_images[int(id_bouton_actif[-1])], orientation=build_orientation, tile_type=Tuile.SIGNALISATION_TILE_TYPES[int(id_bouton_actif)])
                            print("Placé dans signalisation")
                            print(len(self.signalisation_data))
                            self.signalisation_data[y_pos][x_pos] = new_tile

                            if new_tile.tile_type == Tuile.SIGNALISATION_TILE_TYPES[1]:
                                graphe.add_signalisation((x_pos, y_pos), has_light=True)
                            elif new_tile.tile_type == Tuile.SIGNALISATION_TILE_TYPES[2]:
                                graphe.add_signalisation((x_pos, y_pos), is_stop=True)
                            
                            return True, "placed"

                except UnboundLocalError:
                    pass
            if pygame.mouse.get_pressed()[2] == 1:
                if state_manager.état_courant == 2:
                    self.building_data[y_pos][x_pos] = Tuile(self.TILE_SIZE, Tuile.empty_tile, orientation=build_orientation)
                    road_orientation_manager.set_game_data(self.building_data)
                    road_orientation_manager.check_tile_change(x_pos - 1, y_pos)
                    road_orientation_manager.check_tile_change(x_pos + 1, y_pos)
                    road_orientation_manager.check_tile_change(x_pos, y_pos - 1)
                    road_orientation_manager.check_tile_change(x_pos, y_pos + 1)
                    graphe.remove_inter_point((x_pos, y_pos))
                elif state_manager.état_courant == 7:
                    self.signalisation_data[y_pos][x_pos] = Tuile(self.TILE_SIZE, Tuile.empty_tile, orientation=build_orientation)

                return True, "removed"
            return None
        return None

    # Ajoute ou retire dynamiquement les points d’intersection dans le graphe selon la route ciblée
    def modifier_points_graphe(self, pos, road_orientation_manager, graphe, state_manager):
        if pygame.mouse.get_pressed()[0] == 1 and state_manager.état_courant == 2:
            x_pos = int((pos[0] + self.scrollx) // self.TILE_SIZE)
            y_pos = int((pos[1] + self.scrolly) // self.TILE_SIZE)

            if self.last_tuile_checked != self.building_data[y_pos][x_pos]:
                if road_orientation_manager.is_a_road(self.building_data[y_pos][x_pos]):
                    graphe.add_inter_points((x_pos, y_pos))
                else:
                    graphe.remove_inter_point((x_pos, y_pos))

                self.last_tuile_checked = self.building_data[y_pos][x_pos]

    # Met à jour toutes les connexions routières de la grille selon leur orientation
    def update_all_roads(self, road_orientation_manager):
        for y, row in enumerate(self.building_data):
                for x, tile in enumerate(row):
                    if road_orientation_manager.is_a_road(tile):
                        road_orientation_manager.check_tile_change(x, y)

    # Convertit les images des tuiles en données binaires pour la sérialisation
    def tiles_data_to_bytes(self, tiles_data):
        for ligne in tiles_data:
            for t in ligne:
                if isinstance(t.image, bytes):
                    pass
                else:
                    # Sinon, on convertit les données de pixels en bytes
                    pixels = pygame.image.tobytes(t.image, "RGBA")
                    t.image = pixels
        
        return tiles_data

    # Reconvertit les données binaires des tuiles en objets Tuile avec image
    def bytes_to_tiles_data(self, serialized_data):
        tiles_data = []
        for ligne in serialized_data:
            tuiles_ligne = []
            for tuile in ligne:
                # On convertit les bytes en image
                image = pygame.image.frombytes(tuile.image, (self.DEFAULT_TILE_SIZE, self.DEFAULT_TILE_SIZE), "RGBA")
                tuiles_ligne.append(Tuile(self.DEFAULT_TILE_SIZE, image, tuile.orientation, tuile.tile_type))
            tiles_data.append(tuiles_ligne)
        return tiles_data