import random
import pygame


class DiamondSquare:
    def __init__(self, n):
        self.n = n
        self.side_length = 2 ** n + 1
        self.map = []
        for x in range(0, self.side_length):
            self.map.append([])
            for y in range(0, self.side_length):
                self.map[x].append(0)

        self.map[0][0] = random.randint(self.side_length, self.side_length)
        self.map[0][self.side_length - 1] = random.randint(self.side_length, self.side_length)
        self.map[self.side_length - 1][0] = random.randint(self.side_length, self.side_length)
        self.map[self.side_length - 1][self.side_length - 1] = random.randint(self.side_length, self.side_length)
        self.step: int = self.side_length - 1
        self.min = 0
        self.max = 0
        self.blue = (0, 0, 255)
        self.sand = (255,248,220)
        self.brown = (222,184,135)
        self.white = (255, 255, 255)
        self.green = (0, 255, 0)

    def compute(self):
        while self.step > 1:
            self.diamond_step()
            self.square_step()
            self.step = int(self.step / 2)
        self.get_min_max()

    def diamond_step(self):
        half: int = int(self.step / 2)
        for x in range(half, self.side_length, self.step):
            for y in range(half, self.side_length, self.step):
                average = self.get_average(x, y, half)
                self.map[x][y] = average + random.randint(-half, half)

    def get_average(self, x, y, side):
        top_left = self.map[x - side][y - side]
        top_right = self.map[x + side][y - side]
        bottom_left = self.map[x - side][y + side]
        bottom_right = self.map[x + side][y + side]
        return int((top_left + top_right + bottom_right + bottom_left) / 4)

    def square_step(self):
        half: int = int(self.step / 2)
        offset = 0
        for x in range(0, self.side_length, half):
            if offset == 0:
                offset = half
            else:
                offset = 0
            for y in range(offset, self.side_length, self.step):
                total = 0
                vertices = 0
                if x >= half:
                    total += self.map[x - half][y]
                    vertices += 1
                if x + half < self.side_length:
                    total += self.map[x + half][y]
                    vertices += 1
                if y >= half:
                    total += self.map[x][y - half]
                    vertices += 1
                if y + half < self.side_length:
                    total += self.map[x][y + half]
                    vertices += 1
                self.map[x][y] = int(total / vertices) + random.randint(-half, half)

    def get_min_max(self):
        min_value = self.side_length * 10
        max_value = - min_value
        for x in range(0, self.side_length):
            for y in range(0, self.side_length):
                current = self.map[x][y]
                if current > max_value:
                    max_value = current
                if current < min_value:
                    min_value = current
        self.min = min_value
        self.max = max_value

    def draw(self, surface: pygame.surface):
        divider = self.max - self.min
        blue_points = 0
        for x in range(0, self.side_length):
            for y in range(0, self.side_length):
                normalized = (self.map[x][y] - self.min) / divider
                color = 255 if normalized >= float(1) else normalized * 256
                color = int(color)
                point_color = self.blue
                if 0 <= color < 100:
                    point_color = (0, 0, color + 50)
                elif 100 <= color < 102:
                    point_color = self.sand
                elif 102 <= color < 105:
                    point_color = self.brown
                elif 105 <= color < 200:
                    point_color = (0, color - 50, 0)
                else:
                    point_color = (color, color, color)

                if color == 0:
                    blue_points += 1

                surface.set_at((x, y), (color, color, color))

    def __str__(self):
        return "n = {n}\nside = {side}\nmap = {map}".format(n=self.n, side=self.side_length, map=self.map)
