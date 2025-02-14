import pygame_gui
import pygame

class ToolBar:
    def __init__(self, surface, manager, nbr_btns):
        self.WIDTH = surface.get_width()
        self.HEIGHT = surface.get_height()
        self.manager = manager

        self.TOOL_BAR_HEIGHT = self.HEIGHT * 1/8
        self.TOOL_BAR_WIDTH = self.WIDTH * 3/4
        self.TOOL_BAR_BTN_SIZE = 78

        self.tool_bar_btns = pygame.sprite.Group()

        self.draw()
        self.draw_buttons(nbr_btns=nbr_btns)

    def draw(self):
        self.tool_bar_window = pygame_gui.elements.UIWindow(
            rect=pygame.Rect((self.WIDTH - self.TOOL_BAR_WIDTH, 0), (self.TOOL_BAR_WIDTH, self.TOOL_BAR_HEIGHT)), 
            object_id="#tool_bar_window", 
            manager=self.manager)
        
        self.tool_bar_container = pygame_gui.elements.UIScrollingContainer(relative_rect=pygame.Rect((0, 0), (self.TOOL_BAR_WIDTH, self.TOOL_BAR_HEIGHT)), 
                                                                           manager=self.manager, 
                                                                           container=self.tool_bar_window, 
                                                                           object_id="#tool_bar_container",
                                                                           allow_scroll_y=True)
    
    def draw_buttons(self, nbr_btns):
        for i in range(nbr_btns):
            new_btn = pygame_gui.elements.UIButton(
                        relative_rect=pygame.Rect(((3/2 * i * self.TOOL_BAR_BTN_SIZE) + self.TOOL_BAR_BTN_SIZE/2 , 0), (self.TOOL_BAR_BTN_SIZE, self.TOOL_BAR_BTN_SIZE)),
                        text="",
                        manager=self.manager,
                        anchors={"centery": "centery"},
                        container=self.tool_bar_container,
                        object_id=pygame_gui.core.ObjectID(class_id="@tool_tip_btn", object_id=f"#tool_tip_btn_{i + 1}"))
            
            self.tool_bar_btns.add(new_btn)
            
    
    def get_selected_btn(self):
        for btn in self.tool_bar_btns:
            if  btn.is_selected:
                return btn

    def unselect_all_btns(self):
        for btn in self.tool_bar_btns:
            btn.unselect()