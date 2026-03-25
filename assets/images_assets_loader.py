import pygame


class ImagesAssetsLoader:

    def __init__(self, screen):
        self.default_image_height = 100
        self.default_image_width = 100
        self.screen = screen
        self.player_up_image = pygame.image.load("assets/player/player-up.png")
        self.player_down_image = pygame.image.load("assets/player/player-down.png")
        self.player_left_image = pygame.image.load("assets/player/player-left.png")
        self.player_right_image = pygame.image.load("assets/player/player-right.png")
        self.enemies_image = pygame.image.load("assets/enemies/evil-sphere.png")
        self.enemies_image_frame_two = pygame.image.load("assets/enemies/evil-sphere-frame-two.png")
        self.enemy_boss_image = pygame.image.load("assets/enemies/boos-shere-1.png")
        self.enemy_boss_frame_two_image = pygame.image.load("assets/enemies/boos-shere-2.png")
        self.enemy_boss_frame_three_image = pygame.image.load("assets/enemies/boos-shere-3.png")
        self.enemy_boss_frame_four_image = pygame.image.load("assets/enemies/boos-shere-4.png")
        self.explosion = pygame.image.load("assets/attacks/explosion-s.png")
        self.bomb = pygame.image.load("assets/attacks/red-bomb.png")

    def draw(self, loaded_image, x = 0, y = 0, width = None, height = None):
        width = width if width else self.default_image_width
        height = height if height else self.default_image_height
        image = pygame.transform.scale(loaded_image, (width, height))
        return self.screen.blit(image, (x, y))
        