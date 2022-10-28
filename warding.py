import math
import lib
from line import Line

class Warding(Line):
    maxSegments = 100
    def __init__(self, center:tuple[int, int], radius:float) -> None:
        super().__init__()
        #initialize variables
        self.color = (255, 255, 255)
        self.segments = [0 for i in range(0, Warding.maxSegments)]
        self.inscribedTriangle = 0
        #location
        self.centerx = center[0]
        self.centery = center[1]
        self.radius = radius

        #add collision
        collision = lib.getCollision((self.centerx + self.radius, self.centery))
        for i in range(0, Warding.maxSegments):
            next = lib.getCollision((self.centerx + self.radius*math.cos((i+1)*2*math.pi/Warding.maxSegments), self.centery + self.radius*math.sin((i+1)*2*math.pi/Warding.maxSegments)))
            if not next is collision:
                collision.append(self)
                collision = next
        collision.append(self)

    def dmg(self, line, amount) -> None:
        angle1 = math.atan2(self.centery-line[0][1], self.centerx-line[0][0])+math.pi
        angle2 = math.atan2(self.centery-line[1][1], self.centerx-line[1][0])+math.pi
        seg1 = math.floor(angle1*Warding.maxSegments/(2*math.pi))
        seg2 = math.floor(angle2*Warding.maxSegments/(2*math.pi))
        self.segments[seg1] = 200
        self.segments[seg2] = 200
        print("angles: ", (math.degrees(angle1), math.degrees(angle2)))

    def draw(self) -> None:
        super().draw()
        prev =(self.centerx + self.radius, self.centery)
        for i in range(0, len(self.segments)):
            next = (self.centerx + self.radius*math.cos((i+1)*2*math.pi/Warding.maxSegments), self.centery + self.radius*math.sin((i+1)*2*math.pi/Warding.maxSegments))
            lib.drawLine(prev, next, self.color)
            lib.drawLine((self.centerx, self.centery), prev, (max(255-self.segments[i], 0), 0, 0))
            prev = next
