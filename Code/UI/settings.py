import pygame_gui
import json
from Code.Logic.configs_management import ConfigsManager
import pygame

class Settings:
    def __init__(self, surface, manager, configs, home_screen):
        self.manager = manager
        self.screen = surface
        self.config_manager = configs
        self.home_screen = home_screen

        self.font_title = pygame.font.Font("assets/font/Jersey25-Regular.ttf", 96)
        self.font_text = pygame.font.Font("assets/font/Jersey25-Regular.ttf", 64)

        self.saved_configs = self.config_manager.config
        self.changed_configs = self.saved_configs.copy()

        self.width = self.screen.get_width()    
        self.height = self.screen.get_height()

        self.back_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.width/40, self.height * 1/24), (self.width/15, self.height * 1/12)),
            text="Back",
            manager=self.manager,
            object_id=pygame_gui.core.ObjectID(class_id="@settings_btn", object_id="#back_btn"),
            visible=False,
            command=self.back_to_home
        )

        self.window_frame = pygame_gui.elements.UIWindow(
            rect=pygame.Rect((self.width/2 - self.width * 0.7/2, self.height/2 - self.height * 0.7/3), (self.width * 0.7, self.height * 0.7)),
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
            value_range=(0, 1)
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
            value_range=(0, 1)
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

    def show_UI(self):
        self.draw_text("Settings", self.font_title, (255, 255, 255), self.width/2, self.height/6)
        self.back_btn.show()
        self.window_frame.show()
        
        if not self.checked:
            self.config_manager.load_config()
            if self.config_manager.config["save_on_exit"]:
                self.save_on_exit_btn.select()
            else:
                self.save_on_exit_btn.unselect()

        self.checked = True

    def hide_UI(self):
        self.back_btn.hide()
        self.window_frame.hide()

        self.checked = False

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
    
    def back_to_home(self):
        self.hide_UI()
        self.home_screen.montrer_boutons()
        self.home_screen.state_manager.changer_état(1)
    
    def reset_settings(self):
        self.config_manager.config = self.config_manager.default_config.copy()

        self.music_volume_slider.set_current_value(self.config_manager.config["music_volume"])
        self.SFX_volume_slider.set_current_value(self.config_manager.config["sfx_volume"])
        self.save_on_exit_btn.is_selected = self.config_manager.config["save_on_exit"]

        self.config_manager.save_config()
    
    def apply_settings(self):
        self.changed_configs["music_volume"] = self.music_volume_slider.get_current_value()
        self.changed_configs["sfx_volume"] = self.SFX_volume_slider.get_current_value()
        self.changed_configs["save_on_exit"] = self.save_on_exit_btn.is_selected
        self.config_manager.config = self.changed_configs.copy()
        self.config_manager.save_config()
    
    def change_save_on_exit(self):
        self.save_on_exit_btn.is_selected = not self.save_on_exit_btn.is_selected
        # print(self.save_on_exit_btn.is_selected)
        if self.save_on_exit_btn.is_selected:
            self.save_on_exit_btn.select()
        else:
            self.save_on_exit_btn.unselect()
