import pygame
import pygame_gui
import os
import sys

# Permet de charger les modules dans le dossier game_code
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(project_root, "Code"))

from Logic import Partie
from Tiles.tuile import Tuile

class NewSaveWindow(pygame_gui.elements.UIWindow):

    MIN_COLS = 50
    MAX_COLS = 300
    MIN_ROWS = 50
    MAX_ROWS = 300
    TILE_SIZE = 64

    def __init__(self, rect, manager, default_path, state_manager, home_screen):
        # Load tiles images
        """
        Crée une nouvelle fenêtre de sauvegarde.
        Elle permet de définir les paramètres de la sauvegarde (nom, chemin, nombre de colonnes et de lignes) et de l'enregistrer.
        Si la sauvegarde est créée avec succès, la fenêtre se ferme et la méthode `save_new` est appelée avec en paramètre la partie créée.
        Sinon, un message d'erreur est affiché en dessous du champ de texte du chemin.

        :param rect: La taille et la position de la fenêtre.
        :type rect: pygame.Rect
        :param manager: Le gestionnaire d'événements.
        :type manager: pygame_gui.UIManager
        :param default_path: Le chemin par défaut où la sauvegarde sera enregistrée.
        :type default_path: str
        """
        self.empty_tile = pygame.image.load("assets/tile_images/none.png")
        
        # UI Elements
        super().__init__(rect, manager, window_display_title="Créer une nouvelle sauvegarde", object_id="#new_save_window", resizable=False, draggable=False)
        self.rect = rect
        self.manager = manager
        self.state_manager = state_manager
        self.home_screen = home_screen
        self.path = default_path
        self.is_blocking = True
        self.window_container = pygame_gui.elements.UIAutoResizingContainer(relative_rect=pygame.Rect((0, 0), (rect.width, rect.height)), manager=manager, container=self, object_id="#new_save_window_container")
        self.created_game = None

        self.name_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, 0), (self.window_container.get_relative_rect().width, 50)),
            text="Nom de la sauvegarde",
            manager=manager,
            container=self.window_container,
            object_id=pygame_gui.core.ObjectID(class_id="@new_save_window_label", object_id="#name_label"))
        
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
            object_id=pygame_gui.core.ObjectID(class_id="@new_save_window_label", object_id="#cols_label"))

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
            object_id=pygame_gui.core.ObjectID(class_id="@new_save_window_label", object_id="#rows_label"))

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
            object_id=pygame_gui.core.ObjectID(class_id="@new_save_window_label", object_id="#name_label"))

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
            text="",
            manager=manager,
            container=self.window_container,
            object_id=pygame_gui.core.ObjectID(class_id="@new_save_window_label", object_id="#error_label"),
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
            anchors={"centerx": "centerx"},
            command=self.return_to_home_screen
        )

        self.file_explorer_btn.bind(pygame_gui.UI_BUTTON_PRESSED, self.open_file_explorer)

    def open_file_explorer(self):
        """
        Ouvre une fenêtre de sélection de chemin pour que l'utilisateur puisse
        choisir le chemin de sauvegarde de la partie.

        Lorsque le bouton OK est pressé, la méthode set_new_path est appelée.
        """
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
        """
        Called when the user has selected a directory path in the file explorer window.
        Sets the text of the path_text_box to the selected path, and kills the file explorer window.
        """
        self.path = str(self.file_explorer_window.current_directory_path)
        print(self.path)
        self.path_text_box.set_text(self.path)
        self.file_explorer_window.kill()

    def show_error_msg(self, message):
        """
        Affiche un message d'erreur en haut de la fenêtre de création de partie.
        
        :param message: Le message d'erreur à afficher.
        """
        self.error_label.set_text(message)
        self.error_label.visible = True

    def save_new(self):
        # Get save data
        """
        Creates a new save for the game based on user input data and validates it.

        Retrieves the number of columns and rows from text boxes, and verifies that 
        they are integers. Collects the save path and name from text boxes as well.
        Initializes empty data for building, car, and signalisation elements.

        Validates the input data to ensure all fields are filled and that the number 
        of columns and rows is within the allowed range. If validation fails, an 
        error message is displayed.

        Constructs a save data dictionary and attempts to create a new game save. If 
        the save path is correct, the game is saved and a success message is printed; 
        otherwise, an error message is shown.

        :raises ValueError: If the number of columns or rows is not an integer.
        """

        try:
            n_cols = int(self.cols_text_box.get_text())
            n_rows = int(self.rows_text_box.get_text())
        except ValueError:
            self.show_error_msg("Nombre de lignes ou de colonnes invalide")
            return
        path = self.path_text_box.get_text()
        name = self.name_text_box.get_text()
        
        # Clear all fields
        self.cols_text_box.set_text("")
        self.rows_text_box.set_text("")
        self.path_text_box.set_text("")
        self.name_text_box.set_text("")

        # Check save data
        if n_cols == "" or n_rows == "" or path == "" or name == "":
            self.show_error_msg("Veuillez remplir tous les champs")
            return

        if not (self.MIN_COLS < int(n_cols) < self.MAX_COLS and self.MIN_ROWS < int(n_rows) < self.MAX_ROWS):
            self.show_error_msg(f"Les colonnes et rangées doivent être entre {self.MIN_COLS} et {self.MAX_COLS}")
            return

        # Create empty data files
        building_data = self.fill_empty_tile(n_rows, n_cols)
        car_data = None
        signalisation_data = self.fill_empty_tile(n_rows, n_cols)
        
        save_data = {
            "name": name,
            "cols": n_cols,
            "rows": n_rows,
            "tile_size": self.TILE_SIZE,
            "scroll_x": 0,
            "scroll_y": 0,
            "path": path,
            "building_data": building_data,
            "car_data": car_data,
            "signalisation_data": signalisation_data
        }

        new_save = Partie(save_data)
        self.created_game = new_save
        print("Sauvegarde créée")
    
    def fill_empty_tile(self, n_rows, n_cols, data_set=None):
        """
        Fill a 2D array with empty tiles

        Parameters
        ----------
        n_rows : int
            Number of rows to fill
        n_cols : int
            Number of columns to fill
        data_set : list, optional
            List to which the filled 2D array will be appended. If not provided, a new list is created.

        Returns
        -------
        data_set : list
            A 2D array with n_rows and n_cols of empty tiles
        """
        if data_set == None:
            data_set = []
        for _ in range(n_rows):
            new_tile = [Tuile(self.TILE_SIZE, self.empty_tile, tile_type="@empty")] * n_cols
            data_set.append(new_tile)
        return data_set

    def check_save_created(self):
        """
        Checks if a game instance has been successfully created and saved.
        
        If a game instance exists, the current window is closed and the method 
        returns True, indicating that the save was successful. Otherwise, it 
        returns False.
        
        Returns
        -------
        bool
            True if the game was created and saved successfully, False otherwise.
        """
        if self.created_game != None:
            self.hide()
            return True
        return False
    
    def return_to_home_screen(self):
        self.state_manager.changer_état(1)
        self.hide()
        self.home_screen.montrer_boutons()
    
    def change_pos(self, x, y):
        x = x - self.rect.width / 2
        y = y - self.rect.height / 2
        self.set_position((x, y))

