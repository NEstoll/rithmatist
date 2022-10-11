import math
from line import Line
import lib


class Forbiddance(Line):
    def __init__(self, start : tuple[int, int], end: tuple[int, int]) -> None:
        super().__init__()
        self.start = start
        self.end = end
        lib.getCollision(self.start).append(self)
        lib.getCollision(self.end).append(self)
    def draw(self):
        lib.drawLine(self.start, self.end)
    def update(self):
        pass
    def angle(self):
        return math.atan2(self.start[0]-self.end[0], self.start[1] - self.end[1])
