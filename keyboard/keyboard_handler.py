import pygame

from data_models.moving_direction import MovingDirection

class KeyboardHandler:

    key = []
    keys = []
    direction = MovingDirection.NONE
    last_stopped_moving_direction = MovingDirection.DOWN
    space_pressed = False
    w_pressed = False
    s_pressed = False
    a_pressed = False
    d_pressed = False

    def __init__(self):
        self.key = pygame.key

    def update_keys(self):
        self.space_pressed = False
        self.w_pressed = False
        self.s_pressed = False
        self.a_pressed = False
        self.d_pressed = False
        self.direction = None

        self.keys = self.key.get_pressed()
        if self.keys[pygame.K_w]:
            self.direction = MovingDirection.UP
            self.w_pressed = True
            self.last_stopped_moving_direction = MovingDirection.UP
        if self.keys[pygame.K_s]:
            self.direction = MovingDirection.DOWN
            self.s_pressed = True
            self.last_stopped_moving_direction = MovingDirection.DOWN
        if self.keys[pygame.K_a]:
            self.direction = MovingDirection.LEFT
            self.a_pressed = True
            self.last_stopped_moving_direction = MovingDirection.LEFT
        if self.keys[pygame.K_d]:
            self.direction = MovingDirection.RIGHT
            self.d_pressed = True
            self.last_stopped_moving_direction = MovingDirection.RIGHT
        if self.keys[pygame.K_SPACE]:
            self.space_pressed = True


    def get_movement_direction(self):
        return self.direction

    def get_last_movement_direction(self):
        return self.last_stopped_moving_direction