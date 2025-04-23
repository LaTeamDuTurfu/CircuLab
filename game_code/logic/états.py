class ÉtatJeu:
    HOME_PAGE = 1
    GAME_EDITOR = 2
    SIMULATION = 3
    SETTINGS = 4
    NEW_GAME = 5
    LOAD_GAME = 6
    SIGNALISATION = 7

    def __init__(self, initial=HOME_PAGE):
        self.état_courant: int = initial
        print(f"État de départ: {self.état_courant}")

    def changer_état(self, nouvel_état: int):
        """
        Permet de gérer et protéger les transitions d'état
        """
        if nouvel_état == self.GAME_EDITOR and (self.état_courant not in [self.NEW_GAME, self.LOAD_GAME, self.SIMULATION, self.SIGNALISATION]):
            raise ValueError("Impossible de partir la game sans save file.")
        elif nouvel_état == self.SIMULATION and (self.état_courant not in [self.GAME_EDITOR, self.SIGNALISATION]):
            raise ValueError("Impossible de partir la simulation autre que dans le game editor")
        elif nouvel_état == self.SETTINGS and (self.état_courant not in [self.HOME_PAGE]):
            raise ValueError("Impossible d'aller dans les settings autre que par la page principale.")

        print(f"État passe de {self.état_courant} à {nouvel_état}")
        self.état_courant = nouvel_état
