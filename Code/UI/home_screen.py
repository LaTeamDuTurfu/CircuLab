import pygame
import pygame_gui

class HomeScreen:
    def __init__(self, surface, manager, state_manager, config_manager):
        self.surface = surface
        self.manager = manager
        self.state_manager = state_manager
        self.config_manager = config_manager
        
        self.WIDTH = surface.get_width()
        self.HEIGHT = surface.get_height()
        
        self.BTN_HEIGHT = self.HEIGHT * 1/8

        self.new_save_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0, -self.BTN_HEIGHT/2), (self.WIDTH * 1/2, self.BTN_HEIGHT)),
            text="Nouvelle Sauvegarde",
            manager=self.manager,
            anchors={"centerx": "centerx", "centery": "centery"},
            object_id=pygame_gui.core.ObjectID(class_id="@home_btn", object_id=f"#new_save_btn"),
            command=self.créer_nouvelle_sauvegarde
        )
        
        self.load_save_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0, self.new_save_btn.relative_rect.height + self.new_save_btn.relative_rect.y), (self.WIDTH * 1/2, self.BTN_HEIGHT)),
            text="Charger une Sauvegarde",
            manager=self.manager,
            anchors={"centerx": "centerx", "centery": "centery"},
            object_id=pygame_gui.core.ObjectID(class_id="@home_btn", object_id=f"#load_save_btn"),
            command=self.charger_sauvegarde
        )
        
        self.settings_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0, self.load_save_btn.relative_rect.height + self.load_save_btn.relative_rect.y), (self.WIDTH * 1/2, self.BTN_HEIGHT)),
            text="Paramètres",
            manager=self.manager,
            anchors={"centerx": "centerx", "centery": "centery"},
            object_id=pygame_gui.core.ObjectID(class_id="@home_btn", object_id=f"#settings_btn")
        )
        
        self.quit_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0, self.settings_btn.relative_rect.height + self.settings_btn.relative_rect.y), (self.WIDTH * 1/2, self.BTN_HEIGHT)),
            text="Quitter",
            manager=self.manager,
            anchors={"centerx": "centerx", "centery": "centery"},
            object_id=pygame_gui.core.ObjectID(class_id="@home_btn", object_id=f"#quit_btn"),
            command=self.quit_circulab # Placeholder for quit functionality
        )

    def créer_nouvelle_sauvegarde(self):
        self.state_manager.changer_état(5)  # État.NEW_GAME = 5
        self.cacher_boutons()
    
    def charger_sauvegarde(self):
        self.state_manager.changer_état(6)  # État.LOAD_GAME = 6
        self.cacher_boutons()
    
    def quit_circulab(self):
        self.config_manager.save_config()
        exit()
    
    def cacher_boutons(self):
        self.new_save_btn.hide()
        self.load_save_btn.hide()
        self.settings_btn.hide()
        self.quit_btn.hide()
    
    def montrer_boutons(self):
        self.new_save_btn.show()
        self.load_save_btn.show()
        self.settings_btn.show()
        self.quit_btn.show()
    