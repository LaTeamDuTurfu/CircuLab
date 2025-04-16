import os
import pygame_gui
import pickle

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
                self.loaded_game = pickle.load(save_file)
        else:
            pass
    
    def check_save_created(self):
        if self.loaded_game != None:
            self.file_explorer_window.hide()
            return True
        return False