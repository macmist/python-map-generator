import random
from typing import List

import pygame
from utils.draw import Drawer
from utils.point import Point
from utils.point import Site
from utils.distance import DistanceInterface


class VoronoiGenerator:
    def __init__(self, surface: pygame.Surface, interface: DistanceInterface, callback=None):
        self.surface = surface
        self.sites: List[Site] = []
        self.points: List[Point] = []
        self.drawer = Drawer(surface)
        self.max_sites = 100
        self.distanceCalculator = interface
        self.callback = callback

    def generate(self):
        self.init_points()
        self.generate_sites()
        self.add_points_to_sites()
        if self.callback:
            self.callback()

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
            self.sites.append(Site(point))

    def add_points_to_sites(self):
        for point in self.points:
            owner: Site = None
            for site in self.sites:
                distance = self.distanceCalculator.distance(point, site.position)
                if owner is None or distance < self.distanceCalculator.distance(point, owner.position):
                    owner = site
            owner.children.append(point)

    def draw(self):
        site: Site
        for site in self.sites:
            self.draw_site(site)

    def draw_site(self, site: Site):
        point: Point
        drawer = Drawer(self.surface, site.color)
        drawer.draw_points(site.children)