from enemies.enemy import Enemy
import random, math


class Enemies:

    enemies = []
    enemies_dead = 0
    max_enemies = 50

    def __init__(self, screen, images_assets_loader):
        self.screen = screen
        for i in range(self.max_enemies):
            multiplier_x = i * random.randint(1, 50)
            multiplier_y = i * random.randint(1, 50)
            self.enemies.append(Enemy(10 + multiplier_x, 10 + multiplier_y, 25, (0, 255, 255), screen, images_assets_loader))

    def update(self, bullets):
        for enemy in self.enemies:
            enemy.update()
            for bullet in bullets:
                c1 = (bullet.x, bullet.y, bullet.radius)
                c2 = (enemy.x, enemy.y, enemy.radius)
                if self.colision_detection(c1, c2):
                    if enemy.is_alive:
                        enemy.is_alive = False
                        self.enemies_dead += 1

    def colision_detection(self, c1, c2):
        x1, y1, r1 = c1
        x2, y2, r2 = c2
        distance = math.hypot(x2 - x1, y2 - y1)
        return distance <= (r1 + r2)

    def draw(self):
        for enemy in self.enemies:
            enemy.draw(self.screen)