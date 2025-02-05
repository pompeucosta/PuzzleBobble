from objects.arena.hex_grid import HexGrid
from objects.arena.hexcoord import HexCoord
from objects.bubble import Bubble
from objects.colors import BubbleColor
from physics.kinematicPhysics import KinematicPhysics

from pygame import Vector2
from os import path, listdir
from copy import deepcopy
import json

class LevelLoader:
    AVAILABLE_LEVELS = []

    def __init__(
        self,
        real_width: float = None, real_height: float = None, top_left: tuple[float, float] = (0, 0),
        initial_level_index: int = 0
    ) -> None:
        self.LEVEL_FILE_PREFIX = "lvl_"
        self.LEVEL_FILE_SUFFIX = ".json"
        self.level_directory = path.dirname(path.abspath(__file__))
        
        self.grid_properties = (real_width, real_height, top_left)
        self._get_available_levels()

        min_index = 0
        max_index = len(self.levels) - 1
        self.current_level_index = max(min_index, min(initial_level_index, max_index))


    def previous_level(self) -> None:
        self.current_level_index -= 1

    def next_level(self) -> None:
        self.current_level_index += 1

    def is_valid(self) -> bool:
        current = self.current_level_index
        return current >= 0 and current < len(self.levels)

    def load_current_level(self) -> HexGrid | None:
        if not self.is_valid():
            return None

        level_file_name = self.levels[self.current_level_index]
        level_file = path.join(self.level_directory, level_file_name)

        grid_properties = self.get_grid_properties()
        return LevelLoader.load_level(level_file, *grid_properties)

    def get_grid_properties(self) -> tuple[float, float, tuple[float, float]]:
        return deepcopy(self.grid_properties)


    def _get_available_levels(self) -> None:
        if LevelLoader.AVAILABLE_LEVELS:
            self.levels = LevelLoader.AVAILABLE_LEVELS
            return

        size_prefix = len(self.LEVEL_FILE_PREFIX)
        size_suffix = len(self.LEVEL_FILE_SUFFIX)

        def number_sortfn(file: str) -> float:
            lvl_name = file[size_prefix:-size_suffix]
            return float(lvl_name) if lvl_name.isdigit() else float('inf')

        self.levels = [
            f for f in listdir(self.level_directory)
            if f.startswith(self.LEVEL_FILE_PREFIX) and f.endswith(self.LEVEL_FILE_SUFFIX)
        ]
        self.levels.sort(key=number_sortfn)

        if not self.levels:
            raise RuntimeError(f"No levels found in directory: {self.level_directory}")

        LevelLoader.AVAILABLE_LEVELS = self.levels


    @staticmethod
    def load_level(
        level_file: str,
        real_width: float = None, real_height: float = None, top_left: tuple[float, float] = (0, 0)
    ) -> HexGrid | None:
        try:
            level_json = LevelLoader.read_json(level_file)
            width, height, bubbles = LevelLoader.get_basic_level_data(level_json)

            grid = HexGrid(width, height, real_width, real_height, top_left)
            LevelLoader.add_level_bubbles(grid, bubbles)

            return grid
        except RuntimeError as e:
            print(e)
            return None

    @staticmethod
    def add_level_bubbles(grid: HexGrid, bubbles: dict) -> None:
        for color, coords in bubbles.items():
            # Get the bubble color - skip if invalid
            bubble_color = LevelLoader.get_bubbles_color(color)
            if bubble_color is None:
                continue

            # Get the bubble coordinates and add them to the grid - skip if invalid
            bubble_coords = LevelLoader.get_bubbles_hex_coords(coords)
            for coord in bubble_coords:
                if not grid.is_valid_coord(coord):
                    print(f"Skipping bubble - Invalid position: {coord}")
                    continue

                phys = KinematicPhysics(grid.hex_to_pixel(coord),
                                        Vector2(0,0),
                                        Vector2(0,0))
                bubble = Bubble(phys,bubble_color)
                added = grid.add_bubble(bubble)
                if not added:
                    print(f"Skipping bubble - Invalid position: {coord}")


    @staticmethod
    def read_json(file: str) -> dict:
        try:
            with open(file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise RuntimeError(f"File not found: {file}")
        except json.JSONDecodeError:
            raise RuntimeError(f"Invalid JSON file: {file}")
        except Exception as e:
            raise RuntimeError(f"Error reading file: {e}")


    @staticmethod
    def get_basic_level_data(lvl_json: dict) -> tuple[int, int, dict]:
        width = lvl_json.get('width', 15)
        height = lvl_json.get('height', 20)
        bubbles = lvl_json.get('bubbles', {})

        # Check if the data is valid
        try:
            assert isinstance(width, int), f"Width must be an integer, got {type(width)}"
            assert isinstance(height, int), f"Height must be an integer, got {type(height)}"
            assert isinstance(bubbles, dict), f"Bubbles must be a dictionary, got {type(bubbles)}"
            assert width > 0, f"Width must be greater than 0, got {width}"
            assert height > 0, f"Height must be greater than 0, got {height}"
        except AssertionError as e:
            raise RuntimeError(f"Invalid level data: {e}")

        return width, height, bubbles

    @staticmethod
    def get_bubbles_color(color: str) -> BubbleColor | None:
        # Check if the color is valid - skip if invalid
        try:
            color = color.upper()
            return BubbleColor[color]
        except KeyError:
            print(f"Skipping color - Invalid bubble color: {color}")
            return None

    @staticmethod
    def get_bubbles_hex_coords(coords) -> list[HexCoord]:
        # Check if the coordinates are valid - skip if invalid
        try:
            assert isinstance(coords, list), f"Bubble coordinates must be a list, got {type(coords)}"
        except AssertionError as e:
            print(f"Skipping color - {e}")
            return []

        # Convert the coordinates to HexCoord objects or None if invalid
        hex_coords = [
            LevelLoader.get_hex_coord(coord)
            for coord in coords
        ]

        # Return only the valid coordinates
        return [
            coord for coord in hex_coords
            if coord is not None
        ]

    @staticmethod
    def get_hex_coord(coord) -> HexCoord | None:
        try:
            # Check if the coordinate is a list with 2 values
            assert isinstance(coord, list), f"Bubble coordinate must be a list, got {type(coord)}"
            assert len(coord) == 2, f"Bubble coordinate must have 2 values, got {len(coord)}"

            # Check if the values are integers (x, y)
            x, y = coord
            assert isinstance(x, int), f"X coordinate must be an integer, got {type(x)}"
            assert isinstance(y, int), f"Y coordinate must be an integer, got {type(y)}"

            # Return the HexCoord object
            return HexCoord(x, y)
        except (AssertionError, ValueError) as e:
            print(f"Skipping bubble - {e}")
            return None
