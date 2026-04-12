import pygame

class Bullet:

    def __init__(self, x = 0, y = 0, radius = 5, facing = 0):
        self.color = (255, 0, 0)
        self.bullet_speed = 12
        self.bullet_max_range = 300
        self.x = x + 1
        self.y = y
        self.radius = radius
        self.facing = facing
        self.vel = self.bullet_speed * facing
        self.angle = 0
        self.vy = 0
        self.vx = 0

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)