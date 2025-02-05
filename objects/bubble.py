from typing import Any
import pygame
from objects.colors import BubbleColor,bubble_sprites
from physics.physics import Physics
import utils.settings as settings
from states.bubbleStates import *

class Bubble(pygame.sprite.Sprite):
    def __init__(self,
                 physics: Physics,
                color: BubbleColor = BubbleColor.BLUE
    ) -> None:
        super().__init__()

        self.physics = physics
        self.color = color

        self.radius = settings.BUBBLE_RADIUS
        self._sprites = bubble_sprites[color]
        self.set_image(self._sprites[0])
        self.rect = self.image.get_rect()

        self.rect.center = self.physics.position

        self.state = Idle()

        self._on_pop_animation_finish_handlers = list()

    def update(self, *args: Any, **kwargs: Any) -> None:
        dt = kwargs["dt"]

        self.state.update(self,dt)

    def change_direction(self):
        self.physics.change_horizontal_direction()

    def stop(self):
        self.state = Idle()
    
    @property
    def floating(self):
        return self.state.name == "floating"
    
    @property
    def shoted(self):
        return self.state.name == "shoted"
    
    @property
    def position(self):
        return self.rect.center
    
    @position.setter
    def position(self,new_pos):
        self.rect.center = new_pos
        self.physics.position = pygame.Vector2(*new_pos)

    def set_floating(self,duration: float):
        self.state = Floating(duration,self.play_pop_animation)

    def floor_hit(self):
        self.physics.speed.y = -self.physics.speed.y * 0.6
        if abs(self.physics.speed.y) < 0.2:
            self.physics.stop()

    def play_pop_animation(self):
        FRAMES_PER_IMAGE = settings.BUBBLE_TOTAL_POP_ANIMATION_FRAMES // (len(self._sprites)-1)
        self.state = Pop(self._sprites[1:],settings.BUBBLE_TOTAL_POP_ANIMATION_FRAMES,
                         FRAMES_PER_IMAGE,settings.GAME_SCALE,
                         self._pop_finished)

    def shot(self,direction):
        self.physics.direction = direction.copy()
        self.state = Shot()

    def set_image(self,image):
        self.image = pygame.transform.scale_by(image,settings.GAME_SCALE)

    def _pop_finished(self):
        for handler in self._on_pop_animation_finish_handlers:
            handler(self)


    def register_on_pop_animation_finished(self,handler):
        self._on_pop_animation_finish_handlers.append(handler)

    def unregister_on_pop_animation_finished(self,handler):
        self._on_pop_animation_finish_handlers = [h for h in self._on_pop_animation_finish_handlers if h != handler]
