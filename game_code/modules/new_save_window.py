import pygame
import pygame_gui
import pickle
import os

class NewSaveWindow(pygame_gui.elements.UIWindow):
    def __init__(self, rect, manager, default_path):
        # UI Elements
        super().__init__(rect, manager, window_display_title="New Save", object_id="#new_save_window", resizable=False, draggable=True)
        self.default_path = default_path
        self.is_blocking = True
        self.window_container = pygame_gui.elements.UIAutoResizingContainer(relative_rect=pygame.Rect((0, 0), (rect.width, rect.height)), manager=manager, container=self, object_id="#new_save_window_container")

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
            anchors={"centerx": "centerx"},
            placeholder_text=self.default_path
        )

        self.file_explorer_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.path_text_box.get_relative_rect().width + self.window_container.get_relative_rect().width/16, self.path_text_box.get_relative_rect().y), (self.window_container.get_relative_rect().width/8, 50)),
            text="...",
            manager=manager,
            container=self.window_container,
            object_id=pygame_gui.core.ObjectID(class_id="@new_save_window", object_id="#file_explorer_btn")
        )

        self.save_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((-self.window_container.get_relative_rect().width/4, self.path_text_box.get_relative_rect().y + self.path_text_box.get_relative_rect().height * 2), (self.window_container.get_relative_rect().width/4, 50)),
            text="Créer",
            manager=manager,
            container=self.window_container,
            object_id=pygame_gui.core.ObjectID(class_id="@new_save_window", object_id="#save_btn"),
            anchors={"centerx": "centerx"}
        )

        self.cancel_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.window_container.get_relative_rect().width/4, self.path_text_box.get_relative_rect().y + self.path_text_box.get_relative_rect().height * 2), (self.window_container.get_relative_rect().width/4, 50)),
            text="Annuler",
            manager=manager,
            container=self.window_container,
            object_id=pygame_gui.core.ObjectID(class_id="@new_save_window", object_id="#cancel_btn"),
            anchors={"centerx": "centerx"}
        )

    def save_new(self):
        n_cols = self.cols_text_box.get_text()
        n_rows = self.rows_text_box.get_text()
        path = self.path_text_box.get_text()
        name = self.name_text_box.get_text()

        save_data = {
            "name": name,
            "cols": n_cols,
            "rows": n_rows,
            "path": path
        }

        with open(path, "w") as file:
            pass
