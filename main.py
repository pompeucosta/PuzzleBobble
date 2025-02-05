from states.game.start_menu_state import StartMenuState

import pygame
import os
from argparse import ArgumentParser, Namespace

class Game:
    def __init__(self, args) -> None:
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        self._clock = pygame.time.Clock()
        self._state = StartMenuState(args.level)

    def run(self) -> bool:
        dt = 0
        while True:
            events = pygame.event.get()
            if not self._still_running(events):
                break

            self._state.handle_input(events)
            self._state.update(dt / 1000.0)
            self._state.draw()
            
            self._state = self._state.next_state()
            dt = self._clock.tick(60)
        
        self._exit()

    def _still_running(self, events) -> None:
        quit_event = any(event.type == pygame.QUIT for event in events)
        return self._state is not None and not quit_event

    def _exit(self) -> None:
        pygame.quit()


    @staticmethod
    def parse_args() -> Namespace:
        # Parse command line arguments
        argparser = ArgumentParser()
        argparser.add_argument(
            "-l", "--level", 
            type=int, default=1,
            help="Level number to load (starting from 1)"
        )
        args = argparser.parse_args()

        return args


if __name__ == "__main__":
    args = Game.parse_args()
    game = Game(args)
    game.run()
