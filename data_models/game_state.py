from enum import Enum


class GameState(Enum):
    RUN = 1
    PAUSE = 2
    EXIT = 3
    GAME_OVER = 4
    OPEN_MENU = 5
    OPEN_INVENTORY = 6
    NEXT_LEVEL = 7