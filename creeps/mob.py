import logging
import random

from pygame import K_s, K_d, K_w, K_a
from pygame.sprite import DirtySprite

from pursuedpybear.vmath import Vector2 as Vector


class Player(DirtySprite):

    speed = 40

    def __init__(self, image, player, config, _map, *groups):
        super(Player, self).__init__(*groups)
        self.map = _map
        self.image = image
        self.rect = image.get_rect()
        self.pos = Vector(0, 0)
        self.velocity = self.speed
        try:
            controls = config.CONTROLS[player]
        except AttributeError:
            controls = {'up': K_w, 'down': K_s, 'left': K_a, 'right': K_d}
        except KeyError:
            controls = {'up': K_w, 'down': K_s, 'left': K_a, 'right': K_d}

        self._up = controls['up']
        self._down = controls['down']
        self._left = controls['left']
        self._right = controls['right']
        self.prev_offset = Vector(0, 0)

    def update(self, td, keys, camera):
        vert = keys[self._up] * -1 + keys[self._down]
        horiz = keys[self._left] * -1 + keys[self._right]
        if vert or horiz or self.prev_offset != camera:
            direction = Vector(horiz, vert).normalize() * (self.velocity * td)
            self.pos += direction
            self.rect.center = tuple(self.pos - camera)
            self.dirty = 1
        self.prev_offset = camera


class Creep(DirtySprite):

    max_drive = 10
    max_velocity = 30
    drag = 1
    spawn_zone = 200
    sight_range = 75
    approach_range = 30
    target_mod = 3

    def __init__(self, image, m_image, player, camera, config, _map, *groups):
        super(Creep, self).__init__(*groups)
        self.config = config
        self.player = player
        self.map = _map
        self.offset = None
        self.image = image
        self.rect = self.image.get_rect()
        self.pos = Vector(random.randrange(self.player.pos[0] - self.spawn_zone, self.player.pos[0] + self.spawn_zone),
                          random.randrange(self.player.pos[1] - self.spawn_zone, self.player.pos[1] + self.spawn_zone))
        self.rect.center = tuple(self.pos - camera)
        self.target = None
        self.get_target()
        self.velocity = Vector(10., 0.).rotate(random.randint(0, 360))
        self.drive = random.randint(1, self.max_drive)
        Miasma(self, m_image, *groups)

    def update(self, td, camera):

        old_pos = self.pos
        drive = self.target - self.pos
        try:
            target_distance = len(self.target - self.pos)
        except TypeError:
            self.get_target()
            target_distance = len(self.target - self.pos)
        if target_distance < self.approach_range:
            self.get_target()

        move = (drive.truncate(self.max_drive) * td)
        if target_distance < move.length:
            self.get_target()
        self.velocity += move
        self.velocity.truncate(self.max_velocity)

        self.pos += self.velocity * td
        self.dirty = 1
        self.rect.center = tuple(self.pos - camera)
        self.offset = camera

    def get_target(self):
        logging.debug("Acquiring target.")
        player_target = len(self.player.pos - self.pos)
        sight_distance = self.sight_range * self.target_mod
        if player_target < sight_distance:
            self.target = self.player.pos
        else:
            x = int(self.pos['x'])
            y = int(self.pos['y'])
            self.target = Vector(random.randrange(x - self.sight_range, x + self.sight_range),
                                 random.randrange(y - self.sight_range, y + self.sight_range))


class Miasma(DirtySprite):

    def __init__(self, parent, image, *groups):
        super(Miasma, self).__init__(*groups)
        self.parent = parent
        self.image = image
        self.rect = image.get_rect()
        for group in groups:
            try:
                group.change_layer(self, 2)
            except AttributeError:
                pass

    def update(self, td, camera):
        self.rect.center = tuple(self.parent.pos - camera)
        self.dirty = 1