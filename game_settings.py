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
    fire_pit_levels =[1, 2, 3, 4, 21, 22, 23, 24, 41, 42, 43, 44, 61, 62, 63, 64, 81, 82, 83, 84]
    eneny_boss_levels = [5, 25, 45, 65, 85]
    haven_levels = [6, 7, 8, 9, 26, 27, 28, 29, 46, 47, 48, 49, 66, 67, 68, 69, 86, 87, 88, 89]
    heaven_eneny_boss_levels = [10, 30, 50, 70, 90]
    underwater_levels = [11, 12, 13, 14, 31, 32, 33, 34, 51, 52, 53, 54, 71, 72, 73, 74, 91, 92, 93, 94]
    underwater_enemy_boss_levels = [15, 35, 55, 75, 95]
    void_levels = [16, 17, 18, 19, 36, 37, 38, 39, 56, 57, 58, 59, 76, 77, 78, 79, 96, 97, 98, 99]
    void_enemy_boss_levels = [20, 40, 60, 80, 100]
    levels_when_shop_is_restocked = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    enemy_boss_alive = True
    total_enemies_defeated = 0
    game_text_font = None
    player_is_alive = True
    player_coins = 0

    def is_enemy_boss_level(self):
        return self.game_level in self.eneny_boss_levels + self.heaven_eneny_boss_levels + self.underwater_enemy_boss_levels + self.void_enemy_boss_levels