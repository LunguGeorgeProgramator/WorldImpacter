import pygame


class ImagesAssetsLoader:

    default_image_height = 100
    default_image_width = 100
    player_up_image = None
    player_down_image = None
    player_left_image = None
    player_right_image = None
    enemies_image = None
    screen = None
    explosion = None
    bomb = None

    def __init__(self, screen):
        self.screen = screen
        self.player_up_image = pygame.image.load("assets/player/player-up.png")
        self.player_down_image = pygame.image.load("assets/player/player-down.png")
        self.player_left_image = pygame.image.load("assets/player/player-left.png")
        self.player_right_image = pygame.image.load("assets/player/player-right.png")
        self.enemies_image = pygame.image.load("assets/enemies/evil-sphere.png")
        self.explosion = pygame.image.load("assets/attacks/explosion-s.png")
        self.bomb = pygame.image.load("assets/attacks/red-bomb.png")

    def draw(self, loaded_image, x = 0, y = 0, width = None, height = None):
        width = width if width else self.default_image_width
        height = height if height else self.default_image_height
        image = pygame.transform.scale(loaded_image, (width, height))
        return self.screen.blit(image, (x, y))
        