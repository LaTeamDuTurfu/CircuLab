import sys
import os
import pygame
import pygame_gui

# Permet de charger les modules dans le dossier game_code
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(project_root, "game_code"))

from modules import *

class Circulab():
    def __init__(self, height: int = 720, width: int = 1280):
        # Setup Window
        pygame.init()
        pygame.display.set_caption('CircuLab')

        # Load Images
        self.logo = pygame.image.load("assets/other/logo.png")

        # Load Fonts
        self.font = pygame.font.Font("freesansbold.ttf", 32)

        # Color palette
        self.BLACK = "#040f0f"
        self.DARK_GREEN = "#248232"
        self.GREEN = "#2ba84a"
        self.GREY = "#2d3a3a"
        self.WHITE = "#fcfffc"
        self.BLUE_GREY = "#7E99CF"

        # Taille de la fenêtre
        self.HEIGHT = height
        self.WIDTH = width

        # Surface de la fenêtre
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        # GUI Manager
        self.manager = pygame_gui.UIManager((self.WIDTH, self.HEIGHT), theme_path="data/theme_manager/styles_real.json")

        # Dessiner les éléments du GUI
        self.window_border = WindowFrame(self.screen, 10, self.BLUE_GREY, self.manager)
        self.build_tool_bar = ToolBar(self.screen, self.manager, self.window_border, nbr_btns=8)
        self.mode_selector = ModeSelector(self.screen, self.manager, self.window_border)
        
        # Horloge (pour les FPS)
        self.clock = pygame.time.Clock()

        self.new_save_window = NewSaveWindow(pygame.Rect((self.WIDTH/4, self.HEIGHT/6), (self.WIDTH/2, self.HEIGHT * 2/3)), self.manager, default_path="../Circulab/data/saves/")

        # (temp)
        self.ROWS = 150
        self.COLUMNS = 150
        self.TILE_SIZE = 50
        
        # Variable de jeu
        self.build_orientation = 0
        self.see_build_preview = False
        self.running = True
        
        # Position de la souris
        self.pos = [0, 0]
        self.x_pos = self.pos[0]
        self.y_pos = self.pos[1]

        # Data 
        self.current_save = None
        
        # Vérifie si une save est loaded
        self.loaded_save = False
    
    def run(self):
        while self.running:
            # FPS Capping
            time_delta = self.clock.tick(60)/1000


            # Logic
            self.get_mouse_pos()
            self.traiter_inputs()

            if not self.loaded_save:
                if self.new_save_window.check_save_created():
                    self.current_save = self.new_save_window.created_game
                    self.loaded_save = True
                    pygame.display.set_caption(f'CircuLab - {self.current_save.name}')


            # Remplit le fond de couleur grise
            self.screen.fill(self.GREY)
            
            if self.loaded_save:
                # Dessine les tuiles
                self.current_save.change_scroll(self.screen)
                self.change_tuiles()
                self.current_save.draw_tuiles(self.screen)            

                # Dessine la grille
                self.current_save.draw_grid(self.screen)    

                # Dessine les éléments du GUI
                if self.see_build_preview:
                    pygame.draw.rect(self.screen, self.BLUE_GREY, (self.x_pos * self.current_save.TILE_SIZE - self.current_save.scrollx, self.y_pos * self.current_save.TILE_SIZE - self.current_save.scrolly, self.current_save.TILE_SIZE, self.current_save.TILE_SIZE))
                    self.draw_text(f"X: {int(self.x_pos)} | Y: {int(self.y_pos)}", self.font, self.WHITE, self.pos[0], self.pos[1]-self.current_save.TILE_SIZE/2) 

            # Dessine la bordure de l'écran
            self.window_border.draw_border()
            
            # Update l'écran
            self.manager.update(time_delta)
            self.manager.draw_ui(self.screen)
            self.window_border.draw_border(bottom=False)
            pygame.display.flip()
    
        pygame.quit()

    def traiter_inputs(self):
        """
        Vérifie si le joueur clique sur le "X" ou sur un bouton de la barre d'outils,
        et met à jour les valeurs de horizontal_scroll et vertical_scroll en fonction
        des touches de direction presses.

        Si le joueur appuie sur Shift, le scroll est acceleré.
        Si le joueur relache Shift, le scroll redevient normal.
        """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element in self.build_tool_bar.tool_bar_btns:
                btn = event.ui_element
                if not btn.is_selected:
                    self.build_tool_bar.unselect_all_btns()
                    btn.select()
                    continue
                elif btn.is_selected:
                    btn.unselect()
                    continue

            if event.type == pygame.KEYDOWN:
                if self.loaded_save:
                    if event.key == pygame.K_LEFT:
                        self.current_save.horizontal_scroll = -1
                    if event.key == pygame.K_RIGHT:
                        self.current_save.horizontal_scroll = 1
                    if event.key == pygame.K_UP:
                        self.current_save.vertical_scroll = -1
                    if event.key == pygame.K_DOWN:
                        self.current_save.vertical_scroll = 1
                    if event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
                        self.current_save.scroll_speed = 5
                    if event.key == pygame.K_r:
                        self.change_build_orientation()
                    if event.key == pygame.K_p:
                        self.see_build_preview = not self.see_build_preview
                    if event.key == pygame.K_1:
                        self.current_save.zoom(1.1)
                    if event.key == pygame.K_2:
                        self.current_save.zoom(0.9)

            if event.type == pygame.KEYUP:
                if self.loaded_save:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        self.current_save.horizontal_scroll = 0
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        self.current_save.vertical_scroll = 0
                    if event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
                        self.current_save.scroll_speed = 1

            self.manager.process_events(event)  
    
    def draw_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        img_rect = img.get_rect()
        img_rect.center = (x, y)
        self.screen.blit(img, img_rect)

    def get_mouse_pos(self):
        #get mouse position
        self.pos = pygame.mouse.get_pos()
        try:
            self.x_pos = (self.pos[0] + self.current_save.scrollx) // self.current_save.TILE_SIZE
            self.y_pos = (self.pos[1] + self.current_save.scrolly) // self.current_save.TILE_SIZE
        except AttributeError:
            pass


    def change_build_orientation(self):
        self.build_orientation += 1
        if self.build_orientation > 3:
            self.build_orientation = 0

    def change_tuiles(self):
        if self.window_border.thickness < self.pos[0] < (self.WIDTH - self.window_border.thickness) and self.build_tool_bar.TOOL_BAR_HEIGHT < self.pos[1] < (self.HEIGHT - self.window_border.bottom_thickness):
            self.y_pos = int(self.y_pos)
            self.x_pos = int(self.x_pos)
            try:
                bouton_actif = self.build_tool_bar.get_selected_btn()
                id_bouton_actif = bouton_actif.object_ids[-1]
            except AttributeError:
                pass
            if pygame.mouse.get_pressed()[0] == 1:
                try:
                    if self.current_save.road_data[self.y_pos][self.x_pos].image != ToolBar.tile_images[int(id_bouton_actif[-1])]:
                        self.current_save.road_data[self.y_pos][self.x_pos] = Tuile(self.current_save.TILE_SIZE, ToolBar.tile_images[int(id_bouton_actif[-1])], orientation=self.build_orientation)
                except UnboundLocalError:
                    pass
            if pygame.mouse.get_pressed()[2] == 1:
                self.current_save.road_data[self.y_pos][self.x_pos] = Tuile(self.current_save.TILE_SIZE, Tuile.empty_tile, orientation=self.build_orientation)