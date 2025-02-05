from physics.physics import Physics
from pygame import Vector2

class KinematicPhysics(Physics):
    def __init__(self, pos, dir,acceleration=Vector2(0,0)) -> None:
        super().__init__(pos, dir, Vector2(0,0))
        self.acceleration = acceleration

    def update(self, dt):
        self.speed += Vector2(self.acceleration.x * self.direction.x,self.acceleration.y * self.direction.y) * dt
        self.position += self.speed

    def change_horizontal_direction(self):
        self.speed.x *= -1
        self.acceleration.x *= -1

    def stop(self):
        self.speed.y = 0
        self.direction.y = 0