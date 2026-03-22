import pygame
from enemies.enemy import Enemy


class EnemyBoss(Enemy):

    health_colors_dict = {
        "full_health": (100, 0, 0),
        "low_health": (0, 200, 0),
        "border": (255,255,255)
    }
    bar_width = 200
    bar_height = 20
    health = 1000
    max_health = 1000
    screen = None
    damage_to_player = 5

    def __init__(self, x, y, radius, screen, images_assets_loader):
        super().__init__(x, y, radius, screen, images_assets_loader)
        self.screen = screen

    def draw(self, win):
        if self.is_alive:
            self.images_assets_loader.draw(self.images_assets_loader.enemy_boss_image, self.x, self.y, self.default_image_width, self.default_image_height)
            self._draw_health_bar()
    
    def _draw_health_bar(self):
        x = self.x
        y = self.y - (self.radius / 3)
        ratio = self.health / self.max_health
        pygame.draw.rect(self.screen, self.health_colors_dict["full_health"], (x, y, self.bar_width, self.bar_height))
        pygame.draw.rect(self.screen, self.health_colors_dict["low_health"], (x, y, self.bar_width * ratio, self.bar_height))
        pygame.draw.rect(self.screen, self.health_colors_dict["border"], (x, y, self.bar_width, self.bar_height), 2)