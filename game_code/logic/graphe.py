import sys
import os
import pygame
import networkx as nx
import random


# Permet de charger les modules dans le dossier game_code
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(project_root, "game_code"))

from modules import Voiture, Intersection, TrafficLight, Route

class Graphe:
    def __init__(self, current_save, nb_voitures = 3, max_lanes=3):
        """
        Building_data = [
            [Tuile, Tuile, Tuile],
            [Tuile, Tuile, Tuile],
            [Tuile, Tuile, Tuile]
        ]

        Tuile -->
        self.image = image
        self.tile_type = tile_type --> @empty, @road
        self.orientation = orientation --> 0, 1, 2, 3
        self.rect = image.get_rect() --> width, height, x, y
        """
        self.current_save = current_save
        self.name = current_save.name
        self.building_data = current_save.building_data
        self.tile_size = current_save.TILE_SIZE
        self.scrollx = current_save.scrollx
        self.scrolly = current_save.scrolly
        self.max_lanes = max_lanes

        # Charger l'image de voiture ; si le fichier n'existe pas, utiliser un rectangle rouge
        try:
            car_image_raw = pygame.image.load("car.png").convert_alpha()
            self.car_image = pygame.transform.scale(car_image_raw, (80, 80))
        except Exception as e:
            print("Erreur lors du chargement de 'car.png':", e)
            self.car_image = pygame.Surface((40, 20))
            self.car_image.fill((255, 0, 0))

        # Créer les intersections avec ou sans feux de circulation
        self.intersections = {} #contient les Objets Intersection, utilisés pour créer le graph
        self.inter_points = {} #contient les points où créer des intersections
        self.build_intersections()

        # Créer les routes (chaque segment sera décliné en plusieurs voies, sens unique)
        self.routes = []
        self.build_routes()

        # Construire le graphe orienté multiple avec networkx
        self.G = nx.MultiDiGraph()
        self.build_graph()

        # Créer les véhicules avec départ et arrivée aléatoires et chemin calculé
        self.voitures = []
        self.create_vehicles(nb_voitures)

    def add_inter_points(self, point):
        self.inter_points[point] = False #prend un point comme paramètre, qui est un tuple, et l'ajoute au dict d'inter_points

    def build_intersections(self):
        for pos, has_light in self.inter_points.items():
            self.intersections[pos] = Intersection(pos, has_traffic_light=has_light)

    def build_routes(self):
        # sens unique : de chaque point vers le suivant
        for i in range(len(self.inter_points)):
            start = self.intersections[self.inter_points[i]]
            end = self.intersections[self.inter_points[(i + 1) % len(self.inter_points)]]
            for lane in range(1, self.max_lanes + 1):  # Ajoute les différentes voies entre chaque intersection
                self.routes.append(Route(start, end, lane, self.max_lanes))

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
        for _ in range(nb):
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
                # Chaque edge a un attribut 'route'
                available_routes = [edges[key]['route'] for key in edges]
                chosen_route = random.choice(available_routes)
                route_list.append(chosen_route)
            if route_list:
                print("Chemin (nœuds):", path_nodes, "-> Voies choisies:",
                      [f"{r.start.position}->{r.end.position} (voie {r.lane})" for r in route_list])
                self.voitures.append(Voiture(route_list, self.car_image))

    def update(self, dt):
        # Mise à jour des intersections (et de leurs feux)
        for inter in self.intersections.values():
            inter.update(dt)
        # Mise à jour des véhicules
        for v in self.voitures:
            v.update(dt)

