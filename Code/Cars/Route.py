import math
from .Intersection import Intersection

class Route:
    """
    Représente une route entre deux intersections dans un graphe de circulation.
    Cette classe modélise une connexion entre deux points avec une longueur calculée.
    """
    def __init__(self, start: Intersection, end: Intersection):
        """
        Initialise une route entre deux intersections.

        :param start: L'intersection de départ de la route.
        :param end: L'intersection d'arrivée de la route.
        La longueur est calculée comme la distance euclidienne entre les positions des intersections.
        """
        self.start = start  # Intersection de départ de la route
        self.end = end      # Intersection d'arrivée de la route
        self.length = math.dist(start.position, end.position)  # Longueur de la route calculée

    def get_positions(self):
        return self.start.position, self.end.position

