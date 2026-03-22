from enemies.enemy import Enemy
from enemies.enemy_boss import EnemyBoss
from helper.collision_checker import CollisionChecKer
from data_models.game_state import GameState
import random, math
import pygame


class Enemies:

    player = None
    attack = None
    enemy_boss = None
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
        self._increase_max_enemies_by_level()
        self.screen = screen
        self.explosion = explosion
        self._crete_enemy_swarm()
        self.colision_detection = CollisionChecKer().colision_detection
        self.player = player
        self.enemy_boss = EnemyBoss(400, 400, 100, self.screen, self.images_assets_loader)

    def _crete_enemy_swarm(self):
        if self.game_settings.game_level not in self.game_settings.eneny_boss_levels:
            for i in range(self.max_enemies):
                multiplier_x = random.randint(0, self.screen.get_width())
                multiplier_y = random.randint(0, self.screen.get_height())
                self.enemies.append(Enemy(10 + multiplier_x, 10 + multiplier_y, 25, self.screen, self.images_assets_loader))

    def _increase_max_enemies_by_level(self):
        if self.game_settings.game_level not in self.game_settings.eneny_boss_levels:
            self.max_enemies = self.game_settings.game_level * self.max_enemies_per_level
        else:
            self.max_enemies = 1

    def next_level(self):
        self.attack.bullets = []
        self.player.x = self.screen.get_width() / 2
        self.player.y = self.screen.get_height() / 2
        self.player.health = self.player.max_health
        self._increase_max_enemies_by_level()
        self.enemies_dead = 0
        self._crete_enemy_swarm()
        self.enemy_boss.is_alive = True
        self.enemy_boss.health = self.enemy_boss.max_health

    def update(self):
        player_colision_circle = (self.player.x + self.player.radius, self.player.y + self.player.radius, self.player.radius)
        # pygame.draw.circle(self.screen, (255, 0, 0), (self.player.x + self.player.radius, self.player.y + self.player.radius), self.player.radius)
        if self.game_settings.game_level in self.game_settings.eneny_boss_levels:
            self._update_boss_enemies(player_colision_circle)
        else:
            self._update_none_boss_enemies(player_colision_circle)

    def _update_boss_enemies(self, player_colision_circle):
        self.enemy_boss.update()
        # pygame.draw.circle(self.screen, (255, 0, 0), (self.enemy_boss.x + self.enemy_boss.radius, self.enemy_boss.y + self.enemy_boss.radius), self.enemy_boss.radius)
        enemy_boss_colision_circle = (self.enemy_boss.x + self.enemy_boss.radius, self.enemy_boss.y + self.enemy_boss.radius, self.enemy_boss.radius)
        for bullet in self.attack.bullets:
            bullet_colision_circle = (bullet.x, bullet.y, bullet.radius)
            if self.colision_detection(bullet_colision_circle, enemy_boss_colision_circle):
                if self.enemy_boss.is_alive:
                    self.enemy_boss.health -= 1
        if self.enemy_boss.health <= 0:
            self.enemy_boss.is_alive = False
            self.game_settings.enemy_boss_alive = False
        if self.colision_detection(enemy_boss_colision_circle, player_colision_circle) and self.enemy_boss.is_alive and self.player.is_alive:
            self.player.health -= self.enemy_boss.damage_to_player
        if not self.enemy_boss.is_alive:
            self.game_settings.state = GameState.GAME_OVER
    
    def _update_none_boss_enemies(self, player_colision_circle):
        for enemy in self.enemies:
            enemy.update()
            enemy_colision_circle = (enemy.x + enemy.radius, enemy.y + enemy.radius, enemy.radius)
            # pygame.draw.circle(self.screen, (255, 0, 0), (enemy.x + enemy.radius, enemy.y + enemy.radius), enemy.radius)
            explosion_colision_circle = (self.explosion.x, self.explosion.y, self.explosion.explosion_radius)
            # pygame.draw.circle(self.screen, (255, 0, 0), (self.explosion.x, self.explosion.y), self.explosion.explosion_radius)
            if self.colision_detection(explosion_colision_circle, enemy_colision_circle) and self.explosion.has_to_draw_explosion:
                if enemy.is_alive:
                    enemy.is_alive = False
                    self.enemies_dead += 1
            if self.colision_detection(enemy_colision_circle, player_colision_circle) and enemy.is_alive and self.player.is_alive:
                self.player.health -= enemy.damage_to_player
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
        if self.game_settings.game_level in self.game_settings.eneny_boss_levels:
            self._draw_boss_enemies()
        else:
            self._draw_none_boss_enemies()

    def _draw_boss_enemies(self):
        self.enemy_boss.draw(self.screen)

    def _draw_none_boss_enemies(self):
        for enemy in self.enemies:
            enemy.draw(self.screen)