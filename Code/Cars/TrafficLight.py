import pygame

class TrafficLight:
    """
    Représente un feu de circulation dans la simulation, gérant les états vert et rouge,
    ainsi que la possibilité d'agir comme un stop.
    """
    def __init__(self, timer_depart = 0, green_duration=3, red_duration=3, is_stop= False):
        """
        Initialise un feu de circulation.

        :param timer_depart: Temps initial du timer pour désynchroniser les feux.
        :param green_duration: Durée pendant laquelle le feu reste vert.
        :param red_duration: Durée pendant laquelle le feu reste rouge.
        :param is_stop: Booléen indiquant si le feu agit comme un stop.
        """
        self.green_duration = green_duration # Durée d'activation de la lumière verte
        self.red_duration = red_duration # Durée d'activation de la lumière rouge
        self.state = "green"  # état initial
        self.timer = 0.0 + timer_depart # Timer de départ désynchronisé par un incrément aléatoire
        self.is_stop = is_stop # La TrafficLight peut agir comme un stop

        # Chargement des images pour l'affichage visuel des feux verts et rouges
        self.green_image = pygame.image.load("assets/tile_images/traffic_light_green_only.png").convert_alpha()
        self.red_image = pygame.image.load("assets/tile_images/traffic_light_red_only.png").convert_alpha()

    def update(self, dt):
        """
        Met à jour l'état du feu en fonction du temps écoulé.

        :param dt: Temps écoulé depuis la dernière mise à jour (en secondes).

        Cette méthode incrémente le timer interne et change l'état du feu de vert à rouge
        ou de rouge à vert selon les durées spécifiées. Si le feu agit comme un stop,
        il reste toujours rouge.
        """
        self.timer += dt
        if self.is_stop:
            self.state = 'red'
        if self.state == "green" and self.timer >= self.green_duration:
            self.state = "red"
            self.timer = 0.0
        elif self.state == "red" and self.timer >= self.red_duration:
            self.state = "green"
            self.timer = 0.0

    def draw(self, screen, position, scrollx=0, scrolly=0):
        """
        Affiche le feu de circulation à l'écran à la position spécifiée.

        :param screen: Surface Pygame sur laquelle dessiner le feu.
        :param position: Tuple (x, y) indiquant la position centrale du feu sur la carte.
        :param scrollx: Décalage horizontal pour le défilement de la vue.
        :param scrolly: Décalage vertical pour le défilement de la vue.

        Cette méthode dessine l'image correspondant à l'état actuel du feu (vert ou rouge),
        en tenant compte du décalage de la vue pour un affichage correct dans la fenêtre.
        """
        rect = self.green_image.get_rect()
        if not self.is_stop:
            if self.state == "green":
                screen.blit(self.green_image, (position[0] - scrollx- rect.width // 2, position[1]-scrolly- rect.height // 2))
            else:
                screen.blit(self.red_image, (position[0] - scrollx- rect.width // 2, position[1]-scrolly- rect.width // 2))



