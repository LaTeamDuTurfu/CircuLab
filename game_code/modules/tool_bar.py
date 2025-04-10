import pygame_gui
import pygame
import json
import os, sys

# Permet de charger les modules dans le dossier game_code
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(project_root, "game_code"))

from modules import Tuile, NewSaveWindow

class ToolBar:

    # Load tiles images
    empty_tile = pygame.image.load("assets/tile_images/none.png")
    
    straight_road_tile = pygame.image.load("assets/tile_images/road_arrow.png")
    grass_tile = pygame.image.load("assets/tile_images/grass.png")
    sidewalk_tile = pygame.image.load("assets/tile_images/sidewalk.png")
    skyscraper_tile = pygame.image.load("assets/tile_images/Skyscraper.png")
    house1_tile = pygame.image.load("assets/tile_images/house1.png")
    house2_tile = pygame.image.load("assets/tile_images/house2.png")
    house3_tile = pygame.image.load("assets/tile_images/house3.png")
    house4_tile = pygame.image.load("assets/tile_images/house4.png")
    building_tile_images = [empty_tile, straight_road_tile, grass_tile, sidewalk_tile, skyscraper_tile, house1_tile, house2_tile, house3_tile, house4_tile]
    signalisation_tile_images = []
    
    tile_images = {
        0: building_tile_images,
        1: signalisation_tile_images
    }
    
    def __init__(self, surface, manager, mode_selector, window_frame, nbr_btns):
        self.WIDTH = surface.get_width()
        self.HEIGHT = surface.get_height()
        self.manager = manager
        self.window_frame = window_frame

        self.TILE_SIZE = NewSaveWindow.TILE_SIZE
        self.TOOL_BAR_BTN_SIZE = 78
        self.TOOL_BAR_HEIGHT = self.HEIGHT * 1/8
        self.TOOL_BAR_WIDTH = self.WIDTH * 3/4 - self.TOOL_BAR_BTN_SIZE/2

        self.tool_bar_btns = pygame.sprite.Group()
        self.close_btn = None
        self.show = True

        self.mode_selector = mode_selector
        
        self.change_image_btn(1, "assets/tile_images/road_arrow.png")
        self.change_image_btn(2, "assets/tile_images/grass.png")
        self.change_image_btn(3, "assets/tile_images/sidewalk.png")
        self.change_image_btn(4, "assets/tile_images/Skyscraper.png")
        self.change_image_btn(5, "assets/tile_images/house1.png")
        self.change_image_btn(6, "assets/tile_images/house2.png")
        self.change_image_btn(7, "assets/tile_images/house3.png")
        self.change_image_btn(8, "assets/tile_images/house4.png")

        self.tool_bar_window = pygame_gui.elements.UIWindow(
            rect=pygame.Rect((self.WIDTH - self.TOOL_BAR_WIDTH, self.window_frame.thickness), (self.TOOL_BAR_WIDTH, self.TOOL_BAR_HEIGHT)), 
            object_id="#tool_bar_window", 
            manager=self.manager)
        
        self.tool_bar_container = pygame_gui.elements.UIScrollingContainer(relative_rect=pygame.Rect((0, 0), (self.TOOL_BAR_WIDTH, self.TOOL_BAR_HEIGHT)), manager=self.manager, container=self.tool_bar_window, object_id="#tool_bar_container", allow_scroll_y=True)
    
        self.close_btn = pygame_gui.elements.UIButton(
                        relative_rect=pygame.Rect((self.TOOL_BAR_BTN_SIZE/4, self.window_frame.thickness/2), (self.TOOL_BAR_BTN_SIZE/2, self.TOOL_BAR_BTN_SIZE)),
                        text="",
                        manager=self.manager,
                        anchors={"centery": "centery"},
                        container=self.tool_bar_container,
                        object_id=pygame_gui.core.ObjectID(class_id="", object_id=f"#tool_bar_close_btn"),
                        command=self.change_tool_bar_state
                        )
        
        for i in range(len(Tuile.TILE_TYPES[self.mode_selector.current_mode])):
            new_btn = pygame_gui.elements.UIButton(
                        relative_rect=pygame.Rect(((11/8 * i * self.TOOL_BAR_BTN_SIZE) + self.TOOL_BAR_BTN_SIZE, self.window_frame.thickness/2), (self.TOOL_BAR_BTN_SIZE, self.TOOL_BAR_BTN_SIZE)),
                        text="",
                        manager=self.manager,
                        anchors={"centery": "centery"},
                        container=self.tool_bar_container,
                        object_id=pygame_gui.core.ObjectID(class_id="@tool_tip_btn", object_id=f"#tool_tip_btn_{i + 1}"))
            
            self.tool_bar_btns.add(new_btn)
    
    def get_selected_btn(self):
        """
        Returns the currently selected button in the toolbar.

        Iterates through all buttons in the toolbar and checks 
        if a button is selected. If a selected button is found, 
        it returns that button. If no button is selected, the 
        function will return None.
        """

        for btn in self.tool_bar_btns:
            if  btn.is_selected:
                return btn

    def unselect_all_btns(self):
        """
        Unselects all buttons in the toolbar.

        Iterates through all buttons in the toolbar and calls
        the unselect method on each one. This method is used to make
        sure no button is selected when the user changes the mode.
        """
        for btn in self.tool_bar_btns:
            btn.unselect()
    
    def change_image_btn(self, index, image_path):
        """
        Changes the image of a button in the toolbar given its index and the path to the image.

        Args:
        index (int): The index of the button in the toolbar.
        image_path (str): The path to the image that will be used to replace the current image on the button.

        Returns:
        None

        Notes:
        This method modifies the theme data file to update the image path for the button.
        It then reloads the theme data and updates the image on the button.
        """
        with open(f"data/theme_manager/styles_real.json", "r+") as theme_file:
            theme_data = json.load(theme_file)
            new_img = pygame.image.load(image_path)
            new_img = pygame.transform.scale(new_img, (self.TILE_SIZE, self.TILE_SIZE))
            theme_data[f"#tool_tip_btn_{index}"]["images"]["normal_image"]["path"] = image_path
        
        with open(f"data/theme_manager/styles_real.json", "w") as theme_file:
            json.dump(theme_data, theme_file)
        
        # TODO DONE: Faire en sorte d'update le theme après que le nouveau theme file ait été loaded.
        self.tile_images[index] = pygame.image.load(image_path)
        self.manager.rebuild_all_from_changed_theme_data()
    
    def change_tool_bar_state(self):
        """
        Toggles the visibility state of the toolbar.

        This function checks the current visibility state of the toolbar
        and toggles it. If the toolbar is currently visible, it hides the
        toolbar by moving its position off-screen and hiding its buttons.
        Otherwise, it shows the toolbar by bringing it back on-screen and
        displaying its buttons. It also updates the position of the close
        button accordingly and prints the current positions for debugging.
        """
        if self.show:
            self.tool_bar_window.rect.x = self.WIDTH - self.window_frame.thickness - self.TOOL_BAR_BTN_SIZE * 3/4
            self.close_btn.relative_rect.x = self.TOOL_BAR_WIDTH - self.TOOL_BAR_BTN_SIZE * 3/4
            self.show = False
            for btn in self.tool_bar_btns:
                btn.hide()
            print(f"{self.tool_bar_window.rect.x}, {self.close_btn.relative_rect.x}")
        else:
            self.tool_bar_window.rect.x = self.WIDTH - self.TOOL_BAR_WIDTH
            self.close_btn.relative_rect.x = self.TOOL_BAR_BTN_SIZE/4
            self.show = True
            for btn in self.tool_bar_btns:
                btn.show()
            print(f"{self.tool_bar_window.rect.x}, {self.close_btn.relative_rect.x}")