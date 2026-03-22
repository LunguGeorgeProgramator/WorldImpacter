from data_models.game_state import GameState


class GameSettings:

    state = GameState.RUN
    width = 1280
    height = 720
    text_size = 36
    font_name = "Arial"
    text_color = (255, 255, 255)
    game_level = 1
    enemies_alive = 1
    eneny_boss_levels = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    enemy_boss_alive = True