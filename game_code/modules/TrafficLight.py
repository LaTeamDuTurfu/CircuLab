import pygame

class TrafficLight:
    def __init__(self, green_duration=3, red_duration=3):
        self.green_duration = green_duration
        self.red_duration = red_duration
        self.state = "green"  # état initial
        self.timer = 0.0

    def update(self, dt):
        self.timer += dt
        if self.state == "green" and self.timer >= self.green_duration:
            self.state = "red"
            self.timer = 0.0
        elif self.state == "red" and self.timer >= self.red_duration:
            self.state = "green"
            self.timer = 0.0

    def draw(self, screen, position):
        color = (0, 255, 0) if self.state == "green" else (255, 0, 0)
        pygame.draw.circle(screen, color, position, 8)