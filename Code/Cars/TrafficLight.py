import pygame

class TrafficLight:
    def __init__(self, green_duration=3, red_duration=3):
        self.green_duration = green_duration
        self.red_duration = red_duration
        self.state = "green"  # état initial
        self.timer = 0.0

        self.green_image = pygame.image.load("assets/tile_images/traffic_light_green_only.png").convert_alpha()
        self.red_image = pygame.image.load("assets/tile_images/traffic_light_red_only.png").convert_alpha()

    def update(self, dt):
        self.timer += dt
        if self.state == "green" and self.timer >= self.green_duration:
            self.state = "red"
            self.timer = 0.0
        elif self.state == "red" and self.timer >= self.red_duration:
            self.state = "green"
            self.timer = 0.0

    def draw(self, screen, position, scrollx=0, scrolly=0):
        if self.state == "green":
            screen.blit(self.green_image, (position[0] - scrollx, position[1]-scrolly))
        else:
            screen.blit(self.red_image, (position[0] - scrollx, position[1]-scrolly))

