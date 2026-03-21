import pygame


class Explosion:

    radius = 25
    explosion_height = 400
    explosion_width = 400
    bomb_height = 50
    bomb_width = 50
    images_assets_loader = None
    bomb_radius = 25
    explosion_radius = 200
    x = 0
    y = 0
    is_new_explosion = True
    has_to_draw_explosion = False


    def __init__(self, images_assets_loader, x = 250, y = 250):
        self.x = x
        self.y = y
        self.images_assets_loader = images_assets_loader
        
    def draw_bomb(self):
        self.images_assets_loader.draw(self.images_assets_loader.bomb, self.x - self.bomb_width / 2, self.y - self.bomb_height / 2, self.bomb_width, self.bomb_height)

    def draw_explosion(self):
        self.images_assets_loader.draw(self.images_assets_loader.explosion, self.x - self.explosion_width / 2, self.y - self.explosion_height / 2, self.explosion_width, self.explosion_height)