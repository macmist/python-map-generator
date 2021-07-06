import pygame
from pygame.locals import *
import pygame_menu
from utils.draw import Drawer
from ui.button import Button
from voronoi import VoronoiGenerator
from utils.distance import *
from utils.hyperbola import Hyperbola
from diamond_square import DiamondSquare
from datetime import datetime

import logging


class App:
    def __init__(self):
        self._drawer = None
        self.line_displayed = False
        self._running = True
        self._display_surf = None
        self._in_menu = True
        self.size = self.weight, self.height = 1024, 1024
        self.manhattan_button: Button = None
        self.euclidean_button: Button = None
        self.voronoi: VoronoiGenerator = None
        self.hyperbolaes = []
        self.menu = None
        self.seed = "Je vais bieng"
        self.ds = DiamondSquare(10)
        self.ds.compute()

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.ds.draw(self._display_surf)
        self.menu = self.create_menu()
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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.menu.enable()

    def on_loop(self):
        pass

    def on_render(self):
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
            events = pygame.event.get()
            for event in events:
                self.on_event(event)
            if self.menu.is_enabled():
                self.display_menu(events)
            else:
                self.on_loop()
            self.on_render()
        self.on_cleanup()

    def start(self, color: bool):
        self.menu.disable()
        self.ds = DiamondSquare(10, self.seed, color)
        self.ds.compute()
        self.ds.draw(self._display_surf)
        pass

    def set_seed(self, seed):
        self.seed = seed

    def create_menu(self):
        menu = pygame_menu.Menu('Welcome', 400, 300, theme=pygame_menu.themes.THEME_BLUE)
        menu.add.text_input('Seed :', default=self.seed, onchange=self.set_seed)
        menu.add.button('Grey', self.start, False)
        menu.add.button('Color', self.start, True)

        return menu

    def display_menu(self, events):
        if self.menu.is_enabled():
            self.menu.update(events)
            if self.menu.is_enabled():
                self.menu.draw(self._display_surf)


if __name__ == "__main__":
    app = App()
    app.on_execute()
