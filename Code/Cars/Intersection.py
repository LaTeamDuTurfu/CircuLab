import pygame
from .TrafficLight import TrafficLight

class Intersection:
    def __init__(self, position, has_traffic_light=False):
        self.position = position  # (x, y)
        self.traffic_light = TrafficLight() if has_traffic_light else None

    def update(self, dt, screen, scrollx, scrolly):
        if self.traffic_light:
            self.traffic_light.update(dt)
            self.traffic_light.draw(screen, self.position, scrollx, scrolly)

