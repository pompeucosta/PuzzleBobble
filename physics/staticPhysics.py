from physics.physics import Physics
from pygame import Vector2
from utils.settings import GAME_SCALE

class StaticPhysics(Physics):
    def __init__(self, pos, dir=Vector2(0,0), speed=Vector2(200,200)) -> None:
        super().__init__(pos,dir, speed)

    def update(self, dt):
        self.position += Vector2(self.direction.x * self.speed.x * GAME_SCALE,self.direction.y * self.speed.y * GAME_SCALE) * dt

    def change_horizontal_direction(self):
        self.direction.x *= -1

    def stop(self):
        self.speed.x = 0
        self.speed.y = 0