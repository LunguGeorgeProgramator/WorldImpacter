import pygame
from data_models.moving_direction import MovingDirection

class Player:

    keyboard_handler = None
    color = "white"
    pos = None
    screen = None
    keyPressed = None
    direction = None
    attack_speed = None
    last_moving_direction = None

    def __init__(self, screen, keyboard_handler):
        self.screen = screen
        self.keyboard_handler = keyboard_handler
        self.player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
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
        self.player_pos = self._move_vector_x_y(self.player_pos, self.direction, 300 * dt)
        self.attack_speed = 3000 * dt
        if self.keyboard_handler.space_pressed:
            self.draw_attack()

    def draw_player(self):
        pygame.draw.circle(self.screen, self.color, self.player_pos, 40)

    def draw_attack(self):
        max_distance = 10
        while max_distance > 0:
            max_distance -= 1
            self.pos = self._move_vector_x_y(self.pos, self.last_moving_direction, self.attack_speed)
            pygame.draw.circle(self.screen, "red", self.pos, 40)
        else:
            self.pos.x = self.player_pos.x
            self.pos.y = self.player_pos.y