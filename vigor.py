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
        self.drawn = False

        #instantiate position
        self.startx = start[0]
        self.starty = start[1]
        self.endx = end[0]
        self.endy = end[1]

        #math
        self.dy = (self.starty-self.endy)/self.maxLength
        self.dx = (self.startx-self.endx)/self.maxLength
        self.head = (self.startx, self.starty)
        self.amplitude = 0

        #add self to collision
        lib.getCollision(self.head).append(self)

    def draw(self) -> None:
        """ draw self on render surface
        while not $drawn, draw the full line at 50% opacity and trace over it with the "full" line
        
        Pseudo-Formula for sin wave:
        start + change + <rotated> sin(amp + i)
        x + dx - dy*sin()
        y + dy + dx*sin()
        """
        if self.drawn:
            lib.drawPoint((self.startx, self.starty), (0, 255, 0))
            #draw sin wave
            self.drawWave(self.length)
            
            lib.drawPoint((self.endx, self.endx), (255, 0, 0))
        else:
            old = self.color
            self.color += (50,)
            self.drawWave(self.length)
            self.color = old
            self.drawWave(40)
    
    def drawWave(self, length) -> None:
        prev = (self.startx - -self.dy*math.sin(self.amplitude)*self.maxLength/8,self.starty + -self.dx*math.sin(self.amplitude)*self.maxLength/8)
        for i in range(1, length):
            next = (self.startx + -self.dx*i - -self.dy*math.sin(self.amplitude + (i*4*math.pi/self.maxLength))*self.maxLength/8,self.starty + -self.dy*i + -self.dx*math.sin(self.amplitude + (i*4*math.pi/(self.maxLength)))*self.maxLength/8)
            lib.drawLine(prev, next, self.color)
            prev = next
    
    def update(self) -> None:
        """
        updates the line 
        TODO depend on framerate?
    
        """
        super().update()
        if not self.drawn:
            #remove self from collision (setup stuff)
            lib.getCollision(self.head).remove(self)

            #move
            self.starty += self.speed*self.dy
            self.startx += self.speed*self.dx
            self.endx += self.speed*self.dx
            self.endy += self.speed*self.dy
            self.amplitude -= self.speed*4*math.pi/(self.maxLength)

            #update the "real" start point, save reference for collision detection
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
                    if math.dist((self.head[0], self.head[1]), (line.centerx, line.centery)) <= line.radius:
                        #collision
                        pass
                    pass

            #if we are outside the screen, mark ourselves for deletion 
            #TODO make more robust, check entire line, or rect around it
            if (lib.isOutofBounds(self.head) and lib.isOutofBounds((self.head[0] + self.dx*self.length, self.head[1] + self.dy*self.length))):
                self.color = (0, 0, 255)
                #raise IndexError
                pass
            else:
                #add ourselves to collision (and other external stuffs)
                pass
            lib.getCollision(self.head).append(self)


    def toBytes(self) -> bytes:
        return b'\x01' + int(self.startx).to_bytes(2, 'big')+int(self.starty).to_bytes(2, 'big')+int(self.endx).to_bytes(2, 'big')+int(self.endy).to_bytes(2, 'big')

    def __repr__(self) -> str:
        return self.__str__()
    def __str__(self) -> str:
        return "LoV: start=(" + str(self.startx) + ", " + str(self.starty) + ") end=(" + str(self.endx) + ", " + str(self.endy) + ")"