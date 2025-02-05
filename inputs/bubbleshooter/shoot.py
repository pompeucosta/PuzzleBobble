from inputs.command import Command

class Shoot(Command):
    def __init__(self,bubble_shooter) -> None:
        self._bubble_shooter = bubble_shooter

    def on_start(self):
        self._bubble_shooter.shoot()