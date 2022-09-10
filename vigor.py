import math
import lib
from line import Line
from warding import Warding
from forbiddance import Forbiddance

class Vigor(Line):
    #global vars
    maxLength = 100
    speed = .2
    
    def __init__(self, start : tuple[int, int], end: tuple[int, int]) -> None:
        super().__init__()
        #vars
        self.length=self.maxLength
        self.collisions = []
        #instantiate position
        self.startx = start[0]
        self.starty = start[1]
        self.endx = end[0]
        self.endy = end[1]
        #math
        self.dy = (self.endy-self.starty)/self.maxLength
        self.dx = (self.endx-self.startx)/self.maxLength
        self.actual = (self.startx, self.starty)
        self.amplitude = 0
        #add self to collision
        lib.getCollision(self.actual).append(self)

    def draw(self) -> None:
        prev = (self.startx - self.dy*math.sin(self.amplitude)*self.maxLength/8,self.starty + self.dx*math.sin(self.amplitude)*self.maxLength/8)
        for i in range(1, self.length):
            # start + change + sin (rotated)
            # x + dx - dy*sin()
            # y + dy + dx*sin()
            next = (self.startx + self.dx*i - self.dy*math.sin(self.amplitude + (i*4*math.pi/self.maxLength))*self.maxLength/8,self.starty + self.dy*i + self.dx*math.sin(self.amplitude + (i*4*math.pi/(self.maxLength)))*self.maxLength/8)
            lib.drawLine(prev, next)
            prev = next

        #lib.pygame.draw.line(lib.pygame.display.get_surface(), (255, 0, 0), (self.startx, self.starty), (self.endx, self.endy))
    def update(self) -> None:
        super().update()
        #remove ourselves from old collision box
        lib.getCollision(self.actual).remove(self)
        #move
        self.starty += self.speed*self.dy
        self.startx += self.speed*self.dx
        self.endx += self.speed*self.dx
        self.endy += self.speed*self.dy
        self.amplitude += self.speed*4*math.pi/(self.maxLength)
        old = self.actual
        self.actual = (self.startx - self.dy*math.sin(self.amplitude)*self.maxLength/8,self.starty + self.dx*math.sin(self.amplitude)*self.maxLength/8)
        #do collision checks
        for line in lib.getCollision(old) + lib.getCollision(self.actual):
            if isinstance(line, Forbiddance):
                a = ((self.actual[0]-old[0])*(line.start[1]-old[1]) - (self.actual[1]-old[1])*(line.start[0]-old[0])) / ((self.actual[1]-old[1])*(line.end[0]-line.start[0]) - (self.actual[0]-old[0])*(line.end[1]-line.start[1]))
                b = ((line.end[0]-line.start[0])*(line.start[1]-old[1]) - (line.end[1]-line.start[1])*(line.start[0]-old[0])) / ((self.actual[1]-old[1])*(line.end[0]-line.start[0]) - (self.actual[0]-old[0])*(line.end[1]-line.start[1]))
                if (0 <= a <= 1) and (0 <= b <= 1):
                    #collision

                    pass
            elif isinstance(line, Warding):
                if math.dist(self.actual[0], self.actual[1], line.centerx, line.centery) <= line.radius:
                    #collision

                    pass
            pass
        lib.getCollision(self.actual).append(self)
