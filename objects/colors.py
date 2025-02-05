from enum import Enum
from pygame.surface import Surface

class BubbleColor(Enum):
    RED = (255, 0, 0)
    GREEN = (0, 200, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 200, 32)
    BLACK = (0, 0, 0)
    GRAY = (192, 192, 192)
    PURPLE = (128, 0, 128)
    ORANGE = (223, 133, 0)


bubble_sprites: dict[BubbleColor,list[Surface]] = {}
colorList = list(BubbleColor)