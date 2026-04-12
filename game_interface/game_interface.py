import pygame
from translate.translator import Translator
from data_models.game_state import GameState
from data_models.entities_actions import EntitiesActions
from game_interface.shop import Shop
from helper.timer import Timer

class GameInterface(pygame.sprite.Sprite):

    def __init__(self, screen, font, player, enemies, translator, game_settings):
        self.text_size = game_settings.text_size
        self.green_button_color = (0, 255, 0)
        self.red_button_color = (200, 0, 0)
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
        self.shop = Shop(player)
        self.five_seconds_timer_show_no_money_notification = Timer(20)

    def _create_menu_buttons(self):
        possiont_center_screen_x = self.screen_width / 2
        self.button_exit_rect = self._create_menu_button(possiont_center_screen_x, 0, 120, 50)
        self.button_continue_rect = self._create_menu_button(possiont_center_screen_x, -75, 170, 50)
        self.button_next_level_rect = self._create_menu_button(possiont_center_screen_x, -125, 170, 50)
        self.button_retry_rect = self._create_menu_button(possiont_center_screen_x, -125, 170, 50)
        self.button_buy_health_potion_rect = self._create_menu_button(possiont_center_screen_x + 255, 40, 100, 50, False)

    def _create_menu_button(self, position_x, position_y, width, height, use_screen_h = True):
        position_x = position_x - width / 2
        final_possition_y =  position_y + self.screen_height / 2 if use_screen_h else position_y
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
                if self.button_retry_rect.collidepoint(event.pos):
                    self.game_settings.state = GameState.RETRY_LEVEL
                if self.button_buy_health_potion_rect.collidepoint(event.pos):
                    self.game_settings.player_coins = self.shop.make_buy_transaction(self.game_settings.player_coins, self.shop.healing_potion)
                    self.five_seconds_timer_show_no_money_notification.start_time = self.shop.transaction_status is False
            if event.type == pygame.KEYDOWN:
                # secret keys for testing
                if event.key == pygame.K_x and (event.mod & pygame.KMOD_SHIFT):
                    print("Exit game by pressing Shift + X key")
                    return False
                if event.key == pygame.K_c and (event.mod & pygame.KMOD_SHIFT):
                    print("Continue game by pressing Shift + C key")
                    self.game_settings.state = GameState.RUN
                if event.key == pygame.K_a and self.game_settings.player_action == EntitiesActions.OPEN_SHOP:
                    # print("Sell healing potion by pressing A key")
                    self.game_settings.player_coins = self.shop.make_buy_transaction(self.game_settings.player_coins, self.shop.healing_potion)
                    self.five_seconds_timer_show_no_money_notification.start_time = self.shop.transaction_status is False
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
        self.draw_shop_window()
        wait_for_timer_to_finish = self.five_seconds_timer_show_no_money_notification.check_cronometer()
        if wait_for_timer_to_finish is True:
            self._set_text_on_screen('no_money', None, 0, self.screen_height / 2 - self.screen_height + 30)

    def draw_help_window(self):
        if self.game_settings.player_action != EntitiesActions.OPEN_HELP:
            return
        self.screen.blit(self.help_overlay, self.help_window.topleft)
        half_screen_h = self.screen_height / 2
        self._set_text_on_screen('help_title', None, 0, half_screen_h)
        self.font = pygame.font.SysFont(self.game_settings.font_name, 18)
        self._set_text_on_screen('exit_key_message', None, 0, half_screen_h - 50)
        self._set_text_on_screen('pause', None, 0, half_screen_h - 70)
        self._set_text_on_screen('next_level_key_message', None, 0, half_screen_h - 90)
        self._set_text_on_screen('how_to_close_help', None, 0, half_screen_h - 110)
        self._set_text_on_screen('how_to_open_inventory', None, 0, half_screen_h - 130)
        self._set_text_on_screen('how_to_move', None, 0, half_screen_h - 150)
        self._set_text_on_screen('how_to_shoot', None, 0, half_screen_h - 170)
        self._set_text_on_screen('interact_with_bombs', None, 0, half_screen_h - 190)
        self._set_text_on_screen('how_to_use_buttons', None, 0, half_screen_h - 210)  
        self._set_text_on_screen('retry_level_key_message', None, 0, half_screen_h - 230)
        self._set_text_on_screen('how_to_open_shop', None, 0, half_screen_h - 250)
        self._set_text_on_screen('how_to_buy_health_potions', None, 0, half_screen_h - 270)
        self._set_text_on_screen('how_to_consume_health_potions', None, 0, half_screen_h - 290)
        self.font = pygame.font.SysFont(self.game_settings.font_name, self.text_size)

    def draw_shop_window(self):
        if self.game_settings.player_action != EntitiesActions.OPEN_SHOP:
            return
        self.screen.blit(self.help_overlay, self.help_window.topleft)
        half_screen_h = self.screen_height / 2
        self._set_text_on_screen('shop_title', None, 0, half_screen_h)
        self._set_text_on_screen('health_potions', None, 0, half_screen_h - 50, [self.shop.number_of_healing_potion, self.shop.healing_potion_price])
        self.draw_button(self.button_buy_health_potion_rect, 'buy_label', self.green_button_color)
        self._set_text_on_screen('player_coins', None, 0, half_screen_h - self.screen_height + 50, [self.game_settings.player_coins])

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

    def draw_button(self, button_rect, button_label, main_button_color = None):
        mouse_pos = pygame.mouse.get_pos()
        if button_rect.collidepoint(mouse_pos):
            color = self.button_hover
        else:
            color = main_button_color if main_button_color else self.red_button_color
        pygame.draw.rect(self.screen, color, button_rect)
        self._set_text_on_screen(button_label, button_rect)

    def draw_pause_menu(self):
        self._set_text_on_screen('how_to_access_help', None, 0, 150)
        self.draw_button(self.button_continue_rect, 'continue', self.green_button_color)
        self.draw_button(self.button_exit_rect, 'exit')

    def draw_win(self):
        self._set_text_on_screen('how_to_access_help', None, 0, 180)
        self._set_text_on_screen('win')
        self.draw_button(self.button_next_level_rect, 'next_level')
        self.draw_button(self.button_exit_rect, 'exit')
        if self.game_settings.game_level in self.game_settings.levels_when_shop_is_restocked:
            self.shop.restock_shop_inventory()

    def draw_game_over(self):
        self._set_text_on_screen('total_enemies_defeated', None, 0, 180, [self.game_settings.total_enemies_defeated])
        self._set_text_on_screen('lose')
        self.draw_button(self.button_retry_rect, 'retry_level')
        self.draw_button(self.button_exit_rect, 'exit')

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