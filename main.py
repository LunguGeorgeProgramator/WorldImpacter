# Example file showing a circle moving on screen
import pygame

from data_models.moving_direction import MovingDirection
from keyboard.keyboard_handler import KeyboardHandler
from player.bullets import Bullet
from player.player import Player

# pygame setup
pygame.init()

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("World Impacter")
clock = pygame.time.Clock()
running = True
dt = 0
bullets = []

keyboard_handler = KeyboardHandler()
player = Player(screen, keyboard_handler)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("green")

    for bullet in bullets:
        if bullet.x < (player.x + 500) and bullet.x > (player.x + 0):
            bullet.x += bullet.vel
        elif bullet.x < player.x and bullet.x > (player.x - 500):
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    if keyboard_handler.space_pressed:
        if player.last_moving_direction_left_right == MovingDirection.LEFT:
            facing = -1
        else:
            facing = 1
        if len(bullets) < 50:
            bullets.append(
                Bullet(player.x, player.y, 6, (0, 0, 0), facing)
            )

    keyboard_handler.update_keys()
    player.update(dt)
    player.draw()

    for bullet in bullets:
        bullet.draw(screen)

    # flip() the display to put your work on screen
    pygame.display.flip()
    # pygame.display.update()

    # limits FPS to 120
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()