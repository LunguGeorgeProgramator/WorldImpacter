
import pygame
from data_models.moving_direction import MovingDirection


class PlayerSkins:

    def __init__(self):
        self.default_skin = {
            MovingDirection.UP : pygame.image.load("assets/player/player-up.png"),
            MovingDirection.DOWN : pygame.image.load("assets/player/player-down.png"),
            MovingDirection.LEFT : pygame.image.load("assets/player/player-left.png"),
            MovingDirection.RIGHT : pygame.image.load("assets/player/player-right.png")
        }
        self.grim_skin = {
            MovingDirection.UP : pygame.image.load("assets/player/new-player-right-front.png"),
            MovingDirection.DOWN : pygame.image.load("assets/player/new-player-left-front.png"),
            MovingDirection.LEFT : pygame.image.load("assets/player/new-player-left-back.png"),
            MovingDirection.RIGHT : pygame.image.load("assets/player/new-player-right-back.png")
        }
        self.diver_skin = {
            MovingDirection.UP : pygame.image.load("assets/player/underwatter-right.png"),
            MovingDirection.DOWN : pygame.image.load("assets/player/underwatter-left.png"),
            MovingDirection.LEFT : pygame.image.load("assets/player/underwatter-left-back.png"),
            MovingDirection.RIGHT : pygame.image.load("assets/player/underwatter-right-back.png")
        }
        self.void_skin = {
            MovingDirection.UP : pygame.image.load("assets/player/void-warrior-right.png"),
            MovingDirection.DOWN : pygame.image.load("assets/player/void-warrior-left.png"),
            MovingDirection.LEFT : pygame.image.load("assets/player/void-warrior-left-back.png"),
            MovingDirection.RIGHT : pygame.image.load("assets/player/void-warrior-right-back.png") 
        }
