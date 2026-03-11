import pygame

class GameMenu(pygame.sprite.Sprite):

    screen = None
    button_color = None
    button_hover = None
    button_rect = None
    font = None
    
    def __init__(self, screen, font):
        self.font = font
        self.screen = screen
        # screen_x, screen_y = screen.get_size()
        self.button_color = (200, 0, 0)
        self.button_hover = (255, 0, 0) 
        self.button_rect = pygame.Rect(200, 150, 100, 50) 

    def not_exit_game(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.button_rect.collidepoint(event.pos):
                    return False
        return True

    def draw(self):
        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()
        # Change color if hovered
        if self.button_rect.collidepoint(mouse_pos):
            color = self.button_hover
        else:
            color = self.button_color
        # Draw the button
        pygame.draw.rect(self.screen, color, self.button_rect)
        text_surface = self.font.render("Exit", True, (255, 255, 255))
        # Center the text on the button
        text_rect = text_surface.get_rect(center=self.button_rect.center)
        self.screen.blit(text_surface, text_rect)