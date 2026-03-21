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
    button_exit_rect = None
    button_continue_rect = None
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
        self.button_exit_rect = pygame.Rect(-200, self.screen_height / 2, 120, 50)
        self.button_continue_rect = pygame.Rect(-200, self.screen_height / 2 - 75, 170, 50)
        self.translator = translator

    def not_exit_game(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.button_exit_rect.collidepoint(event.pos):
                    return False
                if self.button_continue_rect.collidepoint(event.pos):
                    self.game_settings.state = GameState.RUN
        return True

    def draw(self):
        if  self.enemies.enemies_dead == self.enemies.max_enemies:
            self.draw_exit_button()
            self.draw_win()
        if self.player.is_alive is False:
            self.draw_exit_button()
            self.draw_game_over()
        self.draw_health_bar()
        self.draw_scoring()
        if self.game_settings.state == GameState.PAUSE:
            self.draw_pause_menu()

    def draw_pause_menu(self):
        self._set_text_on_screen('pause', None, 0, 150)
        self.draw_exit_button()
        self.draw_continue_button()

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
        self._set_text_on_screen('win')

    def draw_game_over(self):
        self._set_text_on_screen('lose')

    def _set_text_on_screen(self, textKey, inside_rect = None, x = None, y = None):
        text_surface = self.font.render(self.translator.get_message(textKey), True, (255, 255, 255))
        text_x = (self.screen_width / 2 - text_surface.get_width() / 2) + (x if x else 0)
        text_y = self.screen_height / 2 - (y if y else 60)
        if inside_rect:
            text_rect = text_surface.get_rect(center=inside_rect.center)
            inside_rect.x = self.screen_width / 2 - inside_rect.width / 2
        self.screen.blit(text_surface, text_rect if inside_rect else (text_x, text_y))

    def draw_health_bar(self):
        bar_width = 200
        bar_height = 20
        x = self.screen_width - bar_width - 20
        y = 20
        ratio = self.player.health / self.player.max_health
        pygame.draw.rect(self.screen, (100, 0, 0), (x, y, bar_width, bar_height))
        pygame.draw.rect(self.screen, (0, 200, 0), (x, y, bar_width * ratio, bar_height))
        pygame.draw.rect(self.screen, (255,255,255), (x, y, bar_width, bar_height), 2)

    def draw_scoring(self):
        text_surface = self.font.render(self.translator.get_message('scoring') % (self.enemies.enemies_dead, (self.enemies.max_enemies - self.enemies.enemies_dead)), True, (255, 255, 255))
        self.screen.blit(text_surface, (0, 0))