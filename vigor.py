import math

import lib
from line import Line
from warding import Warding
from forbiddance import Forbiddance

class Vigor(Line):
    #global vars
    maxLength = 1000
    speed = 2
    
    def __init__(self, start : tuple[int, int], end: tuple[int, int], verified:bool=False) -> None:
        """ 
            Creates Line of Vigor, extending in a sin wave from start to end
            Start is the only place with collision, and is the "head" of the line
        """
        super().__init__()
        #vars
        self.length=self.maxLength
        self.points = []
        self.color = (255, 255, 255)
        self.flip = False
        self.skip = 0
        self.skipSpeed = 0
        self.verified = verified
        self.drawn = False
        self.drawAmount = 0

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
        self.createList(int(self.length/self.speed))

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
            # lib.drawPoint((self.startx, self.starty), (255, 0, 0))
            # lib.drawPoint((self.endx, self.endy), (0, 255, 0))
            # self.createList(self.length)
            self.drawPoints(self.length/self.speed)
        else:
            old = self.color
            self.color += (50,)
            self.drawPoints(self.length/self.speed)
            self.color = old
            self.drawPoints(self.drawAmount)

    def drawPoints(self, length) -> None:
        for i in range(1, int(min(len(self.points), length))):
            lib.drawLine(self.points[i-1], self.points[i], self.color)
    


    def createList(self, length) -> None:
        # prev = (self.startx - -self.dy*math.sin(self.amplitude)*self.maxLength/8,self.starty + -self.dx*math.sin(self.amplitude)*self.maxLength/8)
        slope = (self.dx, self.dy)
        for i in range(1, length+1):
            next = (self.startx + -slope[0]*i*self.speed - -slope[1]*math.sin(self.amplitude + (i*self.speed*4*math.pi/self.maxLength))*self.maxLength/8,self.starty + -slope[1]*i*self.speed + -slope[0]*math.sin(self.amplitude + (i*self.speed*4*math.pi/(self.maxLength)))*self.maxLength/8)
            # next = (prev[0] - slope[0] + slope[1]*(self.sin(i)-self.sin(i-1)),prev[1] - slope[1] - slope[0]*(self.sin(i)-self.sin(i-1)))
            self.points.append(next)

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

            

            #if we are outside the screen, mark ourselves for deletion 
            #TODO make more robust, check entire line, or rect around it
            if (lib.isOutofBounds(self.head) and lib.isOutofBounds(self.points[len(self.points)-1])):
                self.color = (0, 0, 255)
                #raise IndexError
                pass

            #if 0 length, delete self
            if len(self.points) > self.length/self.speed:
                self.points.pop()
            if len(self.points) > self.length/self.speed and self.skipSpeed != 0:
                self.skip -= 1 
                if self.skip <= 0:
                    lib.getCollision(self.head).append(self)
                    self.skip += self.skipSpeed
                    return    
            if len(self.points) == 0:
                raise IndexError

            #update the "real" start point, save reference for collision detection
            old = self.head
            self.head = (self.startx + self.dy*math.sin(self.amplitude)*self.maxLength/8,self.starty - self.dx*math.sin(self.amplitude)*self.maxLength/8)
            if (self.head != old):
                good = False
                #do collision checks
                while not good:
                    good = True
                    for line in set(lib.getCollision(old) + lib.getCollision(self.head)):
                        if isinstance(line, Forbiddance):
                            a = ((self.head[0]-old[0])*(line.start[1]-old[1]) - (self.head[1]-old[1])*(line.start[0]-old[0])) / ((self.head[1]-old[1])*(line.end[0]-line.start[0]) - (self.head[0]-old[0])*(line.end[1]-line.start[1]))
                            b = ((line.end[0]-line.start[0])*(line.start[1]-old[1]) - (line.end[1]-line.start[1])*(line.start[0]-old[0])) / ((self.head[1]-old[1])*(line.end[0]-line.start[0]) - (self.head[0]-old[0])*(line.end[1]-line.start[1]))
                            if (0 <= a <= 1) and (0 <= b <= 1):
                                #TODO get angle, do collision
                                print("collision: ", self, line)
                                #collision
                                intersection = (line.start[0] + a*(line.end[0]-line.start[0]), line.start[1] + (a*(line.end[1]+line.start[1])))
                                #calculate angles
                                otherAngle = line.angle()%math.pi
                                selfAngle = math.atan2(-self.dy, -self.dx)
                                diff = 2*(otherAngle-selfAngle)-math.pi
                                print("angles: ", (math.degrees(otherAngle), math.degrees(selfAngle), math.degrees(diff)))
                                #jump back 1 step (to prevent additional collisions)
                                print(((self.startx, self.starty), (self.dx, self.dy)))
                                self.starty -= self.speed*self.dy
                                self.startx -= self.speed*self.dx
                                #update start (jump to sin wave)
                                self.startx += self.dy*math.sin(self.amplitude)*self.maxLength/8
                                self.starty -= self.dx*math.sin(self.amplitude)*self.maxLength/8
                                #change dx and dy
                                oldx = self.dx
                                oldy = self.dy
                                self.dx = math.cos(diff)*oldx - math.sin(diff)*oldy
                                self.dy = math.sin(diff)*oldx + math.cos(diff)*oldy
                                #update start again to be off the sin wave
                                self.startx -= self.dy*math.sin(self.amplitude)*self.maxLength/8
                                self.starty += self.dx*math.sin(self.amplitude)*self.maxLength/8
                                #re-jump forward to not miss a step
                                self.starty += self.speed*self.dy
                                self.startx += self.speed*self.dx

                                #flip amplitude
                                # self.amplitude *= -1
                                self.flip = not self.flip
                                #step amplitude once to prevent re-colliding
                                if self.flip:
                                    self.amplitude = self.amplitude%(2*math.pi) + self.speed*4*math.pi/(self.maxLength)
                                else:
                                    self.amplitude = self.amplitude%(2*math.pi) - self.speed*4*math.pi/(self.maxLength)
                                #update vars
                                print(((self.startx, self.starty), (self.dx, self.dy)))
                                cut = abs(180-math.degrees(abs(diff+math.pi)))/2+10
                                self.skipSpeed = max(self.length/cut, 1)
                                # self.length -= cut
                                self.head = (self.startx + self.dy*math.sin(self.amplitude)*self.maxLength/8,self.starty - self.dx*math.sin(self.amplitude)*self.maxLength/8)
                                # good = False
                                break
                        elif isinstance(line, Warding):
                            if math.dist((self.head[0], self.head[1]), (line.centerx, line.centery)) <= line.radius:
                                #collision
                                pass
                            pass
            #TODO check for multiple collisions

            #update list
            self.points.insert(0, self.head)

            #move
            self.starty += self.speed*self.dy
            self.startx += self.speed*self.dx
            self.endx += self.speed*self.dx
            self.endy += self.speed*self.dy
            if self.flip:
                self.amplitude = self.amplitude%(2*math.pi) + self.speed*4*math.pi/(self.maxLength)
            else:
                self.amplitude = self.amplitude%(2*math.pi) - self.speed*4*math.pi/(self.maxLength)


            
            
            lib.getCollision(self.head).append(self)
        else: #not yet drawn, just update draw amount
            if self.drawAmount >= self.length/self.speed:
                if self.verified:
                    self.drawn = True
            else:
                self.drawAmount += self.length/(100*self.speed)


    def toBytes(self) -> bytes:
        return b'\x01' + int(self.startx).to_bytes(2, 'big')+int(self.starty).to_bytes(2, 'big')+int(self.endx).to_bytes(2, 'big')+int(self.endy).to_bytes(2, 'big')

    def __repr__(self) -> str:
        return self.__str__()
    def __str__(self) -> str:
        return "LoV: start=(" + str(self.startx) + ", " + str(self.starty) + ") end=(" + str(self.endx) + ", " + str(self.endy) + ")"