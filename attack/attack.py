from data_models.moving_direction import MovingDirection
from attack.bullet import Bullet
from attack.explosion import Explosion
# from helper.timer import Timer 
from helper.collision_checker import ColisionChecler
import random, math


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

    def __init__(self, player, keyboard_handler, screen, images_assets_loader, explosion):
        self.images_assets_loader = images_assets_loader
        self.screen = screen
        self.player = player
        self.keyboard_handler = keyboard_handler
        self.explosion = explosion
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.colision_detection = ColisionChecler().colision_detection

    def update(self):
        for bullet in self.bullets:
            if bullet.x < (self.player.x + 500) and bullet.x > (self.player.x + 0):
                bullet.x += bullet.vel
            elif bullet.x < self.player.x and bullet.x > (self.player.x - 500):
                bullet.x += bullet.vel
            else:
                self.bullets.pop(self.bullets.index(bullet))

        if self.keyboard_handler.space_pressed:
            if self.player.last_moving_direction_left_right == MovingDirection.LEFT:
                facing = -1
                initial_x = self.player.x - 10
            else:
                facing = 1
                initial_x = self.player.x + 100
            if len(self.bullets) < 50:
                self.bullets.append(
                    Bullet(initial_x, self.player.y + 50, 6, facing)
                )

        if self.explosion.is_new_explosion:
            player_colision_circle = (self.player.x, self.player.y, self.player.radius)
            bomb_colision_circle = (self.explosion.x, self.explosion.y, self.explosion.bomb_radius)
            if self.colision_detection(player_colision_circle, bomb_colision_circle) and self.explosion.has_to_draw_explosion is False:
                self.explosion.has_to_draw_explosion = True

    def destroy_explosion(self):
        self.explosion.is_new_explosion = False
        self.explosion.has_to_draw_explosion = False

    def create_explosion(self):
        self.explosion.is_new_explosion = True
        self.explosion.has_to_draw_explosion = False
        self.explosion.x = random.randint(0, self.screen_width - 100)
        self.explosion.y = random.randint(0, self.screen_height - 100)

    def draw(self):
        if self.explosion.is_new_explosion is True:
            self.explosion.draw()
            if self.explosion.has_to_draw_explosion:
                # t1 = Timer(2000)
                # if t1.is_time_up():
                self.destroy_explosion()

        if self.explosion.is_new_explosion is False:
            # t2 = Timer(5000)
            # if t2.is_time_up():
            self.create_explosion()

        for bullet in self.bullets:
            bullet.draw(self.screen)