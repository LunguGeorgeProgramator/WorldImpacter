import pygame

class GameInterface(pygame.sprite.Sprite):

    player = None
    enemies = None
    screen = None
    button_color = None
    button_hover = None
    button_rect = None
    font = None
    screen_width = None
    screen_height = None
    
    def __init__(self, screen, font, player, enemies):
        self.enemies = enemies
        self.player = player
        self.font = font
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.button_color = (200, 0, 0)
        self.button_hover = (255, 0, 0) 
        self.button_rect = pygame.Rect(self.screen_width / 2 - 70, self.screen_height / 2 - 100, 100, 50) 

    def not_exit_game(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.button_rect.collidepoint(event.pos):
                    return False
        return True

    def draw(self):
        if  self.enemies.enemies_dead == self.enemies.max_enemies:
            self.draw_exit_button()
            self.draw_win()
        if self.player.is_alive is False:
            self.draw_exit_button()
            self.draw_game_over()
        self.draw_health_bar()
        self.draw_scoring()
    
    def draw_exit_button(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.button_rect.collidepoint(mouse_pos):
            color = self.button_hover
        else:
            color = self.button_color
        pygame.draw.rect(self.screen, color, self.button_rect)
        text_surface = self.font.render("Exit", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.button_rect.center)
        self.screen.blit(text_surface, text_rect)

    def draw_win(self):
        text_surface = self.font.render('You Win', True, (255, 255, 255))
        self.screen.blit(text_surface, (self.screen_width / 2 - 80, self.screen_height / 2))

    def draw_game_over(self):
        text_surface = self.font.render('Game Over', True, (255, 255, 255))
        self.screen.blit(text_surface, (self.screen_width / 2 - 100, self.screen_height / 2))

    def draw_health_bar(self):
        bar_width = 200
        bar_height = 20
        x = self.screen_width - bar_width - 20 
        y = 20 
        ratio = self.player.health / self.player.max_health
        pygame.draw.rect(self.screen, (100, 0, 0), (x, y, bar_width, bar_height))
        pygame.draw.rect(self.screen, (0, 200, 0), (x, y, bar_width * ratio, bar_height))
        pygame.draw.rect(self.screen, (255,255,255), (x, y, bar_width, bar_height), 2)

    def draw_scoring(self):
        text_surface = self.font.render('Enemies killed: ' + str(self.enemies.enemies_dead) + ", enemies alive: " + str(self.enemies.max_enemies - self.enemies.enemies_dead), True, (255, 255, 255))
        self.screen.blit(text_surface, (0, 0))