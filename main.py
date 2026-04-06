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
from inventory.inventory import Inventory

# pygame setup
pygame.init()
game_settings = GameSettings()

screen = pygame.display.set_mode((game_settings.width, game_settings.height))

translator = Translator('en')  # ro - romanian, en - english

pygame.display.set_caption(translator.get_message('title'))
clock = pygame.time.Clock()
running = True
dt = 0
text_size = game_settings.text_size if translator.locale == 'en' else game_settings.text_size_small
game_settings.game_text_font = pygame.font.SysFont(game_settings.font_name, text_size)

player_inventory = Inventory()
images_assets_loader = ImagesAssetsLoader(screen)
keyboard_handler = KeyboardHandler(game_settings)
player = Player(screen, keyboard_handler, images_assets_loader, game_settings, player_inventory)
explosion = explosion.Explosion(game_settings, images_assets_loader)
attack = attack.Attack(player, keyboard_handler, screen, images_assets_loader, explosion, game_settings)
enemies = Enemies(screen, images_assets_loader, player, attack, explosion, game_settings)
game_interface = GameInterface(screen, game_settings.game_text_font, player, enemies, translator, game_settings)


game_settings.state = GameState.PAUSE # initial state
while running:

    # fill the screen with a color to wipe away anything from last frame
    # screen.fill("green")
    if game_settings.game_level in game_settings.haven_levels:
        bg_image = images_assets_loader.haven_bg
    else:
        bg_image = images_assets_loader.fire_pit_bg
    screen.blit(bg_image, (0, 0))

    keyboard_handler.update()

    if game_settings.state == GameState.RETRY_LEVEL and game_settings.player_is_alive == False: 
        game_settings.state = GameState.RUN
        enemies.retry_level()

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