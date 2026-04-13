import pygame
from assets.images_animation_loader import ImagesAnimationLoader
from data_models.moving_direction import MovingDirection
from helper.timer import Timer


class Enemy:

    def __init__(self, x = 0, y = 0, radius = 5, screen = None, images_assets_loader = None, game_settings = None):
        self.images_assets_loader = images_assets_loader
        self.game_settings = game_settings
        self.facing = 0
        self.is_max_x_reached = False
        self.is_min_x_reached = False
        self.is_max_y_reached = False
        self.is_min_y_reached = False
        self.is_alive = True
        self.damage_to_player = 1
        self.images_animation_loader = ImagesAnimationLoader()
        self.haven_images_animation_loader = ImagesAnimationLoader()
        self.underwater_right_loader = ImagesAnimationLoader()
        self.underwater_left_loader = ImagesAnimationLoader()
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
        self.images_animation_loader.set_animation_speed(30)
        self.haven_images_animation_loader.set_frames_assets([
            self.images_assets_loader.haven_enemies_image, 
            self.images_assets_loader.haven_enemies_image_frame_two,
            self.images_assets_loader.haven_enemies_image_frame_three,
            self.images_assets_loader.haven_enemies_image_frame_four
        ])
        self.underwater_right_loader.set_frames_assets([
            self.images_assets_loader.underwater_enemy_image, 
            self.images_assets_loader.underwater_enemy_image_frame_two
        ])
        self.underwater_left_loader.set_frames_assets([
            self.images_assets_loader.underwater_enemy_image_left, 
            self.images_assets_loader.underwater_enemy_image_frame_two_left
        ])
        self.seconds_before_death_timer = Timer(10)
        self.haven_images_animation_loader.set_animation_speed(10)
        self.underwater_right_loader.set_animation_speed(10)
        self.underwater_left_loader.set_animation_speed(10)
        self.moving_direction = MovingDirection.NONE
        

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
            self.moving_direction = MovingDirection.RIGHT
            self.x += self.vel
        else:
            self.moving_direction = MovingDirection.LEFT
            self.x -= self.vel

        if self.is_min_y_reached and not self.is_max_y_reached:
            self.y += self.vel
        else:
            self.y -= self.vel
            
        if self.game_settings.game_level in self.game_settings.haven_levels:
            self.haven_images_animation_loader.update_frame()
        elif self.game_settings.game_level in self.game_settings.underwater_levels:
            if self.moving_direction == MovingDirection.LEFT:
                self.underwater_left_loader.update_frame()
            else:
                self.underwater_right_loader.update_frame()
        else:
            self.images_animation_loader.update_frame()

    def draw(self, win):
        if self.is_alive:
            if self.game_settings.game_level in self.game_settings.haven_levels:
                image_asset = self.haven_images_animation_loader.get_frame()
            elif self.game_settings.game_level in self.game_settings.underwater_levels:
                if self.moving_direction == MovingDirection.LEFT:
                    image_asset = self.underwater_left_loader.get_frame()
                else:
                    image_asset = self.underwater_right_loader.get_frame()
            else:
                image_asset = self.images_animation_loader.get_frame() 
        else:
            if self.game_settings.game_level in self.game_settings.haven_levels:
                image_asset = self.images_assets_loader.haven_exploded_enemies_image
            elif self.game_settings.game_level in self.game_settings.underwater_levels:
                if self.moving_direction == MovingDirection.LEFT:
                    image_asset = self.images_assets_loader.underwater_exploded_enemy_image_left
                else:
                    image_asset = self.images_assets_loader.underwater_exploded_enemy_image
            else:
                image_asset = self.images_assets_loader.exploded_enemies_image
        self.images_assets_loader.draw(image_asset, self.x, self.y, self.default_image_width, self.default_image_height)
    