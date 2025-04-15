import pygame

class RoadOrientationManager():
    def __init__(self, x_pos: int = 0, y_pos: int = 0, game_data = None):
        self.game_data = game_data
        self.x_pos = x_pos
        self.y_pos = y_pos
        
        # Placeholders
        self.tile = None
        self.left_tile = None
        self.right_tile = None
        self.top_tile = None
        self.bottom_tile = None
        
        # Load Road Types Images
        self.branch_out_left = pygame.image.load("assets/roads/branch_out_left.png")
        self.branch_out_right = pygame.image.load("assets/roads/branch_out_right.png")
        
        self.inner_turn_down_left = pygame.image.load("assets/roads/inner_turn_down_left.png")
        self.inner_turn_down_right = pygame.image.load("assets/roads/inner_turn_down_right.png")
        self.inner_turn_up_left = pygame.image.load("assets/roads/inner_turn_up_left.png")
        self.inner_turn_up_right = pygame.image.load("assets/roads/inner_turn_up_right.png")
        
        self.outer_turn_down_left = pygame.image.load("assets/roads/outer_turn_down_left.png")
        self.outer_turn_down_right = pygame.image.load("assets/roads/outer_turn_down_right.png")
        self.outer_turn_up_left = pygame.image.load("assets/roads/outer_turn_up_left.png")
        self.outer_turn_up_right = pygame.image.load("assets/roads/outer_turn_up_right.png")
        
        self.single_turn_down_left = pygame.image.load("assets/roads/single_turn_down_left.png")
        self.single_turn_down_right = pygame.image.load("assets/roads/single_turn_down_right.png")
        self.single_turn_up_left = pygame.image.load("assets/roads/single_turn_up_left.png")
        self.single_turn_up_right = pygame.image.load("assets/roads/single_turn_up_right.png")
        
        self.straight_dotted_white_both = pygame.image.load("assets/roads/straight_dotted_white_both.png")
        self.straight_dotted_white_left = pygame.image.load("assets/roads/straight_dotted_white_left.png")
        self.straight_dotted_white_right = pygame.image.load("assets/roads/straight_dotted_white_right.png")
        
        self.straight_dotted_yellow_both = pygame.image.load("assets/roads/straight_dotted_yellow_both.png")
        self.straight_dotted_yellow_left = pygame.image.load("assets/roads/straight_dotted_yellow_left.png")
        self.straight_dotted_yellow_right = pygame.image.load("assets/roads/straight_dotted_yellow_right.png")
        
        self.straight_simple = pygame.image.load("assets/roads/straight_single.png")
        
    def set_game_data(self, game_data):
        self.game_data = game_data
        
    def get_tile(self):
        self.tile = self.game_data[self.y_pos][self.x_pos]
    
    def get_connecting_tiles(self):
        self.left_tile = self.game_data[self.y_pos][self.x_pos - 1]
        self.right_tile = self.game_data[self.y_pos][self.x_pos + 1]
        self.top_tile = self.game_data[self.y_pos - 1][self.x_pos]
        self.bottom_tile = self.game_data[self.y_pos + 1][self.x_pos]
        
        self.top_left_tile = self.game_data[self.y_pos - 1][self.x_pos - 1]
        self.top_right_tile = self.game_data[self.y_pos - 1][self.x_pos + 1]
        self.bottom_left_tile = self.game_data[self.y_pos + 1][self.x_pos - 1]
        self.bottom_right_tile = self.game_data[self.y_pos + 1][self.x_pos + 1]
    
    def is_a_road(self, tile):
        if tile.tile_type == "Road":
            return True
        return False
    
    def is_up_or_down(self, tile):
        if tile.orientation % 2 == 0:
            return True
        return False
    
    def change_tile_image(self, tile, image, rotation_manuelle: int = None):
        img_copy = image.copy()
        if rotation_manuelle is not None:
            tile.image = pygame.transform.rotate(img_copy, rotation_manuelle * 90)
        else:
            tile.image = pygame.transform.rotate(img_copy, tile.orientation * 90)
    
    def check_tile_change(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
        
        self.get_tile()
        self.get_connecting_tiles()
        
        if self.is_a_road(self.tile):
            if self.is_a_road(self.left_tile):  # Changement quand on place une tuile à droite d'une autre
                if self.tile.orientation == self.left_tile.orientation:  # Lignes blanches pointillées quand les deux tuiles vont dans le même sens
                    if self.tile.orientation == 0:
                        self.change_tile_image(self.tile, self.straight_dotted_white_left)
                        self.change_tile_image(self.left_tile, self.straight_dotted_white_right)
                    elif self.tile.orientation == 2:
                        self.change_tile_image(self.tile, self.straight_dotted_white_right)
                        self.change_tile_image(self.left_tile, self.straight_dotted_white_left)
                elif self.tile.orientation == (self.left_tile.orientation + 2) % 4: # Lignes jaunes pointillées quand les deux tuiles vont à contre sens
                    if self.tile.orientation == 0:
                        self.change_tile_image(self.tile, self.straight_dotted_yellow_left)
                        self.change_tile_image(self.left_tile, self.straight_dotted_yellow_left)
                    elif self.tile.orientation == 2:
                        self.change_tile_image(self.tile, self.straight_dotted_yellow_right)
                        self.change_tile_image(self.left_tile, self.straight_dotted_yellow_right)
                
                # Gère les routes qui branch out
                if not self.is_a_road(self.bottom_tile) and self.tile.orientation == 0 and self.left_tile.orientation == 0:
                    self.change_tile_image(self.tile, self.branch_out_right)
                elif not self.is_a_road(self.top_tile) and self.tile.orientation == 2 and self.left_tile.orientation == 2:
                    self.change_tile_image(self.tile, self.branch_out_left)
                
                # Gère les singles turns 
                if self.tile.orientation % 2 == (self.left_tile.orientation + 1) % 2:
                    if self.left_tile.orientation == 3:
                        if self.tile.orientation == 0:
                            self.change_tile_image(self.tile, self.single_turn_down_right, rotation_manuelle=1)
                        elif self.tile.orientation == 2:
                            self.change_tile_image(self.tile, self.single_turn_down_left, rotation_manuelle=1) 
                
                if not self.is_a_road(self.right_tile):
                    if self.is_a_road(self.bottom_tile) and self.left_tile.orientation == self.bottom_tile.orientation and self.left_tile.orientation == 3:
                        self.change_tile_image(self.tile, self.branch_out_right, rotation_manuelle=1)
                        self.check_tile_change(self.x_pos - 1, self.y_pos)  # Check la tuile gauche pour voir si elle doit changer
                    elif self.is_a_road(self.top_tile) and self.left_tile.orientation == self.top_tile.orientation and self.left_tile.orientation == 3:
                        self.change_tile_image(self.tile, self.branch_out_left, rotation_manuelle=1)  
                        self.check_tile_change(self.x_pos - 1, self.y_pos)  # Check la tuile gauche pour voir si elle doit changer
                
                # # Gère les inner doubles turns 
                # if self.tile.orientation % 2 == (self.bottom_tile.orientation + 1) % 2:
                #     if self.bottom_tile.orientation == 2:
                #         if self.tile.orientation == 3:
                #             self.change_tile_image(self.tile, self.straight_dotted_white_right)
                #             self.change_tile_image(self.bottom_tile, self.inner_turn_up_left, rotation_manuelle=0)
                # if self.tile.orientation % 2 == (self.top_tile.orientation + 1) % 2:
                #     if self.top_tile.orientation == 0:
                #         if self.tile.orientation == 3:
                #             self.change_tile_image(self.tile, self.straight_dotted_white_right, rotation_manuelle=1)
                #             self.change_tile_image(self.top_tile, self.inner_turn_down_left, rotation_manuelle=0)      
                
                # # Gère les outer doubles turns
                # if self.tile.orientation % 2 == (self.left_tile.orientation + 1) % 2:
                #     if self.left_tile.orientation == 3:
                #         if self.tile.orientation == 0 and self.top_left_tile.orientation == self.tile.orientation:
                #             self.change_tile_image(self.tile, self.outer_turn_down_left, rotation_manuelle=0)
                #         elif self.tile.orientation == 2 and self.bottom_left_tile.orientation == self.tile.orientation:
                #             self.change_tile_image(self.tile, self.outer_turn_up_left, rotation_manuelle=0)
                            
            if self.is_a_road(self.right_tile): # Changement quand on place une tuile à gauche d'une autre
                if self.tile.orientation == self.right_tile.orientation: # Lignes blanches pointillées quand les deux tuiles vont dans le même sens
                    if self.tile.orientation == 0:
                        self.change_tile_image(self.tile, self.straight_dotted_white_right)
                        self.change_tile_image(self.right_tile, self.straight_dotted_white_left)
                    elif self.tile.orientation == 2:
                        self.change_tile_image(self.tile, self.straight_dotted_white_left)
                        self.change_tile_image(self.right_tile, self.straight_dotted_white_right)
                elif self.tile.orientation == (self.right_tile.orientation + 2) % 4: # Lignes jaunes pointillées quand les deux tuiles vont à contre sens
                    if self.tile.orientation == 0:
                        self.change_tile_image(self.tile, self.straight_dotted_yellow_right)
                        self.change_tile_image(self.right_tile, self.straight_dotted_yellow_right)
                    elif self.tile.orientation == 2:
                        self.change_tile_image(self.tile, self.straight_dotted_yellow_left)
                        self.change_tile_image(self.right_tile, self.straight_dotted_yellow_left)
            
                # Gère les routes qui branch out
                if not self.is_a_road(self.bottom_tile) and self.tile.orientation == 0 and self.right_tile.orientation == 0:
                    self.change_tile_image(self.tile, self.branch_out_left)
                elif not self.is_a_road(self.top_tile) and self.tile.orientation == 2 and self.right_tile.orientation == 2:
                    self.change_tile_image(self.tile, self.branch_out_right)
                
                # Gère les singles turns 
                if self.tile.orientation % 2 == (self.right_tile.orientation + 1) % 2:
                    if self.right_tile.orientation == 1:
                        if self.tile.orientation == 0:
                            self.change_tile_image(self.tile, self.single_turn_up_right, rotation_manuelle=1)
                        elif self.tile.orientation == 2:
                            self.change_tile_image(self.tile, self.single_turn_up_left, rotation_manuelle=1)
                
                if not self.is_a_road(self.left_tile):
                    if self.is_a_road(self.bottom_tile) and self.right_tile.orientation == self.bottom_tile.orientation and self.right_tile.orientation == 1:
                        self.change_tile_image(self.tile, self.branch_out_left, rotation_manuelle=3)
                        self.check_tile_change(self.x_pos + 1, self.y_pos)  # Check la tuile droite pour voir si elle doit changer
                    elif self.is_a_road(self.top_tile) and self.right_tile.orientation == self.top_tile.orientation and self.right_tile.orientation == 1:
                        self.change_tile_image(self.tile, self.branch_out_right, rotation_manuelle=3)  
                        self.check_tile_change(self.x_pos + 1, self.y_pos)  # Check la tuile droite pour voir si elle doit changer

            if self.is_a_road(self.top_tile): # Changement quand on place une tuile en dessous d'une autre
                if self.tile.orientation == self.top_tile.orientation: # Lignes blanches pointillées quand les deux tuiles vont dans le même sens
                    if self.tile.orientation == 1:
                        self.change_tile_image(self.tile, self.straight_dotted_white_right)
                        self.change_tile_image(self.top_tile, self.straight_dotted_white_left)
                    elif self.tile.orientation == 3:
                        self.change_tile_image(self.tile, self.straight_dotted_white_left)
                        self.change_tile_image(self.top_tile, self.straight_dotted_white_right)
                elif self.tile.orientation == (self.top_tile.orientation + 2) % 4: # Lignes jaunes pointillées quand les deux tuiles vont à contre sens
                    if self.tile.orientation == 1:
                        self.change_tile_image(self.tile, self.straight_dotted_yellow_right)
                        self.change_tile_image(self.top_tile, self.straight_dotted_yellow_right)
                    elif self.tile.orientation == 3:
                        self.change_tile_image(self.tile, self.straight_dotted_yellow_left)
                        self.change_tile_image(self.top_tile, self.straight_dotted_yellow_left)

                # Gère les routes qui branch out
                if not self.is_a_road(self.right_tile) and self.tile.orientation == 1 and self.top_tile.orientation == 1:
                    self.change_tile_image(self.tile, self.branch_out_left)
                elif not self.is_a_road(self.left_tile) and self.tile.orientation == 3 and self.top_tile.orientation == 3:
                    self.change_tile_image(self.tile, self.branch_out_right)
                
                # Gère les singles turns 
                if self.tile.orientation % 2 == (self.top_tile.orientation + 1) % 2:
                    if self.top_tile.orientation == 2:
                        if self.tile.orientation == 1:
                            self.change_tile_image(self.tile, self.single_turn_down_left, rotation_manuelle=0)
                        elif self.tile.orientation == 3:
                            self.change_tile_image(self.tile, self.single_turn_down_right, rotation_manuelle=0)
                
                # S'occupe du branch in des routes
                if not self.is_a_road(self.bottom_tile):
                    if self.is_a_road(self.left_tile) and self.left_tile.orientation == self.top_tile.orientation and self.left_tile.orientation == 2:
                        self.change_tile_image(self.tile, self.branch_out_right, rotation_manuelle=0)
                        self.check_tile_change(self.x_pos, self.y_pos - 1)  # Check la tuile du dessus pour voir si elle doit changer
                    elif self.is_a_road(self.right_tile) and self.right_tile.orientation == self.top_tile.orientation and self.right_tile.orientation == 2:
                        self.change_tile_image(self.tile, self.branch_out_left, rotation_manuelle=0)
                        self.check_tile_change(self.x_pos, self.y_pos - 1)  # Check la tuile du dessus pour voir si elle doit changer
                
                # Gère les inner doubles turns 
                if self.tile.orientation % 2 == (self.right_tile.orientation + 1) % 2:
                    if self.right_tile.orientation == 3:
                        if self.tile.orientation == 2:
                            self.change_tile_image(self.tile, self.straight_dotted_white_right, rotation_manuelle=0)
                            self.change_tile_image(self.right_tile, self.inner_turn_down_right, rotation_manuelle=0)
                if self.tile.orientation % 2 == (self.left_tile.orientation + 1) % 2:
                    if self.left_tile.orientation == 1:
                        if self.tile.orientation == 2:
                            self.change_tile_image(self.tile, self.straight_dotted_white_left, rotation_manuelle=0)
                            self.change_tile_image(self.left_tile, self.inner_turn_down_left, rotation_manuelle=0)      
                
                # Gère les outer doubles turns
                if self.tile.orientation % 2 == (self.top_tile.orientation + 1) % 2:
                    if self.top_tile.orientation == 2:
                        if self.tile.orientation == 3 and self.top_right_tile.orientation == self.tile.orientation:
                            self.change_tile_image(self.tile, self.outer_turn_down_right, rotation_manuelle=0)
                        elif self.tile.orientation == 1 and self.top_left_tile.orientation == self.tile.orientation:
                            self.change_tile_image(self.tile, self.outer_turn_down_left, rotation_manuelle=0)
            
            if self.is_a_road(self.bottom_tile): # Changement quand on place une tuile au dessus d'une autre
                if self.tile.orientation == self.bottom_tile.orientation: # Lignes blanches pointillées quand les deux tuiles vont dans le même sens
                    if self.tile.orientation == 1:
                        self.change_tile_image(self.tile, self.straight_dotted_white_left)
                        self.change_tile_image(self.bottom_tile, self.straight_dotted_white_right)
                    elif self.tile.orientation == 3:
                        self.change_tile_image(self.tile, self.straight_dotted_white_right)
                        self.change_tile_image(self.bottom_tile, self.straight_dotted_white_left)
                elif self.tile.orientation == (self.bottom_tile.orientation + 2) % 4: # Lignes jaunes pointillées quand les deux tuiles vont à contre sens
                    if self.tile.orientation == 1:
                        self.change_tile_image(self.tile, self.straight_dotted_yellow_left)
                        self.change_tile_image(self.bottom_tile, self.straight_dotted_yellow_left)
                    elif self.tile.orientation == 3:
                        self.change_tile_image(self.tile, self.straight_dotted_yellow_right)
                        self.change_tile_image(self.bottom_tile, self.straight_dotted_yellow_right)

                # Gère les routes qui branch out
                if not self.is_a_road(self.right_tile) and self.tile.orientation == 1 and self.bottom_tile.orientation == 1:
                    self.change_tile_image(self.tile, self.branch_out_right)
                elif not self.is_a_road(self.left_tile) and self.tile.orientation == 3 and self.bottom_tile.orientation == 3:
                    self.change_tile_image(self.tile, self.branch_out_left)
                
                # Gère les singles turns 
                if self.tile.orientation % 2 == (self.bottom_tile.orientation + 1) % 2:
                    if self.bottom_tile.orientation == 0:
                        if self.tile.orientation == 1:
                            self.change_tile_image(self.tile, self.single_turn_up_left, rotation_manuelle=0)
                        elif self.tile.orientation == 3:
                            self.change_tile_image(self.tile, self.single_turn_up_right, rotation_manuelle=0)
                
                # S'occupe du branch in des routes
                if not self.is_a_road(self.top_tile):
                    if self.is_a_road(self.left_tile) and self.left_tile.orientation == self.bottom_tile.orientation and self.left_tile.orientation == 0:
                        self.change_tile_image(self.tile, self.branch_out_left, rotation_manuelle=2)
                        self.check_tile_change(self.x_pos, self.y_pos + 1)  # Check la tuile du dessous pour voir si elle doit changer
                    elif self.is_a_road(self.right_tile) and self.right_tile.orientation == self.bottom_tile.orientation and self.right_tile.orientation == 0:
                        self.change_tile_image(self.tile, self.branch_out_right, rotation_manuelle=2)
                        self.check_tile_change(self.x_pos, self.y_pos + 1)  # Check la tuile du dessous pour voir si elle doit changer

                # Gère les inner doubles turns 
                if self.tile.orientation % 2 == (self.right_tile.orientation + 1) % 2:
                    if self.right_tile.orientation == 3:
                        if self.tile.orientation == 0:
                            self.change_tile_image(self.tile, self.straight_dotted_white_right, rotation_manuelle=0)
                            self.change_tile_image(self.right_tile, self.inner_turn_up_right, rotation_manuelle=0)
                if self.tile.orientation % 2 == (self.left_tile.orientation + 1) % 2:
                    if self.left_tile.orientation == 1:
                        if self.tile.orientation == 0:
                            self.change_tile_image(self.tile, self.straight_dotted_white_left, rotation_manuelle=0)
                            self.change_tile_image(self.left_tile, self.inner_turn_up_left, rotation_manuelle=0)      
                
                # Gère les outer doubles turns
                if self.tile.orientation % 2 == (self.bottom_tile.orientation + 1) % 2:
                    if self.bottom_tile.orientation == 0:
                        if self.tile.orientation == 3 and self.bottom_right_tile.orientation == self.tile.orientation:
                            self.change_tile_image(self.tile, self.outer_turn_up_right, rotation_manuelle=0)
                        elif self.tile.orientation == 1 and self.bottom_left_tile.orientation == self.tile.orientation:
                            self.change_tile_image(self.tile, self.outer_turn_up_left, rotation_manuelle=0)