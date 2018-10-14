from itertools import product
from os import getenv
from random import choices
from random import seed
from string import ascii_letters
from string import digits
from string import punctuation
from typing import Sequence

from ppb import BaseSprite
from ppb import Vector
from ppb.flags import DoNotRender
from pygame import key

DOWN_LEFT = Vector(-1, 1)
DOWN_RIGHT = Vector(1, 1)
UP_LEFT = Vector(-1, -1)
UP_RIGHT = Vector(1, -1)


class Detector:

    def point_is_in(self, p: Vector) -> bool:
        return (self.left < p.x < self.right) and (self.top < p.y < self.bottom)


class Bush(BaseSprite, Detector):

    def on_update(self, event, signal):
        player = event.scene.player
        if (player.position - self.position).length < .9:
            push_vector = Vector(0, 0)
            if self.point_is_in(player.bottom.left):
                push_vector += UP_RIGHT
            if self.point_is_in(player.bottom.right):
                push_vector += UP_LEFT
            if self.point_is_in(player.top.right):
                push_vector += DOWN_LEFT
            if self.point_is_in(player.top.left):
                push_vector += DOWN_RIGHT
            player.position += push_vector.normalize() * 0.2


class Controller(BaseSprite):
    """
    An abstraction around the keyboard.
    """
    image = DoNotRender

    def __init__(self, axes: Sequence, buttons: Sequence):
        super().__init__()
        self.__values = {}
        self.__axes = {}
        self.__buttons = {}
        for name, negative, positive in axes:
            if name in self.__values:
                raise ValueError("Can't have two controls with the same name.")
            self.__axes[name] = negative, positive
            self.__values[name] = 0
        for name, button in buttons:
            if name in self.__values:
                raise ValueError("Can't have two controls with the same name.")
            self.__buttons[name] = button
            self.__values[name] = 0

    def on_update(self, update_event, signal):
        keys = key.get_pressed()
        for name, (negative, positive) in self.__axes.items():
            self.__values[name] = keys[positive] - keys[negative]
        for name, button in self.__buttons:
            self.__values[name] = key[button]

    def __getattribute__(self, item):
        try:
            return super().__getattribute__(item)
        except AttributeError:
            v = self.__values.get(item)
            if v is None:
                raise
            return v


class Player(BaseSprite):
    """
    The player class. Will own any data that belongs to play mechanics.
    """
    speed = 5

    def __init__(self, controller, *args, **kwargs):
        self.controller = controller
        super().__init__(*args, **kwargs)

    def on_update(self, update_event, signal):
        delta = Vector(self.controller.horizontal, self.controller.vertical)
        self.position += delta.scale(self.speed) * update_event.time_delta

    def on_pre_render(self, event, signal):
        camera = event.scene.main_camera
        camera_path = self.position - camera.position
        camera.position += camera_path * 0.05


class Spawner(BaseSprite):
    """
    This is where most of the code for adding objects to the game exists.
    """
    image = DoNotRender

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _seed = getenv("CREEPS_SEED")
        if _seed is None:
            _seed = ''.join(choices(ascii_letters + digits + punctuation, k=10))
        self.seed = _seed
        self.choices = (Bush, None)
        self.weights = (10, 90)
        self.created_zones = {}

    def on_pre_render(self, event, signal):
        core_position = event.scene.player.position
        min_x = int((core_position.x // 10) * 10)
        min_y = int((core_position.y // 10) * 10)
        if (min_x, min_y) not in self.created_zones:
            _seed = self.seed + f"{min_x}-{min_y}"
            seed(_seed)
            results = choices(self.choices, weights=self.weights, k=100)
            self.created_zones[(min_x, min_y)] = {"spawned": True, "classes": results}
            for (x, y), cls in zip(product(range(min_x, min_x + 10), range(min_y, min_y + 10)), results):
                if cls is not None:
                    event.scene.add(cls(scene=event.scene, pos=Vector(x, y)))
