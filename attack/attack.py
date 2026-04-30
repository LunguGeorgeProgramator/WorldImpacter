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
        self.flower_attack_bullets = []
        self.bullet_radius = 6
        self.max_bullets_per_attack = 1
        self.images_assets_loader = images_assets_loader
        self.screen = screen
        self.player = player
        self.keyboard_handler = keyboard_handler
        self.explosion = explosion
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.colision_detection = CollisionChecKer().colision_detection
        self.wait_time_until_hide_explosion = Timer(20)
        self.wait_time_between_draw_next_bomb = Timer(500)
        self.game_settings = game_settings
        self.percentage_of_player_bullets_multiplier_per_level = 5
        self.num_bullets_flower_attack = 12
        self.speed_flower_attack = 3

    def get_level_attack_multiplier(self, percentage = None):
        if percentage is None:
            percentage = self.percentage_of_player_bullets_multiplier_per_level
        return  self.game_settings.game_level * (percentage / 100)

    def move_bomb_to_random_position(self):
        self.explosion.x = random.randint(0 + 100, self.screen_width - 100) # -100 just to not create the explosion too close to the edge of the screen
        self.explosion.y = random.randint(0 + 100, self.screen_height - 100)

    def update(self):
        self._update_shooting_attack()
        self._update_bomb_explotion_attack()
        self._update_flower_attack()

    def _update_shooting_attack(self):
        level_multiplier = self.get_level_attack_multiplier()

        for bullet in self.bullets:
            max_range = bullet.bullet_max_range
            bullet.vel = math.floor(bullet.bullet_speed + level_multiplier)    
            if bullet.left_right_direction is None:
                bullet.left_right_direction = self.player.last_moving_direction_left_right
            if bullet.left_right_direction == MovingDirection.RIGHT:
                bullet.x += bullet.vel
            else:   
                bullet.x -= bullet.vel
            if bullet.x > (self.player.x + (self.player.radius * 2) + max_range) or bullet.x < (self.player.x - max_range) or bullet.x > self.screen_width or bullet.x < 0:
                self.bullets.pop(self.bullets.index(bullet))

        if self.keyboard_handler.space_pressed:
            if self.player.last_moving_direction_left_right == MovingDirection.LEFT:
                initial_x = self.player.x
            else:
                initial_x = self.player.x + (self.player.radius * 2)
            if len(self.bullets) <= 0:
                for i in range(math.floor(self.max_bullets_per_attack + level_multiplier)):
                    self.bullets.append(
                        Bullet(initial_x, self.player.y + self.player.radius, self.bullet_radius, 0)
                    )

    def _update_bomb_explotion_attack(self):
        if self.game_settings.is_enemy_boss_level() is False:
            self.wait_time_until_hide_explosion.check_cronometer()
            if self.wait_time_until_hide_explosion.trigger_action_at_the_end:
                self.wait_time_between_draw_next_bomb.start_time = True
                self.explosion.has_to_draw_explosion = False
                self.wait_time_until_hide_explosion.start_time = False

            self.wait_time_between_draw_next_bomb.check_cronometer()
            if self.wait_time_between_draw_next_bomb.trigger_action_at_the_end:
                self.wait_time_between_draw_next_bomb.start_time = False
                self.move_bomb_to_random_position()
                self.explosion.has_to_draw_bomb = True
                self.explosion.has_to_draw_explosion = False
                
            if self.explosion.has_to_draw_bomb:
                player_colision_circle = (self.player.x, self.player.y, self.player.radius)
                bomb_colision_circle = (self.explosion.x - self.explosion.bomb_width, self.explosion.y - self.explosion.bomb_height, self.explosion.bomb_radius)
                if self.colision_detection(player_colision_circle, bomb_colision_circle):
                    self.explosion.has_to_draw_explosion = True
                    self.explosion.has_to_draw_bomb = False
                    self.wait_time_until_hide_explosion.start_time = True

    def _update_flower_attack(self):
        for bullet in self.flower_attack_bullets:
            bullet.x += bullet.vx
            bullet.y += bullet.vy
            if bullet.x > self.screen_width or bullet.x < 0 or bullet.y > self.screen_height or bullet.y < 0:
                self.flower_attack_bullets.pop(self.flower_attack_bullets.index(bullet))

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
                self.flower_attack_bullets.append(bullet)

    def draw(self):
        # Draw explosion/bomb
        if self.game_settings.is_enemy_boss_level() is False:
            if self.explosion.has_to_draw_bomb:
                self.explosion.draw_bomb()
            if self.explosion.has_to_draw_explosion:
                self.explosion.draw_explosion()

        # Draw bullets from shooting attack
        for bullet in self.bullets:
            if bullet.destroied is False:
                bullet.draw(self.screen)

        # Draw bullets from flower attack
        for bullet in self.flower_attack_bullets:
            bullet.draw(self.screen)