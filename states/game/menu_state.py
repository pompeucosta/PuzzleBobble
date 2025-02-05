from states.game.game_state import GameState
from inputs.inputHandler import InputHandler
from inputs.menu.option_navigation import Next, Previous, Select
import utils.settings as settings

import pygame
from typing import Callable

class MenuState(GameState):
    def __init__(self, caption: str, options: dict[str, Callable], information: list[str] = []) -> None:
        self._information = information
        self._options = options

        self._next_state = None if len(options) == 0 else self
        self._selected_option = 0
        self._create_input_handler()

        pygame.display.set_caption(caption)
        self._display = pygame.display.set_mode(settings.MENU_WINDOW_SIZE)
        self._information_font = pygame.font.Font(None, settings.INFORMATION_FONT_SIZE)
        self._option_font = pygame.font.Font(None, settings.OPTION_FONT_SIZE)
        self._calculate_layout()


    def _create_input_handler(self):
        prev_command, next_command = Previous(self), Next(self)
        select_command = Select(self)
    
        self._input_handler = InputHandler()
        self._input_handler.bind_command(prev_command, pygame.K_UP)
        self._input_handler.bind_command(next_command, pygame.K_DOWN)
        self._input_handler.bind_command(select_command, pygame.K_RETURN)

    def handle_input(self, events) -> None:
        for event in events:
            if event.type == pygame.KEYDOWN:
                self._input_handler.input_triggered(event.key)


    def next_option(self):
        if len(self._options) != 0:
            self._selected_option = (self._selected_option + 1) % len(self._options)
    
    def previous_option(self):
        if len(self._options) != 0:
            self._selected_option = (self._selected_option - 1) % len(self._options)
    
    def select_option(self):
        if len(self._options) != 0:
            options_fn = list(self._options.values())
            options_fn[self._selected_option]()

    def update(self, dt: float) -> None:
        pass


    def _calculate_layout(self) -> None:
        width, height = self._display.get_size()

        self._information_total_height = len(self._information) * settings.INFORMATION_SPACING
        self._options_total_height = len(self._options) * settings.OPTION_SPACING

        self._information_x = self._option_x = width / 2

        self._information_start_y = height / 4 - self._information_total_height / 2

        self._options_start_y = height / 2 - self._options_total_height / 2 if len(self._information) == 0 \
            else height / 2 + (height / 2 - self._options_total_height) / 2

    def draw(self) -> None:
        self._display.fill(settings.BG_COLOR)

        for i, text in enumerate(self._information):
            x = self._information_x
            y = self._information_start_y + i * settings.INFORMATION_SPACING

            text_surface = self._information_font.render(text, True, settings.INFORMATION_COLOR)
            text_rect = text_surface.get_rect(center=(x, y))

            self._display.blit(text_surface, text_rect)
        
        for i, option in enumerate(self._options.keys()):
            x = self._option_x
            y = self._options_start_y + i * settings.OPTION_SPACING

            color = settings.OPTION_SELECTED_COLOR if i == self._selected_option else settings.OPTION_COLOR
            text_surface = self._option_font.render(option, True, color)
            text_rect = text_surface.get_rect(center=(x, y))

            self._display.blit(text_surface, text_rect)

        pygame.display.flip()

    def next_state(self) -> GameState:
        return self._next_state