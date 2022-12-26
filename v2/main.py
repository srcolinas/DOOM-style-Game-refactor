import sys

import pygame as pg
from map import Map
from object_handler import ObjectHandler
from object_renderer import ObjectRenderer
from pathfinding import PathFinding
from player import Player
from raycasting import RayCasting
from settings import FPS, RES
from sound import Sound
from weapon import Weapon


class Game:
    def __init__(self):
        pg.init()
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(RES)
        self.delta_time = 1
        self.global_trigger = False
        self._global_event = pg.USEREVENT + 0
        self._clock = pg.time.Clock()
        pg.time.set_timer(self._global_event, 40)
        self.new_game()

    def new_game(self):
        self.map = Map(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.object_handler = ObjectHandler(self)
        self.weapon = Weapon(self)
        self.sound = Sound(self)
        self.pathfinding = PathFinding(self)
        pg.mixer.music.play(-1)

    def update(self):
        self.player.update()
        self.raycasting.update()
        self.object_handler.update()
        self.weapon.update()
        pg.display.flip()
        self.delta_time = self._clock.tick(FPS)
        pg.display.set_caption(f"{self._clock.get_fps() :.1f}")

    def _draw(self):
        self.object_renderer.draw()
        self.weapon.draw()

    def _check_events(self):
        self.global_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (
                event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE
            ):
                pg.quit()
                sys.exit()
            elif event.type == self._global_event:
                self.global_trigger = True
            self.player.single_fire_event(event)

    def run(self):
        while True:
            self._check_events()
            self.update()
            self._draw()


if __name__ == "__main__":
    game = Game()
    game.run()
