import math

class Voiture:
    def __init__(self, route_list, car_image, speed=1000):
        """
        route_list : liste d'objets Route formant le trajet à suivre (dans l'ordre)
        car_image  : image ou surface représentant la voiture
        """
        self.route_list = route_list
        self.car_image = car_image
        self.speed = speed
        self.current_index = 0  # indice de la route en cours dans route_list
        self.progress = 0.0  # distance parcourue sur la voie actuelle
        # Position initiale sur la première voie (en tenant compte du décalage)
        self.position = route_list[0].get_positions()[0]
        self.finished = False
        self.rect = self.car_image.get_rect(center=(int(self.position[0]), int(self.position[1])))

    def update(self, dt):
        if self.finished:
            return

        if self.current_index >= len(self.route_list):
            self.finished = True
            return

        current_route = self.route_list[self.current_index]
        start_pos, end_pos = current_route.get_positions()
        segment_length = math.dist(start_pos, end_pos)
        distance_to_travel = self.speed * dt

        # Arrêt devant un feu rouge si on est proche de l'intersection de fin
        if current_route.end.traffic_light and (segment_length - self.progress < 20): #Le paramètre 20 ici sert à arrêter le véhicule si celui-ci est à une distance inférieure à 20m de la lumière.
            if current_route.end.traffic_light.state == "red":
                distance_to_travel = 0

        self.progress += distance_to_travel

        if self.progress >= segment_length:
            # Passage à la route suivante
            self.position = end_pos
            self.current_index += 1
            self.progress = 0.0
            if self.current_index >= len(self.route_list):
                self.finished = True
        else:
            ratio = self.progress / segment_length
            x = start_pos[0] + (end_pos[0] - start_pos[0]) * ratio
            y = start_pos[1] + (end_pos[1] - start_pos[1]) * ratio
            self.position = (x, y)

        self.rect.center = (int(self.position[0]), int(self.position[1]))


    def draw(self, screen, scrollx=0, scrolly=0):
        screen.blit(self.car_image, (self.rect.x - scrollx,self.rect.y - scrolly))
