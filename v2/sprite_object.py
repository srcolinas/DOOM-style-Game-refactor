import math
import os
from collections import deque

import pygame as pg
from settings import (DELTA_ANGLE, HALF_HEIGHT, HALF_NUM_RAYS, SCALE,
                      SCREEN_DIST, WIDTH)


class SpriteObject:
    def __init__(
        self,
        game,
        path="resources/sprites/static_sprites/candlebra.png",
        pos=(10.5, 3.5),
        scale=0.7,
        shift=0.27,
    ):
        self.game = game
        self._player = game._player
        self.x, self.y = pos
        self.image = pg.image.load(path).convert_alpha()
        self._IMAGE_WIDTH = self.image.get_width()
        self._IMAGE_HALF_WIDTH = self.image.get_width() // 2
        self._IMAGE_RATIO = self._IMAGE_WIDTH / self.image.get_height()
        self._dx, self._dy, self.theta, self.screen_x, self.dist, self._norm_dist = (
            0,
            0,
            0,
            0,
            1,
            1,
        )
        self.sprite_half_width = 0
        self._SPRITE_SCALE = scale
        self._SPRITE_HEIGHT_SHIFT = shift

    def _get_sprite_projection(self):
        proj = SCREEN_DIST / self._norm_dist * self._SPRITE_SCALE
        proj_width, proj_height = proj * self._IMAGE_RATIO, proj

        image = pg.transform.scale(self.image, (proj_width, proj_height))

        self.sprite_half_width = proj_width // 2
        height_shift = proj_height * self._SPRITE_HEIGHT_SHIFT
        pos = (
            self.screen_x - self.sprite_half_width,
            HALF_HEIGHT - proj_height // 2 + height_shift,
        )

        self.game.raycasting.objects_to_render.append((self._norm_dist, image, pos))

    def get_sprite(self):
        dx = self.x - self._player.x
        dy = self.y - self._player.y
        self._dx, self._dy = dx, dy
        self.theta = math.atan2(dy, dx)

        delta = self.theta - self._player.angle
        if (dx > 0 and self._player.angle > math.pi) or (dx < 0 and dy < 0):
            delta += math.tau

        delta_rays = delta / DELTA_ANGLE
        self.screen_x = (HALF_NUM_RAYS + delta_rays) * SCALE

        self.dist = math.hypot(dx, dy)
        self._norm_dist = self.dist * math.cos(delta)
        if (
            -self._IMAGE_HALF_WIDTH < self.screen_x < (WIDTH + self._IMAGE_HALF_WIDTH)
            and self._norm_dist > 0.5
        ):
            self._get_sprite_projection()

    def update(self):
        self.get_sprite()


class AnimatedSprite(SpriteObject):
    def __init__(
        self,
        game,
        path="resources/sprites/animated_sprites/green_light/0.png",
        pos=(11.5, 3.5),
        scale=0.8,
        shift=0.16,
        animation_time=120,
    ):
        super().__init__(game, path, pos, scale, shift)
        self.path = path.rsplit("/", 1)[0]
        self.images = self.get_images(self.path)
        self.animation_trigger = False
        self._animation_time_prev = pg.time.get_ticks()
        self._animation_time = animation_time

    def update(self):
        super().update()
        self.check_animation_time()
        self.animate(self.images)

    def animate(self, images):
        if self.animation_trigger:
            images.rotate(-1)
            self.image = images[0]

    def check_animation_time(self):
        self.animation_trigger = False
        time_now = pg.time.get_ticks()
        if time_now - self._animation_time_prev > self._animation_time:
            self._animation_time_prev = time_now
            self.animation_trigger = True

    def get_images(self, path):
        images = deque()
        for file_name in os.listdir(path):
            if os.path.isfile(os.path.join(path, file_name)):
                img = pg.image.load(path + "/" + file_name).convert_alpha()
                images.append(img)
        return images
