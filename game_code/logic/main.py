import sys
import os
import pygame
import pygame_gui

# Permet de charger les modules dans le dossier game_code
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(project_root, "game_code"))

from modules import Tuile
from modules import NewSaveWindow

class Circulab():
    def __init__(self, height: int = 720, width: int = 1280):
        # Setup Window
        pygame.init()
        pygame.display.set_caption('CircuLab')

        # Load Images
        self.logo = pygame.image.load("assets/other/logo.png")

        # Load tiles images
        self.empty_tile = pygame.image.load("assets/tile_images/none.png")
        self.black_tile = pygame.image.load("assets/tile_images/black.png")
        self.blue_tile = pygame.image.load("assets/tile_images/blue.png")
        self.green_tile = pygame.image.load("assets/tile_images/green.png")
        self.pink_tile = pygame.image.load("assets/tile_images/pink.png")
        self.red_tile = pygame.image.load("assets/tile_images/red.png")
        self.orange_tile = pygame.image.load("assets/tile_images/orange.png")
        self.yellow_tile = pygame.image.load("assets/tile_images/yellow.png")
        self.white_tile = pygame.image.load("assets/tile_images/white_A.png")
        self.tile_images = [self.empty_tile, self.black_tile, self.blue_tile, self.green_tile, self.pink_tile, self.red_tile, self.orange_tile, self.yellow_tile, self.white_tile]

        # Load Fonts
        self.font = pygame.font.Font("freesansbold.ttf", 32)

        # Color palette
        self.BLACK = "#040f0f"
        self.DARK_GREEN = "#248232"
        self.GREEN = "#2ba84a"
        self.GREY = "#2d3a3a"
        self.WHITE = "#fcfffc"
        self.BLUE_GREY = "#77a6b6"

        # Taille de la fenêtre
        self.HEIGHT = height
        self.WIDTH = width
        self.TOOL_BAR_HEIGHT = self.HEIGHT * 1/8
        self.TOOL_BAR_WIDTH = self.WIDTH * 3/4
        self.TOOL_BAR_BTN_SIZE = 78
        
        # Transform Images
        self.logo = pygame.transform.scale(self.logo, (self.WIDTH - self.TOOL_BAR_WIDTH, self.TOOL_BAR_HEIGHT + 10))

        # Surface de la fenêtre
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        # GUI Manager
        self.manager = pygame_gui.UIManager((self.WIDTH, self.HEIGHT), theme_path="data/theme_manager/styles_real.json")

        # Dessiner les éléments du GUI
        self.tool_bar_btns = pygame.sprite.Group()
        self.draw_top_UI()
        self.draw_button_tool_bar()
        self.new_save_window = NewSaveWindow(
            rect=pygame.Rect((self.WIDTH/4, self.HEIGHT/6), (self.WIDTH/2, self.HEIGHT * 2/3)),
            manager=self.manager,
            default_path="../Circulab/data/saves/"
            )

        # Horloge (pour les FPS)
        self.clock = pygame.time.Clock()

        # Variable de jeu
        self.ROWS = 150
        self.COLUMNS = 150
        self.TILE_SIZE = 50
        self.scrollx = (self.COLUMNS * self.TILE_SIZE) / 2  # Set le scroll x au milieu
        self.scrolly = (self.ROWS * self.TILE_SIZE) / 2  # Set le scroll y au milieu
        self.scroll_speed = 1
        self.vertical_scroll = 0
        self.horizontal_scroll = 0
        self.build_orientation = 0
        self.see_build_preview = False
        self.running = True

        # Position de la souris
        self.pos = [0, 0]
        self.x_pos = self.pos[0]
        self.y_pos = self.pos[1]

        # Data
        self.tuiles = pygame.sprite.Group()
        self.world_data = []
        for _ in range(self.ROWS):
            new_tile = [Tuile(self.TILE_SIZE, self.empty_tile, sprite_group=self.tuiles, orientation=self.build_orientation)] * self.COLUMNS
            self.world_data.append(new_tile)

    
    def run(self):
        while self.running:
            # FPS Capping
            time_delta = self.clock.tick(60)/1000

            # Logic
            self.get_mouse_pos()
            self.change_scroll()
            self.traiter_inputs()

            # Remplit le fond de couleur verte
            self.screen.fill(self.GREY)

            # Dessine les tuiles
            self.change_tuiles()
            self.draw_tuiles()            

            # Dessine la grille
            self.draw_grid()    

            # Dessine les éléments du GUI
            if self.see_build_preview:
                pygame.draw.rect(self.screen, self.BLUE_GREY, (self.x_pos * self.TILE_SIZE - self.scrollx, self.y_pos * self.TILE_SIZE - self.scrolly, self.TILE_SIZE, self.TILE_SIZE))
                self.draw_text(f"X: {int(self.x_pos)} | Y: {int(self.y_pos)}", self.font, self.WHITE, self.pos[0], self.pos[1]-self.TILE_SIZE/2) 

            # Affiche le logo
            self.screen.blit(self.logo, (0, 0))    

            # Update l'écran
            self.manager.update(time_delta)
            self.manager.draw_ui(self.screen)
            pygame.display.flip()
    
        pygame.quit()
    
    def draw_tuiles(self):
        """
        Dessine les tuiles sur l'écran, en fonction de la
        position actuelle du scroll.
        """
        for y, row in enumerate(self.world_data):
                for x, tile in enumerate(row):
                    if tile.image != self.empty_tile:
                        tile.rect = pygame.Rect(x * self.TILE_SIZE - self.scrollx, y * self.TILE_SIZE - self.scrolly, self.TILE_SIZE, self.TILE_SIZE)
                        tile.draw(self.screen)

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
            
            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element in self.tool_bar_btns:
                btn = event.ui_element
                if not btn.is_selected:
                    self.unselect_all_btns()
                    btn.select()
                    continue
                elif btn.is_selected:
                    btn.unselect()
                    continue

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.horizontal_scroll = -1
                if event.key == pygame.K_RIGHT:
                    self.horizontal_scroll = 1
                if event.key == pygame.K_UP:
                    self.vertical_scroll = -1
                if event.key == pygame.K_DOWN:
                    self.vertical_scroll = 1
                if event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
                    self.scroll_speed = 5
                if event.key == pygame.K_r:
                    self.change_build_orientation()
                if event.key == pygame.K_p:
                    self.see_build_preview = not self.see_build_preview

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.horizontal_scroll = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    self.vertical_scroll = 0
                if event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
                    self.scroll_speed = 1

            self.manager.process_events(event)

    def change_scroll(self):
        #scroll la grip
        if self.horizontal_scroll == 1 and self.scrollx < (self.COLUMNS * self.TILE_SIZE) - self.WIDTH:
            self.scrollx += 5 * self.scroll_speed
        elif self.horizontal_scroll == -1 and self.scrollx > 0:
            self.scrollx -= 5 * self.scroll_speed
        
        if self.vertical_scroll == 1 and self.scrolly < (self.ROWS * self.TILE_SIZE) - self.HEIGHT:  # Descend l'écran
            self.scrolly += 5 * self.scroll_speed
        elif self.vertical_scroll == -1 and self.scrolly > 0:  # Monte l'écran
            self.scrolly -= 5 * self.scroll_speed

    def draw_top_UI(self):
        self.tool_bar_window = pygame_gui.elements.UIWindow(
            rect=pygame.Rect((self.WIDTH - self.TOOL_BAR_WIDTH, 0), (self.TOOL_BAR_WIDTH, self.TOOL_BAR_HEIGHT)), 
            object_id="#tool_bar_window", 
            manager=self.manager)
        
        self.tool_bar_container = pygame_gui.elements.UIScrollingContainer(relative_rect=pygame.Rect((0, 0), (self.TOOL_BAR_WIDTH, self.TOOL_BAR_HEIGHT)), 
                                                                           manager=self.manager, 
                                                                           container=self.tool_bar_window, 
                                                                           object_id="#tool_bar_container",
                                                                           allow_scroll_y=True)
    
    def draw_button_tool_bar(self):
        for i in range(8):
            new_btn = pygame_gui.elements.UIButton(
                        relative_rect=pygame.Rect(((3/2 * i * self.TOOL_BAR_BTN_SIZE) + self.TOOL_BAR_BTN_SIZE/2 , 0), (self.TOOL_BAR_BTN_SIZE, self.TOOL_BAR_BTN_SIZE)),
                        text="",
                        manager=self.manager,
                        anchors={"centery": "centery"},
                        container=self.tool_bar_container,
                        object_id=pygame_gui.core.ObjectID(class_id="@tool_tip_btn", object_id=f"#tool_tip_btn_{i + 1}"))

            self.tool_bar_btns.add(new_btn)
    
    def draw_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        img_rect = img.get_rect()
        img_rect.center = (x, y)
        self.screen.blit(img, img_rect)

    def unselect_all_btns(self):
        for btn in self.tool_bar_btns:
            btn.unselect()

    def draw_grid(self):
        for c in range(self.COLUMNS + 1):
            pygame.draw.line(self.screen, self.WHITE, (c * self.TILE_SIZE - self.scrollx, 0), (c * self.TILE_SIZE - self.scrollx, self.HEIGHT))
        for c in range(self.ROWS + 1):
            pygame.draw.line(self.screen, self.WHITE, (0, c * self.TILE_SIZE - self.scrolly), (self.WIDTH, c * self.TILE_SIZE - self.scrolly))

    def get_mouse_pos(self):
        #get mouse position
        self.pos = pygame.mouse.get_pos()
        self.x_pos = (self.pos[0] + self.scrollx) // self.TILE_SIZE
        self.y_pos = (self.pos[1] + self.scrolly) // self.TILE_SIZE

    def get_selected_btn(self):
        for btn in self.tool_bar_btns:
            if  btn.is_selected:
                return btn

    def change_build_orientation(self):
        self.build_orientation += 1
        if self.build_orientation > 3:
            self.build_orientation = 0

    def change_tuiles(self):
        if self.pos[0] < self.WIDTH and self.TOOL_BAR_HEIGHT < self.pos[1] < self.HEIGHT:
            self.y_pos = int(self.y_pos)
            self.x_pos = int(self.x_pos)
            try:
                bouton_actif = self.get_selected_btn()
                id_bouton_actif = bouton_actif.object_ids[-1]
            except AttributeError:
                pass
            if pygame.mouse.get_pressed()[0] == 1:
                try:
                    if self.world_data[self.y_pos][self.x_pos].image != self.tile_images[int(id_bouton_actif[-1])]:
                        self.world_data[self.y_pos][self.x_pos] = Tuile(self.TILE_SIZE, self.tile_images[int(id_bouton_actif[-1])], sprite_group=self.tuiles, orientation=self.build_orientation)
                except UnboundLocalError:
                    pass
            if pygame.mouse.get_pressed()[2] == 1:
                self.world_data[self.y_pos][self.x_pos] = Tuile(self.TILE_SIZE, self.empty_tile, sprite_group=self.tuiles, orientation=self.build_orientation)