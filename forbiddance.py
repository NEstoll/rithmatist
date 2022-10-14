import math
from line import Line
import lib


class Forbiddance(Line):
    segments = 100

    def __init__(self, start : tuple[int, int], end: tuple[int, int]) -> None:
        super().__init__()
        #initialize variables
        self.start = start
        self.end = end
        self.color = (255, 255, 255)

        #math
        slopex = (end[0]-start[0])/Forbiddance.segments
        slopey = (end[1]-start[1])/Forbiddance.segments

        #create segments
        self.segments = []
        for i in range(0, Forbiddance.segments):
            self.segments.append(Segment((start[0]+slopex*i, start[1]+slopey*i), (start[0]+slopex*(i+1), start[1]+slopey*(i+1))))
        
        #add segments to collision
        for s in self.segments:
            collision1 = lib.getCollision(s.start)
            collision2 = lib.getCollision(s.end)
            if (collision1 != collision2):
                lib.getCollision((s.start[0], s.end[1])).append(s)
                lib.getCollision((s.end[0], s.start[1])).append(s)
            collision1.append(s)
            collision2.append(s)
            
        


    def draw(self) -> None:
        lib.drawPoint(self.start, (255, 0, 0))
        for s in self.segments:
            s.draw()
        lib.drawPoint(self.end, (255, 0, 0))
    def update(self) -> None:
        for s in self.segments:
            s.update()


    def __repr__(self) -> str:
        return self.__str__()
    def __str__(self) -> str:
        return "LoV: start=" + str(self.start) + " end=" + str(self.end)
    def toBytes(self) -> bytes:
        return b'\x02' + int(self.start[0]).to_bytes(2, 'big')+int(self.start[1]).to_bytes(2, 'big')+int(self.end[0]).to_bytes(2, 'big')+int(self.end[1]).to_bytes(2, 'big')

class Segment(Line):
    def __init__(self, start: tuple[float, float], end: tuple[float, float]) -> None:
        self.start = start
        self.end = end
        self.damage = 0
        self.color = (255, 255, 255)
    def draw(self) -> None:
        lib.drawLine(self.start, self.end, self.color+(max(255-(self.damage*2.55),0),))
    def update(self) -> None:
        pass
    def dmg(self, amount):
        self.damage += amount*100/4



    def angle(self) -> float:
        return math.atan2(self.start[1]-self.end[1], self.start[0] - self.end[0])
    def __repr__(self) -> str:
        return self.__str__()
    def __str__(self) -> str:
        return "Segment from " + str(self.start) + " to " + str(self.end)