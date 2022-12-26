from random import choices, randrange

import pygame as pg
from npc import CacoDemonNPC, CyberDemonNPC, SoldierNPC
from sprite_object import AnimatedSprite


class ObjectHandler:
    def __init__(self, game):
        self.game = game
        self._sprite_list = []
        self._npc_list = []
        self._anim_sprite_path = "resources/sprites/animated_sprites/"
        add_sprite = self._add_sprite
        self.npc_positions = {}

        # spawn npc
        self._enemies = 20  # npc count
        self._npc_types = [SoldierNPC, CacoDemonNPC, CyberDemonNPC]
        self._weights = [70, 20, 10]
        self._restricted_area = {(i, j) for i in range(10) for j in range(10)}
        self._spawn_npc()

        # sprite map
        add_sprite(AnimatedSprite(game))
        add_sprite(AnimatedSprite(game, pos=(1.5, 1.5)))
        add_sprite(AnimatedSprite(game, pos=(1.5, 7.5)))
        add_sprite(AnimatedSprite(game, pos=(5.5, 3.25)))
        add_sprite(AnimatedSprite(game, pos=(5.5, 4.75)))
        add_sprite(AnimatedSprite(game, pos=(7.5, 2.5)))
        add_sprite(AnimatedSprite(game, pos=(7.5, 5.5)))
        add_sprite(AnimatedSprite(game, pos=(14.5, 1.5)))
        add_sprite(AnimatedSprite(game, pos=(14.5, 4.5)))
        add_sprite(
            AnimatedSprite(
                game, path=self._anim_sprite_path + "red_light/0.png", pos=(14.5, 5.5)
            )
        )
        add_sprite(
            AnimatedSprite(
                game, path=self._anim_sprite_path + "red_light/0.png", pos=(14.5, 7.5)
            )
        )
        add_sprite(
            AnimatedSprite(
                game, path=self._anim_sprite_path + "red_light/0.png", pos=(12.5, 7.5)
            )
        )
        add_sprite(
            AnimatedSprite(
                game, path=self._anim_sprite_path + "red_light/0.png", pos=(9.5, 7.5)
            )
        )
        add_sprite(
            AnimatedSprite(
                game, path=self._anim_sprite_path + "red_light/0.png", pos=(14.5, 12.5)
            )
        )
        add_sprite(
            AnimatedSprite(
                game, path=self._anim_sprite_path + "red_light/0.png", pos=(9.5, 20.5)
            )
        )
        add_sprite(
            AnimatedSprite(
                game, path=self._anim_sprite_path + "red_light/0.png", pos=(10.5, 20.5)
            )
        )
        add_sprite(
            AnimatedSprite(
                game, path=self._anim_sprite_path + "red_light/0.png", pos=(3.5, 14.5)
            )
        )
        add_sprite(
            AnimatedSprite(
                game, path=self._anim_sprite_path + "red_light/0.png", pos=(3.5, 18.5)
            )
        )
        add_sprite(AnimatedSprite(game, pos=(14.5, 24.5)))
        add_sprite(AnimatedSprite(game, pos=(14.5, 30.5)))
        add_sprite(AnimatedSprite(game, pos=(1.5, 30.5)))
        add_sprite(AnimatedSprite(game, pos=(1.5, 24.5)))

    def _spawn_npc(self):
        for i in range(self._enemies):
            npc = choices(self._npc_types, self._weights)[0]
            pos = x, y = randrange(self.game.map.cols), randrange(self.game.map.rows)
            while (pos in self.game.map.world_map) or (pos in self._restricted_area):
                pos = x, y = randrange(self.game.map.cols), randrange(
                    self.game.map.rows
                )
            self._add_npc(npc(self.game, pos=(x + 0.5, y + 0.5)))

    def _check_win(self):
        if not len(self.npc_positions):
            self.game.object_renderer.win()
            pg.display.flip()
            pg.time.delay(1500)
            self.game.new_game()

    def update(self):
        self.npc_positions = {npc.map_pos for npc in self._npc_list if npc.alive}
        [sprite.update() for sprite in self._sprite_list]
        [npc.update() for npc in self._npc_list]
        self._check_win()

    def _add_npc(self, npc):
        self._npc_list.append(npc)

    def _add_sprite(self, sprite):
        self._sprite_list.append(sprite)
