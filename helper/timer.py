import pygame

class Timer:

    duration = 0

    def __init__(self, duration):
        self.start_time = pygame.time.get_ticks()
        self.duration = duration

    def is_time_up(self):
        return pygame.time.get_ticks() - self.start_time < self.duration