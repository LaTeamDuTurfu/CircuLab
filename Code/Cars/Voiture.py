import math
import random

class Voiture:
    """
    Représente un véhicule dans la simulation, capable de suivre une liste de routes,
    de gérer la vitesse, les arrêts aux stops et feux de circulation, et de se déplacer
    en fonction du temps écoulé.
    """

    def __init__(self, route_list, car_image, speed=100):
        """
        Initialise une instance de Voiture.

        Args:
            route_list (list): Liste des routes (segments) que la voiture doit parcourir.
            car_image (Surface): Image représentant la voiture pour l'affichage.
            speed (int, optional): Vitesse maximale de la voiture. Par défaut à 100.

        Initialise également la position initiale, la vitesse, les timers d'arrêt et les flags d'état.
        """
        self.route_list = route_list # liste de routes à parcourir
        self.position = route_list[0].get_positions()[0] # position initiale du véhicule
        self.current_index = 0  # indice de la route en cours dans route_list
        self.progress = 0.0  # distance parcourue sur la voie actuelle

        self.stop_timer = 0 # Timer pour le temps d'attente au stop
        self.is_waiting_at_stop = False # Flag si le véhicule est à un stop
        self.stop_done = False # Flag pour savoir si le stop et complété
        self.finished = False # Flag pour savoir si la voiture a fini son parcours

        self.speed = speed # Vitesse maximale à atteindre
        self.current_speed = 0 # Vitesse instantanée à un instant donné
        self.acceleration = 70 # valeur arbitraire de l'accélération

        # Position initiale sur la première voie (en tenant compte du décalage)
        self.car_image = car_image # image de la voiture
        self.rect = self.car_image.get_rect(center=(int(self.position[0]), int(self.position[1])))

    def update(self, dt):
        """
        Met à jour la position et l'état de la voiture en fonction du temps écoulé.

        Gère l'accélération, les arrêts aux stops et feux rouges, la progression le long
        des segments de route, et la transition vers le segment suivant.

        Args:
            dt (float): Temps écoulé depuis la dernière mise à jour (en secondes).
        """
        if self.finished:
            return

        if self.current_index >= len(self.route_list):
            self.finished = True
            return

        current_route = self.route_list[self.current_index]
        start_pos, end_pos = current_route.get_positions()
        segment_length = math.dist(start_pos, end_pos)

        # Calcul de la vitesse avec accélération jusqu'à la vitesse maximale
        self.current_speed += self.acceleration * dt
        if self.current_speed > self.speed:
            self.current_speed = self.speed

        distance_to_travel = self.current_speed * dt

        # Arrêt devant un feu rouge ou stop si on est proche de l'intersection de fin
        if current_route.end.traffic_light and (segment_length - self.progress < 64):
            tl = current_route.end.traffic_light
            if tl.is_stop:
                if not self.stop_done:
                    distance_to_travel = 0
                    self.current_speed = 0
                    if not self.is_waiting_at_stop:
                        self.stop_timer = random.uniform(1, 3)
                        self.is_waiting_at_stop = True
            elif tl.state == "red":
                distance_to_travel = 0
                self.current_speed = 0

        # Gestion de l'arrêt au stop avec temporisation
        if self.is_waiting_at_stop:
            self.stop_timer -= dt
            if self.stop_timer <= 0:
                self.is_waiting_at_stop = False
                self.stop_done = True
                distance_to_travel = self.current_speed * dt

        self.progress += distance_to_travel

        # Passage à la route suivante si le segment courant est terminé
        if self.progress >= segment_length:
            self.position = end_pos
            self.current_index += 1
            self.progress = 0.0
            if self.current_index >= len(self.route_list):
                self.finished = True
            else:
                self.stop_done = False # Update pour éviter que la voiture skip un stop
        else:
            # Calcul de la position intermédiaire sur le segment courant
            ratio = self.progress / segment_length
            x = start_pos[0] + (end_pos[0] - start_pos[0]) * ratio
            y = start_pos[1] + (end_pos[1] - start_pos[1]) * ratio
            self.position = (x, y)

        # Mise à jour du rectangle de collision/affichage
        self.rect.center = (int(self.position[0]), int(self.position[1]))


    def draw(self, screen, scrollx=0, scrolly=0):
        """
        Dessine la voiture à l'écran en tenant compte du décalage de la vue.

        Args:
            screen (Surface): Surface sur laquelle dessiner la voiture.
            scrollx (int, optional): Décalage horizontal de la vue. Par défaut à 0.
            scrolly (int, optional): Décalage vertical de la vue. Par défaut à 0.
        """
        screen.blit(self.car_image, (self.rect.x - scrollx,self.rect.y - scrolly))
