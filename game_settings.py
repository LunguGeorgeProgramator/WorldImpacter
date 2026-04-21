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
    eneny_boss_levels = [10, 40, 70, 100, 130]
    heaven_eneny_boss_levels = [20, 50, 80, 110, 140]
    underwater_enemy_boss_levels = [30, 60, 90, 120, 150]
    fire_pit_levels = [1, 5, 9, 14, 18, 23, 27, 32, 36, 41, 45, 49, 54, 58, 63, 67, 72, 76, 81, 85, 91, 95, 99]
    void_levels = [2, 6, 11, 15, 19, 24, 28, 33, 37, 42, 46, 51, 55, 59, 64, 68, 73, 77, 82, 86, 92, 96, 101]
    haven_levels = [3, 7, 12, 16, 21, 25, 29, 34, 38, 43, 47, 52, 56, 61, 65, 69, 74, 78, 83, 87, 93, 97, 102]
    underwater_levels = [4, 8, 13, 17, 22, 26, 31, 35, 39, 44, 48, 53, 57, 62, 66, 71, 75, 79, 84, 88, 94, 98, 103]
    levels_when_shop_is_restocked = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    enemy_boss_alive = True
    total_enemies_defeated = 0
    game_text_font = None
    player_is_alive = True
    player_coins = 0

    def is_enemy_boss_level(self):
        return self.game_level in self.eneny_boss_levels + self.heaven_eneny_boss_levels + self.underwater_enemy_boss_levels