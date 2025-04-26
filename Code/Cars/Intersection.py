from .TrafficLight import TrafficLight
import random

class Intersection:
    def __init__(self, position, has_traffic_light=False, is_stop=False):
        self.position = position  # (x, y)
        self.traffic_light = None
        if is_stop:
            self.traffic_light = TrafficLight(is_stop=True)
        elif has_traffic_light:
            self.traffic_light = TrafficLight(timer_depart=random.uniform(0, 3))

    def update(self, dt, screen, scrollx, scrolly):
        if self.traffic_light:
            self.traffic_light.update(dt)
            self.traffic_light.draw(screen, self.position, scrollx, scrolly)

