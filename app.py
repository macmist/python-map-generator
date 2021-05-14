import pygame
from pygame.locals import *
from utils.draw import Drawer
from ui.button import Button
from voronoi import VoronoiGenerator
from utils.distance import *
from utils.hyperbola import Hyperbola
import logging


class App:
    def __init__(self):
        self._drawer = None
        self.line_displayed = False
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 640, 400
        self.manhattan_button: Button = None
        self.euclidean_button: Button = None
        self.voronoi: VoronoiGenerator = None

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._drawer = Drawer(self._display_surf)
        self._running = True
        self.manhattan_button = Button(self._display_surf, (10, 10), "Manhattan")
        self.euclidean_button = Button(self._display_surf, (110, 10), "Euclidean")
        return self._running

    def on_finished_calculation(self):
        if self.voronoi:
            self.voronoi.draw()

    def on_event(self, event):
        logging.info(event.type)
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            position = pygame.mouse.get_pos()
            print(position)
            if self.euclidean_button.is_point_inside(position):
                self.start_voronoi(EuclideanDistance())
                print('euclidean')
            if self.manhattan_button.is_point_inside(position):
                print('manhattan')
                self.start_voronoi(ManhattanDistance())

    def on_loop(self):
        pass

    def on_render(self):
        self._display_surf.fill((0, 0, 0))
        self.manhattan_button.show()
        self.euclidean_button.show()
        self.draw_mouse_line()
        pygame.display.update()

    def on_cleanup(self):
        pygame.quit()

    def start_voronoi(self, interface: DistanceInterface):
        self.voronoi = VoronoiGenerator(self._display_surf, interface, self.on_finished_calculation)
        self.voronoi.generate()

    def draw_hyperbola(self, distance_from_line, top: bool = True):
        hyperbola = Hyperbola(ManhattanDistance(), Point(100, 150), distance_from_line)
        self._drawer.draw_point((100, 150))

        for x in range(self.weight):
            y = hyperbola.get_point_from_x(x, top)
            if 0 <= y < self.height:
                self._drawer.draw_point((x, y))

    def draw_mouse_line(self):
        x, y = pygame.mouse.get_pos()
        mouse_line_drawer = Drawer(self._display_surf, (255, 0, 0))
        mouse_line_drawer.draw_line((0, y), (self.weight - 1, y))
        distance = y - 150
        if distance != 0:
            self.draw_hyperbola(distance, distance > 0)

    def on_execute(self):
        if not self.on_init():
            self._running = False

        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()


if __name__ == "__main__":
    app = App()
    app.on_execute()
