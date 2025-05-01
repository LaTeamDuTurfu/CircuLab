from .TrafficLight import TrafficLight
import random

class Intersection:
    """
    Représente une intersection dans la simulation de trafic, et un sommet dans le graphe.
    Elle peut être équipée d'un feu de circulation ou d'un panneau stop.
    """

    def __init__(self, position, has_traffic_light=False, is_stop=False):
        """
        Initialise une intersection.

        :param position: tuple (x, y) indiquant la position de l'intersection.
        :param has_traffic_light: bool indiquant si l'intersection possède un feu de circulation.
        :param is_stop: bool indiquant si l'intersection possède un panneau stop.

        Selon les paramètres, initialise un feu de circulation avec un timer aléatoire ou un panneau stop.
        """
        self.position = position  # (x, y)
        self.traffic_light = None
        if is_stop:
            self.traffic_light = TrafficLight(is_stop=True)
        elif has_traffic_light:
            self.traffic_light = TrafficLight(timer_depart=random.uniform(0, 3))

    def update(self, dt, screen, scrollx, scrolly):
        """
        Met à jour l'état du feu de circulation ou du panneau stop et l'affiche.

        :param dt: float, temps écoulé depuis la dernière mise à jour.
        :param screen: surface sur laquelle dessiner.
        :param scrollx: décalage horizontal de la vue.
        :param scrolly: décalage vertical de la vue.
        """
        if self.traffic_light:
            self.traffic_light.update(dt)
            self.traffic_light.draw(screen, self.position, scrollx, scrolly)
