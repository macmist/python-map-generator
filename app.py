import pygame
from pygame.locals import *
from utils.draw import Drawer
from ui.button import Button
from voronoi import VoronoiGenerator
from utils.distance import *
from utils.hyperbola import Hyperbola
from diamond_square import DiamondSquare
import logging


class App:
    def __init__(self):
        self._drawer = None
        self.line_displayed = False
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 512, 512
        self.manhattan_button: Button = None
        self.euclidean_button: Button = None
        self.voronoi: VoronoiGenerator = None
        self.hyperbolaes = []
        self.ds = DiamondSquare(9)

        self.ds.compute()

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        # self._drawer = Drawer(self._display_surf)
        # self._running = True
        # self.manhattan_button = Button(self._display_surf, (10, 10), "Manhattan")
        # self.euclidean_button = Button(self._display_surf, (110, 10), "Euclidean")
        # self.voronoi = VoronoiGenerator(self._display_surf, ManhattanDistance())
        # self.voronoi.generate_without_voronoi()
        self.ds.draw(self._display_surf)
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
            # if self.euclidean_button.is_point_inside(position):
            #     self.start_voronoi(EuclideanDistance())
            #     print('euclidean')
            # if self.manhattan_button.is_point_inside(position):
            #     print('manhattan')
            #     self.start_voronoi(ManhattanDistance())

    def on_loop(self):
        pass

    def on_render(self):
        # self._display_surf.fill((0, 0, 0))
        # self.manhattan_button.show()
        # self.euclidean_button.show()
        # self.draw_mouse_line()
        pygame.display.update()


    def on_cleanup(self):
        pygame.quit()

    def start_voronoi(self, interface: DistanceInterface):
        self.voronoi = VoronoiGenerator(self._display_surf, interface, self.on_finished_calculation)
        self.voronoi.generate()

    def draw_hyperbola(self, focus: Point, distance_from_line, top: bool = True):
        hyperbola = Hyperbola(ManhattanDistance(), focus, distance_from_line)
        self._drawer.draw_point(focus.to_coordinates())
        if distance_from_line > 0:
            for x in range(self.weight):
                y = hyperbola.get_point_from_x(x, top)
                if 0 <= y < self.height:
                    self._drawer.draw_point((x, y))

    def draw_hyperbolaes(self, mouse_y):
        for site in self.voronoi.sites:
            distance = mouse_y - site.position.y
            self.draw_hyperbola(site.position, distance, distance < 0)

    def draw_mouse_line(self):
        x, y = pygame.mouse.get_pos()
        mouse_line_drawer = Drawer(self._display_surf, (255, 0, 0))
        mouse_line_drawer.draw_line((0, y), (self.weight - 1, y))
        self.draw_hyperbolaes(y)

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
