from typing import Sequence

from ppb import BaseSprite
from ppb import Vector
from ppb.flags import DoNotRender
from pygame import key


class Controller(BaseSprite):
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
