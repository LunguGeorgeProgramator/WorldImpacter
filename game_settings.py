from data_models.game_state import GameState


class GameSettings:

    state = GameState.RUN
    player_action = None
    width = 1280
    height = 720
    text_size = 27
    text_size_small = 27
    font_name = "Arial"
    text_color = (255, 255, 255)
    haven_level_text_color = (58, 51, 38) 
    game_level = 1
    enemies_alive = 1
    eneny_boss_levels = [10, 30, 50, 70, 90]
    heaven_eneny_boss_levels = [20, 40, 60, 80, 100]
    fire_pit_levels = [1, 5, 8, 12, 15, 18, 22, 25, 28, 32, 35, 38, 42, 45, 48, 52, 55, 58, 62, 65, 68, 72, 75, 78, 82, 85, 88, 92, 95, 98, 102]
    haven_levels = [2, 4, 6, 9, 13, 16, 19, 23, 26, 29, 33, 36, 39, 43, 46, 49, 53, 56, 59, 63, 66, 69, 73, 76, 79, 83, 86, 89, 93, 96, 99, 103]
    underwater_levels = [3, 7, 11, 14, 17, 21, 24, 27, 31, 34, 37, 41, 44, 47, 51, 54, 57, 61, 64, 67, 71, 74, 77, 81, 84, 87, 91, 94, 97, 101, 104]
    levels_when_shop_is_restocked = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    enemy_boss_alive = True
    total_enemies_defeated = 0
    game_text_font = None
    player_is_alive = True
    player_coins = 0

    def is_enemy_boss_level(self):
        return self.game_level in self.eneny_boss_levels or self.game_level in self.heaven_eneny_boss_levels