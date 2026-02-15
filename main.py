# Example file showing a circle moving on screen
import pygame
from keyboard.keyboard_handler import KeyboardHandler
from player.player import Player

# pygame setup
pygame.init()

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("World Impacter")
clock = pygame.time.Clock()
running = True
dt = 0

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


    keyboard_handler.update_keys()
    player.update_player(dt)
    player.draw_player()


    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 120
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(120) / 1000

pygame.quit()