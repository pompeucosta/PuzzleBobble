from states.game.menu_state import MenuState
from states.game.play_state import PlayState
import utils.settings as settings

class StartMenuState(MenuState):
    def __init__(self, level: int = 1) -> None:
        caption = settings.START_MENU_CAPTION
        options = {
            settings.PLAY_OPTION: self._on_play,
            settings.EXIT_OPTION: self._on_exit
        }

        super().__init__(caption, options)
        self._initial_level = level

    def _on_play(self):
        self._next_state = PlayState(self._initial_level)

    def _on_exit(self):
        self._next_state = None
