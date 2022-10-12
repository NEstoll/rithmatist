import math
from operator import ne
from line import Line
import lib


class Forbiddance(Line):
    segments = 100

    def __init__(self, start : tuple[int, int], end: tuple[int, int]) -> None:
        super().__init__()
        self.start = start
        self.end = end
        collision = lib.getCollision(self.start)
        collision.append(self)
        lib.getCollision(self.end).append(self)

        slopex = (end[0]-start[0])/lib.collisionNum
        slopey = (end[1]-start[1])/lib.collisionNum

        for i in range(0, lib.collisionNum):
            if not collision == lib.getCollision((start[0]+slopex*i, start[1]+slopey*i)):
                collision = lib.getCollision((start[0]+slopex*i, start[1]+slopey*i))
                collision.append(self)


    def draw(self) -> None:
        lib.drawLine(self.start, self.end)
    def update(self) -> None:
        pass
    def angle(self) -> float:
        return math.atan2(self.start[0]-self.end[0], self.start[1] - self.end[1])
    def __repr__(self) -> str:
        return self.__str__()
    def __str__(self) -> str:
        return "LoV: start=" + str(self.start) + " end=" + str(self.end)
    def toBytes(self) -> bytes:
        return b'\x02' + int(self.start[0]).to_bytes(2, 'big')+int(self.start[1]).to_bytes(2, 'big')+int(self.end[0]).to_bytes(2, 'big')+int(self.end[1]).to_bytes(2, 'big')

