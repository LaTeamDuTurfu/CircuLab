import sys
import os
import pygame
import networkx as nx
import random
import matplotlib.pyplot as plt
from PIL.ImageOps import scale

# Permet de charger les modules dans le dossier game_code
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(project_root, "Code"))

from Cars.Intersection import Intersection
from Cars.Route import Route
from Cars.Voiture import Voiture
from Cars.TrafficLight import TrafficLight

class Graphe:
    def __init__(self,TILE_SIZE, nb_voitures = 3, max_lanes=1):
        self.max_lanes = max_lanes
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
        
        # Créer les intersections avec ou sans feux de circulation
        self.intersections = None # Contient les Objets Intersection, utilisés pour créer le graph
        self.inter_points = None # Contient les points où créer des intersections
        self.ordered_points = None # Conserver l'ordre de placement des points

        # Créer les routes (chaque segment sera décliné en plusieurs voies, sens unique)
        self.routes = []

        # Construire le graphe orienté multiple avec networkx
        self.G = nx.MultiDiGraph()

        # Créer les véhicules avec départ et arrivée aléatoires et chemin calculé
        self.voitures = []

        # Vérifier si la simulation est terminée
        self.simulation_finished = False


    def set_current_save(self, partie=None):
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
        scaled_point = (point[0] * self.TILE_SIZE + self.TILE_SIZE // 2, point[1] * self.TILE_SIZE + self.TILE_SIZE // 2)
        return scaled_point

    def build_routes(self):
        seq = self.ordered_points

        for i in range(len(seq) - 1):
            start_pos, end_pos = seq[i], seq[i + 1]

            if start_pos is None or end_pos is None:
                continue  # on saute la coupure

            # S’assure que les Intersection objets existent
            start = self.intersections[start_pos]
            end = self.intersections[end_pos]

            # Crée une arête par voie
            for lane in range(1, self.max_lanes + 1):
                self.routes.append(Route(start, end, lane, self.max_lanes))

    def add_inter_points(self, point):
        """
        Ajoute un point à la liste des points d'intersection.

        :param point: un tuple (x, y) représentant le point à ajouter
        """
        scaled_point = self.scale_point(point)
        self.inter_points[scaled_point] = {'has_light': False} # prend un point scalé comme paramètre, qui est un tuple, et l'ajoute au dict d'inter_points
        self.ordered_points.append(scaled_point)
        print(self.inter_points)
        print(self.ordered_points)

    def remove_inter_point(self, point):
        scaled_point = self.scale_point(point)

        self.inter_points.pop(scaled_point, None)
        if scaled_point in self.ordered_points:
            self.ordered_points.remove(scaled_point)
        self.intersections.pop(scaled_point, None)

        self.routes = [r for r in self.routes if r.start.position != scaled_point and r.end.position != scaled_point]

        if self.G.has_node(scaled_point):
            self.G.remove_node(scaled_point)

    def add_signalisation(self, point, has_light = False,is_stop = False):
        scaled_point = self.scale_point(point)
        if scaled_point not in self.inter_points:
            self.inter_points[scaled_point] = {}

        self.inter_points[scaled_point]['has_light'] = has_light
        self.inter_points[scaled_point]['is_stop'] = is_stop

    def unbind_graph(self):
        self.ordered_points.append(None) # Crée une coupure dans la création des routes

    def build_intersections(self):
        for pos, info in self.inter_points.items():
            has_light = info.get('has_light', False) # info est un dict tel que {'has_light': True, 'is_stop': False}, donc on récupère l'info, si elle existe, sinon fausse
            is_stop = info.get('is_stop', False) # Pareil ici
            self.intersections[pos] = Intersection(pos, has_traffic_light=has_light, is_stop=is_stop)

    def nb_points(self):
        return len(self.inter_points.keys())

    def build_graph(self):
        # Utiliser un MultiDiGraph pour représenter les voies à sens unique
        for pos in self.intersections:
            self.G.add_node(pos)
        for route in self.routes:
            u = route.start.position
            v = route.end.position
            # Chaque voie est une arête avec un poids égal à la distance
            self.G.add_edge(u, v, weight=route.length, route=route)

    def create_vehicles(self, nb):
        positions = list(self.intersections.keys())
        vehicles_created = 0
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

    def update(self, dt, screen, scrollx, scrolly):
        # Mise à jour des intersections (et de leurs feux)
        for pos, inter in self.intersections.items():
            inter.update(dt, screen, scrollx, scrolly)
        # Mise à jour des véhicules
        for v in self.voitures:
            v.update(dt, self.voitures)
            v.draw(screen, scrollx, scrolly)
        pygame.display.flip()
        if all(v.finished for v in self.voitures):
            self.simulation_finished = True

    def draw_vehicles(self, screen, scrollx, scrolly):
        for v in self.voitures:
            v.draw(screen, scrollx, scrolly)

    def show_graph(self):
        pos = {node: node for node in self.G.nodes()}
        plt.figure("Graphe de circulation")
        nx.draw(self.G,
                pos,
                with_labels=False,
                node_size=300,
                arrows=True)
        plt.title("Représentation du Graphe de Circulation")
        plt.show()


