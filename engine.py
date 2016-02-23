import pygame
import errors
import logging
from pygame.locals import K_LALT, K_RALT, K_ESCAPE, QUIT
from collections import defaultdict
from pygame import Surface
from vmath import Vector2 as Vector

scenes = []


def current_scene():
    return scenes[-1]


def pop_scene():
    scenes.pop()


def push_scene(scene):
    scenes.append(scene)


def replace_scene(scene):
    scenes.pop()
    scenes.append(scene)


def commands(command, scene):
    if command == "continue":
        return
    elif command == "pop":
        pop_scene()
    elif command == "push":
        push_scene(scene)
    elif command == "replace":
        replace_scene(scene)
    elif command == "quit":
        raise errors.GameQuit


def run(display_surface, clock, menu, config=None):
    running = True

    push_scene(Splash(config, display_surface, menu))

    while running:
        td = clock.tick(config.FPS) / 1000.
        pressed = pygame.key.get_pressed()
        events = pygame.event.get()
        try:
            cur_scene = current_scene()
            commands(*cur_scene.manage(events, pressed))
            commands(*cur_scene.update(td, pressed))
            updates = cur_scene.render(display_surface)
        except errors.GameQuit:
            return
        if config.FULL_SCREEN:
            pygame.display.flip()
        else:
            pygame.display.update(updates)
        logging.info(clock.get_fps())


class Publisher(object):

    def __init__(self):
        self.subscribers = defaultdict(list)

    def publish(self, event_type, value):

        for subscriber in self.subscribers[event_type]:
            subscriber['callback'](value)

    def subscribe(self, event_type, identity, callback):
        self.subscribers[event_type].append({'identity': identity, 'callback': callback})

    def unsubscribe(self, event_type, identity):
        for subscriber in self.subscribers[event_type]:
            if subscriber['identity'] == identity:
                self.subscribers[event_type].remove(subscriber)


class Scene(Publisher):

    def __init__(self, config, display, *args, **kwargs):
        super(Scene, self).__init__()
        self.config = config
        self.display = display
        logging.debug("{} initialized.".format(str(self.__class__)))

    def manage(self, events, pressed, *args, **kwargs):
        logging.debug("{} handled events.".format(str(self.__class__)))
        for event in events:
            if event.type == QUIT:
                return "quit", None
        if (pressed[K_RALT] or pressed[K_LALT]) and pressed[K_ESCAPE]:
            return "quit", None
        return "continue", None

    def update(self, time_delta, keys_pressed, *args, **kwargs):
        logging.debug("{} updated.".format(str(self.__class__)))
        return "continue", None

    def render(self, display_surface):
        logging.debug("{} rendered.".format(str(self.__class__)))
        return []


class Splash(Scene):

    def __init__(self, config, display, next_scene=Scene, *args, **kwargs):
        super(Splash, self).__init__(config, display, *args, **kwargs)
        try:
            self.time = config.SPLASH_LENGTH
        except AttributeError:
            self.time = 3000

        try:
            title = config.TITLE
        except AttributeError:
            title = "Default Title"

        font = pygame.font.Font(pygame.font.get_default_font(), 36)
        self.logo = font.render(title, True, (255, 255, 255))
        self.rect = self.logo.get_rect()
        self.rect.center = config.RESOLUTION[0] / 2, config.RESOLUTION[1] / 2
        self.next_scene = next_scene
        self.background = Surface(config.RESOLUTION)


    def manage(self, events, pressed, *args, **kwargs):
        command, scene = super(Splash, self).manage(events, pressed, *args, **kwargs)
        if command == "quit":
            return "quit", None
        return "continue", None

    def update(self, time_delta, keys_pressed, *args, **kwargs):
        super(Splash, self).update(time_delta, keys_pressed, *args, **kwargs)
        self.time += time_delta * -1
        if self.time <= 0:
            return "replace", self.next_scene(self.config, self.display)
        else:
            return "continue", None

    def render(self, display_surface):
        super(Splash, self).render(display_surface)
        display_surface.fill((0, 0, 0))
        display_surface.blit(self.logo, self.rect)
        return [self.rect]


class FollowCam(object):

    def __init__(self, pos, target, config, max_dist=50, max_speed=10.0):
        self.pos = pos
        self.target = target
        self.max_distance = max_dist
        self.speed = max_speed
        self.offset = Vector(config.RESOLUTION[0] / 2, config.RESOLUTION[1] / 2)

    def update(self, td):
        direction = self.target.pos - self.pos
        distance = direction.length
        direction = direction.normalize()
        if distance > self.max_distance:
            self.pos += direction * self.speed * td

    def get_offset(self):
        return self.pos - self.offset
