import pygame as pg
from settings import FLOOR_COLOR, HALF_HEIGHT, HEIGHT, RES, TEXTURE_SIZE, WIDTH


class ObjectRenderer:
    def __init__(self, game):
        self.game = game
        self._screen = game.screen
        self.wall_textures = self._load_wall_textures()
        self._sky_image = self._get_texture(
            "resources/textures/sky.png", (WIDTH, HALF_HEIGHT)
        )
        self._sky_offset = 0
        self._blood_screen = self._get_texture(
            "resources/textures/blood_screen.png", RES
        )
        self._digit_size = 90
        self._digit_images = [
            self._get_texture(
                f"resources/textures/digits/{i}.png", [self._digit_size] * 2
            )
            for i in range(11)
        ]
        self._digits = dict(zip(map(str, range(11)), self._digit_images))
        self._game_over_image = self._get_texture(
            "resources/textures/game_over.png", RES
        )
        self._win_image = self._get_texture("resources/textures/win.png", RES)

    def draw(self):
        self._draw_background()
        self._render_game_objects()
        self._draw_player_health()

    def win(self):
        self._screen.blit(self._win_image, (0, 0))

    def game_over(self):
        self._screen.blit(self._game_over_image, (0, 0))

    def _draw_player_health(self):
        health = str(self.game.player.health)
        for i, char in enumerate(health):
            self._screen.blit(self._digits[char], (i * self._digit_size, 0))
        self._screen.blit(self._digits["10"], ((i + 1) * self._digit_size, 0))

    def player_damage(self):
        self._screen.blit(self._blood_screen, (0, 0))

    def _draw_background(self):
        self._sky_offset = (self._sky_offset + 4.5 * self.game.player.rel) % WIDTH
        self._screen.blit(self._sky_image, (-self._sky_offset, 0))
        self._screen.blit(self._sky_image, (-self._sky_offset + WIDTH, 0))
        # floor
        pg.draw.rect(self._screen, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HEIGHT))

    def _render_game_objects(self):
        list_objects = sorted(
            self.game.raycasting.objects_to_render, key=lambda t: t[0], reverse=True
        )
        for depth, image, pos in list_objects:
            self._screen.blit(image, pos)

    @staticmethod
    def _get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)

    def _load_wall_textures(self):
        return {
            1: self._get_texture("resources/textures/1.png"),
            2: self._get_texture("resources/textures/2.png"),
            3: self._get_texture("resources/textures/3.png"),
            4: self._get_texture("resources/textures/4.png"),
            5: self._get_texture("resources/textures/5.png"),
        }
