import pygame
import math
from .Intersection import Intersection

class Route:
    def __init__(self, start: Intersection, end: Intersection, lane=1, num_lanes=1):
        self.start = start
        self.end = end
        self.length = math.dist(start.position, end.position)
        self.lane = lane  # numéro de la voie (1, 2 ou 3)
        self.num_lanes = num_lanes  # nombre total de voies sur ce segment
        # Calcul de l'offset pour décaler visuellement les voies
        self.offset = (lane - (num_lanes + 1) / 2) * 10 # Offset de -10, 0, ou 10 si nb_total de voies = 3

    def get_offset_positions(self):
        """Retourne les positions de départ et d'arrivée décalées selon l'offset."""
        start_x, start_y = self.start.position
        end_x, end_y = self.end.position
        dx = end_x - start_x
        dy = end_y - start_y
        dist = math.hypot(dx, dy)
        if dist != 0:
            # Vecteur perpendiculaire normalisé
            perp_x = -dy / dist
            perp_y = dx / dist
        else:
            perp_x, perp_y = 0, 0
        offset_x = perp_x * self.offset
        offset_y = perp_y * self.offset
        start_offset = (start_x + offset_x, start_y + offset_y)
        end_offset = (end_x + offset_x, end_y + offset_y)
        return start_offset, end_offset

    def draw(self, screen):
        start_offset, end_offset = self.get_offset_positions()
        pygame.draw.line(screen, (200, 200, 200),
                         (int(start_offset[0]), int(start_offset[1])),
                         (int(end_offset[0]), int(end_offset[1])), 3)
