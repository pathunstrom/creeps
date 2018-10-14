from random import random as rand

from ppb import Vector


def seek(sprite, event, signal):
    desired_velocity = (sprite.target - sprite.position).scale(sprite.speed)
    steering_force = (desired_velocity - sprite.velocity).scale(sprite.max_force)
    sprite.velocity = (sprite.velocity + steering_force).truncate(sprite.speed)


def wander(sprite, event, signal):
    circle = sprite.velocity.scale(sprite.speed / 2)
    angle_change = rand() * sprite.angle_change - sprite.angle_change * .5
    sprite.wander_angle = (sprite.wander_angle + angle_change) % 360
    displacement = Vector(0, -1).rotate(sprite.wander_angle).scale(sprite.circle_radius)
    _wander = circle + displacement
    sprite.velocity = (sprite.velocity + _wander).truncate(sprite.speed)
