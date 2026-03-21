import pygame

class Bullet:

    x = 0
    y = 0
    radius = 5
    color = (255, 0, 0)
    facing = 0
    bullet_speed = 12
    bullet_max_range = 300

    def __init__(self, x, y, radius, facing):
        self.x = x + 1
        self.y = y
        self.radius = radius
        self.facing = facing
        self.vel = self.bullet_speed * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)