from enemies.enemy import Enemy
from helper.collision_checker import CollisionChecKer
from data_models.game_state import GameState
import random, math


class Enemies:

    player = None
    attack = None
    enemies = []
    enemies_dead = 0
    max_enemies = 300
    max_enemies_per_level = 10
    explosion = None
    colision_detection = None
    images_assets_loader = None
    game_settings = None

    def __init__(self, screen, images_assets_loader, player, attack, explosion, game_settings):
        self.game_settings = game_settings
        self.attack = attack
        self.images_assets_loader = images_assets_loader
        self.max_enemies = self.game_settings.game_level * self.max_enemies_per_level
        self.screen = screen
        self.explosion = explosion
        self._crete_enemy_swarm()
        self.colision_detection = CollisionChecKer().colision_detection
        self.player = player

    def _crete_enemy_swarm(self):
        for i in range(self.max_enemies):
            multiplier_x = random.randint(0, self.screen.get_width())
            multiplier_y = random.randint(0, self.screen.get_height())
            self.enemies.append(Enemy(10 + multiplier_x, 10 + multiplier_y, 25, self.screen, self.images_assets_loader))

    def next_level(self):
        self.attack.bullets = []
        self.player.x = self.screen.get_width() / 2
        self.player.y = self.screen.get_height() / 2
        self.player.health = self.player.max_health
        self.max_enemies = self.game_settings.game_level * self.max_enemies_per_level
        self.enemies_dead = 0
        self._crete_enemy_swarm()

    def update(self):
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
            for bullet in self.attack.bullets:
                bullet_colision_circle = (bullet.x, bullet.y, bullet.radius)
                if self.colision_detection(bullet_colision_circle, enemy_colision_circle):
                    if enemy.is_alive:
                        enemy.is_alive = False
                        self.enemies_dead += 1
            if not enemy.is_alive:
                self.enemies.remove(enemy)
        if len(self.enemies) == 0:
            self.game_settings.state = GameState.GAME_OVER
        self.game_settings.enemies_alive = len(self.enemies)

    def draw(self):
        for enemy in self.enemies:
            enemy.draw(self.screen)