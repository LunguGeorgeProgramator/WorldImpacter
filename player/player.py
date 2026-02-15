import pygame
from data_models.moving_direction import MovingDirection

class Player:

    keyboard_handler = None
    color = "white"
    player_pos = None
    screen = None
    keyPressed = None
    direction = None
    do_it = True
    attack_speed = None
    last_moving_direction = None

    def __init__(self, screen, keyboard_handler):
        self.screen = screen
        self.keyboard_handler = keyboard_handler
        self.player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

    def update_player(self, dt):
        self.direction = self.keyboard_handler.get_movement_direction()
        self.last_moving_direction = self.keyboard_handler.get_last_movement_direction()

        if self.direction == MovingDirection.UP:
            self.color = "black"
            self.player_pos.y -= 300 * dt
        elif self.direction == MovingDirection.DOWN:
            self.player_pos.y += 300 * dt
            self.color = "blue"
        elif self.direction == MovingDirection.LEFT:
            self.player_pos.x -= 300 * dt
            self.color = "grey"
        elif self.direction == MovingDirection.RIGHT:
            self.player_pos.x += 300 * dt
            self.color = "yellow"

        self.attack_speed = 1000 * dt
        if self.keyboard_handler.space_pressed:
            self.draw_attack(self.player_pos)

    def draw_player(self):
        pygame.draw.circle(self.screen, self.color, self.player_pos, 40)


    def draw_attack(self, player_pos):
        duration_counter = 100000
        if self.do_it:
            x = player_pos.x
            y = player_pos.y
            pos = pygame.Vector2(x, y)

            while duration_counter > 0:
                duration_counter -= 1


                if self.last_moving_direction == MovingDirection.UP:
                    pos.y -= self.attack_speed
                elif self.last_moving_direction == MovingDirection.DOWN:
                    pos.y += self.attack_speed
                elif self.last_moving_direction == MovingDirection.LEFT:
                    pos.x -= self.attack_speed
                elif self.last_moving_direction == MovingDirection.RIGHT:
                    pos.x += self.attack_speed


                pygame.draw.circle(self.screen, "red", pos , 40)
                self.do_it = False
                if duration_counter == 0:
                    self.do_it = True