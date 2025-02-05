from inputs.command import Command
from enum import Enum

class Direction(Enum):
    LEFT = 0
    RIGHT = 1

class Rotate(Command):
    def __init__(self,bubble_shooter,direction: Direction) -> None:
        self._bubble_shooter = bubble_shooter
        self._direction = direction

    def on_triggered(self):
        self._bubble_shooter.rotate(self._direction)