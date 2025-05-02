"""
Module ModeSelector
Gère l’interface de sélection de mode (construction, signalisation, simulation) pour l’utilisateur.
Permet de changer l’état du jeu et d’adapter dynamiquement la barre d’outils affichée.
"""

import pygame_gui
import pygame

# Classe pour la gestion de l’interface de sélection de mode dans CircuLab
class ModeSelector:
    
    # Dictionnaire des modes avec leur identifiant numérique
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
                
        # Création de la fenêtre flottante contenant les boutons de mode
        self.mode_selector_window = pygame_gui.elements.UIWindow(
            rect=pygame.Rect((self.window_frame.thickness, self.window_frame.thickness), (self.MODE_SELECTOR_WIDTH, self.MODE_SELECTOR_HEIGHT)), 
            object_id="#mode_selector_window", 
            manager=self.manager)
        
        self.mode_selector_container = pygame_gui.elements.UIScrollingContainer(relative_rect=pygame.Rect((0, 0), (self.MODE_SELECTOR_WIDTH, self.MODE_SELECTOR_HEIGHT)), manager=self.manager, container=self.mode_selector_window, object_id="#mode_selector_container", allow_scroll_y=False)
    
        # Création et positionnement des trois boutons de mode
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
        Retourne le bouton actuellement sélectionné.
        """

        for btn in self.mode_selector_btns:
            if  btn.is_selected:
                return btn

    def unselect_all_btns(self):
        """
        Désélectionne tous les boutons du sélecteur de mode.
        """
        for btn in self.mode_selector_btns:
            btn.unselect()
    
    def check_change_mode(self):
        current_mode = self.get_selected_btn()
        try:
            id_bouton_actif = int(current_mode.object_ids[-1][-1])
        except AttributeError:
            id_bouton_actif = 0
            
        # Passage au mode de construction
        if id_bouton_actif == 1 and self.state_manager.état_courant != 2:
            self.window_frame.color = self.BLUE_GREY
            self.tool_bar.set_building_tool_bar()
            self.state_manager.changer_état(2)  # Building
            self.tool_bar.unselect_all_btns()
        # Passage au mode de signalisation
        elif id_bouton_actif == 2 and self.state_manager.état_courant != 7:
            self.window_frame.color = self.YELLOW
            self.tool_bar.set_signalisation_tool_bar()
            self.state_manager.changer_état(7)
            self.tool_bar.unselect_all_btns()
        # Passage au mode simulation
        if id_bouton_actif == 3 and self.state_manager.état_courant != 3:
            self.window_frame.color = self.GREEN
            self.state_manager.changer_état(3)  # Simulation
            self.tool_bar.unselect_all_btns()