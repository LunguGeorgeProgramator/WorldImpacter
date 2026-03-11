import pygame


class Enemy:

    x = 0
    y = 0
    screen_x = 0
    screen_y = 0
    radius = 5
    color = (255, 0, 0)
    facing = 0
    vel = 0
    is_max_x_reached = False
    is_min_x_reached = False
    is_max_y_reached = False
    is_min_y_reached = False
    is_alive = True


    def __init__(self, x, y, radius, color, screen):
        self.x = x + 1
        self.y = y
        self.radius = radius
        self.color = color
        # self.vel = 0.5
        self.vel = 2
        self.screen_x, self.screen_y = screen.get_size()

    def update(self):
        if self.x < 0:
            self.is_max_x_reached = False
            self.is_min_x_reached = True
        elif self.x > self.screen_x:
            self.is_max_x_reached = True
            self.is_min_x_reached = False
        if self.y < 0:
            self.is_max_y_reached = False
            self.is_min_y_reached = True
        elif self.y > self.screen_y:
            self.is_max_y_reached = True
            self.is_min_y_reached = False
        if self.is_min_x_reached and not self.is_max_x_reached:
            self.x += self.vel
        else:
            self.x -= self.vel
        if self.is_min_y_reached and not self.is_max_y_reached:
            self.y += self.vel
        else:
            self.y -= self.vel

    def draw(self, win):
        if self.is_alive:
            pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)
    