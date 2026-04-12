from data_models.moving_direction import MovingDirection
from attack.bullet import Bullet
from attack.explosion import Explosion
from helper.timer import Timer 
from helper.collision_checker import CollisionChecKer
from data_models.entities_actions import EntitiesActions
import random, math
from datetime import datetime


class Attack:

    def __init__(self, player, keyboard_handler, screen, images_assets_loader, explosion, game_settings):
        self.bullets = []
        self.flower_attask_bullets = []
        self.has_to_draw_explosion = False
        self.bullet_radius = 6
        self.max_bullets_per_attack = 2
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
        self.percentage_of_bullets_number_per_level = 10
        self.percentage_of_bullets_range_per_level = 120
        self.num_bullets_flower_attack = 12
        self.speed_flower_attack = 3

    def _level_attack_multiplier(self, percentage = 10):
        return  self.game_settings.game_level * (percentage / 100)

    def update(self):
        for bullet in self.flower_attask_bullets:
            bullet.x += bullet.vx
            bullet.y += bullet.vy
            if bullet.x > self.screen_width or bullet.x < 0 or bullet.y > self.screen_height or bullet.y < 0:
                self.flower_attask_bullets.pop(self.flower_attask_bullets.index(bullet))

        for bullet in self.bullets:
            max_range = bullet.bullet_max_range + self._level_attack_multiplier(self.percentage_of_bullets_range_per_level)
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
            if len(self.bullets) < self.max_bullets_per_attack * self._level_attack_multiplier(self.percentage_of_bullets_number_per_level):
                self.bullets.append(
                    Bullet(initial_x, self.player.y + self.player.radius, self.bullet_radius, facing)
                )

        if self.explosion.is_new_explosion and self.game_settings.is_enemy_boss_level() is False:
            player_colision_circle = (self.player.x, self.player.y, self.player.radius)
            bomb_colision_circle = (self.explosion.x - self.explosion.bomb_width, self.explosion.y - self.explosion.bomb_height, self.explosion.bomb_radius)
            if self.colision_detection(player_colision_circle, bomb_colision_circle) and self.explosion.has_to_draw_explosion is False:
                self.explosion.has_to_draw_explosion = True
                self.five_seconds_timer.start_time = True

        self.detect_flower_attack()

    def detect_flower_attack(self):
        if self.game_settings.player_action == EntitiesActions.FLOWER_ATTACK:
            self.game_settings.player_action = None
            center_x = self.player.x + self.player.radius
            center_y = self.player.y + self.player.radius / 2
            for i in range(self.num_bullets_flower_attack):
                bullet = Bullet(self.player.x, self.player.y + self.player.radius, self.bullet_radius, 0)
                angle = i * (2 * math.pi / self.num_bullets_flower_attack)
                bullet = Bullet()
                bullet.x = center_x
                bullet.y = center_y
                bullet.vx = math.cos(angle) * self.speed_flower_attack
                bullet.vy = math.sin(angle) * self.speed_flower_attack
                self.flower_attask_bullets.append(bullet)

    def move_explosion_to_random_position(self):
        self.explosion.x = random.randint(0 + 100, self.screen_width - 100) # -100 just to not create the explosion too close to the edge of the screen
        self.explosion.y = random.randint(0 + 100, self.screen_height - 100)

    def draw(self):
        if self.game_settings.is_enemy_boss_level() is False:
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

        for bullet in self.flower_attask_bullets:
            bullet.draw(self.screen)