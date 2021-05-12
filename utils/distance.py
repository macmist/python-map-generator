from point import Point
from math import sqrt


class DistanceInterface:
    def distance(self, point_one: Point, point_two: Point) -> int:
        pass


class EuclideanDistance(DistanceInterface):
    def distance(self, point_one: Point, point_two: Point) -> int:
        dx = point_one.x - point_two.x
        dy = point_one.y - point_two.y
        return int(sqrt(dx * dx + dy * dy))


class ManhattanDistance(DistanceInterface):
    def distance(self, point_one: Point, point_two: Point) -> int:
        dx = point_one.x - point_two.x
        dy = point_one.y - point_two.y
        return abs(dx) + abs(dy)
