import pygame
from utils.point import Point
from utils.point import Site
from typing import List


class Drawer:
    def __init__(self, surface, color=(255, 0, 255)):
        self.surface = surface
        self.color = color
        self.line_width = 1

    def draw_line(self, start_point, end_point):
        pygame.draw.line(self.surface, self.color, start_point, end_point, self.line_width)

    def draw_point(self, point):
        self.surface.set_at(point, self.color)

    def draw_sites(self, sites: List[Site]):
        for site in sites:
            self.draw_point(site.position.to_coordinates())

    def draw_points(self, points: List[Point]):
        for point in points:
            self.draw_point(point.to_coordinates())
