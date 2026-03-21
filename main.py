import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

# Example file showing a circle moving on screen
import pygame

from keyboard.keyboard_handler import KeyboardHandler
from attack import attack, explosion
from player.player import Player
from enemies.enemies import Enemies
from game_interface.game_interface import GameInterface
from assets.images_assets_loader import ImagesAssetsLoader
from translate.translator import Translator
from data_models.game_state import GameState
from game_settings import GameSettings

# pygame setup
pygame.init()
game_settings = GameSettings()

screen = pygame.display.set_mode((game_settings.width, game_settings.height))
bg_image = pygame.image.load("assets/fire_pit.png").convert()
bg_image = pygame.transform.scale(bg_image, (game_settings.width, game_settings.height))

translator = Translator('en')  # ro - romanian, en - english

pygame.display.set_caption(translator.get_message('title'))
clock = pygame.time.Clock()
running = True
dt = 0
font = pygame.font.SysFont(game_settings.font_name, game_settings.text_size)

images_assets_loader = ImagesAssetsLoader(screen)
keyboard_handler = KeyboardHandler(game_settings)
player = Player(screen, keyboard_handler, images_assets_loader, game_settings)
explosion = explosion.Explosion(images_assets_loader)
attack = attack.Attack(player, keyboard_handler, screen, images_assets_loader, explosion)
enemies = Enemies(screen, images_assets_loader, player, attack, explosion, game_settings)
game_interface = GameInterface(screen, font, player, enemies, translator, game_settings)

game_settings.state = GameState.PAUSE # initial state
while running:

    # fill the screen with a color to wipe away anything from last frame
    # screen.fill("green")
    screen.blit(bg_image, (0, 0))

    keyboard_handler.update()

    if game_settings.state == GameState.NEXT_LEVEL:
        enemies.next_level()
        game_settings.state = GameState.RUN

    if game_settings.state not in [GameState.PAUSE, GameState.GAME_OVER]:
        player.update(dt)
        attack.update()
        enemies.update()

    enemies.draw()
    attack.draw()
    player.draw()
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