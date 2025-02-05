from abc import ABC, abstractmethod
from pygame import Vector2

class Physics(ABC):
    def __init__(self,pos: Vector2,dir: Vector2,speed: Vector2) -> None:
        self.direction = dir.copy()
        self.speed = speed.copy()
        self.position = pos.copy()

    @abstractmethod
    def update(self,dt):
        pass

    @abstractmethod
    def change_horizontal_direction(self):
        pass

    @abstractmethod
    def stop(self):
        pass