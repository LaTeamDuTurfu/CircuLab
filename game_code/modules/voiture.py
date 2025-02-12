
class Voiture:
    def __init__(self, id, position, vitesse=0, acceleration=0, couleur="blue"):
        """
        Initialise une voiture dans la simulation.

        :param id: Identifiant unique de la voiture
        :param position: Position initiale (x, y) sur la carte
        :param vitesse: Vitesse initiale (m/s)
        :param acceleration: Accélération initiale (m/s²)
        :param couleur: Couleur pour l'affichage graphique
        """
        self.id = id
        self.position = position  # Tuple (x, y)
        self.vitesse = vitesse
        self.acceleration = acceleration
        self.couleur = couleur
        self.direction = (1, 0)  # Par défaut, la voiture avance vers la droite (x+)

    def avancer(self, delta_t):
        """
        Met à jour la position de la voiture en fonction de la vitesse et de l'accélération.
        """
        self.vitesse += self.acceleration * delta_t
        dx = self.vitesse * delta_t * self.direction[0]
        dy = self.vitesse * delta_t * self.direction[1]
        self.position = (self.position[0] + dx, self.position[1] + dy)

    def arreter(self):
        """ Force la voiture à s'arrêter immédiatement. """
        self.vitesse = 0
        self.acceleration = 0

    def reagir_au_feu(self, couleur_feu):
        """
        Gère le comportement de la voiture selon la couleur du feu de circulation.
        """
        if couleur_feu == "rouge":
            self.arreter()
        elif couleur_feu == "vert":
            self.acceleration = 1.5  

    def recevoir_instruction(self, instruction):
        """
        Permet à un algorithme externe d'envoyer une instruction (ex: optimisation des feux).
        """
        if instruction == "ralentir": 
            self.acceleration = -1
        elif instruction == "accélérer":
            self.acceleration = 2

    def __repr__(self):
        return f"Voiture {self.id} - Position: {self.position}, Vitesse: {self.vitesse} m/s"