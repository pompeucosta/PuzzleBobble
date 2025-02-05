from typing import Any
from objects.arena.hexcoord import HexCoord
from objects.colors import BubbleColor
from objects.bubble import Bubble
import pygame
import utils.settings as settings

class HexGrid(pygame.sprite.Group):
    def __init__(
        self,
        width: int, height: int,
        real_width: float = None, real_height: float = None,
        top_left: tuple[float, float] = (0, 0)
    ) -> None:
        super().__init__()
        self.width = width
        self.height = height
        if self.width < 1 or self.height < 1:
            raise ValueError("Width and height must be at least 1")

        self.real_width = real_width if real_width is not None else self.width
        self.real_height = real_height if real_height is not None else self.height
        if self.real_width <= 0 or self.real_height <= 0:
            raise ValueError("Real width and height must be positive")

        self.top_left = top_left
        self.scale = (self.real_width / self.width, self.real_height / self.height)
        self._calculate_playable_area()

        self.hex_to_bubble: dict[HexCoord,Bubble] = {}

        self._on_bubble_pop_handlers = list()
        self._on_bubble_float_handlers = list()
        self._on_empty_handlers = list()

    def add_bubble(self, bubble: Bubble):
        hex_pos = self._pixel_to_hex(bubble.position)
        if not self.is_valid_coord(hex_pos):
            return None

        new_pos = self.hex_to_pixel(hex_pos)
        bubble.position = (new_pos.x,new_pos.y)
        self.hex_to_bubble[hex_pos] = bubble

        self.add(bubble)
        return hex_pos
    
    def move_grid_down(self,amount):
        self.top_left = (self.top_left[0],self.top_left[1] + amount)
        self._update_bubbles_pos(amount)
        self._calculate_playable_area()

    def _calculate_playable_area(self) -> None:
        self.playable_width = self.real_width - 20
        self.playable_height = self.real_height - 10
        self.playable_scale = (self.playable_width / self.width, self.playable_height / self.height)

        scale_x, scale_y = self.playable_scale
        top_left_x, top_left_y = self.top_left
        top_left_x, top_left_y = (top_left_x + scale_x / 2, top_left_y + scale_y / 2)
        self.playable_top_left = (top_left_x + 3 * settings.GAME_SCALE, top_left_y + 3 * settings.GAME_SCALE)

    def _get_bubble(self, hexcoord: HexCoord) -> Bubble | None:
        return self.hex_to_bubble.get(hexcoord,None)

    def is_valid_coord(self, coord: HexCoord) -> bool:
        if coord.row < 0 or coord.row >= self.height or coord.col < 0 or coord.col >= self.width:
            return False
        elif self._get_bubble(coord) is not None:
            return False
        return True

    def _get_connected_bubbles(self, hexcoord: HexCoord, color: BubbleColor = None) -> list[Bubble]:
        coords_to_check = [hexcoord]
        connected_bubbles = []
        coords_checked = []

        while coords_to_check:
            coord = coords_to_check.pop(0)
            coords_checked.append(coord)

            bubble = self._get_bubble(coord)
            if bubble is None or (color is not None and bubble.color != color):
                continue

            connected_bubbles.append(bubble)
            coords_to_check.extend([
                neighbor for neighbor in coord.neighbors()
                if neighbor not in coords_to_check and neighbor not in coords_checked
            ])

        return connected_bubbles


    def _pop_bubbles_from(self, hexcoord: HexCoord) -> bool:
        bubble = self._get_bubble(hexcoord)
        if bubble is None:
            return False
        
        adjacent_bubbles = self._get_connected_bubbles(hexcoord, bubble.color)
        if len(adjacent_bubbles) < 3:
            return False
        
        for bubble in adjacent_bubbles:
            if len(self._on_bubble_pop_handlers) > 0:
                for callback in self._on_bubble_pop_handlers:
                    callback(bubble)

            self._remove_bubble(bubble)

        self._pop_floating_bubbles()
        self._check_empty()
        
        return True
    

    def _remove_bubble(self,bubble: Bubble):
        h = None
        for hex,b in self.hex_to_bubble.items():
            if bubble == b:
                h = hex
                break

        if h != None:
            del self.hex_to_bubble[hex]
            self.remove(bubble)

    def _get_floating_bubbles(self): 
        first_row = 0
        non_floating_bubbles = set()
        for hex,bubble in self.hex_to_bubble.items():
            if hex.row != first_row:
                continue
            
            if bubble not in non_floating_bubbles:
                non_floating_bubbles.add(bubble)

            neigh = self._get_connected_bubbles(hex)
            if neigh:
                non_floating_bubbles.update(neigh)

        return [bubble for bubble in self.sprites() if bubble not in non_floating_bubbles]

    def _pop_floating_bubbles(self) -> None:
        floating_bubbles = self._get_floating_bubbles()

        for bubble in floating_bubbles:
            if len(self._on_bubble_float_handlers) > 0:
                for callback in self._on_bubble_float_handlers:
                    callback(bubble)
                    
            self._remove_bubble(bubble)
    
    def _check_empty(self) -> None:
        if self.sprites():
            return
        
        if len(self._on_empty_handlers) > 0:
            for callback in self._on_empty_handlers:
                callback()


    def get_present_colors(self) -> set[BubbleColor]:
        return set(bubble.color for bubble in self.sprites())
    

    def _pixel_to_hex(self, position: tuple[float, float]) -> HexCoord:
        x, y = position
        scale_x, scale_y = self.playable_scale
        top_left_x, top_left_y = self.playable_top_left

        # pixel -> arena
        pixel_arena_x, pixel_arena_y = x - top_left_x, y - top_left_y
        arena_col = pixel_arena_x / scale_x
        arena_row = pixel_arena_y / scale_y

        # arena -> hex (rounded)
        rounded_row = round(arena_row)
        rounded_col = round(arena_col)
        row_multiplier, col_multiplier = 2, 1
        diff_fn = lambda c: row_multiplier * abs(c.row - arena_row) + col_multiplier * abs(c.col - arena_col)
        
        # non hex -> hex (closest between left and right)
        if not HexCoord.is_valid(rounded_row, rounded_col):
            left_coord = HexCoord(rounded_row, rounded_col - 1)
            right_coord = HexCoord(rounded_row, rounded_col + 1)
            rounded_col = min([left_coord, right_coord], key=diff_fn).col

        # possible hex coord + neighbors
        coord = HexCoord(rounded_row, rounded_col)
        neighbors = coord.neighbors()
        neighbors.sort(key=diff_fn)

        # find the first valid neighbor (or the original coord)
        while not self.is_valid_coord(coord) and neighbors:
            coord = neighbors.pop(0)

        # not found?
        if not self.is_valid_coord(coord):
            print("PANIC! No valid hex coord found")

        return coord
    
    def hex_to_pixel(self,hex_coord: HexCoord):
        scale_x, scale_y = self.playable_scale
        top_left_x, top_left_y = self.playable_top_left

        pixel_arena_x = hex_coord.col * scale_x
        pixel_arena_y = hex_coord.row * scale_y

        x = pixel_arena_x + top_left_x
        y = pixel_arena_y + top_left_y

        return pygame.Vector2(x,y)

    
    def _update_bubbles_pos(self,move_amount):
        for bubble in self.sprites():
            x,y = bubble.position
            bubble.position = (x,y + move_amount)


    def register_on_bubble_pop_handler(self,handler):
        self._on_bubble_pop_handlers.append(handler)

    def register_on_bubble_float_handler(self,handler):
        self._on_bubble_float_handlers.append(handler)
    
    def register_on_empty_handler(self,handler):
        self._on_empty_handlers.append(handler)

    def unregister_on_bubble_pop_handler(self,handler):
        self._on_bubble_pop_handlers = [h for h in self._on_bubble_pop_handlers if h != handler]
    
    def unregister_on_bubble_float_handler(self,handler):
        self._on_bubble_float_handlers = [h for h in self._on_bubble_float_handlers if h != handler]
    
    def unregister_on_empty_handler(self,handler):
        self._on_empty_handlers = [h for h in self._on_empty_handlers if h != handler]
