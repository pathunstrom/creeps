from dataclasses import dataclass

from ppb.abc import Scene
from ppb.systems import System



@dataclass
class BehaviorCheck:
    scene: Scene = None


class BehaviorSystem(System):

    def __init__(self, **kwargs):
        self.activation_time = 1
        self.lapsed_time = 0

    def activate(self, engine):
        if self.lapsed_time >= self.activation_time:
            self.lapsed_time = 0
            yield BehaviorCheck()

    def on_update(self, event, signal):
        self.lapsed_time += event.time_delta
