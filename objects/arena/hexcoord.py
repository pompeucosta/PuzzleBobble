from enum import Enum

class HexDirection(Enum):
    NORTHWEST = (-1, -1)
    NORTHEAST = (-1, 1)
    EAST = (0, 2)
    SOUTHEAST = (1, 1)
    SOUTHWEST = (1, -1)
    WEST = (0, -2)

class HexCoord:
    def __init__(self, row: int, col: int) -> None:
        if not HexCoord.is_valid(row, col):
            raise ValueError(f"Invalid hex coordinates: ({row}, {col})")

        self.row = row
        self.col = col

    @staticmethod
    def is_valid(row: int, col: int) -> bool:
        return (row + col) % 2 == 0
    
    def neighbors(self) -> list["HexCoord"]:
        directions = HexDirection.__members__.values()
        return [HexCoord(self.row + dir.value[0], self.col + dir.value[1]) for dir in directions]
    

    def __eq__(self, other) -> bool:
        return isinstance(other, HexCoord) and self.row == other.row and self.col == other.col
    
    def __hash__(self) -> int:
        return hash((self.row, self.col))
    
    def __str__(self) -> str:
        return f"({self.row}, {self.col})"
    
    def __repr__(self) -> str:
        return str(self)
