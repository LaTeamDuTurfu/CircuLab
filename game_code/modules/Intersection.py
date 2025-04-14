import pygame
from .TrafficLight import TrafficLight

class Intersection:
    def __init__(self, position, has_traffic_light=False):
        self.position = position  # (x, y)
        self.traffic_light = TrafficLight() if has_traffic_light else None

    def update(self, dt):
        if self.traffic_light:
            self.traffic_light.update(dt)

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), self.position, 5)
        if self.traffic_light:
            self.traffic_light.draw(screen, self.position)