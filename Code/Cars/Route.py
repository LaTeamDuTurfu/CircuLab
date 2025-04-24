import math
from .Intersection import Intersection

class Route:
    def __init__(self, start: Intersection, end: Intersection, lane=1, num_lanes=1):
        self.start = start
        self.end = end
        self.length = math.dist(start.position, end.position)
        self.lane = lane  # numéro de la voie (1, 2 ou 3)
        self.num_lanes = num_lanes  # nombre total de voies sur ce segment

    def get_positions(self):
        return self.start.position, self.end.position


