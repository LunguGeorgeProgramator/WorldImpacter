from enemies.enemy import Enemy
from helper.collision_checker import ColisionChecler
import random, math


class Enemies:

    player = None
    enemies = []
    enemies_dead = 0
    max_enemies = 1500
    explosion = None
    colision_detection = None
    images_assets_loader = None

    def __init__(self, screen, images_assets_loader, player, explosion):
        self.images_assets_loader = images_assets_loader
        self.screen = screen
        self.explosion = explosion
        self._crete_enemy_swarm()
        self.colision_detection = ColisionChecler().colision_detection
        self.player = player

    def _crete_enemy_swarm(self):
        for i in range(self.max_enemies):
            multiplier_x = i * random.randint(1, 50)
            multiplier_y = i * random.randint(1, 50)
            self.enemies.append(Enemy(10 + multiplier_x, 10 + multiplier_y, 25, (0, 255, 255), self.screen, self.images_assets_loader))

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

    def draw(self):
        for enemy in self.enemies:
            enemy.draw(self.screen)