import pygame.event as event
from pygame.font import SysFont
from pygame.locals import USEREVENT
from pygame.sprite import DirtySprite


class Button(DirtySprite):

    def __init__(self, text, position, next_scene, clicked_event=USEREVENT, *groups):
        super(Button, self).__init__(*groups)
        font = SysFont('tahoma', 32)
        self.name = text
        self.image = font.render(text, True, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.event = clicked_event
        self.next_scene = next_scene

    def clicked(self, mouse_event):
        if self.rect.collidepoint(mouse_event.pos):
            event.post(event.Event(self.event, {"name": self.name, "command": "push", "scene": self.next_scene}))