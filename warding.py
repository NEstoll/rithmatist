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
            if (next != collision):
                collision.append(self)
                collision = next
        collision.append(self)

    def dmg(self, location, amount):
        self.segments[0] = amount

    def draw(self) -> None:
        super().draw()
        prev =(self.centerx + self.radius, self.centery)
        for i in range(0, len(self.segments)):
            next = (self.centerx + self.radius*math.cos((i+1)*2*math.pi/Warding.maxSegments), self.centery + self.radius*math.sin((i+1)*2*math.pi/Warding.maxSegments))
            lib.drawLine(prev, next, self.color)
            prev = next
