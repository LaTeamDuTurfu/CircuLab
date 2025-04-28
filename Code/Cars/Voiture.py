import math
import random

class Voiture:
    def __init__(self, route_list, car_image, speed=100):
        self.route_list = route_list
        self.car_image = car_image
        self.last_min_distance = None
        self.stop_timer = 0
        self.is_waiting_at_stop = False
        self.stop_done = False
        self.speed = speed
        self.current_speed = 0
        self.acceleration = 70 # valeur arbitraire de l'accélération
        self.current_index = 0  # indice de la route en cours dans route_list
        self.progress = 0.0  # distance parcourue sur la voie actuelle
        # Position initiale sur la première voie (en tenant compte du décalage)
        self.position = route_list[0].get_positions()[0]
        self.finished = False
        self.rect = self.car_image.get_rect(center=(int(self.position[0]), int(self.position[1])))

    def update(self, dt, list_voitures):
        if self.finished:
            return

        distance_securite = 64 # distance de sécurité arbitraire, pour éviter les collisions
        min_gap = self.rect.width

        if self.current_index >= len(self.route_list):
            self.finished = True
            return

        current_route = self.route_list[self.current_index]
        start_pos, end_pos = current_route.get_positions()
        segment_length = math.dist(start_pos, end_pos)

        self.current_speed += self.acceleration * dt
        if self.current_speed > self.speed:
            self.current_speed = self.speed

        #TODO CODE POUR ÉVITER LES COLLISIONS NE FONCTIONNE PAS
        for autre in list_voitures:
            if autre is self or autre.finished:
                continue
            dx = autre.position[0] - self.position[0]
            dy = autre.position[1] - self.position[1]
            distance = math.hypot(dx, dy)

            if distance < distance_securite:
                if self.last_min_distance is None:
                    self.last_min_distance = distance

                if distance < self.last_min_distance:
                    factor = (distance - min_gap) / (distance_securite - min_gap)
                    factor = max(0.0, min(1.0, factor))
                    target_speed = self.speed * factor
                    self.current_speed = min(self.current_speed, target_speed)
                else:
                    self.current_speed = min(self.speed, self.current_speed + self.acceleration * dt)

                self.last_min_distance = distance
            else:
                self.last_min_distance = None

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

        # Gestion de l'arrêt au stop
        if self.is_waiting_at_stop:
            self.stop_timer -= dt
            if self.stop_timer <= 0:
                self.is_waiting_at_stop = False
                self.stop_done = True
                distance_to_travel = self.current_speed * dt

        self.progress += distance_to_travel

        if self.progress >= segment_length:
            # Passage à la route suivante
            self.position = end_pos
            self.current_index += 1
            self.progress = 0.0
            if self.current_index >= len(self.route_list):
                self.finished = True
            else:
                self.stop_done = False
        else:
            ratio = self.progress / segment_length
            x = start_pos[0] + (end_pos[0] - start_pos[0]) * ratio
            y = start_pos[1] + (end_pos[1] - start_pos[1]) * ratio
            self.position = (x, y)

        self.rect.center = (int(self.position[0]), int(self.position[1]))


    def draw(self, screen, scrollx=0, scrolly=0):
        screen.blit(self.car_image, (self.rect.x - scrollx,self.rect.y - scrolly))
