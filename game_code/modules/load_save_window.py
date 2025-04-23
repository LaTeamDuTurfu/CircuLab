import os, sys
import pygame_gui
import dill

# Permet de charger les modules dans le dossier game_code
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(project_root, "game_code"))

from modules.partie import Partie

class LoadSaveWindow:
    def __init__(self, rect, surface, manager, default_path, home_screen, state_manager):
        self.WIDTH = surface.get_width()
        self.HEIGHT = surface.get_height()
        self.manager = manager
        self.rect = rect
        self.path = default_path
        self.home_screen = home_screen
        self.state_manager = state_manager
        
        self.file_explorer_window = pygame_gui.windows.UIFileDialog(
            rect=self.rect,
            manager=self.manager,
            visible=True,
            window_title="Sélection de sauvegarde",
            initial_file_path=self.path,
            allow_picking_directories=False,
            allow_existing_files_only=True,
            always_on_top=True,
            object_id="#load_save_window",
            allowed_suffixes={".clab"}
        )
        
        self.file_explorer_window.draggable = False
        self.file_explorer_window.cancel_button.bind(pygame_gui.UI_BUTTON_PRESSED, self.return_to_home_screen)
        self.file_explorer_window.ok_button.bind(pygame_gui.UI_BUTTON_PRESSED, self.read_save_file)
        
        self.file_explorer_window.current_file_path
        
        self.loaded_game = None
        
        self.file_explorer_window.hide()
    
    def return_to_home_screen(self):
        self.state_manager.changer_état(1)
        self.file_explorer_window.hide()
        self.home_screen.montrer_boutons()
    
    def read_save_file(self):
        current_file_path = self.file_explorer_window.current_file_path
        
        if os.path.isfile(current_file_path):
            with open(current_file_path, "rb") as save_file:
                save = dill.load(save_file)
        else:
            pass

        save_data = {
            "name": save["name"],
            "cols": save["cols"],
            "rows": save["rows"],
            "tile_size": save["tile_size"],
            "scroll_x": save["scroll_x"],
            "scroll_y": save["scroll_y"],
            "path": save["path"],
            "building_data": save["building_data"],
            "car_data": save["car_data"],
            "signalisation_data": save["signalisation_data"]
        }

        game = Partie(save_data)
        game.building_data = game.bytes_to_tiles_data(game.building_data)
        game.signalisation_data = game.bytes_to_tiles_data(game.signalisation_data)

        self.loaded_game = game
        print("Sauvegarde chargée avec succès")

    
    def check_save_created(self):
        if self.loaded_game != None:
            self.file_explorer_window.hide()
            return True
        return False