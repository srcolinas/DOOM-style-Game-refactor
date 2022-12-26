import pygame as pg


class Sound:
    def __init__(self, game):
        self.game = game
        pg.mixer.init()
        self._path = "resources/sound/"
        self.shotgun = pg.mixer.Sound(self._path + "shotgun.wav")
        self.npc_pain = pg.mixer.Sound(self._path + "npc_pain.wav")
        self.npc_death = pg.mixer.Sound(self._path + "npc_death.wav")
        self.npc_shot = pg.mixer.Sound(self._path + "npc_attack.wav")
        self.npc_shot.set_volume(0.2)
        self.player_pain = pg.mixer.Sound(self._path + "player_pain.wav")
        pg.mixer.music.set_volume(0.4)
