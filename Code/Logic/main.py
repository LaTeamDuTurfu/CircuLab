import sys
import os
import pygame
import pygame_gui
from pygame.examples.grid import TILE_SIZE

# Permet de charger les modules dans le dossier game_code
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(project_root, "Code"))


from Logic.états import *
from Logic.partie import *
from Tiles import *
from UI import *
from Cars import *

class Circulab():
    
    # Color palette
    BLACK = "#040f0f"
    DARK_GREEN = "#248232"
    GREEN = "#2ba84a"
    GREY = "#1E1E1E"
    WHITE = "#fcfffc"
    BLUE_GREY = "#7E99CF"
    YELLOW = "#D6E026"
    RED = "#FF0000"

    def __init__(self, height: int = 720, width: int = 1280):
        # Setup Window
        pygame.init()
        pygame.display.set_caption('CircuLab')

        # Load Fonts
        self.font = pygame.font.Font("freesansbold.ttf", 24)
        self.font_title = pygame.font.Font("assets/font/Jersey25-Regular.ttf", 96)
        self.font_text = pygame.font.Font("assets/font/Jersey25-Regular.ttf", 24)
        
        # Taille de la fenêtre
        self.HEIGHT = height
        self.WIDTH = width

        # Surface de la fenêtre
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        # GUI Manager
        self.manager = pygame_gui.UIManager((self.WIDTH, self.HEIGHT), theme_path="data/theme_manager/styles_real.json")
        
        # State Manager
        self.state_manager = ÉtatJeu(ÉtatJeu.HOME_PAGE)
        
        # Road Orientation Manager
        self.road_orientation_manager = RoadOrientationManager()
        
        # Horloge (pour les FPS)
        self.clock = pygame.time.Clock()

        # Instancie l'écran d'acceuil
        self.home_screen = HomeScreen(self.screen, self.manager, self.state_manager)
        
        # Dessiner les éléments du GUI (En Game)
        self.window_border = WindowFrame(self.screen, 20, self.BLUE_GREY, self.manager, self.home_screen, self.state_manager)

        # Instancie la fenêtre de sélection de mode (cachée par défaut)
        self.mode_selector = ModeSelector(self.screen, self.manager, self.window_border, self.state_manager)
        self.mode_selector.mode_selector_window.hide()
        
        # Instancie la tool_bar (cachée par défaut)
        self.build_tool_bar = ToolBar(self.screen, self.manager, self.mode_selector, self.window_border)
        self.build_tool_bar.tool_bar_window.hide()

        # Associe la tool_bar au mode_selector
        self.mode_selector.set_tool_bar(self.build_tool_bar)

        # Relie la tool_bar à la bordure de fenêtre
        self.window_border.mode_selector = self.mode_selector
        self.window_border.tool_bar = self.build_tool_bar

        # Instancie les fenêtres de sauvegarde (cachée par défaut)
        self.default_path = "../Circulab/data/saves/"
        self.new_save_window = NewSaveWindow(pygame.Rect((self.WIDTH/4, self.HEIGHT/6), (self.WIDTH/2, self.HEIGHT * 2/3)), self.manager, default_path=self.default_path, state_manager=self.state_manager, home_screen=self.home_screen)
        self.new_save_window.hide()
        
        self.load_save_window = LoadSaveWindow(rect=pygame.Rect((self.WIDTH/4, self.HEIGHT/6), (self.WIDTH/2, self.HEIGHT * 2/3)), surface=self.screen, manager=self.manager, default_path=self.default_path, state_manager=self.state_manager, home_screen=self.home_screen)
        
        # Variable de jeu
        self.build_orientation = 0
        self.see_build_preview = False
        self.debug_view = False
        self.running = True
        
        # Position de la souris
        self.pos = [0, 0]
        self.x_pos = self.pos[0]
        self.y_pos = self.pos[1]

        # Data 
        self.current_save = None

        # Graph
        self.graphe = Graphe(TILE_SIZE=NewSaveWindow.TILE_SIZE)

        # Flag pour le graph
        self.graph_created = False

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
                self.current_save = None
                self.draw_text("CircuLab", self.font_title, "white", self.WIDTH/2, self.HEIGHT/4)
                
                pygame.display.set_caption(f'CircuLab - Home Page')
            elif self.state_manager.état_courant == ÉtatJeu.SETTINGS:
                pygame.display.set_caption(f'CircuLab - Settings')
            elif self.state_manager.état_courant == ÉtatJeu.NEW_GAME:
                pygame.display.set_caption(f'CircuLab - New Game')
                self.new_save_window.show()
                if self.new_save_window.check_save_created():
                    self.current_save = self.new_save_window.created_game
                    self.new_save_window.created_game = None

                    self.road_orientation_manager.set_game_data(self.current_save.building_data)
                    self.window_border.set_game(self.current_save)
                    self.window_border.show_all_btns()
                    pygame.display.set_caption(f'CircuLab - {self.current_save.name}')

                    self.mode_selector.mode_selector_btns[0].select()
                    self.mode_selector.check_change_mode()

            elif self.state_manager.état_courant == ÉtatJeu.LOAD_GAME:
                self.load_save_window.file_explorer_window.show()
                pygame.display.set_caption(f'CircuLab - Load Game')
                if self.load_save_window.check_save_created():
                    self.current_save = self.load_save_window.loaded_game
                    self.load_save_window.loaded_game = None

                    self.window_border.set_game(self.current_save)
                    self.window_border.show_all_btns()
                    self.road_orientation_manager.set_game_data(self.current_save.building_data)

                    pygame.display.set_caption(f'CircuLab - {self.current_save.name}')
                    
                    print(self.current_save.building_data[5][5].image)
                    
                    self.mode_selector.mode_selector_btns[0].select()
                    self.mode_selector.check_change_mode()
                    
                    self.current_save.update_all_roads(self.road_orientation_manager)
                    
            elif self.state_manager.état_courant == ÉtatJeu.GAME_EDITOR or self.state_manager.état_courant == ÉtatJeu.SIGNALISATION:
                self.mode_selector.mode_selector_window.show()
                self.build_tool_bar.tool_bar_window.show()
                
                # Bouge la grille
                self.current_save.change_scroll(self.screen)

                # Change l'apparence des tuiles si la souris est sur la grille
                self.current_save.change_tuiles(self.screen, self.build_tool_bar, self.pos, self.window_border, self.state_manager, self.road_orientation_manager, self.build_orientation, self.graphe)
                 
            
            # Dessine la bordure de l'écran si le game editor ou la simulation est en cours
            elif self.state_manager.état_courant == ÉtatJeu.SIMULATION and self.graphe.nb_points >= 2:
                    if not self.graph_created:
                        self.graphe.build_intersections()
                        self.graphe.build_routes()
                        self.graphe.build_graph()
                        self.graphe.create_vehicles(10)
                        self.graph_created = True
                        self.graphe.show_graph()

            # Dessine la bordure de l'écran si le game editor ou la simulation est en cours
            if self.state_manager.état_courant in [ÉtatJeu.GAME_EDITOR, ÉtatJeu.SIMULATION, ÉtatJeu.SIGNALISATION]:
                # Check si le mode est changé
                self.mode_selector.check_change_mode()
                
                # Dessine les tuiles
                self.current_save.draw_tuiles(self.screen)            

                # Dessine la grille
                self.current_save.draw_grid(self.screen)    
                
                # Dessine les éléments du GUI (si le user veut voir le preview [P])
                if self.see_build_preview:
                    pygame.draw.rect(self.screen, self.BLUE_GREY, (self.x_pos * self.current_save.TILE_SIZE - self.current_save.scrollx, self.y_pos * self.current_save.TILE_SIZE - self.current_save.scrolly, self.current_save.TILE_SIZE, self.current_save.TILE_SIZE))
                    self.draw_text(f"Build Orientation: {Tuile.BUILD_ORIENTATIONS[self.build_orientation]}", self.font_text, self.WHITE, self.pos[0], self.pos[1]-self.current_save.TILE_SIZE/2)
                    self.draw_text(f"X: {int(self.x_pos)} | Y: {int(self.y_pos)}", self.font, self.WHITE, self.pos[0], self.pos[1])
                
                if self.debug_view:
                    hover_tile = self.current_save.building_data[self.y_pos][self.x_pos]
                    color = self.GREEN
                    if hover_tile.tile_type == "@empty":
                        color = self.RED
                    self.draw_text(f"Type: {hover_tile.tile_type} | Orientation: {Tuile.BUILD_ORIENTATIONS[hover_tile.orientation]}", self.font_text, color, self.pos[0], self.pos[1]-self.current_save.TILE_SIZE)
                    
            
                # Dessine la bordure de l'écran
                self.window_border.draw_border() 
                # Update l'écran
                self.window_border.draw_border(bottom=False)
                    
        
            # Gère les éléments de pygame_GUI
            self.manager.update(time_delta)
            self.manager.draw_ui(self.screen)

            if self.state_manager.état_courant == ÉtatJeu.SIMULATION and self.graphe.nb_points >= 2 and not self.graphe.simulation_finished:
                self.graphe.update(time_delta, self.screen, self.current_save.scrollx, self.current_save.scrolly)
            # elif self.current_save is not None:
            #     self.graphe.draw_vehicles(self.screen, self.current_save.scrollx, self.current_save.scrolly)
            
            # Update l'écran
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
                if self.current_save is not None:
                     self.current_save.update_save()
                self.running = False
                exit()
            
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

                    self.check_debut_simulation()
                    continue
                elif btn.is_selected:
                    btn.unselect()
                    continue

            if event.type == pygame.KEYDOWN:
                if self.state_manager.état_courant in [ÉtatJeu.GAME_EDITOR, ÉtatJeu.SIMULATION, ÉtatJeu.SIGNALISATION]:
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
                        self.change_build_orientation(-1)
                    if event.key == pygame.K_q:
                        self.change_build_orientation(1)
                    if event.key == pygame.K_p:
                        self.see_build_preview = not self.see_build_preview
                    if event.key == pygame.K_b:
                        self.debug_view = not self.debug_view
                    if event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                        self.current_save.zoom(1)
                        self.current_save.draw_tuiles(self.screen)
                    if event.key == pygame.K_MINUS:
                        self.current_save.zoom(-1)
                        self.current_save.draw_tuiles(self.screen)
                if event.key == pygame.K_h:
                    if self.state_manager.état_courant == ÉtatJeu.SIMULATION and self.graphe.simulation_finished:
                        self.state_manager.changer_état(ÉtatJeu.GAME_EDITOR)

            if event.type == pygame.KEYUP:
                if self.state_manager.état_courant in [ÉtatJeu.GAME_EDITOR, ÉtatJeu.SIMULATION, ÉtatJeu.SIGNALISATION]:
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

    def change_build_orientation(self, increment: int = 1):
        """
        Cycles through the build orientations in a clockwise manner.

        This function increments the 'build_orientation' attribute by 1 to change
        the orientation of a building. If the orientation exceeds 3, it resets to 0,
        ensuring the orientation remains within the valid range of 0 to 3.
        """
        self.build_orientation += increment
        if self.build_orientation > 3:
            self.build_orientation = 0
        elif self.build_orientation < 0:
            self.build_orientation = 3
    
    def check_debut_simulation(self):
        current_mode = self.mode_selector.get_selected_btn()
        id_mode_actif = int(current_mode.object_ids[-1][-1])
        print(id_mode_actif)
        if id_mode_actif == 3:
            self.window_border.color = self.GREEN
            self.state_manager.changer_état(ÉtatJeu.SIMULATION)