import pygame

from data_models.moving_direction import MovingDirection
from data_models.game_state import GameState

class KeyboardHandler:

    key = []
    keys = []
    game_settings = None
    direction = MovingDirection.NONE
    last_stopped_moving_direction = MovingDirection.DOWN
    last_stopped_left_right_moving_direction = MovingDirection.RIGHT
    tracked_keys = [pygame.K_p, pygame.K_m, pygame.K_i]
    pressed_last = {key: False for key in tracked_keys}
    space_pressed = False
    w_pressed = False
    s_pressed = False
    a_pressed = False
    d_pressed = False
    p_pressed = False

    def __init__(self, game_settings):
        self.key = pygame.key
        self.game_settings = game_settings

    def update(self):
        self.space_pressed = False
        self.w_pressed = False
        self.s_pressed = False
        self.a_pressed = False
        self.d_pressed = False
        self.p_pressed = False
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
            self.last_stopped_left_right_moving_direction = MovingDirection.LEFT
        if self.keys[pygame.K_d]:
            self.direction = MovingDirection.RIGHT
            self.d_pressed = True
            self.last_stopped_moving_direction = MovingDirection.RIGHT
            self.last_stopped_left_right_moving_direction = MovingDirection.RIGHT
        if self.keys[pygame.K_SPACE]:
            self.space_pressed = True
        if self.keys[pygame.K_p]:
            self.p_pressed = True
        # check if a key has been pressed, prevent repeating true when continuously pressed, 
        # good for open/close game menus with the same key
        for key in self.tracked_keys:
            if self.keys[key] and not self.pressed_last[key]:
                if key == pygame.K_p:
                    self.game_settings.state = GameState.PAUSE if self.game_settings.state == GameState.RUN else GameState.RUN
            self.pressed_last[key] = self.keys[key]

    def get_movement_direction(self):
        return self.direction

    def get_last_movement_direction(self):
        return self.last_stopped_moving_direction

    def get_last_left_right_direction(self):
        return self.last_stopped_left_right_moving_direction