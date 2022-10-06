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
        """ 
            Creates Line of Vigor, extending in a sin wave from start to end
            Start is the only place with collision, and is the "head" of the line
        """
        super().__init__()
        #vars
        self.length=self.maxLength
        self.collisions = {}
        self.color = (255, 255, 255)
        #instantiate position
        self.startx = start[0]
        self.starty = start[1]
        self.endx = end[0]
        self.endy = end[1]
        #math
        self.dy = (self.endy-self.starty)/self.maxLength
        self.dx = (self.endx-self.startx)/self.maxLength
        self.head = (self.startx, self.starty)
        self.amplitude = 0
        #add self to collision
        lib.getCollision(self.head).append(self)

    def draw(self) -> None:
        prev = (self.startx - self.dy*math.sin(self.amplitude)*self.maxLength/8,self.starty + self.dx*math.sin(self.amplitude)*self.maxLength/8)
        lib.pygame.draw.circle(lib.drawing, (0, 255, 0), prev, 3)
        for i in range(1, self.length):
            # start + change + sin (rotated)
            # x + dx - dy*sin()
            # y + dy + dx*sin()
            next = (self.startx + self.dx*i - self.dy*math.sin(self.amplitude + (i*4*math.pi/self.maxLength))*self.maxLength/8,self.starty + self.dy*i + self.dx*math.sin(self.amplitude + (i*4*math.pi/(self.maxLength)))*self.maxLength/8)
            lib.drawLine(prev, next, self.color)
            prev = next
        lib.pygame.draw.circle(lib.drawing, (255, 0, 0), next, 3)
        #lib.pygame.draw.line(lib.pygame.display.get_surface(), (255, 0, 0), (self.startx, self.starty), (self.endx, self.endy))
    
    """
    updates the line TODO depend on framerate?
    @returns bool True if line should be deleted
    
    """
    def update(self) -> bool:
        super().update()
        #if we are outside the screen, delete ourselves
        if (lib.getCollision(self.head) == []):
            delete = True
            for i in range(-self.maxLength*2, self.maxLength*2, self.maxLength*2):
                for j in range(-self.maxLength*2, self.maxLength*2, self.maxLength*2):
                    if (lib.getCollision((self.head[0]+i, self.head[1]+j)) != []):
                        delete = False
            if delete:
                return 1
        else:
            #remove ourselves from old collision box
            lib.getCollision(self.head).remove(self)
        #move
        self.starty -= self.speed*self.dy
        self.startx -= self.speed*self.dx
        self.endx -= self.speed*self.dx
        self.endy -= self.speed*self.dy
        self.amplitude -= self.speed*4*math.pi/(self.maxLength)
        old = self.head
        self.head = (self.startx - self.dy*math.sin(self.amplitude)*self.maxLength/8,self.starty + self.dx*math.sin(self.amplitude)*self.maxLength/8)
        #do collision checks
        for line in lib.getCollision(old) + lib.getCollision(self.head):
            if isinstance(line, Forbiddance):
                a = ((self.head[0]-old[0])*(line.start[1]-old[1]) - (self.head[1]-old[1])*(line.start[0]-old[0])) / ((self.head[1]-old[1])*(line.end[0]-line.start[0]) - (self.head[0]-old[0])*(line.end[1]-line.start[1]))
                b = ((line.end[0]-line.start[0])*(line.start[1]-old[1]) - (line.end[1]-line.start[1])*(line.start[0]-old[0])) / ((self.head[1]-old[1])*(line.end[0]-line.start[0]) - (self.head[0]-old[0])*(line.end[1]-line.start[1]))
                if (0 <= a <= 1) and (0 <= b <= 1):
                    #TODO get angle, do collision
                    print("collision")
                    #collision
                    intersection = (line.start[0] + a*(line.end[0]-line.start[0]), line.start[1] + (a*(line.end[1]+line.start[1])))
                    #calculate angle, change start/end
                    #angle = math.tan(12)
                    self.color = (255, 0, 0)
                    #save for later drawing
                    #self.collisions.update((1, angle))
                    pass
            elif isinstance(line, Warding):
                if math.dist(self.head[0], self.head[1], line.centerx, line.centery) <= line.radius:
                    #collision

                    pass
            pass
        lib.getCollision(self.head).append(self)
        return 0
