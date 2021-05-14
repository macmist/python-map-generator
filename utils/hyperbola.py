from utils.point import Point
from utils.distance import *


class Hyperbola:
    a: float = None
    b: float = None
    origin: Point = None

    def __init__(self, distance_calculator: DistanceInterface,
                 focus_point: Point, distance_to_origin: float):
        self.distance_calculator: DistanceInterface = distance_calculator
        self.distance_to_origin: float = distance_to_origin
        self.focus_point: Point = focus_point
        self.compute_hyperbola_construct_points()

    def compute_hyperbola_construct_points(self):
        self.a = self.distance_to_origin / 2
        self.b = sqrt(self.distance_to_origin ** 2 - self.a ** 2)
        origin_y = self.focus_point.y + self.distance_to_origin
        self.origin = Point(self.focus_point.x, origin_y)

    def get_point_from_x(self, x: int, sup: bool = True) -> int:
        h = self.origin.x
        k = self.origin.y
        a2 = self.a * self.a
        X = (x - h) * (x - h)
        b2 = self.b * self.b
        ratio = X / b2
        intermediate = a2 * (1 + ratio)
        if intermediate <= 0:
            return self.get_asymptote_from_x(x, sup)
        hyperbola = sqrt(intermediate)
        y = k - hyperbola
        if sup:
            y = k + hyperbola
        return int(y)

    def get_asymptote_from_x(self, x: int, sup: bool = True) -> int:
        h = self.origin.x
        k = self.origin.y
        ratio = self.a / self.b
        if not sup:
            ratio = -ratio
        return int(ratio * (x - h) + k)
