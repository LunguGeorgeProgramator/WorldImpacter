import pygame
from enemies.enemy import Enemy
from assets.images_animation_loader import ImagesAnimationLoader
from helper.collision_checker import CollisionChecKer
from data_models.moving_direction import MovingDirection
from attack.bullet import Bullet
from helper.timer import Timer
import math


class EnemyBoss(Enemy):

    health_colors_dict = {
        "full_health": (100, 0, 0),
        "low_health": (0, 200, 0),
        "border": (255,255,255)
    }
    bar_width = 200
    bar_height = 20
    health = 1000
    max_health = 1000
    screen = None
    damage_to_player = 5
    heaven_animation = ImagesAnimationLoader()
    injured_heaven_animation = ImagesAnimationLoader()
    fire_pit_animation = ImagesAnimationLoader()
    underwater_enemy_boss_animation = ImagesAnimationLoader()
    underwater_enemy_boss_right_animation = ImagesAnimationLoader()
    spread_bullets_attack = []
    num_bullets_per_attack = 10
    boss_bullet_radius = 10
    boss_bullet_speed = 1
    time_between_attacks_timer = Timer(500)

    def __init__(self, x, y, radius, screen, images_assets_loader, game_settings, player, attack):
        super().__init__(x, y, radius, screen, images_assets_loader, game_settings)
        self.attack = attack
        self.enemy_boos_damage_to_player = 1
        self.enemy_boos_damage_percentage_multiplier = 5
        self.player = player
        self.colision_detection = CollisionChecKer().colision_detection
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.heaven_animation.set_frames_assets([
            self.images_assets_loader.enemy_boss_heavan_frame_one_image, 
            self.images_assets_loader.enemy_boss_heavan_frame_two_image
        ])
        self.injured_heaven_animation.set_frames_assets([
            self.images_assets_loader.injured_enemy_boss_heavan_frame_one_image, 
            self.images_assets_loader.injured_enemy_boss_heavan_frame_two_image
        ])
        self.fire_pit_animation.set_frames_assets([
            self.images_assets_loader.enemy_boss_image, 
            self.images_assets_loader.enemy_boss_frame_two_image,
            self.images_assets_loader.enemy_boss_frame_three_image,
            self.images_assets_loader.enemy_boss_frame_four_image
            
        ])
        self.underwater_enemy_boss_animation.set_frames_assets([
            self.images_assets_loader.enemy_boss_underwater_frame_one_image,
            self.images_assets_loader.enemy_boss_underwater_frame_two_image
        ])
        self.underwater_enemy_boss_right_animation.set_frames_assets([
            self.images_assets_loader.enemy_boss_underwater_frame_one_right_image,
            self.images_assets_loader.enemy_boss_underwater_frame_two_right_image
        ])
        self.fire_pit_animation.set_animation_speed(20)
        self.heaven_animation.set_animation_speed(20)
        self.injured_heaven_animation.set_animation_speed(20)
        self.underwater_enemy_boss_animation.set_animation_speed(20)
        self.underwater_enemy_boss_right_animation.set_animation_speed(20)
        self.screen = screen

    def _is_heaven_level(self):
        return self.game_settings.game_level in self.game_settings.heaven_eneny_boss_levels

    def _is_underwater_level(self):
        return self.game_settings.game_level in self.game_settings.underwater_enemy_boss_levels

    def update(self):
        super().update()
        if not self._is_underwater_level() and not self._is_heaven_level():
            self.fire_pit_animation.update_frame()
        if self._is_underwater_level():
            if self.moving_direction == MovingDirection.LEFT:
                self.underwater_enemy_boss_animation.update_frame()
            else:
                self.underwater_enemy_boss_right_animation.update_frame()
        if self._is_heaven_level():
            if self.health <= self.max_health / 2:
                self.injured_heaven_animation.update_frame()
            else:
                self.heaven_animation.update_frame()

        if self.time_between_attacks_timer.start_time is False:
            self.create_boss_attack()
            self.time_between_attacks_timer.start_time = True

        self.time_between_attacks_timer.start_time = self.time_between_attacks_timer.check_cronometer()
        
        for bullet in self.spread_bullets_attack:
            bullet.x += bullet.vx
            bullet.y += bullet.vy
            if bullet.x > self.screen_width or bullet.x < 0 or bullet.y > self.screen_height or bullet.y < 0:
                self.spread_bullets_attack.pop(self.spread_bullets_attack.index(bullet))

        self.boos_attack_colision()
        
        if self.is_alive is False:
            self.spread_bullets_attack = []

    def draw(self, win):
        if self.is_alive:
            for bullet in self.spread_bullets_attack:
                bullet.draw(self.screen)

            if self._is_heaven_level():
                if self.health <= self.max_health / 2:
                    image_asset = self.injured_heaven_animation.get_frame()
                else:   
                    image_asset = self.heaven_animation.get_frame()
            elif self._is_underwater_level():
                if self.moving_direction == MovingDirection.LEFT:
                    image_asset = self.underwater_enemy_boss_animation.get_frame()
                else:
                    image_asset = self.underwater_enemy_boss_right_animation.get_frame()
            else:
                image_asset = self.fire_pit_animation.get_frame()
            self.images_assets_loader.draw(image_asset, self.x, self.y, self.default_image_width, self.default_image_height)
            self._draw_health_bar()
    
    def _draw_health_bar(self):
        x = self.x
        y = self.y - (self.radius / 3)
        ratio = self.health / self.max_health
        pygame.draw.rect(self.screen, self.health_colors_dict["full_health"], (x, y, self.bar_width, self.bar_height))
        pygame.draw.rect(self.screen, self.health_colors_dict["low_health"], (x, y, self.bar_width * ratio, self.bar_height))
        pygame.draw.rect(self.screen, self.health_colors_dict["border"], (x, y, self.bar_width, self.bar_height), 2)

    def create_boss_attack(self):
        center_x = self.x + self.radius
        center_y = self.y + self.radius / 2
        if self._is_heaven_level():
            bullet_color = (255, 165, 0)
        elif self._is_underwater_level():
            bullet_color = (0, 0, 139)
        else:
            bullet_color = (255, 0, 0)
        for i in range(self.num_bullets_per_attack):
            bullet = Bullet(self.x, (self.y + self.boss_bullet_radius), self.boss_bullet_radius, 0, bullet_color)
            angle = i * (2 * math.pi / self.num_bullets_per_attack)
            bullet.x = center_x
            bullet.y = center_y
            bullet.vx = math.cos(angle) * self.boss_bullet_speed
            bullet.vy = math.sin(angle) * self.boss_bullet_speed
            self.spread_bullets_attack.append(bullet)
    
    def boos_attack_colision(self):
        boss_bullet_damage = math.floor(self.enemy_boos_damage_to_player + self.attack.get_level_attack_multiplier(self.enemy_boos_damage_percentage_multiplier))
        for bullet in self.spread_bullets_attack:
            bullet_colision_circle = (bullet.x, bullet.y, bullet.radius)
            player_colision_circle = (self.player.x + self.player.radius, self.player.y + self.player.radius, self.player.radius)
            if self.colision_detection(bullet_colision_circle, player_colision_circle):
                self.player.health -= boss_bullet_damage