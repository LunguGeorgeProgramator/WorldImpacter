import pygame


class Explosion:

    def __init__(self, game_settings, images_assets_loader, x = 250, y = 250):
        self.radius = 25
        self.explosion_height = 400
        self.explosion_width = 400
        self.bomb_height = 50
        self.bomb_width = 50
        self.bomb_radius = 25
        self.explosion_radius = 200
        self.has_to_draw_explosion = False
        self.has_to_draw_bomb = True
        self.x = x
        self.y = y
        self.images_assets_loader = images_assets_loader
        self.game_settings = game_settings
        
    def draw_bomb(self):
        if self.game_settings.game_level in self.game_settings.haven_levels:
            image = self.images_assets_loader.haven_bomb
        else:
            image = self.images_assets_loader.bomb
        self.images_assets_loader.draw(image, self.x - self.bomb_width / 2, self.y - self.bomb_height / 2, self.bomb_width, self.bomb_height)

    def draw_explosion(self):
        if self.game_settings.game_level in self.game_settings.haven_levels:
            image_asset = self.images_assets_loader.haven_explosion
        else:
            image_asset = self.images_assets_loader.explosion
        self.images_assets_loader.draw(image_asset, self.x - self.explosion_width / 2, self.y - self.explosion_height / 2, self.explosion_width, self.explosion_height)