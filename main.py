# Example file showing a circle moving on screen
import pygame

from keyboard.keyboard_handler import KeyboardHandler
from attack.attack import Attack
from player.player import Player
from enemies.enemies import Enemies
from player_ui.game_menu import GameMenu

# pygame setup
pygame.init()

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("World Impacter")
clock = pygame.time.Clock()
running = True
dt = 0
font = pygame.font.SysFont('Arial', 36)

keyboard_handler = KeyboardHandler()
player = Player(screen, keyboard_handler)
attack = Attack(player, keyboard_handler, screen)
enemies = Enemies(screen)
game_menu = GameMenu(screen, font)

while running:

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("green")

    keyboard_handler.update()
    player.update(dt)
    attack.update()
    enemies.update(attack.bullets)

    enemies.draw()
    player.draw()
    attack.draw()
    if enemies.enemies_dead == enemies.max_enemies:
        game_menu.draw()
    game_menu.draw_scoring(enemies.enemies_dead)

    running = game_menu.not_exit_game()

    # flip() the display to put your work on screen
    # pygame.display.flip()
    pygame.display.update()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()