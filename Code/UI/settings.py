"""
Module Settings
Gère l’interface des paramètres utilisateur dans CircuLab (volume, sauvegarde automatique, etc.).
Affiche une fenêtre avec des sliders et boutons pour modifier les configurations et les sauvegarder.
"""
import pygame_gui
import json
from Code.Logic.configs_management import ConfigsManager
import pygame

# Classe gérant l’interface graphique des paramètres utilisateur

class Settings:
    def __init__(self, surface, manager, configs, home_screen, audio_manager):
        self.manager = manager
        self.screen = surface
        self.config_manager = configs
        self.home_screen = home_screen
        self.audio_manager = audio_manager

        self.font_title = pygame.font.Font("assets/font/Jersey25-Regular.ttf", 96)
        self.font_text = pygame.font.Font("assets/font/Jersey25-Regular.ttf", 64)

        self.saved_configs = self.config_manager.config
        self.changed_configs = self.saved_configs.copy()

        self.width = self.screen.get_width()    
        self.height = self.screen.get_height()

        self.back_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.width/40, self.height * 1/24), (self.width/12, self.height * 1/12)),
            text="Back",
            manager=self.manager,
            object_id=pygame_gui.core.ObjectID(class_id="@settings_btn", object_id="#back_btn"),
            visible=False,
            command=self.back_to_home
        )

        # Fenêtre principale contenant tous les éléments de l’interface des paramètres
        self.window_frame = pygame_gui.elements.UIWindow(
            rect=pygame.Rect((self.width/2 - self.width * 0.7/2, self.height/2 - self.height * 0.7/2), (self.width * 0.7, self.height * 0.7)),
            manager=self.manager,
            window_display_title="Settings",
            object_id=pygame_gui.core.ObjectID(class_id="@settings_window", object_id="#settings_window"),
            resizable=False,
            draggable=False,
            visible=False
        )

        self.music_volume_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((-self.window_frame.get_relative_rect().width * 5/8, self.window_frame.get_relative_rect().height/8), (self.window_frame.get_relative_rect().width, 50)),
            text="Music Volume",
            manager=self.manager,
            anchors={"centerx": "right", "top": "centery"},
            object_id=pygame_gui.core.ObjectID(class_id="@settings_label", object_id="#music_volume_label"),
            container=self.window_frame,
            parent_element=self.window_frame,
            visible=False
        )

        self.music_volume_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((self.window_frame.get_relative_rect().width/2, self.window_frame.get_relative_rect().height/8), (self.window_frame.get_relative_rect().width/3, 50)),
            manager=self.manager,
            anchors={"top": "centery"},
            object_id=pygame_gui.core.ObjectID(class_id="@settings_slider", object_id="#music_volume_slider"),
            container=self.window_frame,
            parent_element=self.window_frame,
            visible=False,
            start_value=self.saved_configs["music_volume"],
            value_range=(0, 1),
            click_increment=0.1
        )

        self.sfx_volume_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((-self.window_frame.get_relative_rect().width * 5/8, self.window_frame.get_relative_rect().height * 3/8), (self.window_frame.get_relative_rect().width, 50)),
            text="SFX Volume",
            manager=self.manager,
            anchors={"centerx": "right", "top": "centery"},
            object_id=pygame_gui.core.ObjectID(class_id="@settings_label", object_id="#sfx_volume_label"),
            container=self.window_frame,
            parent_element=self.window_frame,
            visible=False
        )

        self.SFX_volume_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((self.window_frame.get_relative_rect().width/2, self.window_frame.get_relative_rect().height * 3/8), (self.window_frame.get_relative_rect().width/3, 50)),
            manager=self.manager,
            anchors={"top": "centery"},
            object_id=pygame_gui.core.ObjectID(class_id="@settings_slider", object_id="#sfx_volume_slider"),
            container=self.window_frame,
            parent_element=self.window_frame,
            visible=False,
            start_value=self.saved_configs["sfx_volume"],
            value_range=(0, 1),
            click_increment=0.1
        )

        self.save_on_exit_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((-self.window_frame.get_relative_rect().width * 5/8, self.window_frame.get_relative_rect().height * 5/8), (self.window_frame.get_relative_rect().width, 50)),
            text="Save On Exit",
            manager=self.manager,
            anchors={"centerx": "centerx", "top": "centery"},
            object_id=pygame_gui.core.ObjectID(class_id="@settings_label", object_id="#save_on_exit_volume_label"),
            container=self.window_frame,
            parent_element=self.window_frame,
            visible=False
        )

        self.save_on_exit_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.window_frame.get_relative_rect().width/2, self.window_frame.get_relative_rect().height * 5/8), (self.window_frame.get_relative_rect().width/15, self.window_frame.get_relative_rect().width/15)),
            text="",
            manager=self.manager,
            anchors={"top": "centery"},
            object_id=pygame_gui.core.ObjectID(object_id="#save_on_exit_btn"),
            container=self.window_frame,
            parent_element=self.window_frame,
            visible=False,
            command=self.change_save_on_exit
        )

        

        self.reset_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.window_frame.get_relative_rect().width/8, self.window_frame.get_relative_rect().height * 13/16), (self.window_frame.get_relative_rect().width/4, self.window_frame.get_relative_rect().width/15)),
            text="Reset",
            manager=self.manager,
            anchors={"right": "centerx", "top": "centery"},
            object_id=pygame_gui.core.ObjectID(class_id="@settings_btn", object_id="#reset_btn"),
            container=self.window_frame,
            parent_element=self.window_frame,
            visible=False,
            command=self.reset_settings
        )

        self.apply_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.window_frame.get_relative_rect().width * 5/8, self.window_frame.get_relative_rect().height * 13/16), (self.window_frame.get_relative_rect().width/4, self.window_frame.get_relative_rect().width/15)),
            text="Apply",
            manager=self.manager,
            anchors={"right": "centerx", "top": "centery"},
            object_id=pygame_gui.core.ObjectID(class_id="@settings_btn", object_id="#apply_btn"),
            container=self.window_frame,
            parent_element=self.window_frame,
            visible=False,
            command=self.apply_settings
        )

        self.checked = False

        self.settings_btns = [
            self.back_btn,
            self.apply_btn,
            self.reset_btn
        ]

        self.title_x_pos = self.width/2

    # Affiche l’interface des paramètres et recharge les options si nécessaire
    def show_UI(self):
        self.draw_text("Settings", self.font_title, (255, 255, 255), self.title_x_pos, self.height/2 - self.window_frame.get_relative_rect().height/2 - 50)
        self.back_btn.show()
        self.window_frame.show()
        
        if not self.checked:
            self.config_manager.load_config()
            if self.config_manager.config["save_on_exit"]:
                self.save_on_exit_btn.select()
            else:
                self.save_on_exit_btn.unselect()

        self.checked = True

    # Cache l’interface des paramètres
    def hide_UI(self):
        self.back_btn.hide()
        self.window_frame.hide()

        self.checked = False

    # Affiche du texte centré sur l’écran
    def draw_text(self, text: str, font: pygame.font.Font, text_col: tuple[int, int, int], x: int, y: int) -> None:
        """
        Render the given text on the screen at the given position.

        Args:
            text (str): The text to render.
            font (pygame.font.Font): The font to use.
            text_col (tuple of int): The color of the text in RGB format.
            x (int): The x-coordinate of the center of the text.
            y (int): The y-coordinate of the center of the text.
        """
        # Render the text using the given font
        img = font.render(text, True, text_col)
        # Get the bounding rectangle of the rendered text
        img_rect = img.get_rect()
        # Set the center of the bounding rectangle to the given position
        img_rect.center = (x, y)
        # Blit the rendered text onto the main surface at the given position
        self.screen.blit(img, img_rect)
    
    # Revenir à l’écran d’accueil en jouant un son
    def back_to_home(self):
        self.audio_manager.play_sfx("button_click")
        self.hide_UI()
        self.home_screen.montrer_boutons()
        self.home_screen.state_manager.changer_état(1)
    
    # Réinitialise les paramètres aux valeurs par défaut
    def reset_settings(self):
        self.config_manager.config = self.config_manager.default_config.copy()

        self.music_volume_slider.set_current_value(self.config_manager.config["music_volume"])
        self.SFX_volume_slider.set_current_value(self.config_manager.config["sfx_volume"])
        self.save_on_exit_btn.is_selected = self.config_manager.config["save_on_exit"]
        self.change_selection()

        self.config_manager.save_config()

        self.audio_manager.play_sfx("button_click")
    
    # Applique les modifications des paramètres et les sauvegarde
    def apply_settings(self):
        self.changed_configs["music_volume"] = self.music_volume_slider.get_current_value()
        self.changed_configs["sfx_volume"] = self.SFX_volume_slider.get_current_value()
        self.changed_configs["save_on_exit"] = self.save_on_exit_btn.is_selected
        self.config_manager.config = self.changed_configs.copy()
        self.config_manager.save_config()

        self.audio_manager.load_config()

        self.audio_manager.play_sfx("button_click")
    
    # Inverse l’état de la case « Save On Exit »
    def change_save_on_exit(self):
        self.audio_manager.play_sfx("button_click")
        self.save_on_exit_btn.is_selected = not self.save_on_exit_btn.is_selected
        self.change_selection()
        
    
    # Sélectionne ou désélectionne le bouton de sauvegarde automatique visuellement
    def change_selection(self):
        if self.save_on_exit_btn.is_selected:
            self.save_on_exit_btn.select()
        else:
            self.save_on_exit_btn.unselect()
    
    # Centre dynamiquement la fenêtre des paramètres selon les coordonnées fournies
    def change_pos(self, x, y):
        self.title_x_pos = x

        x = x - self.window_frame.rect.width / 2
        y = y - self.window_frame.rect.height / 2
        self.window_frame.set_position((x, y))
