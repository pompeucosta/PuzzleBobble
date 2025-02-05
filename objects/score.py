from objects.bubble import Bubble
from objects.colors import BubbleColor

class Score:
    def __init__(self) -> None:
        self._score = 0
        self._color_to_points = {
            BubbleColor.RED: 1,
            BubbleColor.GREEN: 2,
            BubbleColor.BLUE: 3,
            BubbleColor.YELLOW: 4,
            BubbleColor.BLACK: 5,
            BubbleColor.GRAY: 6,
            BubbleColor.PURPLE: 7,
            BubbleColor.ORANGE: 8 
        }

    @property
    def score(self):
        return self._score

    def handle_bubble_pop(self,bubble: Bubble):
        points = self._color_to_points.get(bubble.color,None)
        if  points != None:
            self._score += points
        else:
            print(f"[SCORE] unknown color {str(bubble.color)}")