import pickle
import os

class Partie():
    def __init__(self, save_data):
        self.world_data = save_data["world_data"]
        self.name = save_data["name"]
        self.columns = save_data["cols"]
        self.rows = save_data["rows"]
        self.path = save_data["path"]
    
    def check_correct_path(self):
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
            with open(self.path, "w") as file:
                pickle.dump(save_data, file)
                return True
        
        print("Le chemin de sauvegarde n'est pas correct")
        return False