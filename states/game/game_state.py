from abc import ABC, abstractmethod

class GameState(ABC):
    @abstractmethod
    def handle_input(self, events) -> None:
        pass

    @abstractmethod
    def update(self, dt: float) -> None:
        pass

    @abstractmethod
    def draw(self) -> None:
        pass

    @abstractmethod
    def next_state(self) -> "GameState":
        return self

