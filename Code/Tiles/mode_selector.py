import pygame_gui
import pygame

class ModeSelector:
    
    modes = {
        "Building": 0,
        "Signalisation": 1,
        "Simulation": 2
    }
    
    # Color palette
    BLACK = "#040f0f"
    DARK_GREEN = "#248232"
    GREEN = "#2ba84a"
    GREY = "#2d3a3a"
    WHITE = "#fcfffc"
    BLUE_GREY = "#7E99CF"
    YELLOW = "#D6E026"

    def __init__(self, surface, manager, window_frame, state_manager):
        self.WIDTH = surface.get_width()
        self.HEIGHT = surface.get_height()
        self.manager = manager
        self.window_frame = window_frame
        self.state_manager = state_manager
        self.tool_bar = None

        self.MODE_SELECTOR_HEIGHT = self.HEIGHT * 1/8
        self.MODE_SELECTOR_WIDTH = self.WIDTH * 1/4
        self.MODE_SELECTOR_BTN_SIZE = 78
        
        self.mode_selector_btns = []
        
        self.current_mode = self.state_manager.état_courant
                
        self.mode_selector_window = pygame_gui.elements.UIWindow(
            rect=pygame.Rect((self.window_frame.thickness, self.window_frame.thickness), (self.MODE_SELECTOR_WIDTH, self.MODE_SELECTOR_HEIGHT)), 
            object_id="#mode_selector_window", 
            manager=self.manager)
        
        self.mode_selector_container = pygame_gui.elements.UIScrollingContainer(relative_rect=pygame.Rect((0, 0), (self.MODE_SELECTOR_WIDTH, self.MODE_SELECTOR_HEIGHT)), manager=self.manager, container=self.mode_selector_window, object_id="#mode_selector_container", allow_scroll_y=False)
    
        for i in range(3):
            new_btn = pygame_gui.elements.UIButton(
                        relative_rect=pygame.Rect(((5/4 * i * self.MODE_SELECTOR_BTN_SIZE) + self.MODE_SELECTOR_BTN_SIZE/4, self.window_frame.thickness/4), (self.MODE_SELECTOR_BTN_SIZE, self.MODE_SELECTOR_BTN_SIZE)),
                        text="",
                        manager=self.manager,
                        anchors={"centery": "centery"},
                        container=self.mode_selector_container,
                        object_id=pygame_gui.core.ObjectID(class_id="@mode_selector_btn", object_id=f"#mode_selector_btn_{str(i + 1)}"))
            
            self.mode_selector_btns.append(new_btn)
        
        self.mode_selector_btns[0].select()

    def set_tool_bar(self, tool_bar):
        self.tool_bar = tool_bar

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
    
    def check_change_mode(self):
        current_mode = self.get_selected_btn()
        try:
            id_bouton_actif = int(current_mode.object_ids[-1][-1])
        except AttributeError:
            id_bouton_actif = 0
            
        if id_bouton_actif == 1 and self.state_manager.état_courant != 2:
            self.window_frame.color = self.BLUE_GREY
            self.tool_bar.set_building_tool_bar()
            self.state_manager.changer_état(2)  # Building
        elif id_bouton_actif == 2 and self.state_manager.état_courant != 7:
            self.window_frame.color = self.YELLOW
            self.tool_bar.set_signalisation_tool_bar()
            self.state_manager.changer_état(7)
        if id_bouton_actif == 3 and self.state_manager.état_courant != 3:
            self.window_frame.color = self.GREEN
            self.state_manager.changer_état(3)  # Simulation