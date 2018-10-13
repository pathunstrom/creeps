from ppb import BaseScene
from pygame import K_w
from pygame import K_a
from pygame import K_s
from pygame import K_d

from creeps.game_objects import Bush
from creeps.game_objects import Controller
from creeps.game_objects import Player
from creeps.game_objects import Spawner


class MainScene(BaseScene):

    def __init__(self, engine, **kwargs):
        super().__init__(engine, **kwargs)
        self.add(Spawner())
        controller = Controller(axes=(("horizontal", K_a, K_d),
                                      ("vertical", K_w, K_s)
                                      ),
                                buttons=())
        self.add(controller)
        self.add(Player(controller), ["player"])

    @property
    def player(self):
        return next(self.get(tag="player"))
