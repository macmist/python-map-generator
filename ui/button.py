import pygame


class Button:
    def __init__(self, screen: pygame.surface, position, text):
        self.screen: pygame.surface = screen
        self.position = position
        self.text = text
        self.font = pygame.font.SysFont("Arial", 14)
        self.text_render = self.font.render(text, True, (255, 0, 0))
        self.button = None

    def show(self):
        x, y, w, h = self.text_render.get_rect()
        x, y = self.position
        pygame.draw.line(self.screen, (150, 150, 150), (x, y), (x + w, y), 5)
        pygame.draw.line(self.screen, (150, 150, 150), (x, y - 2), (x, y + h), 5)
        pygame.draw.line(self.screen, (50, 50, 50), (x, y + h), (x + w, y + h), 5)
        pygame.draw.line(self.screen, (50, 50, 50), (x + w, y + h), [x + w, y], 5)
        pygame.draw.rect(self.screen, (100, 100, 100), (x, y, w, h))
        self.button = self.screen.blit(self.text_render, (x, y))

    def is_point_inside(self, point):
        return self.button.collidepoint(point)
