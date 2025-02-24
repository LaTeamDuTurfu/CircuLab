import pygame
import pygame_gui
import os
import sys

# Permet de charger les modules dans le dossier game_code
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(project_root, "game_code"))

from modules.partie import Partie
from modules.tuile import Tuile

class NewSaveWindow(pygame_gui.elements.UIWindow):

    MIN_COLS = 1
    MAX_COLS = 500
    MIN_ROWS = 1
    MAX_ROWS = 500
    TILE_SIZE = 64

    def __init__(self, rect, manager, default_path):
        # Load tiles images
        self.empty_tile = pygame.image.load("assets/tile_images/none.png")
        
        # UI Elements
        super().__init__(rect, manager, window_display_title="New Save", object_id="#new_save_window", resizable=False, draggable=True)
        self.rect = rect
        self.manager = manager
        self.path = default_path
        self.is_blocking = True
        self.window_container = pygame_gui.elements.UIAutoResizingContainer(relative_rect=pygame.Rect((0, 0), (rect.width, rect.height)), manager=manager, container=self, object_id="#new_save_window_container")
        self.created_game = None

        self.name_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, 0), (self.window_container.get_relative_rect().width, 50)),
            text="Nom de la sauvegarde",
            manager=manager,
            container=self.window_container,
            object_id=pygame_gui.core.ObjectID(class_id="@new_save_window", object_id="#name_label"))
        
        self.name_text_box = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((0, self.name_label.get_relative_rect().height), (self.window_container.get_relative_rect().width * 27/32, 50)),
            manager=manager,
            container=self.window_container,
            object_id=pygame_gui.core.ObjectID(class_id="@new_save_window", object_id="#name_text_box"),
            anchors={"centerx": "centerx"},
        )

        self.name_text_box.forbidden_characters = ['<', '>', ':', '"', '/', '\\', '|', '?', '*', '\0', '.', " "]
        self.name_text_box.length_limit = 30

        self.cols_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, self.name_label.get_relative_rect().height + self.name_text_box.get_relative_rect().height), (self.window_container.get_relative_rect().width/2, 50)),
            text="Nombre de colonnes",
            manager=manager,
            container=self.window_container,
            object_id=pygame_gui.core.ObjectID(class_id="@new_save_window", object_id="#cols_label"))

        self.cols_text_box = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((-self.window_container.get_relative_rect().width/4, self.cols_label.get_relative_rect().y + self.cols_label.get_relative_rect().height), (self.window_container.get_relative_rect().width/3, 50)),
            manager=manager,
            container=self.window_container,
            object_id=pygame_gui.core.ObjectID(class_id="@new_save_window", object_id="#cols_text_box"),
            anchors={"centerx": "centerx"}
        )

        self.cols_text_box.allowed_characters = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        self.cols_text_box.length_limit = 4

        self.rows_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((self.window_container.get_relative_rect().width/2, self.name_label.get_relative_rect().height + self.name_text_box.get_relative_rect().height), (self.window_container.get_relative_rect().width/2, 50)),
            text="Nombre de lignes",
            manager=manager,
            container=self.window_container,
            object_id=pygame_gui.core.ObjectID(class_id="@new_save_window", object_id="#rows_label"))

        self.rows_text_box = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((self.window_container.get_relative_rect().width/4, self.rows_label.get_relative_rect().y + self.rows_label.get_relative_rect().height), (self.window_container.get_relative_rect().width/3, 50)),
            manager=manager,
            container=self.window_container,
            object_id=pygame_gui.core.ObjectID(class_id="@new_save_window", object_id="#rows_text_box"),
            anchors={"centerx": "centerx"},
        )

        self.rows_text_box.allowed_characters = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        self.rows_text_box.length_limit = 4

        self.path_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, self.rows_text_box.get_relative_rect().y + self.rows_text_box.get_relative_rect().height), (self.window_container.get_relative_rect().width, 50)),
            text="Chemin de la sauvegarde",
            manager=manager,
            container=self.window_container,
            object_id=pygame_gui.core.ObjectID(class_id="@new_save_window", object_id="#name_label"))

        self.path_text_box = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((-self.window_container.get_relative_rect().width/16, self.path_label.get_relative_rect().height + self.path_label.get_relative_rect().y), (self.window_container.get_relative_rect().width * 23/32, 50)),
            manager=manager,
            container=self.window_container,
            object_id=pygame_gui.core.ObjectID(class_id="@new_save_window", object_id="#name_text_box"),
            anchors={"centerx": "centerx"}
        )

        self.file_explorer_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.path_text_box.get_relative_rect().width + self.window_container.get_relative_rect().width/16 + 5, self.path_text_box.get_relative_rect().y), (self.window_container.get_relative_rect().width/8, 50)),
            text="...",
            manager=manager,
            container=self.window_container,
            object_id=pygame_gui.core.ObjectID(class_id="@new_save_window", object_id="#file_explorer_btn")
        )

        self.error_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, self.path_text_box.get_relative_rect().y + self.path_text_box.get_relative_rect().height), (self.window_container.get_relative_rect().width, 50)),
            text="Error Message",
            manager=manager,
            container=self.window_container,
            object_id=pygame_gui.core.ObjectID(class_id="@new_save_window", object_id="#error_label"),
            visible=False)

        self.save_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((-self.window_container.get_relative_rect().width/4, self.path_text_box.get_relative_rect().y + self.path_text_box.get_relative_rect().height * 2), (self.window_container.get_relative_rect().width/4, 50)),
            text="Créer",
            manager=manager,
            container=self.window_container,
            object_id=pygame_gui.core.ObjectID(class_id="@new_save_window", object_id="#save_btn"),
            anchors={"centerx": "centerx"}
        )
        self.save_btn.bind(pygame_gui.UI_BUTTON_PRESSED, self.save_new)

        self.cancel_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.window_container.get_relative_rect().width/4, self.path_text_box.get_relative_rect().y + self.path_text_box.get_relative_rect().height * 2), (self.window_container.get_relative_rect().width/4, 50)),
            text="Annuler",
            manager=manager,
            container=self.window_container,
            object_id=pygame_gui.core.ObjectID(class_id="@new_save_window", object_id="#cancel_btn"),
            anchors={"centerx": "centerx"}
        )

        self.file_explorer_btn.bind(pygame_gui.UI_BUTTON_PRESSED, self.open_file_explorer)

    def open_file_explorer(self):
        self.file_explorer_window = pygame_gui.windows.UIFileDialog(
            rect=self.rect,
            manager=self.manager,
            visible=True,
            window_title="Sélection de chemin de sauvegarde",
            initial_file_path=self.path,
            allow_picking_directories=True,
            always_on_top=True
        )

        self.file_explorer_window.ok_button.bind(pygame_gui.UI_BUTTON_PRESSED, self.set_new_path)

    def set_new_path(self):
        self.path = str(self.file_explorer_window.current_directory_path)
        print(self.path)
        self.path_text_box.set_text(self.path)
        self.file_explorer_window.kill()

    def show_error_msg(self, message):
        self.error_label.set_text(message)
        self.error_label.visible = True

    def save_new(self):
        # Get save data
        try:
            n_cols = int(self.cols_text_box.get_text())
            n_rows = int(self.rows_text_box.get_text())
        except ValueError:
            self.show_error_msg("Veuillez entrer un nombre entier pour le nombre de colonnes et de lignes")
            return
        path = self.path_text_box.get_text()
        name = self.name_text_box.get_text()

        # Create empty data files
        road_data = self.fill_empty_tile(n_rows, n_cols)
        car_data = self.fill_empty_tile(n_rows, n_cols)
        signalisation_data = self.fill_empty_tile(n_rows, n_cols)

        # Check save data
        if n_cols == "" or n_rows == "" or path == "" or name == "":
            self.show_error_msg("Veuillez remplir tous les champs")
            return

        if not (self.MIN_COLS < int(n_cols) < self.MAX_COLS and self.MIN_ROWS < int(n_rows) < self.MAX_ROWS):
            self.show_error_msg(f"Le nombre de colonnes doit être entre {self.MIN_COLS} et {self.MAX_COLS}, puis le nombre de lignes entre {self.MIN_ROWS} et {self.MAX_ROWS}")
            return

        save_data = {
            "name": name,
            "cols": n_cols,
            "rows": n_rows,
            "tile_size": self.TILE_SIZE,
            "scroll_x": 0,
            "scroll_y": 0,
            "path": path,
            "road_data": road_data,
            "car_data": car_data,
            "signalisation_data": signalisation_data
        }

        new_save = Partie(save_data)
        if new_save.update_save():
            self.created_game = new_save
            print("Partie sauvegardée")
        else:
            self.show_error_msg("Le chemin de sauvegarde n'est pas correct")
    
    def fill_empty_tile(self, n_rows, n_cols, data_set=[]):
        for _ in range(n_rows):
            new_tile = [Tuile(self.TILE_SIZE, self.empty_tile, tile_type="@empty")] * n_cols
            data_set.append(new_tile)
        return data_set

    def check_save_created(self):
        if self.created_game != None:
            self.kill()
            return True
        return False

