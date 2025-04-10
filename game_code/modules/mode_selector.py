import pygame_gui
import pygame

class ModeSelector:
    
    modes = {
        "Building": 0,
        "Signalisation": 1,
        "Simulation": 2
    }
    
    def __init__(self, surface, manager, window_frame):
        self.WIDTH = surface.get_width()
        self.HEIGHT = surface.get_height()
        self.manager = manager
        self.window_frame = window_frame

        self.MODE_SELECTOR_HEIGHT = self.HEIGHT * 1/8
        self.MODE_SELECTOR_WIDTH = self.WIDTH * 1/4
        self.MODE_SELECTOR_BTN_SIZE = 78
        
        self.mode_selector_btns = pygame.sprite.Group()
        
        self.default_mode = self.modes["Building"]
        self.current_mode = self.default_mode
                
        self.mode_selector_window = pygame_gui.elements.UIWindow(
            rect=pygame.Rect((0, self.window_frame.thickness), (self.MODE_SELECTOR_WIDTH, self.MODE_SELECTOR_HEIGHT)), 
            object_id="#mode_selector_window", 
            manager=self.manager)
        
        self.mode_selector_container = pygame_gui.elements.UIScrollingContainer(relative_rect=pygame.Rect((0, 0), (self.MODE_SELECTOR_WIDTH, self.MODE_SELECTOR_HEIGHT)), manager=self.manager, container=self.mode_selector_window, object_id="#mode_selector_container", allow_scroll_y=False)
    
        for i in range(3):
            new_btn = pygame_gui.elements.UIButton(
                        relative_rect=pygame.Rect(((5/4 * i * self.MODE_SELECTOR_BTN_SIZE) + self.MODE_SELECTOR_BTN_SIZE/4, self.window_frame.thickness/2), (self.MODE_SELECTOR_BTN_SIZE, self.MODE_SELECTOR_BTN_SIZE)),
                        text="",
                        manager=self.manager,
                        anchors={"centery": "centery"},
                        container=self.mode_selector_container,
                        object_id=pygame_gui.core.ObjectID(class_id="@mode_selector_btn", object_id=f"#mode_selector_btn_{str(i + 1)}"))
            
            self.mode_selector_btns.add(new_btn)
    
    def get_selected_btn(self):
        """
        Returns the currently selected button in the mode selector.

        Iterates through all buttons in the mode selector and checks 
        if a button is selected. If a selected button is found, it 
        returns that button. If no button is selected, the function 
        will return None.
        """

        for btn in self.mode_selector_btns:
            if  btn.is_selected:
                return btn

    def unselect_all_btns(self):
        """
        Unselects all buttons in the mode selector.

        Iterates through all buttons in the mode selector and calls
        the unselect method on each one. This method is used to make
        sure no button is selected when the user changes the mode.
        """
        for btn in self.mode_selector_btns:
            btn.unselect()
    
    def change_mode(self, new_mode: str):
        """
        Changes the current mode to a new mode.

        Args:
        new_mode (str): The name of the new mode to switch to.

        Returns:
        bool: True if the mode change was successful, False if the mode does not exist.
        """
        try:
            self.current_mode = self.modes[new_mode]
            return True
        except:
            return False