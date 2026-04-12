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
    eneny_boss_levels = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    haven_levels = [2, 4, 6, 8, 12, 14, 16, 18, 22, 24, 26, 28, 32, 34, 36, 38, 42, 44, 46, 48, 52, 54, 56, 58, 62, 64, 66, 68, 72, 74, 76, 78, 82, 84, 86, 88, 92, 94, 96, 98]
    fire_pit_levels = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57, 59, 61, 63, 65, 67, 69, 71, 73, 75, 77, 79, 81, 83, 85, 87, 89, 91, 93, 95, 97, 99]
    levels_when_shop_is_restocked = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    enemy_boss_alive = True
    total_enemies_defeated = 0
    game_text_font = None
    player_is_alive = True
    player_coins = 0