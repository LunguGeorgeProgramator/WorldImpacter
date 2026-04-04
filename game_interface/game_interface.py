import pygame
from translate.translator import Translator
from data_models.game_state import GameState
from data_models.entities_actions import EntitiesActions

class GameInterface(pygame.sprite.Sprite):

    def __init__(self, screen, font, player, enemies, translator, game_settings):
        self.continue_button_color = (0, 255, 0)
        self.button_color = (200, 0, 0)
        self.button_hover = (255, 0, 0)
        self.health_colors_dict = {
            "full_health": (100, 0, 0),
            "low_health": (0, 200, 0),
            "border": (255,255,255)
        }
        self.bar_width = 200
        self.bar_height = 20
        self.health_x = 20
        self.health_y = 20
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
        self.inventory_overlay = surface = pygame.Surface((100, 50), pygame.SRCALPHA)
        self.inventory_overlay.fill((255, 0, 0, 128)) # color with 50% transparency, red
        self.inventory_window = pygame.Rect(50, 100, 300, 200)

        self.help_overlay = surface = pygame.Surface((self.screen_width / 2, self.screen_height), pygame.SRCALPHA)
        self.help_overlay.fill((255, 0, 0, 204)) # color with 50% transparency, red
        self.help_window = pygame.Rect(self.screen_width / 2 / 2, 0, self.screen_width / 2, self.screen_height)

    def _create_menu_buttons(self):
        self.button_exit_rect = self._create_menu_button(-200, 0, 120, 50)
        self.button_continue_rect = self._create_menu_button(-200, -75, 170, 50)
        self.button_next_level_rect = self._create_menu_button(-200, -125, 170, 50)

    def _create_menu_button(self, position_x, position_y, width, height):
        final_possition_y =  position_y + self.screen_height / 2
        return pygame.Rect(position_x, final_possition_y, width, height)

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
                if event.key == pygame.K_n and (event.mod & pygame.KMOD_SHIFT) and self.game_settings.state != GameState.GAME_OVER:
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
        self.draw_player_inventory()
        self.draw_help_window()

    def draw_help_window(self):
        if self.game_settings.player_action != EntitiesActions.OPEN_HELP:
            return
        self.screen.blit(self.help_overlay, self.help_window.topleft)
        half_screen_h = self.screen_height / 2
        self._set_text_on_screen('help_title', None, 0, half_screen_h)
        self._set_text_on_screen('exit_key_message', None, 0, half_screen_h - 50)
        self._set_text_on_screen('pause', None, 0, half_screen_h - 100)
        self._set_text_on_screen('next_level_key_message', None, 0, half_screen_h - 150)
        self._set_text_on_screen('how_to_close_help', None, 0, half_screen_h - 200)
        self._set_text_on_screen('how_to_open_inventory', None, 0, half_screen_h - 250)
        self._set_text_on_screen('how_to_move', None, 0, half_screen_h - 300)
        self._set_text_on_screen('how_to_shoot', None, 0, half_screen_h - 350)
        self._set_text_on_screen('interact_with_bombs', None, 0, half_screen_h - 400)
        self._set_text_on_screen('how_to_use_buttons', None, 0, half_screen_h - 450)  

    def draw_player_inventory(self):
        if self.game_settings.player_action != EntitiesActions.OPEN_INVENTORY:
            return
        items_on_screen = self.player.player_inventory.inventory_items
        self.inventory_window.height = 100 + (len(items_on_screen) * 50)
        self.inventory_overlay = pygame.transform.smoothscale(
            self.inventory_overlay, 
            (self.inventory_window.width, self.inventory_window.height)
        )
        r_x = self.inventory_window.x
        r_y = self.inventory_window.y
        scaled_surface = pygame.transform.scale(self.inventory_overlay, (self.inventory_window.width, self.inventory_window.height))
        self.screen.blit(scaled_surface, self.inventory_window.topleft)
        self._set_text_on_screen('inventory_title', None, r_x + 10, r_y, [], False)
        for i, item in enumerate(items_on_screen):
            text_surface = self.game_settings.game_text_font.render(item.name + " " + str(item.count), True, self.game_settings.text_color)
            self.screen.blit(text_surface, (r_x + 10, r_y + ((i + 1) * 50)))

    def draw_pause_menu(self):
        self._set_text_on_screen('how_to_access_help', None, 0, 150)
        self.draw_continue_button()
        self.draw_exit_button()

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
        self._set_text_on_screen('how_to_access_help', None, 0, 180)
        self._set_text_on_screen('win')
        self.draw_next_level_button()
        self.draw_exit_button()

    def draw_game_over(self):
        self._set_text_on_screen('total_enemies_defeated', None, 0, 120, [self.game_settings.total_enemies_defeated])
        self._set_text_on_screen('lose')
        self.draw_exit_button()

    def _set_text_on_screen(self, textKey, inside_rect = None, x = None, y = None, text_params = [], use_screen_dimensions = True):
        if text_params:
            text = self.translator.get_message(textKey).format(*text_params)
        else:
            text = self.translator.get_message(textKey)
        if self.game_settings.game_level in self.game_settings.haven_levels:
            text_color = self.game_settings.haven_level_text_color
        else:
            text_color = self.text_color
        text_surface = self.font.render(text, True, text_color)
        if use_screen_dimensions:
            text_x = (self.screen_width / 2 - text_surface.get_width() / 2) + (x if x else 0)
            text_y = self.screen_height / 2 - (y if y else 60)
        else:
            text_x = x
            text_y = y
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