import random

import pygame
from utils.draw import Drawer
from utils.point import Point

class VoronoiGenerator:
    def __init__(self, surface: pygame.Surface, max_sites = 100):
        self.surface = surface
        self.sites = []
        self.points = []
        self.drawer = Drawer(surface)
        self.max_sites = max_sites



    def generate(self):
        self.init_points()
        self.generate_sites()

    def init_points(self):
        range_x, range_y = self.surface.get_size()
        for x in range(0, range_x):
            for y in range(0, range_y):
                self.points.append(Point(x, y))

    def generate_sites(self):
        for x in range(0, self.max_sites):
            value = random.randint(0, len(self.points))
            point = self.points[value]
            self.points.remove(point)
            self.sites.append(point)

    def draw(self):
        self.drawer.draw_points(self.sites)


