import sys
import os
import pygame
import pygame_gui

# Permet de charger les modules dans le dossier game_code
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(project_root, "game_code"))


from modules import *
from logic.graphe import *
from logic.états import *

class Circulab():
    def __init__(self, height: int = 720, width: int = 1280):
        # Setup Window
        pygame.init()
        pygame.display.set_caption('CircuLab')

        # Load Fonts
        self.font = pygame.font.Font("freesansbold.ttf", 24)
        self.font_title = pygame.font.Font("assets/font/Jersey25-Regular.ttf", 96)
        self.font_text = pygame.font.Font("assets/font/Jersey25-Regular.ttf", 24)
        
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
        
        # State Manager
        self.state_manager = ÉtatJeu(ÉtatJeu.NEW_GAME)
        
        # Road Orientation Manager
        self.road_orientation_manager = RoadOrientationManager()
        
        # Dessiner les éléments du GUI (En Game)
        self.window_border = WindowFrame(self.screen, 10, self.BLUE_GREY, self.manager)
        
        self.mode_selector = ModeSelector(self.screen, self.manager, self.window_border)
        self.mode_selector.mode_selector_window.hide()
        
        self.build_tool_bar = ToolBar(self.screen, self.manager, self.mode_selector, self.window_border, nbr_btns=8)
        self.build_tool_bar.tool_bar_window.hide()
        
        # Horloge (pour les FPS)
        self.clock = pygame.time.Clock()

        # Instancie la fenêtre de sauvegarde (cachée par défaut)
        self.new_save_window = NewSaveWindow(pygame.Rect((self.WIDTH/4, self.HEIGHT/6), (self.WIDTH/2, self.HEIGHT * 2/3)), self.manager, default_path="../Circulab/data/saves/")
        self.new_save_window.hide()
        
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
    
    def run(self):
        
        """
        Boucle principale du jeu.
        
        Gère les événements clavier et souris, met à jour l'écran
        en fonction de l'état courant du jeu, et gère les éléments du GUI.
        """
        while self.running:
            # FPS Capping
            time_delta = self.clock.tick(60)/1000

            # Logic
            self.get_mouse_pos()
            self.traiter_inputs()
            
            # Remplit le fond de couleur grise
            self.screen.fill(self.GREY)
            
            if self.state_manager.état_courant == ÉtatJeu.HOME_PAGE:
                self.draw_text("CircuLab", self.font_title, "white", self.WIDTH/2, self.HEIGHT/3)
            elif self.state_manager.état_courant == ÉtatJeu.SETTINGS:
                pass
            elif self.state_manager.état_courant == ÉtatJeu.NEW_GAME:
                self.new_save_window.show()
                if self.new_save_window.check_save_created():
                    self.current_save = self.new_save_window.created_game
                    self.road_orientation_manager.set_game_data(self.current_save.building_data)
                    self.graphe = Graphe(current_save=self.current_save)
                    pygame.display.set_caption(f'CircuLab - {self.current_save.name}')
                    self.state_manager.changer_état(ÉtatJeu.GAME_EDITOR)
            elif self.state_manager.état_courant == ÉtatJeu.LOAD_GAME:
                pass
            elif self.state_manager.état_courant == ÉtatJeu.GAME_EDITOR:
                self.mode_selector.mode_selector_window.show()
                self.build_tool_bar.tool_bar_window.show()
                
                # Dessine les tuiles
                self.current_save.change_scroll(self.screen)
                self.change_tuiles()
                self.current_save.draw_tuiles(self.screen)            

                # Dessine la grille
                self.current_save.draw_grid(self.screen)    
                
                # Dessine les éléments du GUI
                if self.see_build_preview:
                    pygame.draw.rect(self.screen, self.BLUE_GREY, (self.x_pos * self.current_save.TILE_SIZE - self.current_save.scrollx, self.y_pos * self.current_save.TILE_SIZE - self.current_save.scrolly, self.current_save.TILE_SIZE, self.current_save.TILE_SIZE))
                    self.draw_text(f"Orientation: {Tuile.BUILD_ORIENTATIONS[self.build_orientation]}", self.font_text, self.WHITE, self.pos[0], self.pos[1]-self.current_save.TILE_SIZE/2)
                    self.draw_text(f"X: {int(self.x_pos)} | Y: {int(self.y_pos)}", self.font, self.WHITE, self.pos[0], self.pos[1]) 

                    
                # Dessine la bordure de l'écran
                self.window_border.draw_border() 
                 
                # Update l'écran
                self.window_border.draw_border(bottom=False)
                
            self.manager.update(time_delta)
            self.manager.draw_ui(self.screen)
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
            elif event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element in self.mode_selector.mode_selector_btns:
                btn = event.ui_element
                if not btn.is_selected:
                    self.mode_selector.unselect_all_btns()
                    btn.select()
                    continue
                elif btn.is_selected:
                    btn.unselect()
                    continue

            if event.type == pygame.KEYDOWN:
                if self.state_manager.état_courant in [ÉtatJeu.GAME_EDITOR]:
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
                    if event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                        self.current_save.zoom(1)
                        self.current_save.draw_tuiles(self.screen)
                    if event.key == pygame.K_MINUS:
                        self.current_save.zoom(-1)
                        self.current_save.draw_tuiles(self.screen)

            if event.type == pygame.KEYUP:
                if self.state_manager.état_courant in [ÉtatJeu.GAME_EDITOR]:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        self.current_save.horizontal_scroll = 0
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        self.current_save.vertical_scroll = 0
                    if event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
                        self.current_save.scroll_speed = 1

            self.manager.process_events(event)  
    
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

    def get_mouse_pos(self):
        #get mouse position
        """
        Updates the current mouse position and calculates the corresponding tile position.

        This function retrieves the current mouse position and calculates the indices
        of the tile being hovered over on the grid. The positions are adjusted based
        on the current scroll offset and tile size.
        """

        self.pos = pygame.mouse.get_pos()
        try:
            self.x_pos = (self.pos[0] + self.current_save.scrollx) // self.current_save.TILE_SIZE
            self.y_pos = (self.pos[1] + self.current_save.scrolly) // self.current_save.TILE_SIZE
        except AttributeError:
            pass

    def change_build_orientation(self):
        """
        Cycles through the build orientations in a clockwise manner.

        This function increments the 'build_orientation' attribute by 1 to change
        the orientation of a building. If the orientation exceeds 3, it resets to 0,
        ensuring the orientation remains within the valid range of 0 to 3.
        """
        self.build_orientation += 1
        if self.build_orientation > 3:
            self.build_orientation = 0

    def change_tuiles(self):
        """
        Updates the tile at the current mouse position to the selected tile
        image from the toolbar, but only if the left mouse button is pressed
        and the current tile at the mouse position is not the same as the
        selected tile. If the right mouse button is pressed, the tile is reset
        to an empty tile.

        This function is used in the game loop to update the tiles on the grid
        based on the user's input. It is called every frame when the game is in
        the game editor state.
        """
        if self.window_border.thickness < self.pos[0] < (self.WIDTH - self.window_border.thickness) and self.build_tool_bar.TOOL_BAR_HEIGHT < self.pos[1] < (self.HEIGHT - self.window_border.bottom_thickness):
            self.y_pos = int(self.y_pos)
            self.x_pos = int(self.x_pos)
            try:
                bouton_actif = self.build_tool_bar.get_selected_btn()
                id_bouton_actif = bouton_actif.object_ids[-1][-1]
            except AttributeError:
                pass
            if pygame.mouse.get_pressed()[0] == 1:
                try:
                    if self.current_save.game_data[self.mode_selector.current_mode][self.y_pos][self.x_pos].image != ToolBar.tile_images[self.mode_selector.current_mode][int(id_bouton_actif)]:
                        if self.mode_selector.current_mode == 0:
                            self.current_save.game_data[self.mode_selector.current_mode][self.y_pos][self.x_pos] = Tuile(self.current_save.TILE_SIZE, ToolBar.tile_images[int(id_bouton_actif[-1])], orientation=self.build_orientation, tile_type=Tuile.BUILD_TILE_TYPES[int(id_bouton_actif)])
                            
                            self.road_orientation_manager.check_tile_change(self.x_pos, self.y_pos)
                            
                        elif self.mode_selector.current_mode == 1:
                            self.current_save.game_data[self.mode_selector.current_mode][self.y_pos][self.x_pos] = Tuile(self.current_save.TILE_SIZE, ToolBar.tile_images[int(id_bouton_actif[-1])], orientation=self.build_orientation, tile_type=Tuile.SIGNALISATION_TILE_TYPES[int(id_bouton_actif)])
                        elif self.mode_selector.current_mode == 2:
                            pass
                        
                except UnboundLocalError:
                    pass
            if pygame.mouse.get_pressed()[2] == 1:
                self.current_save.game_data[self.mode_selector.current_mode][self.y_pos][self.x_pos] = Tuile(self.current_save.TILE_SIZE, Tuile.empty_tile, orientation=self.build_orientation)