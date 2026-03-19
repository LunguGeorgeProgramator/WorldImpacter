from enemies.enemy import Enemy
import random, math


class Enemies:

    player = None
    enemies = []
    enemies_dead = 0
    max_enemies = 250
    explosion = None

    def __init__(self, screen, images_assets_loader, player, explosion):
        self.screen = screen
        self.explosion = explosion
        for i in range(self.max_enemies):
            self.player = player
            multiplier_x = i * random.randint(1, 50)
            multiplier_y = i * random.randint(1, 50)
            self.enemies.append(Enemy(10 + multiplier_x, 10 + multiplier_y, 25, (0, 255, 255), screen, images_assets_loader))

    def update(self, bullets):
        player_colision_circle = (self.player.x, self.player.y, self.player.radius)
        for enemy in self.enemies:
            enemy.update()
            enemy_colision_circle = (enemy.x, enemy.y, enemy.radius)
            explosion_colision_circle = (self.explosion.x, self.explosion.y, self.explosion.explosion_radius)
            if self.colision_detection(explosion_colision_circle, enemy_colision_circle) and self.explosion.has_to_draw_explosion:
                if enemy.is_alive:
                    enemy.is_alive = False
                    self.enemies_dead += 1
            if self.colision_detection(enemy_colision_circle, player_colision_circle) and enemy.is_alive and self.player.is_alive:
                self.player.health -= 1
            for bullet in bullets:
                bullet_colision_circle = (bullet.x, bullet.y, bullet.radius)
                if self.colision_detection(bullet_colision_circle, enemy_colision_circle):
                    if enemy.is_alive:
                        enemy.is_alive = False
                        self.enemies_dead += 1
            if not enemy.is_alive:
                self.enemies.remove(enemy)
               

    def colision_detection(self, c1, c2):
        x1, y1, r1 = c1
        x2, y2, r2 = c2
        distance = math.hypot(x2 - x1, y2 - y1)
        return distance <= (r1 + r2)

    def draw(self):
        for enemy in self.enemies:
            enemy.draw(self.screen)