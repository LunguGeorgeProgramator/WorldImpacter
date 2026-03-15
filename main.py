# Example file showing a circle moving on screen
import pygame

from keyboard.keyboard_handler import KeyboardHandler
from attack.attack import Attack
from player.player import Player
from enemies.enemies import Enemies
from game_interface.game_interface import GameInterface
from assets.images_assets_loader import ImagesAssetsLoader

# pygame setup
pygame.init()

screen = pygame.display.set_mode((1280, 720))
bg_image = pygame.image.load("assets/fire_pit.png").convert()
bg_image = pygame.transform.scale(bg_image, (1280, 720))

pygame.display.set_caption("World Impacter")
clock = pygame.time.Clock()
running = True
dt = 0
font = pygame.font.SysFont('Arial', 36)

images_assets_loader = ImagesAssetsLoader(screen)
keyboard_handler = KeyboardHandler()
player = Player(screen, keyboard_handler, images_assets_loader)
attack = Attack(player, keyboard_handler, screen)
enemies = Enemies(screen, images_assets_loader, player)
game_interface = GameInterface(screen, font, player, enemies)

while running:

    # fill the screen with a color to wipe away anything from last frame
    # screen.fill("green")
    screen.blit(bg_image, (0, 0))

    if player.is_alive and len(enemies.enemies) > 0:
        keyboard_handler.update()
        player.update(dt)
        attack.update()
        enemies.update(attack.bullets)

    enemies.draw()
    player.draw()
    attack.draw()
    game_interface.draw()

    running = game_interface.not_exit_game()

    # flip() the display to put your work on screen
    # pygame.display.flip()
    pygame.display.update()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()