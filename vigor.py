import math

import lib
from line import Line
from warding import Warding
from forbiddance import Forbiddance

class Vigor(Line):
    #global vars
    maxLength = 100
    speed = .2
    
    def __init__(self, start : tuple[int, int], end: tuple[int, int], verified:bool=False) -> None:
        """ 
            Creates Line of Vigor, extending in a sin wave from start to end
            Start is the only place with collision, and is the "head" of the line
        """
        super().__init__()
        #vars
        self.length=self.maxLength
        self.collisions = {}
        self.color = (255, 255, 255)
        self.verified = verified
        self.drawn = False
        self.drawAmount = 90

        #instantiate position
        self.startx = start[0]
        self.starty = start[1]
        self.endx = end[0] #TODO remove, use dx/dy
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
            # lib.drawLine(self.head, (self.head[0]-self.dx*self.length, self.head[1]-self.dy*self.length))
            #draw sin wave
            # lib.drawLine((self.startx, self.starty), (self.endx, self.endy))
            # lib.drawPoint((self.startx, self.starty), (0, 255, 0))
            # lib.drawPoint((self.endx, self.endy), (0, 255, 0))
            self.drawWave(self.length)
        else:
            old = self.color
            self.color += (50,)
            self.drawWave(self.length)
            self.color = old
            self.drawWave(self.drawAmount)
    
    def drawWave(self, length) -> None:
        prev = (self.startx - -self.dy*math.sin(self.amplitude)*self.maxLength/8,self.starty + -self.dx*math.sin(self.amplitude)*self.maxLength/8)
        slope = (self.dx, self.dy)
        for i in range(1, length+1):
            slope = self.collisions.get(i, slope)
            # next = (self.startx + -slope[0]*i - -slope[1]*math.sin(self.amplitude + (i*4*math.pi/self.maxLength))*self.maxLength/8,self.starty + -slope[1]*i + -slope[0]*math.sin(self.amplitude + (i*4*math.pi/(self.maxLength)))*self.maxLength/8)
            next = (prev[0] - slope[0] + slope[1]*(self.sin(i)-self.sin(i-1)),prev[1] - slope[1] - slope[0]*(self.sin(i)-self.sin(i-1)))
            
            lib.drawLine(prev, next, self.color)
            prev = next

    def sin(self, i:int) -> float:
        return math.sin(self.amplitude + (i*4*math.pi/self.maxLength))*self.maxLength/8
    
    def update(self) -> None:
        """
        updates the line 
        TODO depend on framerate?
    
        """
        super().update()
        if self.drawn:
            #remove self from collision (setup stuff)
            lib.getCollision(self.head).remove(self)

            

            #update the "real" start point, save reference for collision detection
            old = self.head
            self.head = (self.startx - -self.dy*math.sin(self.amplitude)*self.maxLength/8,self.starty + -self.dx*math.sin(self.amplitude)*self.maxLength/8)
            if (self.head != old):
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
                            #save past angle for later drawing
                            self.collisions.update({25: (self.dx, self.dy)})
                            #calculate angles
                            otherAngle = line.angle()%math.pi
                            selfAngle = math.atan2(self.endx-self.startx, self.endy-self.starty)
                            diff = -2*abs(otherAngle-selfAngle)-math.pi
                            #update x and y based on collision
                            oldx = self.dx
                            oldy = self.dy
                            self.dx = math.cos(diff)*oldx - math.sin(diff)*oldy
                            self.dy = math.sin(diff)*oldx + math.cos(diff)*oldy
                            #update vars
                            self.length -= 1
                            self.head = (self.startx - -self.dy*math.sin(self.amplitude)*self.maxLength/8,self.starty + -self.dx*math.sin(self.amplitude)*self.maxLength/8)
                            pass
                    elif isinstance(line, Warding):
                        if math.dist((self.head[0], self.head[1]), (line.centerx, line.centery)) <= line.radius:
                            #collision
                            pass
                        pass
            #TODO check for multiple collisions

            #move
            self.starty += self.speed*self.dy
            self.startx += self.speed*self.dx
            self.endx += self.speed*self.dx
            self.endy += self.speed*self.dy
            self.amplitude -= self.speed*4*math.pi/(self.maxLength)


            #if we are outside the screen, mark ourselves for deletion 
            #TODO make more robust, check entire line, or rect around it
            if (lib.isOutofBounds(self.head) and lib.isOutofBounds((self.head[0] - self.dx*self.length, self.head[1] - self.dy*self.length))):
                self.color = (0, 0, 255)
                #raise IndexError
                pass
            else:
                #add ourselves to collision (and other external stuffs)
                pass
            lib.getCollision(self.head).append(self)
        else: #not yet drawn, just update draw amount
            if self.drawAmount == self.length:
                if self.verified:
                    self.drawn = True
            else:
                self.drawAmount += 1


    def toBytes(self) -> bytes:
        return b'\x01' + int(self.startx).to_bytes(2, 'big')+int(self.starty).to_bytes(2, 'big')+int(self.endx).to_bytes(2, 'big')+int(self.endy).to_bytes(2, 'big')

    def __repr__(self) -> str:
        return self.__str__()
    def __str__(self) -> str:
        return "LoV: start=(" + str(self.startx) + ", " + str(self.starty) + ") end=(" + str(self.endx) + ", " + str(self.endy) + ")"