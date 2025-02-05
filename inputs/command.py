from abc import ABC

class Command(ABC):
    def on_start(self):
        pass

    def on_triggered(self):
        pass