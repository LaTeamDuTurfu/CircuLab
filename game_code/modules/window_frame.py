import pygame_gui
import pygame
import json

import pygame_gui.elements.ui_2d_slider

class WindowFrame:
    def __init__(self, screen, thickness, color, manager):
        # Border parameters
        self.screen = screen
        self.thickness = thickness
        self.bottom_thickness = 2 * thickness
        self.color = color
        self.manager = manager
        
        # Build Rectangles
        self.top = pygame.Rect(0, 0, self.screen.get_width(), self.thickness)
        self.bottom = pygame.Rect(0, self.screen.get_height() - self.bottom_thickness, self.screen.get_width(), self.bottom_thickness)
        self.left = pygame.Rect(0, 0, self.thickness, self.screen.get_height())
        self.right = pygame.Rect(self.screen.get_width() - self.thickness, 0, self.thickness, self.screen.get_height())
        
        # Draw Border
        self.build_zoom_scroll()
        
    def draw_border(self):
        pygame.draw.rect(self.screen, self.color, self.top)
        pygame.draw.rect(self.screen, self.color, self.bottom)
        pygame.draw.rect(self.screen, self.color, self.left)
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