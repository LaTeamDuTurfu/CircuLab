import sys
import os
import pygame
import networkx as nx
import random
import matplotlib.pyplot as plt

# Permet de charger les modules dans le dossier game_code
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(project_root, "Code"))

from Cars.Intersection import Intersection
from Cars.Route import Route
from Cars.Voiture import Voiture
from Cars.TrafficLight import TrafficLight

class Graphe:
    """
    Classe représentant un graphe de circulation routière.

    Cette classe gère les intersections, les routes, les véhicules, ainsi que la simulation
    du trafic sur un réseau routier modélisé par un graphe orienté multiple. Elle intègre
    la gestion des feux de circulation, la création de véhicules avec des itinéraires
    calculés, et la visualisation du graphe.
    """
    def __init__(self,TILE_SIZE):
        """
        Initialise un objet Graphe.

        :param TILE_SIZE: Taille d'une tuile pour le calcul des positions à l'écran.
        """
        self.TILE_SIZE = TILE_SIZE

        # Charger l'image de voiture ; si le fichier n'existe pas, utiliser un rectangle rouge
        try:
            car_image_raw = pygame.image.load("assets/cars/car1.png").convert_alpha()
            self.car_image = pygame.transform.scale(car_image_raw, (80, 80))
        except Exception as e:
            print("Erreur lors du chargement de 'car.png':", e)
            self.car_image = pygame.Surface((40, 20))
            self.car_image.fill((255, 0, 0))

        self.current_save = None

        # Attributs pour la gestion des intersections et points d'intersection
        self.intersections = None  # Dictionnaire des objets Intersection, clé = position (tuple)
        self.inter_points = None   # Dictionnaire des points où créer des intersections avec leurs propriétés
        self.ordered_points = None # Liste ordonnée des points pour la création des routes

        # Liste des routes (segments routiers) du graphe
        self.routes = []

        # Graphe orienté multiple représentant les voies à sens unique
        self.G = nx.MultiDiGraph()

        # Liste des véhicules présents dans la simulation
        self.voitures = []

        # Indicateur si la simulation est terminée
        self.simulation_finished = False

    def set_current_save(self, partie=None):
        """
        Définit la sauvegarde courante et initialise les intersections et points associés.

        :param partie: Objet de sauvegarde contenant les données des intersections et points.
        """
        self.current_save = partie

        if self.current_save != None:
            self.intersections = self.current_save.intersections # Contient les Objets Intersection, utilisés pour créer le graph
            self.inter_points = self.current_save.inter_points # Contient les points où créer des intersections
            self.ordered_points = self.current_save.ordered_points # Conserver l'ordre de placement des points
        else:
            self.intersections = None
            self.inter_points = None
            self.ordered_points = None

    def scale_point(self, point):
        """
        Convertit un point de coordonnées en indices de grille vers des coordonnées pixel.

        :param point: Tuple (x, y) représentant la position en indices de grille.
        :return: Tuple (x_pixel, y_pixel) position centrée dans la tuile.
        """
        scaled_point = (point[0] * self.TILE_SIZE + self.TILE_SIZE // 2, point[1] * self.TILE_SIZE + self.TILE_SIZE // 2)
        return scaled_point

    def nb_points(self):
        """
        Retourne le nombre de points d'intersection.

        :return: Entier nombre de points d'intersection.
        """
        return len(self.inter_points.keys())

    def unbind_graph(self):
        """
        Ajoute une coupure dans la liste ordonnée des points pour séparer les routes.
        """
        self.ordered_points.append(None)

    def add_inter_points(self, point):
        """
        Ajoute un point à la liste des points d'intersection.

        :param point: un tuple (x, y) représentant le point à ajouter
        """
        scaled_point = self.scale_point(point)
        self.inter_points[scaled_point] = {'has_light': False} # prend un point scalé comme paramètre, qui est un tuple, et l'ajoute au dict d'inter_points
        self.ordered_points.append(scaled_point)


    def remove_inter_point(self, point):
        """
        Supprime un point d'intersection et ses routes associées.

        :param point: Tuple (x, y) représentant le point à supprimer.
        """
        scaled_point = self.scale_point(point)

        self.inter_points.pop(scaled_point, None)
        if scaled_point in self.ordered_points:
            self.ordered_points.remove(scaled_point)
        self.intersections.pop(scaled_point, None)

        # Supprimer les routes qui commencent ou finissent à ce point
        self.routes = [r for r in self.routes if r.start.position != scaled_point and r.end.position != scaled_point]

        if self.G.has_node(scaled_point):
            self.G.remove_node(scaled_point)

    def add_signalisation(self, point, has_light = False,is_stop = False):
        """
        Ajoute ou met à jour la signalisation à un point d'intersection.

        :param point: Tuple (x, y) représentant le point d'intersection.
        :param has_light: Booléen indiquant la présence d'un feu de circulation.
        :param is_stop: Booléen indiquant la présence d'un panneau stop.
        """
        scaled_point = self.scale_point(point)
        if scaled_point not in self.inter_points:
            self.inter_points[scaled_point] = {}

        self.inter_points[scaled_point]['has_light'] = has_light
        self.inter_points[scaled_point]['is_stop'] = is_stop

    def build_routes(self):
        """
        Construit la liste des routes entre les points ordonnés, en ignorant les coupures.
        """
        seq = self.ordered_points

        # Parcours séquentiel des points pour créer des routes entre points consécutifs valides
        for i in range(len(seq) - 1):
            start_pos, end_pos = seq[i], seq[i + 1]

            if start_pos is None or end_pos is None:
                continue  # coupure volontaire
            if start_pos not in self.intersections or end_pos not in self.intersections:
                continue  # intersection supprimée

            # S’assure que les objets Intersection existent
            start = self.intersections[start_pos]
            end = self.intersections[end_pos]
            self.routes.append(Route(start, end))

    def build_intersections(self):
        """
        Crée les objets Intersection à partir des points d'intersection avec leurs propriétés.
        """
        for pos, info in self.inter_points.items():
            has_light = info.get('has_light', False) # info est un dict tel que {'has_light': True, 'is_stop': False}, donc on récupère l'info, si elle existe, sinon fausse
            is_stop = info.get('is_stop', False) # Pareil ici
            self.intersections[pos] = Intersection(pos, has_traffic_light=has_light, is_stop=is_stop)

    def build_graph(self):
        """
        Construit le graphe orienté multiple à partir des intersections et routes.
        """
        # Utiliser un MultiDiGraph pour représenter les voies à sens unique
        for pos in self.intersections:
            self.G.add_node(pos)
        for route in self.routes:
            u = route.start.position
            v = route.end.position
            # Chaque voie est une arête avec un poids égal à la distance
            self.G.add_edge(u, v, weight=route.length, route=route)

    def create_vehicles(self, nb):
        """
        Crée un nombre donné de véhicules avec des itinéraires calculés aléatoirement.

        :param nb: Nombre de véhicules à créer.
        """
        positions = list(self.intersections.keys())
        vehicles_created = 0
        # Créer des véhicules avec départ et arrivée aléatoires, et calculer leur chemin
        while vehicles_created < nb:
            dep = random.choice(positions)
            arr = random.choice(positions)
            while arr == dep:
                arr = random.choice(positions)
            try:
                # Calcul du chemin le plus court en terme de distance
                path_nodes = nx.shortest_path(self.G, source=dep, target=arr, weight='weight')
            except nx.NetworkXNoPath:
                continue

            # Pour chaque segment du chemin, choisir aléatoirement l'une des voies disponibles
            route_list = []
            for i in range(len(path_nodes) - 1):
                u = path_nodes[i]
                v = path_nodes[i + 1]
                # Récupérer toutes les voies de u vers v
                edges = self.G.get_edge_data(u, v)
                if edges is None:
                    continue
                available_routes = [edges[key]['route'] for key in edges]
                chosen_route = random.choice(available_routes)
                route_list.append(chosen_route)
            if route_list:
                self.voitures.append(Voiture(route_list, self.car_image))
                vehicles_created += 1

    def reset_simulation(self):
        """
        Réinitialise la simulation en vidant les véhicules, routes et le graphe.
        """
        self.voitures.clear()
        self.routes.clear()
        self.G.clear()
        if self.intersections:
            self.intersections.clear()
        self.simulation_finished = False

    def update(self, dt, screen, scrollx, scrolly):
        """
        Met à jour l'état des intersections et véhicules, puis affiche la simulation.

        :param dt: Variation de temps servant à la mise à jour de la simulation.
        :param screen: Surface Pygame sur laquelle dessiner.
        :param scrollx: Décalage horizontal pour le rendu.
        :param scrolly: Décalage vertical pour le rendu.
        """
        # Mise à jour des intersections (et de leurs feux)
        for pos, inter in self.intersections.items():
            inter.update(dt, screen, scrollx, scrolly)
        # Mise à jour des véhicules
        for v in self.voitures:
            v.update(dt)
            v.draw(screen, scrollx, scrolly)
        pygame.display.flip()
        # Vérifie si tous les véhicules ont terminé leur trajet
        if all(v.finished for v in self.voitures):
            self.simulation_finished = True

    def show_graph(self):
        """
        Affiche une représentation visuelle du graphe de circulation à l'aide de matplotlib.
        """
        pos = {node: node for node in self.G.nodes()}
        plt.figure("Graphe de circulation")
        nx.draw(self.G,pos,with_labels=False,node_size=300,arrows=True)
        plt.title("Représentation du Graphe de Circulation")
        plt.show()
