from inputs.command import Command

class Next(Command):
    def __init__(self, menu) -> None:
        self._menu = menu

    def on_triggered(self):
        self._menu.next_option()

class Previous(Command):
    def __init__(self, menu) -> None:
        self._menu = menu

    def on_triggered(self):
        self._menu.previous_option()

class Select(Command):
    def __init__(self, menu) -> None:
        self._menu = menu

    def on_triggered(self):
        self._menu.select_option()
