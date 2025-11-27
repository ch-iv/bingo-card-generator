from dataclasses import dataclass


@dataclass
class Cell:
    row: int
    col: int
    x1: int
    y1: int
    x2: int
    y2: int

    @property
    def width(self):
        return self.x2 - self.x1

    @property
    def height(self):
        return self.y2 - self.y1

    def as_tuple(self):
        return self.row, self.col, self.x1, self.y1, self.x2, self.y2

    def top_left(self) -> tuple[int, int]:
        return self.x1, self.y1
