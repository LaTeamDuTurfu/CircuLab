import pickle
import os

class Partie():
    def __init__(self, save_data):
        self.world_data = save_data["world_data"]
        self.name = save_data["name"]
        self.columns = save_data["cols"]
        self.rows = save_data["rows"]
        self.path = save_data["path"]
        
        self.TILE_SIZE = 50
        self.scrollx = (self.columns * self.TILE_SIZE) / 2
        self.scrolly = (self.rows * self.TILE_SIZE) / 2
        self.scroll_speed = 1
        self.vertical_scroll = 0
        self.horizontal_scroll = 0
        self.build_orientation = 0
        self.see_build_preview = False
        self.running = True
    
    def check_correct_path(self):
        print("Chemin Valide")
        return os.path.exists(self.path)

    def update_save(self):
        save_data = {
            "name": self.name,
            "cols": self.columns,
            "rows": self.rows,
            "path": self.path,
            "world_data": self.world_data
        }

        # print(save_data)

        if self.check_correct_path():
            with open(self.path + f"/{self.name}.clab", "wb") as file:
                pickle.dump(str(save_data), file)
                return True
        
        print("Le chemin de sauvegarde n'est pas correct")
        return False