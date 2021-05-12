import pygame


class Drawer:
    def __init__(self, surface):
        self.color = (255, 0, 255)
        self.surface = surface
        self.line_width = 1

    def draw_line(self, start_point, end_point):
        pygame.draw.line(self.surface, self.color, start_point, end_point, self.line_width)

    def draw_point(self, point):
        self.surface.set_at(point, self.color)

    def draw_points(self, points: list):
        for point in points:
            self.draw_point(point)
