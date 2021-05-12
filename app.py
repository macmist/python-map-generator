import pygame
from pygame.locals import *
from utils.draw import Drawer
from voronoi import VoronoiGenerator
from utils.distance import *


class App:
    def __init__(self):
        self._drawer = None
        self.line_displayed = False
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 640, 400

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._drawer = Drawer(self._display_surf)
        self._running = True
        return self._running

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self):
        pass

    def on_render(self):
        if not self.line_displayed:
            generator = VoronoiGenerator(self._display_surf, EuclideanDistance())
            generator.generate()
            generator.draw()
            self.line_displayed = True
        pygame.display.update()

    def on_cleanup(self):
        pygame.quit()

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
