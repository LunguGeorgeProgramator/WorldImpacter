import pygame
from data_models.moving_direction import MovingDirection

class Player:

    keyboard_handler = None
    color = "white"
    pos = None
    screen = None
    keyPressed = None
    direction = None
    last_moving_direction = None
    last_moving_direction_left_right = None
    x = 0
    y = 0
    with_p = 0
    height_p = 0

    def __init__(self, screen, keyboard_handler):
        self.screen = screen
        self.keyboard_handler = keyboard_handler
        self.player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
        self.with_p = screen.get_width() / 2
        self.height_p = screen.get_height() / 2
        self.pos = pygame.Vector2(self.player_pos.x, self.player_pos.y)

    def _move_vector_x_y(self, vector_pos, direction, speed):
        if direction == MovingDirection.UP:
            self.color = "black"
            vector_pos.y -= speed
        elif direction == MovingDirection.DOWN:
            vector_pos.y += speed
            self.color = "blue"
        elif direction == MovingDirection.LEFT:
            vector_pos.x -= speed
            self.color = "grey"
        elif direction == MovingDirection.RIGHT:
            vector_pos.x += speed
            self.color = "yellow"
        return vector_pos

    def update_player(self, dt):
        self.direction = self.keyboard_handler.get_movement_direction()
        self.last_moving_direction = self.keyboard_handler.get_last_movement_direction()
        self.last_moving_direction_left_right = self.keyboard_handler.get_last_left_right_direction()
        # self.player_pos = self._move_vector_x_y(self.player_pos, self.direction, 30)
        self.player_pos = self._move_vector_x_y(self.player_pos, self.direction, 150 * dt)
        self.x = self.player_pos.x
        self.y = self.player_pos.y

    def draw_player(self):
        pygame.draw.circle(self.screen, self.color, self.player_pos, 40)