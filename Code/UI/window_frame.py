"""
Module WindowFrame
Gère l'encadrement de l'écran de jeu et les boutons d’interface liés à la sauvegarde et au retour au menu.
Affiche des bordures et des éléments d’interface utilisateur persistants en haut et en bas de l’écran.
"""
import pygame_gui
import pygame
import time
import pygame_gui.elements.ui_2d_slider

# Classe qui gère la bordure d’interface et les actions de sauvegarde/menu dans CircuLab

class WindowFrame:
    def __init__(self, screen, thickness, color, manager, home_screen, state_manager, audio_manager):
        # Border parameters
        self.screen = screen
        self.thickness = thickness
        self.bottom_thickness = thickness
        self.color = color
        self.manager = manager
        self.home_screen = home_screen
        self.state_manager = state_manager
        self.audio_manager = audio_manager
        self.tool_bar = None
        self.mode_selector = None   
        self.game = None
        
        # Initialise les rectangles représentant les bordures de l’écran
        self.update_border()
        
        self.WIDTH = self.screen.get_width()
        self.HEIGHT = self.screen.get_height()
        
        # Bouton pour revenir au menu principal
        self.menu_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.thickness, 0), (self.screen.get_width()/12, self.thickness)),
            text='Menu',
            manager=self.manager,
            object_id=pygame_gui.core.ObjectID(class_id="@window_frame_btns", object_id="#menu_btn"),
            visible=False,
            command=self.retour_menu
        )
        
        # Bouton pour sauvegarder la partie courante
        self.save_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.menu_btn.relative_rect.width + self.menu_btn.relative_rect.x, 0), (self.screen.get_width()/8, self.thickness)),
            text='Sauvegarder',
            manager=self.manager,
            object_id=pygame_gui.core.ObjectID(class_id="@window_frame_btns", object_id="#save_btn"),
            visible=False,
            command=self.update_game
        )
        
    
    # Met à jour les rectangles de bordure aux nouvelles dimensions de l’écran
    def update_border(self):
        # Build Rectangles
        self.top = pygame.Rect(0, 0, self.screen.get_width(), self.thickness)
        self.bottom = pygame.Rect(0, self.screen.get_height() - self.bottom_thickness, self.screen.get_width(), self.bottom_thickness)
        self.left = pygame.Rect(0, 0, self.thickness, self.screen.get_height())
        self.right = pygame.Rect(self.screen.get_width() - self.thickness, 0, self.thickness, self.screen.get_height())
    
    # Dessine les bordures visibles autour de l’écran selon les directions spécifiées
    def draw_border(self, top: bool = 1, bottom: bool = 1, left: bool = 1, right: bool = 1):
        if top:
            pygame.draw.rect(self.screen, self.color, self.top)
        if bottom:
            pygame.draw.rect(self.screen, self.color, self.bottom)
        if left:
            pygame.draw.rect(self.screen, self.color, self.left)
        if right:
            pygame.draw.rect(self.screen, self.color, self.right)
    
    # Crée un slider horizontal dans la bordure inférieure (ex. zoom ou scroll)
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

    # Définit l’objet Partie sur lequel effectuer les sauvegardes
    def set_game(self, game):
        self.game = game

    # Ouvre une fenêtre modale de feedback et tente de sauvegarder la partie en cours
    def update_game(self):
        
        self.saving_window = pygame_gui.windows.UIMessageWindow(
                        rect=pygame.Rect((self.WIDTH / 2 - 150, self.HEIGHT / 2 - 75), (300, 150)),
                        manager=self.manager,
                        window_title="Sauvegarde de la partie",
                        html_message="Sauvegarde en cours..."
                    )
        self.saving_window.dismiss_button.set_text("Continuer")
        self.saving_window.set_blocking(True)
        self.saving_window.title_bar.hide()
        self.saving_window.close_window_button.hide()
            
        self.audio_manager.play_sfx("button_click")
        self.saving_window.dismiss_button.disable()
        if self.game.update_save():
            self.saving_window.text_block.set_text("Sauvegarde réussie! ✅")
        else:
            self.saving_window.text_block.set_text("Sauvegarde echouée! ❌")
        self.saving_window.dismiss_button.enable()
        

    # Change dynamiquement le texte du bouton de sauvegarde après un délai
    def change_save_btn_text(self, text:str, sleep_time:int=0):
        time.sleep(sleep_time)
        self.save_btn.set_text(text)

    # Affiche (ou cache) tous les boutons visibles de la bordure
    def show_all_btns(self):
        self.menu_btn.show()
        self.save_btn.show()
    
    # Affiche (ou cache) tous les boutons visibles de la bordure
    def hide_all_btns(self):    
        self.menu_btn.hide()
        self.save_btn.hide()
    
    # Action de retour au menu principal : joue un son, masque les outils et change l’état du jeu
    def retour_menu(self):
        self.audio_manager.play_sfx("button_click")
        self.state_manager.changer_état(1)
        self.hide_all_btns()
        self.tool_bar.tool_bar_window.hide()
        self.mode_selector.mode_selector_window.hide()
        self.home_screen.montrer_boutons()