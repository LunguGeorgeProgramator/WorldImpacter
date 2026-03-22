import pygame
from assets.images_animation_loader import ImagesAnimationLoader


class Enemy:

    images_assets_loader = None
    default_image_height = 0
    default_image_width = 0
    x = 0
    y = 0
    screen_x = 0
    screen_y = 0
    radius = 5
    facing = 0
    vel = 0
    is_max_x_reached = False
    is_min_x_reached = False
    is_max_y_reached = False
    is_min_y_reached = False
    is_alive = True
    damage_to_player = 1
    images_animation_loader = ImagesAnimationLoader()


    def __init__(self, x, y, radius, screen, images_assets_loader):
        self.images_assets_loader = images_assets_loader
        self.x = x + 1
        self.y = y
        self.radius = radius
        # self.vel = 0.5
        self.vel = 2
        self.screen_x, self.screen_y = screen.get_size()
        self.default_image_height = radius * 2
        self.default_image_width = radius * 2
        self.images_animation_loader.set_frames_assets([
            self.images_assets_loader.enemies_image, 
            self.images_assets_loader.enemies_image_frame_two
        ])
        self.images_animation_loader.set_animation_speed(200)

    def update(self):
        if self.x < 0:
            self.is_max_x_reached = False
            self.is_min_x_reached = True
        elif self.x > self.screen_x - self.radius * 2:
            self.is_max_x_reached = True
            self.is_min_x_reached = False
        if self.y < 0:
            self.is_max_y_reached = False
            self.is_min_y_reached = True
        elif self.y > self.screen_y - self.radius * 2:
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
        self.images_animation_loader.update_frame()

    def draw(self, win):
        if self.is_alive:
            image_asset = self.images_animation_loader.get_frame()
            self.images_assets_loader.draw(image_asset, self.x, self.y, self.default_image_width, self.default_image_height)
    