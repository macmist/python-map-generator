import pygame
from pygame.locals import *
from utils.draw import Drawer
from ui.button import Button
from voronoi import VoronoiGenerator
from utils.distance import *
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
        self.manhattan_button.show()
        self.euclidean_button.show()
        pygame.display.update()

    def on_cleanup(self):
        pygame.quit()

    def start_voronoi(self, interface: DistanceInterface):
        self.voronoi = VoronoiGenerator(self._display_surf, interface, self.on_finished_calculation)
        self.voronoi.generate()

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
