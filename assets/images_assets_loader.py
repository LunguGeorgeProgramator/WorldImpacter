import pygame
from assets.player_skins import PlayerSkins
from assets.enemies_skins import EnemiesSkins


class ImagesAssetsLoader:

    def __init__(self, screen):
        self.default_image_height = 100
        self.default_image_width = 100
        self.screen = screen
        self.screen_width, self.screen_height = self.screen.get_size()
        self.explosion = pygame.image.load("assets/attacks/explosion-s.png")
        self.haven_explosion = pygame.image.load("assets/attacks/holly_explosion_mini.png")
        self.bomb = pygame.image.load("assets/attacks/red-bomb.png")
        self.haven_bomb = pygame.image.load("assets/attacks/gold-bomb.png")
        self.fire_pit_bg = self.draw_game_background("assets/back-grounds/fire-pit-bg.png")
        self.haven_bg = self.draw_game_background("assets/back-grounds/haven-bg.png")
        self.underwater_bg = self.draw_game_background("assets/back-grounds/underwater-bg.png")
        self.void_bg = self.draw_game_background("assets/back-grounds/dark-void-bg.png")
        self.player_skins = PlayerSkins()
        self.enemies_skins = EnemiesSkins()

    def draw(self, loaded_image, x = 0, y = 0, width = None, height = None):
        width = width if width else self.default_image_width
        height = height if height else self.default_image_height
        image = pygame.transform.scale(loaded_image, (width, height))
        return self.screen.blit(image, (x, y))
    
    def draw_game_background(self, background_path):
        bg_image = pygame.image.load(background_path).convert()
        return pygame.transform.scale(bg_image, (self.screen_width, self.screen_height))    
        