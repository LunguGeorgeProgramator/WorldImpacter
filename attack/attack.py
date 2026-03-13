from data_models.moving_direction import MovingDirection
from attack.bullet import Bullet


class Attack:

    bullets = []
    player = None
    keyboard_handler = None
    screen = None

    def __init__(self, player, keyboard_handler, screen):
        self.screen = screen
        self.player = player
        self.keyboard_handler = keyboard_handler

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
                    Bullet(initial_x, self.player.y + 50, 6, (0, 0, 0), facing)
                )

    def draw(self):
        for bullet in self.bullets:
            bullet.draw(self.screen)