import pygame
from data_models.moving_direction import MovingDirection

class Player:

    keyboard_handler = None
    images_assets_loader = None
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
    is_player_out_of_screen = False
    screen_x = 0
    screen_y = 0
    radius = 50
    health = 1000
    max_health = 1000
    is_alive = True

    def __init__(self, screen, keyboard_handler, images_assets_loader):
        self.images_assets_loader = images_assets_loader
        self.screen = screen
        self.keyboard_handler = keyboard_handler
        self.player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
        self.with_p = screen.get_width() / 2
        self.height_p = screen.get_height() / 2
        self.pos = pygame.Vector2(self.player_pos.x, self.player_pos.y)
        self.screen_x, self.screen_y = screen.get_size()

    def _move_vector_x_y(self, vector_pos, direction, speed):
        is_out_of_scrren_left = self.player_pos.x < 0
        is_out_of_scrren_right = self.player_pos.x > self.screen_x - 100
        is_out_of_scrren_top = self.player_pos.y < 0
        is_out_of_scrren_down = self.player_pos.y > self.screen_y - 100
        if direction == MovingDirection.UP and is_out_of_scrren_top is False:
            self.color = "black"
            vector_pos.y -= speed
        elif direction == MovingDirection.DOWN and is_out_of_scrren_down is False:
            vector_pos.y += speed
            self.color = "blue"
        elif direction == MovingDirection.LEFT and is_out_of_scrren_left is False:
            vector_pos.x -= speed
            self.color = "grey"
        elif direction == MovingDirection.RIGHT and is_out_of_scrren_right is False:
            vector_pos.x += speed
            self.color = "yellow"
        return vector_pos

    def update(self, dt):
        self.direction = self.keyboard_handler.get_movement_direction()
        self.last_moving_direction = self.keyboard_handler.get_last_movement_direction()
        self.last_moving_direction_left_right = self.keyboard_handler.get_last_left_right_direction()
        self.player_pos = self._move_vector_x_y(self.player_pos, self.direction, 5)
        # self.player_pos = self._move_vector_x_y(self.player_pos, self.direction, 300 * dt)
        self.x = self.player_pos.x
        self.y = self.player_pos.y
        if self.health <= 0:
            self.is_alive = False

    def draw(self):
        if self.last_moving_direction == MovingDirection.UP:
            player_image = self.images_assets_loader.player_up_image
        elif self.last_moving_direction == MovingDirection.DOWN:
            player_image = self.images_assets_loader.player_down_image
        elif self.last_moving_direction == MovingDirection.LEFT:
            player_image = self.images_assets_loader.player_left_image
        elif self.last_moving_direction == MovingDirection.RIGHT:
            player_image = self.images_assets_loader.player_right_image
        self.images_assets_loader.draw(player_image, self.player_pos.x, self.player_pos.y)