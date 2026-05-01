import pygame

class Bullet:

    def __init__(self, x = 0, y = 0, radius = 5, facing = 0, color = (255, 0, 0)):
        self.color = color
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
        self.left_right_direction = None
        self.destroied = False

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

    # def update(self):
    #     # move
    #     self.x += self.vx
    #     self.y += self.vy

    #     # rotate velocity (this creates spiral motion)
    #     angle = 0.05  # rotation speed (tweak this)

    #     cos_a = math.cos(angle)
    #     sin_a = math.sin(angle)

    #     new_vx = self.vx * cos_a - self.vy * sin_a
    #     new_vy = self.vx * sin_a + self.vy * cos_a

    #     self.vx = new_vx
    #     self.vy = new_vy