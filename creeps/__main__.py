from ppb import GameEngine
from ppb.systems import Updater, Renderer, PygameEventPoller, PygameMouseSystem

from creeps.scenes import MainScene
from creeps.systems import BehaviorSystem

ge = GameEngine(MainScene,
                systems=(Updater, BehaviorSystem, Renderer, PygameEventPoller, PygameMouseSystem),
                scene_kwargs={"background_color": (25, 100, 50)}
                )

with ge:
    ge.run()
