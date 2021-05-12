import random
from typing import List


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def to_coordinates(self):
        return self.x, self.y


class Site:
    def __init__(self, point: Point, color=None):
        self.position = point
        self.children: List[Point] = []
        if color is None:
            self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def add_child(self, point: Point):
        self.children.append(point)