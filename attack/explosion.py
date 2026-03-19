import pygame


class Explosion:

    radius = 25
    height = 150
    whidth = 150
    bomb_height = 50
    bomb_whidth = 50
    images_assets_loader = None
    bomb_radius = 25
    explosion_radius = 75
    x = 0
    y = 0
    is_new_explosion = True
    has_to_draw_explosion = False


    def __init__(self, images_assets_loader, x, y):
        self.x = x
        self.y = y
        self.images_assets_loader = images_assets_loader

    def draw(self):
        if self.has_to_draw_explosion:
            self.images_assets_loader.draw(self.images_assets_loader.explosion, self.x - self.explosion_radius / 2, self.y - self.explosion_radius / 2, self.whidth, self.height)
        else:
            self.images_assets_loader.draw(self.images_assets_loader.bomb, self.x, self.y, self.bomb_whidth, self.bomb_height)