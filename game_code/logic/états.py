class ÉtatJeu:
    HOME_PAGE = 1
    GAME_EDITOR = 2
    SIMULATION = 3
    SETTINGS = 4
    MORT = 5

    def __init__(self):
        self.état_courant: int = self.DÉBUT

    def changer_état(self, nouvel_état: int):
        """
        Permet de gérer et protéger les transitions d'état
        """
        if nouvel_état == self.DÉBUT and (self.état_courant not in [self.VICTOIRE, self.MORT]):
            raise ValueError("Impossible de revenir au début sauf après être mort")
        elif nouvel_état == self.JEU and self.état_courant in [self.JEU, self.VICTOIRE, self.MORT]:
            raise ValueError("Impossible de reprendre le jeu")
        elif nouvel_état == self.PAUSE and self.état_courant != self.JEU:  # in [self.DÉBUT, self.PAUSE,
            # self.VICTOIRE, self.MORT]:
            raise ValueError("Impossible de faire pause le jeu")
        elif nouvel_état == self.VICTOIRE and self.état_courant != self.JEU:
            raise ValueError("Impossible de passer en mode victoire sauf quand on est en jeu.")
        elif nouvel_état == self.MORT and self.état_courant != self.JEU:
            raise ValueError("Impossible de passer en mode défaite sauf quand on est en jeu.")

        print(f"État passe de {self.état_courant} à {nouvel_état}")
        self.état_courant = nouvel_état
