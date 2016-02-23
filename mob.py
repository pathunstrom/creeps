from pygame.sprite import DirtySprite
from pygame import K_s, K_d, K_w, K_a
from vmath import Vector2 as Vector
import random
import logging


class Player(DirtySprite):

    def __init__(self, image, player, config, _map, *groups):
        super(Player, self).__init__(*groups)
        self.map = _map
        self.image = image
        self.rect = image.get_rect()
        self.pos = Vector(0, 0)
        try:
            self.velocity = config.PLAYER_SPEED
        except AttributeError:
            self.velocity = 20
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
    sight_range = 50

    def __init__(self, image, player, camera, config, _map, *groups):
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
        self.velocity = Vector(10., 0.).rotate(random.randint(0, 360))
        self.drive = random.randint(1, 10)

    def update(self, td, camera):

        old_pos = self.pos

        if self.target is None:
            logging.debug("Target is None")
            self.get_target()
        elif len(self.target - self.pos) < 15:
            logging.critical("Target reached")
            self.get_target()
        else:
            modifier = self.target - self.pos
            self.velocity += (modifier.truncate(self.max_drive) * td)
            self.velocity.truncate(self.max_velocity)



        self.pos += self.velocity * td
        self.dirty = 1
        self.rect.center = tuple(self.pos - camera)
        self.offset = camera

    def get_target(self):
        if len(self.player.pos - self.pos) < 100:
            self.target = self.player.pos
        else:
            x = int(self.pos['x'])
            y = int(self.pos['y'])
            self.target = Vector(random.randrange(x - self.sight_range, x + self.sight_range),
                                 random.randrange(y - self.sight_range, y + self.sight_range))