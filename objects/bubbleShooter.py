import pygame
from inputs.inputHandler import InputHandler
from inputs.bubbleshooter.shoot import Shoot
from inputs.bubbleshooter.rotate import Rotate,Direction
import utils.settings as settings

class Arrow(pygame.sprite.Sprite):
    def __init__(self,init_pos: pygame.Vector2,group,arrow_image_path) -> None:
        super().__init__(group)
        self._pos = init_pos
        self._angle = 0

        self._create_image(arrow_image_path)
        self.rotate(0)
        
    def rotate(self, angle: float):
        self._angle += angle
        self.image = pygame.transform.rotate(self._original_image,-self._angle)
        self.rect = self.image.get_rect(center=self._pos)

    def _create_image(self,image_path):
        self._original_image = pygame.image.load(image_path).convert_alpha()
        self._original_image = pygame.transform.scale_by(self._original_image,settings.GAME_SCALE)
        self.image = self._original_image
        self.rect = self.image.get_rect()
        self.rect.center = self._pos


class BubbleShooter(pygame.sprite.Group):
    def __init__(self,pos: pygame.Vector2,shooter_image_path,arrow_image_path) -> None:
        super().__init__()

        self._shootDir = pygame.Vector2(0,-1)
        self.center = pos.copy()

        self._create_sprite_and_arrow(shooter_image_path,arrow_image_path)
        self._create_input_handler()

        self._on_shoot_callbacks = list()
        self._angle = 90

    @property
    def input_handler(self):
        return self._input_handler
    
    @property
    def position(self):
        return self.center

    def _create_sprite_and_arrow(self,shooter_image_path,arrow_image_path):
        sprite = pygame.sprite.Sprite(self)

        sprite.image = pygame.image.load(shooter_image_path).convert_alpha()
        sprite.image = pygame.transform.scale_by(sprite.image,settings.GAME_SCALE)

        sprite.rect = sprite.image.get_rect()
        sprite.rect.center = self.center

        self._arrow = Arrow(pygame.Vector2(*sprite.rect.center),self,arrow_image_path)
        self.add(sprite,self._arrow)

    def _create_input_handler(self):
        self._input_handler = InputHandler()
        self._input_handler.bind_command(Shoot(self),pygame.K_SPACE)
        self._input_handler.bind_command(Rotate(self,Direction.LEFT),pygame.K_LEFT)
        self._input_handler.bind_command(Rotate(self,Direction.RIGHT),pygame.K_RIGHT)

    def shoot(self):
        for callback in self._on_shoot_callbacks:
            callback(self._shootDir)

    def rotate(self,direction: Direction):
        dir = -1 if direction == Direction.LEFT else 1

        angle = settings.BUBBLE_SHOOTER_ROTATION_DEGREES * dir
        if self._angle + angle < settings.BUBBLE_SHOOTER_MINIMUM_ROTATION or self._angle + angle > settings.BUBBLE_SHOOTER_MAXIMUM_ROTATION:
            return None
        
        self._angle += angle

        self._shootDir.rotate_ip(angle)
        self._arrow.rotate(angle)

    def register_on_shoot_event(self,callback):
        self._on_shoot_callbacks.append(callback)

    def unregister_on_shoot_event(self,callback):
        self._on_shoot_callbacks = [c for c in self._on_shoot_callbacks if c != callback]
