import pygame

from data_models.moving_direction import MovingDirection
from data_models.game_state import GameState
from data_models.entities_actions import EntitiesActions

class KeyboardHandler:

    def __init__(self, game_settings):
        self.keys = []
        self.direction = MovingDirection.NONE
        self.last_stopped_moving_direction = MovingDirection.DOWN
        self.last_stopped_left_right_moving_direction = MovingDirection.RIGHT
        self.tracked_keys = [pygame.K_p, pygame.K_n, pygame.K_m, pygame.K_i, pygame.K_h, pygame.K_r, pygame.K_b, pygame.K_1]
        self.pressed_last = {key: False for key in self.tracked_keys}
        self.space_pressed = False
        self.w_pressed = False
        self.s_pressed = False
        self.a_pressed = False
        self.d_pressed = False
        self.key = pygame.key
        self.game_settings = game_settings

    def update(self):
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
            self.last_stopped_left_right_moving_direction = MovingDirection.LEFT
        if self.keys[pygame.K_d]:
            self.direction = MovingDirection.RIGHT
            self.d_pressed = True
            self.last_stopped_moving_direction = MovingDirection.RIGHT
            self.last_stopped_left_right_moving_direction = MovingDirection.RIGHT
        if self.keys[pygame.K_SPACE]:
            self.space_pressed = True
        # check if a key has been pressed, prevent repeating true when continuously pressed, 
        # good for open/close game menus with the same key
        for key in self.tracked_keys:
            if self.keys[key] and not self.pressed_last[key]:
                if key == pygame.K_p and self.game_settings.state != GameState.GAME_OVER:
                    self.game_settings.state = GameState.PAUSE if self.game_settings.state == GameState.RUN else GameState.RUN
                if key == pygame.K_n and self.game_settings.enemies_alive == 0:
                    self.game_settings.game_level = self.game_settings.game_level + 1
                    self.game_settings.state = GameState.NEXT_LEVEL
                if key == pygame.K_n and self.game_settings.enemy_boss_alive == False and self.game_settings.game_level in self.game_settings.eneny_boss_levels:
                    self.game_settings.state = GameState.NEXT_LEVEL
                    self.game_settings.game_level = self.game_settings.game_level + 1
                    self.game_settings.enemy_boss_alive = True
                if key == pygame.K_i and self.game_settings.state in [GameState.RUN, GameState.PAUSE] and self.game_settings.player_action in [EntitiesActions.OPEN_INVENTORY, None]:
                    self.game_settings.player_action = EntitiesActions.OPEN_INVENTORY if self.game_settings.player_action != EntitiesActions.OPEN_INVENTORY else None
                if key == pygame.K_b and self.game_settings.state in [GameState.RUN, GameState.PAUSE] and self.game_settings.player_action in [EntitiesActions.OPEN_SHOP, None]:
                    self.game_settings.player_action = EntitiesActions.OPEN_SHOP if self.game_settings.player_action != EntitiesActions.OPEN_SHOP else None
                if key == pygame.K_h:
                    self.game_settings.player_action = EntitiesActions.OPEN_HELP if self.game_settings.player_action != EntitiesActions.OPEN_HELP else None
                if self.keys[pygame.K_r] and self.game_settings.player_is_alive == False:
                    self.game_settings.state = GameState.RETRY_LEVEL
                if key == pygame.K_1:
                    self.game_settings.player_action = EntitiesActions.CONSUME_HEALING_POTION
            self.pressed_last[key] = self.keys[key]

    def get_movement_direction(self):
        return self.direction

    def get_last_movement_direction(self):
        return self.last_stopped_moving_direction

    def get_last_left_right_direction(self):
        return self.last_stopped_left_right_moving_direction