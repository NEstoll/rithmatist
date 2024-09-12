import math
from Lines.line import Line
import lib


class Forbiddance(Line):
    maxSegments = 100

    def __init__(self, start : tuple[float, float], end: tuple[float, float]) -> None:
        super().__init__()
        #initialize variables
        self.color = (255, 255, 255)
        self.segments = []
        self.colliding = False
        
        self.instantiate(start, end)
        self.setCollision(True)

    def setCollision(self, collision:bool):
        if collision and not self.colliding:
            for s in self.segments:
                Forbiddance.addCollision(s)
        elif not collision and self.colliding:
            for s in self.segments:
                Forbiddance.removeCollision(s)
        self.colliding = collision



    def instantiate(self, start, end) -> None:

        self.start = start
        self.end = end

        #math
        slopex = (end[0]-start[0])/Forbiddance.maxSegments
        slopey = (end[1]-start[1])/Forbiddance.maxSegments

        #create segments
        if len(self.segments) != 0:
            self.segments = []
        for i in range(0, Forbiddance.maxSegments):
            self.segments.append(Segment((start[0]+slopex*i, start[1]+slopey*i), (start[0]+slopex*(i+1), start[1]+slopey*(i+1)), self))

    @staticmethod      
    def addCollision(segment) -> None:
        collision1 = lib.getCollision(segment.start)
        collision2 = lib.getCollision(segment.end)
        if (collision1 is not collision2):
            collision3 = lib.getCollision((segment.start[0], segment.end[1]))
            collision4 = lib.getCollision((segment.end[0], segment.start[1]))
            if (collision3 is not collision1 and collision3 is not collision2):
                collision3.append(segment)
                collision4.append(segment) #must be 4 distinct, can't have only 3 collision boxes
            collision1.append(segment)
            collision2.append(segment)
        else:
            collision1.append(segment)

    @staticmethod      
    def removeCollision(segment):
        collision1 = lib.getCollision(segment.start)
        collision2 = lib.getCollision(segment.end)
        if (collision1 is not collision2):
            collision3 = lib.getCollision((segment.start[0], segment.end[1]))
            collision4 = lib.getCollision((segment.end[0], segment.start[1]))
            if (collision3 is not collision1 and collision3 is not collision2):
                collision3.remove(segment)
                collision4.remove(segment) #must be 4 distinct, can't have only 3 collision boxes
            collision1.remove(segment)
            collision2.remove(segment)
        else:
            collision1.remove(segment)


    def draw(self) -> None:
        lib.drawPoint(self.start, (255, 0, 0))
        for s in self.segments:
            s.draw()
        lib.drawPoint(self.end, (255, 0, 0))
    def update(self) -> None:
        remove = []
        for s in self.segments:
            try:
                s.update()
            except lib.LineOutofBounds:
                remove.append(s)
                #TODO refactor collision to be better
                self.removeCollision(s)
                pass
        for s in remove:
            self.segments.remove(s)


    def __repr__(self) -> str:
        return self.__str__()
    def __str__(self) -> str:
        return "LoV: start=" + str(self.start) + " end=" + str(self.end)
    def toBytes(self) -> bytes:
        return b'\x02' + int(self.start[0]).to_bytes(2, 'big')+int(self.start[1]).to_bytes(2, 'big')+int(self.end[0]).to_bytes(2, 'big')+int(self.end[1]).to_bytes(2, 'big')

class Segment(Line):
    def __init__(self, start: tuple[float, float], end: tuple[float, float], parent) -> None:
        self.start = start
        self.end = end
        self.damage = 0
        self.color = (255, 255, 255)
        self.parent = parent
    def draw(self) -> None:
        lib.drawLine(self.start, self.end, self.color+(max(255-(self.damage*2.55),0),))
    def update(self) -> None:
        if self.damage >= 100:
            raise lib.LineOutofBounds
    def dmg(self, amount) -> None:
        self.damage += amount*100/4



    def angle(self) -> float:
        return math.atan2(self.start[1]-self.end[1], self.start[0] - self.end[0])
    def __repr__(self) -> str:
        return self.__str__()
    def __str__(self) -> str:
        return "Segment from " + str(self.start) + " to " + str(self.end)