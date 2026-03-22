from data_models.moving_direction import MovingDirection
from attack.bullet import Bullet
from attack.explosion import Explosion
from helper.timer import Timer 
from helper.collision_checker import CollisionChecKer
import random, math
from datetime import datetime


class Attack:

    bullets = []
    screen_width = 0
    screen_height = 0
    player = None
    keyboard_handler = None
    screen = None
    explosion = None
    has_to_draw_explosion = False
    images_assets_loader = None
    explosion = None
    colision_detection = None
    bullet_radius = 6
    max_bullets_per_attack = 2
    five_seconds_timer = None
    game_settings = None

    def __init__(self, player, keyboard_handler, screen, images_assets_loader, explosion, game_settings):
        self.images_assets_loader = images_assets_loader
        self.screen = screen
        self.player = player
        self.keyboard_handler = keyboard_handler
        self.explosion = explosion
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.colision_detection = CollisionChecKer().colision_detection
        self.five_seconds_timer = Timer(20)
        self.game_settings = game_settings

    def update(self):
        for bullet in self.bullets:
            max_range = bullet.bullet_max_range
            if   bullet.x > self.player.x and bullet.x < (self.player.x + max_range):
                bullet.x += bullet.vel
            elif bullet.x < self.player.x and bullet.x > (self.player.x + (self.player.radius * 2) - max_range):
                bullet.x += bullet.vel
            else:
                self.bullets.pop(self.bullets.index(bullet))

        if self.keyboard_handler.space_pressed:
            if self.player.last_moving_direction_left_right == MovingDirection.LEFT:
                facing = -1
                initial_x = self.player.x
            else:
                facing = 1
                initial_x = self.player.x + (self.player.radius * 2)
            if len(self.bullets) < self.max_bullets_per_attack:
                self.bullets.append(
                    Bullet(initial_x, self.player.y + self.player.radius, self.bullet_radius, facing)
                )

        if self.explosion.is_new_explosion and self.game_settings.game_level not in self.game_settings.eneny_boss_levels:
            player_colision_circle = (self.player.x, self.player.y, self.player.radius)
            bomb_colision_circle = (self.explosion.x - self.explosion.bomb_width, self.explosion.y - self.explosion.bomb_height, self.explosion.bomb_radius)
            if self.colision_detection(player_colision_circle, bomb_colision_circle) and self.explosion.has_to_draw_explosion is False:
                self.explosion.has_to_draw_explosion = True
                self.five_seconds_timer.start_time = True

    def move_explosion_to_random_position(self):
        self.explosion.x = random.randint(0 + 100, self.screen_width - 100) # -100 just to not create the explosion too close to the edge of the screen
        self.explosion.y = random.randint(0 + 100, self.screen_height - 100)

    def draw(self):
        if self.game_settings.game_level not in self.game_settings.eneny_boss_levels:
            wait_for_timer_to_finish = self.five_seconds_timer.check_cronometer()

            if self.explosion.is_new_explosion:
                self.explosion.draw_bomb()

            if self.explosion.has_to_draw_explosion and wait_for_timer_to_finish:
                self.explosion.draw_explosion()
            else:
                self.explosion.has_to_draw_explosion = False
                
            if self.five_seconds_timer.trigger_action_at_the_end:
                self.move_explosion_to_random_position()

        for bullet in self.bullets:
            bullet.draw(self.screen)