import pygame

class EnemiesSkins:

    def __init__(self):
        self.haven_little_angel_frames = [
            pygame.image.load("assets/enemies/little-angel.png"),
            pygame.image.load("assets/enemies/little-angel-frame-two.png"),
            pygame.image.load("assets/enemies/little-angel-frame-three.png"),
            pygame.image.load("assets/enemies/little-angel-frame-two.png")
        ]
        self.haven_exploded_enemies_image = pygame.image.load("assets/enemies/exploded-little-angel.png")
        self.fire_pit_shere_demon_frames = [
            pygame.image.load("assets/enemies/evil-sphere.png"),
            pygame.image.load("assets/enemies/evil-sphere-frame-two.png")
        ]
        self.exploded_enemies_image = pygame.image.load("assets/enemies/exploded-evil-shere.png")
        self.underwatter_angry_fish_left_side_frames = [
            pygame.image.load("assets/enemies/angry-fish-left-side.png"),
            pygame.image.load("assets/enemies/angry-fish-left-side-two.png"),
        ]
        self.underwatter_angry_fish_right_side_frames = [
            pygame.image.load("assets/enemies/angry-fish-right-side.png"),
            pygame.image.load("assets/enemies/angry-fish-right-side-two.png"),
        ]
        self.void_enemy_exploded = pygame.image.load("assets/enemies/void-enemy-exploded.png")
        self.void_spectral_frames = [
            pygame.image.load("assets/enemies/void-enemy.png"),
            pygame.image.load("assets/enemies/void-enemy-two.png")
        ]
        self.underwater_exploded_enemy_image = pygame.image.load("assets/enemies/exploded-angry-fish-right-side.png")
        self.underwater_exploded_enemy_image_left = pygame.image.load("assets/enemies/exploded-angry-fish-left-side.png")
        self.fire_pit_boss_frames = [
            pygame.image.load("assets/enemies/boos-shere-1.png"),
            pygame.image.load("assets/enemies/boos-shere-2.png"),
            pygame.image.load("assets/enemies/boos-shere-3.png"),
            pygame.image.load("assets/enemies/boos-shere-3.png")
        ]
        self.haven_angel_boss_frames = [
            pygame.image.load("assets/enemies/heaven-boss.png"),
            pygame.image.load("assets/enemies/heaven-boss-frame-two.png")
        ]
        self.haven_angel_injured_boss_frames = [
            pygame.image.load("assets/enemies/injured-heaven-boss.png"),
            pygame.image.load("assets/enemies/injured-heaven-boss-frame-two.png")
        ]
        self.underwater_shark_boss_frames_left = [
            pygame.image.load("assets/enemies/shark-boos-left.png"),
            pygame.image.load("assets/enemies/shark-boos-left-two.png")
        ]
        self.underwater_shark_boss_frames_right = [
            pygame.image.load("assets/enemies/shark-boos-right.png"),
            pygame.image.load("assets/enemies/shark-boos-right-two.png")
        ]
