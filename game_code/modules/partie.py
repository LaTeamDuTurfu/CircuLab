import pickle
import os

class Partie():
    
    vertical_scroll = 0
    horizontal_scroll = 0
    scroll_speed = 1
    
    def __init__(self, save_data: dict):
        self.name = save_data["name"]
        self.columns = save_data["cols"]
        self.rows = save_data["rows"]
        self.scrollx = save_data["scroll_x"]
        self.scrolly = save_data["scroll_y"]
        self.path = save_data["path"]
        self.TILE_SIZE = save_data["tile_size"]
        self.road_data = save_data["road_data"]
        self.car_data = None
        self.signalisation_data = None
        
    
    def check_correct_path(self):
        print("Chemin Valide")
        return os.path.exists(self.path)

    def update_save(self):
        save_data = {
            "name": self.name,
            "cols": self.columns,
            "rows": self.rows,
            "tile_size": self.TILE_SIZE,
            "scroll_x": self.scrollx,
            "scroll_y": self.scrolly,
            "path": self.path,
            "road_data": self.road_data
        }

        # print(save_data)

        if self.check_correct_path():
            with open(self.path + f"/{self.name}.clab", "wb") as file:
                pickle.dump(str(save_data), file)
                return True
        
        print("Le chemin de sauvegarde n'est pas correct")
        return False