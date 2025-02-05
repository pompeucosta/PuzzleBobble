from states.game.menu_state import MenuState
import states.game.start_menu_state as sms
import utils.settings as settings

class GameOverMenuState(MenuState):
    def __init__(self, score: int, level: int, win: bool) -> None:
        caption = settings.GAME_OVER_MENU_CAPTION
        options = {
            settings.PLAY_AGAIN_OPTION: self._on_play_again,
            settings.START_MENU_OPTION: self._on_start_menu,
            settings.EXIT_OPTION: self._on_exit
        }
        information = [
            settings.WIN_INFORMATION if win else settings.LOSE_INFORMATION,
            f"{settings.SCORE_INFORMATION}{score}",
            f"{settings.LEVEL_INFORMATION}{level}"
        ]

        super().__init__(caption, options, information)
        self._level = level

    def _on_play_again(self):
        self._next_state = sms.PlayState(self._level)
    
    def _on_start_menu(self):
        self._next_state = sms.StartMenuState()
    
    def _on_exit(self):
        self._next_state = None
