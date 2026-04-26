import pygame
from data_models.moving_direction import MovingDirection
from data_models.game_state import GameState
from data_models.entities_actions import EntitiesActions
from game_interface.shop import Shop


class Player:

    def __init__(self, screen, keyboard_handler, images_assets_loader, game_settings, player_inventory):
        self.color = "white"
        self.player_inventory = player_inventory
        self.pos = None
        self.keyPressed = None
        self.direction = None
        self.last_moving_direction = None
        self.last_moving_direction_left_right = None
        self.x = 0
        self.y = 0
        self.with_p = 0
        self.height_p = 0
        self.is_player_out_of_screen = False
        self.screen_x = 0
        self.screen_y = 0
        self.radius = 50
        self.health = 1000
        self.max_health = 1000
        self.is_alive = True
        self.game_settings = game_settings
        self.images_assets_loader = images_assets_loader
        self.screen = screen
        self.keyboard_handler = keyboard_handler
        half_of_player_image_width = self.images_assets_loader.default_image_width / 2
        half_of_player_image_height = self.images_assets_loader.default_image_height / 2
        self.player_pos = pygame.Vector2(screen.get_width() / 2 - half_of_player_image_width, screen.get_height() / 2 - half_of_player_image_height)
        self.with_p = screen.get_width() / 2
        self.height_p = screen.get_height() / 2
        self.pos = pygame.Vector2(self.player_pos.x, self.player_pos.y)
        self.screen_x, self.screen_y = screen.get_size()
        self.shop = Shop(self)
        self.player_skins = images_assets_loader.player_skins

    def _move_vector_x_y(self, vector_pos, direction, speed):
        is_out_of_scrren_left = self.player_pos.x < 0
        is_out_of_scrren_right = self.player_pos.x > self.screen_x - 100
        is_out_of_scrren_top = self.player_pos.y < 0
        is_out_of_scrren_down = self.player_pos.y > self.screen_y - 100
        if direction == MovingDirection.UP and is_out_of_scrren_top is False:
            self.color = "black"
            vector_pos.y -= speed
        elif direction == MovingDirection.DOWN and is_out_of_scrren_down is False:
            vector_pos.y += speed
            self.color = "blue"
        elif direction == MovingDirection.LEFT and is_out_of_scrren_left is False:
            vector_pos.x -= speed
            self.color = "grey"
        elif direction == MovingDirection.RIGHT and is_out_of_scrren_right is False:
            vector_pos.x += speed
            self.color = "yellow"
        return vector_pos

    def update(self, dt):
        self.direction = self.keyboard_handler.get_movement_direction()
        self.last_moving_direction = self.keyboard_handler.get_last_movement_direction()
        self.last_moving_direction_left_right = self.keyboard_handler.get_last_left_right_direction()
        self.player_pos = self._move_vector_x_y(self.player_pos, self.direction, 5)
        # self.player_pos = self._move_vector_x_y(self.player_pos, self.direction, 300 * dt)
        self.x = self.player_pos.x
        self.y = self.player_pos.y
        if self.health <= 0:
            self.is_alive = False
            self.game_settings.player_is_alive = False
            self.game_settings.state = GameState.GAME_OVER
        self.consume_healing_potion()
        self.consume_flower_attack()

    def consume_healing_potion(self):
        if self.game_settings.player_action is not None and self.game_settings.player_action == EntitiesActions.CONSUME_HEALING_POTION:
            self.game_settings.player_action = None
            inventoryItem = self.player_inventory.get_item_by_name(self.shop.healing_potion)
            if inventoryItem.count <= 0:
                return
            self.player_inventory.remove_from_inventory(self.shop.healing_potion, 1)
            healing_amount = self.max_health / 3
            self.health = min(self.health + healing_amount, self.max_health)

    def consume_flower_attack(self):
        if self.game_settings.player_action is not None and self.game_settings.player_action == EntitiesActions.CONSUME_FLOWER_ATTACK:
            inventoryItem = self.player_inventory.get_item_by_name(self.shop.flower_attack)
            if inventoryItem.count <= 0:
                self.game_settings.player_action = None
                return
            self.player_inventory.remove_from_inventory(self.shop.flower_attack, 1)
            self.game_settings.player_action = EntitiesActions.FLOWER_ATTACK

    def draw(self):
        if self._is_level_in_list(self.game_settings.haven_levels + self.game_settings.heaven_eneny_boss_levels):
            player_image = self._get_player_skin_type_plain(self.player_skins.grim_skin)
        elif self._is_level_in_list(self.game_settings.underwater_levels + self.game_settings.underwater_enemy_boss_levels):
            player_image = self._get_player_skin_type_plain(self.player_skins.diver_skin)
        elif self._is_level_in_list(self.game_settings.void_levels):
            player_image = self._get_player_skin_type_plain(self.player_skins.void_skin)
        else:
            player_image = self._get_player_default_image(self.player_skins.default_skin)
        self.images_assets_loader.draw(player_image, self.player_pos.x, self.player_pos.y)

    def _is_level_in_list(self, levels_list):
        return self.game_settings.game_level in levels_list

    def _get_player_default_image(self, player_skin):
        if self.last_moving_direction == MovingDirection.UP:
            player_image = player_skin[MovingDirection.UP]
        elif self.last_moving_direction == MovingDirection.DOWN:
            player_image = player_skin[MovingDirection.DOWN]
        elif self.last_moving_direction == MovingDirection.LEFT:
            player_image = player_skin[MovingDirection.LEFT]
        elif self.last_moving_direction == MovingDirection.RIGHT:
            player_image = player_skin[MovingDirection.RIGHT]
        else:
            player_image = player_skin[MovingDirection.DOWN]
        return player_image
    
    def _get_player_skin_type_plain(self, player_skin):
        if self.last_moving_direction == MovingDirection.UP and self.last_moving_direction_left_right == MovingDirection.LEFT:
            player_image = player_skin[MovingDirection.LEFT]
        elif self.last_moving_direction == MovingDirection.UP and self.last_moving_direction_left_right == MovingDirection.RIGHT:
            player_image = player_skin[MovingDirection.RIGHT]
        elif self.last_moving_direction == MovingDirection.LEFT:
            player_image = player_skin[MovingDirection.DOWN]
        elif self.last_moving_direction == MovingDirection.RIGHT:
            player_image = player_skin[MovingDirection.UP]
        elif self.last_moving_direction == MovingDirection.DOWN and self.last_moving_direction_left_right == MovingDirection.LEFT:
            player_image = player_skin[MovingDirection.DOWN]
        elif self.last_moving_direction == MovingDirection.DOWN and self.last_moving_direction_left_right == MovingDirection.RIGHT:
            player_image = player_skin[MovingDirection.UP]
        else:
            player_image = player_skin[MovingDirection.UP]
        return player_image