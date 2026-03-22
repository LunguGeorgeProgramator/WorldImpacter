import pygame
from translate.translator import Translator
from data_models.game_state import GameState

class GameInterface(pygame.sprite.Sprite):

    player = None
    enemies = None
    screen = None
    continue_button_color = (0, 255, 0)
    button_color = (200, 0, 0)
    button_hover = (255, 0, 0)
    health_colors_dict = {
        "full_health": (100, 0, 0),
        "low_health": (0, 200, 0),
        "border": (255,255,255)
    }
    bar_width = 200
    bar_height = 20
    health_x = 20
    health_y = 20
    text_color = None
    button_exit_rect = None
    button_exit_w = 120
    button_exit_h = 50
    button_exit_x = -200
    button_exit_y = 0
    button_continue_rect = None
    button_continue_w = 170
    button_continue_h = 50
    button_continue_x = -200
    button_continue_y = -75
    button_next_level_rect = None
    button_next_level_w = 170
    button_next_level_h = 50
    button_next_level_x = -200
    button_next_level_y = -125
    font = None
    screen_width = None
    screen_height = None
    translator = None

    def __init__(self, screen, font, player, enemies, translator, game_settings):
        self.game_settings = game_settings
        self.enemies = enemies
        self.player = player
        self.font = font
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.translator = translator
        self.text_color = game_settings.text_color
        self.health_x = self.screen_width - self.bar_width - self.health_x
        self._create_menu_buttons()

    def _create_menu_buttons(self):
        self.button_exit_y = self.button_exit_y + self.screen_height / 2
        self.button_continue_y =  self.button_continue_y + self.screen_height / 2
        self.button_next_level_y =  self.button_next_level_y + self.screen_height / 2
        self.button_exit_rect = pygame.Rect(self.button_exit_x, self.button_exit_y, self.button_exit_w, self.button_exit_h)
        self.button_continue_rect = pygame.Rect(self.button_continue_x, self.button_continue_y, self.button_continue_w, self.button_continue_h)
        self.button_next_level_rect = pygame.Rect(self.button_next_level_x, self.button_next_level_y, self.button_next_level_w, self.button_next_level_h)

    def not_exit_game(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.button_exit_rect.collidepoint(event.pos):
                    return False
                if self.button_continue_rect.collidepoint(event.pos):
                    self.game_settings.state = GameState.RUN
                if self.button_next_level_rect.collidepoint(event.pos):
                    self.game_settings.game_level = self.game_settings.game_level + 1
                    self.game_settings.state = GameState.NEXT_LEVEL
            if event.type == pygame.KEYDOWN:
                # secret keys for testing
                if event.key == pygame.K_x and (event.mod & pygame.KMOD_SHIFT):
                    print("Exit game by pressing Shift + X key")
                    return False
                if event.key == pygame.K_c and (event.mod & pygame.KMOD_SHIFT):
                    print("Continue game by pressing Shift + C key")
                    self.game_settings.state = GameState.RUN
                if event.key == pygame.K_n and (event.mod & pygame.KMOD_SHIFT):
                    print("Next level by pressing Shift + N key")
                    self.game_settings.game_level = self.game_settings.game_level + 1
                    self.game_settings.state = GameState.NEXT_LEVEL
        return True

    def draw(self):
        self.draw_health_bar()
        self.draw_scoring()
        if  self.enemies.enemies_dead == self.enemies.max_enemies or self.enemies.enemy_boss.is_alive is False:
            self.draw_win()
        if self.player.is_alive is False:
            self.draw_game_over()
        if self.game_settings.state == GameState.PAUSE:
            self.draw_pause_menu()

    def draw_pause_menu(self):
        self._set_text_on_screen('pause', None, 0, 150)
        self.draw_continue_button()
        self.draw_exit_button()
        self._set_text_on_screen('exit_key_message', None, 0, -70)

    def draw_next_level_button(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.button_next_level_rect.collidepoint(mouse_pos):
            color = self.button_hover
        else:
            color = self.button_color
        pygame.draw.rect(self.screen, color, self.button_next_level_rect)
        self._set_text_on_screen('next_level', self.button_next_level_rect)

    def draw_continue_button(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.button_continue_rect.collidepoint(mouse_pos):
            color = self.button_hover
        else:
            color = self.continue_button_color
        pygame.draw.rect(self.screen, color, self.button_continue_rect)
        self._set_text_on_screen('continue', self.button_continue_rect)

    def draw_exit_button(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.button_exit_rect.collidepoint(mouse_pos):
            color = self.button_hover
        else:
            color = self.button_color
        pygame.draw.rect(self.screen, color, self.button_exit_rect)
        self._set_text_on_screen('exit', self.button_exit_rect)

    def draw_win(self):
        self._set_text_on_screen('next_level_key_message', None, 0, 180)
        self._set_text_on_screen('win')
        self.draw_next_level_button()
        self.draw_exit_button()
        self._set_text_on_screen('exit_key_message', None, 0, -70)

    def draw_game_over(self):
        self._set_text_on_screen('lose')
        self.draw_exit_button()
        self._set_text_on_screen('exit_key_message', None, 0, -70)

    def _set_text_on_screen(self, textKey, inside_rect = None, x = None, y = None):
        text_surface = self.font.render(self.translator.get_message(textKey), True, self.text_color)
        text_x = (self.screen_width / 2 - text_surface.get_width() / 2) + (x if x else 0)
        text_y = self.screen_height / 2 - (y if y else 60)
        if inside_rect:
            text_rect = text_surface.get_rect(center=inside_rect.center)
            inside_rect.x = self.screen_width / 2 - inside_rect.width / 2
        self.screen.blit(text_surface, text_rect if inside_rect else (text_x, text_y))

    def draw_health_bar(self):
        x = self.health_x
        y = self.health_y
        ratio = self.player.health / self.player.max_health
        pygame.draw.rect(self.screen, self.health_colors_dict["full_health"], (x, y, self.bar_width, self.bar_height))
        pygame.draw.rect(self.screen, self.health_colors_dict["low_health"], (x, y, self.bar_width * ratio, self.bar_height))
        pygame.draw.rect(self.screen, self.health_colors_dict["border"], (x, y, self.bar_width, self.bar_height), 2)

    def draw_scoring(self):
        text_surface = self.font.render(self.translator.get_message('scoring') % (self.enemies.enemies_dead, (self.enemies.max_enemies - self.enemies.enemies_dead), self.game_settings.game_level), True, self.text_color)
        self.screen.blit(text_surface, (0, 0))