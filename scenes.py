from engine import Scene, FollowCam
import pygame.sprite as sprite
import ui
import mob
from pygame.locals import MOUSEBUTTONDOWN, USEREVENT
from pygame import Surface
from vmath import Vector2 as Vector
import logging


class Menu(Scene):

    PUSH_SCENE = USEREVENT

    def __init__(self, config, *args, **kwargs):
        super(Menu, self).__init__(config, *args, **kwargs)
        self.interface = sprite.LayeredDirty()
        button_pos = config.RESOLUTION[0] / 2, config.RESOLUTION[1] / 2
        button = ui.Button("Play", button_pos, Game, Menu.PUSH_SCENE, self.interface)
        self.subscribe(MOUSEBUTTONDOWN, button.name, button.clicked)
        self.background = Surface(config.RESOLUTION)

    def manage(self, events, pressed, *args, **kwargs):
        command, scene = super(Menu, self).manage(events, pressed, *args, **kwargs)
        if command == "quit":
            return command, scene

        for event in events:
            if event.type == Menu.PUSH_SCENE:
                return event.command, event.scene(self.config, self.display)
            self.publish(event.type, event)
        return 'continue', None

    def render(self, display_surface):
        super(Menu, self).render(display_surface)
        return self.interface.draw(display_surface, self.background)


class Game(Scene):

    def __init__(self, config, *args, **kwargs):
        super(Game, self).__init__(config, *args, **kwargs)
        self.background = Surface(config.RESOLUTION)
        self.rendering = sprite.LayeredDirty()
        self.player = sprite.GroupSingle()
        self.creeps = sprite.Group()
        image = Surface((20, 20)).convert(self.display)
        image.fill((255, 255, 255))
        mob.Player(image, 0, config, self.rendering, self.player, self.rendering)
        self.rendering.change_layer(self.player.sprite, 1)
        self.camera = FollowCam(Vector(0, 0), self.player.sprite, config,
                                max_dist=100, max_speed=(config.PLAYER_SPEED * 1.5))
        offset = self.camera.get_offset()
        image = Surface((20, 20)).convert(self.display)
        image.fill((0, 128, 0))
        for x in xrange(config.INITIAL_SPAWN):
            mob.Creep(image, self.player.sprite, offset, config, self.rendering, self.creeps, self.rendering)

    def manage(self, events, pressed, *args, **kwargs):
        return super(Game, self).manage(events, pressed, *args, **kwargs)

    def update(self, time_delta, keys_pressed, *args, **kwargs):
        super(Game, self).update(time_delta, keys_pressed, *args, **kwargs)
        self.camera.update(time_delta)
        self.player.update(time_delta, keys_pressed, self.camera.get_offset())
        self.creeps.update(time_delta, self.camera.get_offset())
        return "continue", None

    def render(self, display_surface):
        super(Game, self).render(display_surface)
        return self.rendering.draw(display_surface, self.background)
