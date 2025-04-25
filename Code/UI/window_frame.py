import pygame_gui
import pygame
import time
import pygame_gui.elements.ui_2d_slider

class WindowFrame:
    def __init__(self, screen, thickness, color, manager, home_screen, state_manager):
        # Border parameters
        self.screen = screen
        self.thickness = thickness
        self.bottom_thickness = thickness
        self.color = color
        self.manager = manager
        self.home_screen = home_screen
        self.state_manager = state_manager
        self.tool_bar = None
        self.mode_selector = None   
        self.game = None
        
        self.update_border()
        
        self.menu_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.thickness, 0), (self.screen.get_width()/12, self.thickness)),
            text='Menu',
            manager=self.manager,
            object_id="#menu_btn",
            visible=False,
            command=self.retour_menu
        )
        
        self.save_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.menu_btn.relative_rect.width + self.menu_btn.relative_rect.x, 0), (self.screen.get_width()/12, self.thickness)),
            text='Sauvegarder',
            manager=self.manager,
            object_id="#save_btn",
            visible=False,
            command=self.update_game
        )
    
    def update_border(self):
        # Build Rectangles
        self.top = pygame.Rect(0, 0, self.screen.get_width(), self.thickness)
        self.bottom = pygame.Rect(0, self.screen.get_height() - self.bottom_thickness, self.screen.get_width(), self.bottom_thickness)
        self.left = pygame.Rect(0, 0, self.thickness, self.screen.get_height())
        self.right = pygame.Rect(self.screen.get_width() - self.thickness, 0, self.thickness, self.screen.get_height())
    
    def draw_border(self, top: bool = 1, bottom: bool = 1, left: bool = 1, right: bool = 1):
        if top:
            pygame.draw.rect(self.screen, self.color, self.top)
        if bottom:
            pygame.draw.rect(self.screen, self.color, self.bottom)
        if left:
            pygame.draw.rect(self.screen, self.color, self.left)
        if right:
            pygame.draw.rect(self.screen, self.color, self.right)
    
    def build_zoom_scroll(self):
        scroller = pygame_gui.elements.ui_2d_slider.UI2DSlider(
            relative_rect = pygame.Rect((self.screen.get_width() - self.screen.get_width()/6, self.screen.get_height() - self.bottom_thickness), (self.screen.get_width()/8, self.bottom_thickness)),
            manager=self.manager,
            start_value_x=1,
            start_value_y=0,
            value_range_x=(0, 2),
            value_range_y=(0, 0),
            object_id="#zoom_slider",
            visible=True
            )

    def set_game(self, game):
        self.game = game

    def update_game(self):
        self.game.update_save()

    def change_save_btn_text(self, text:str, sleep_time:int=0):
        time.sleep(sleep_time)
        self.save_btn.set_text(text)

    def show_all_btns(self):
        self.menu_btn.show()
        self.save_btn.show()
    
    def hide_all_btns(self):    
        self.menu_btn.hide()
        self.save_btn.hide()
    
    def retour_menu(self):
        self.state_manager.changer_état(1)
        self.hide_all_btns()
        self.tool_bar.tool_bar_window.hide()
        self.mode_selector.mode_selector_window.hide()
        self.home_screen.montrer_boutons()