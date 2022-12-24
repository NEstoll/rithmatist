#imports
import pygame
import math
from pygame.locals import *

#drawing functions
def drawRect(self, start :tuple[float, float], end : tuple[float, float]):
    self.image = pygame.image.load("image.jfif").convert()  
    if start.getValue1() > end.getValue1():
        topLeftY = start.getValue1()
        botRightY = end.getValue1()
    else:
        topLeftY = start.getValue1()
        botRightY = end.getValue1()
    coordinates = pythag(start.getValue0(), topLeftY, end.getValue0(), botRightY)
    rect = Rect(coordinates.getValue0(), coordinates.getValue1(), 10, topLeftY-botRightY)
    rect.topleft = {coordinates.getValue0(), coordinates.getValue1()}
    rect.bottomright = {coordinates.getValue2(), coordinates.getValue3()}
    pygame.draw.rect(renderSurface, (255, 255, 255), rect)
    self.blit(self.image, renderSurface)

def pythag(topLX, topLY, botRX, botRY):
    size = 10
    m = botRY - topLY/botRX - topLX
    l = math.sqrt(((size/2)^2)/m)
    if (m > 1):
        topLX = topLX - (l*m)
        topLY = topLY + l
        botRX = botRX - (l*m)
        botRY = botRY - l
    else:
        topLY = topLY - (l*m)
        topLY = topLX + l
        botRY = botRY - (l*m)
        botRX = botRX - l
    return (topLX, topLY, botRX, botRY)

#def drawLine(start :tuple[float, float], end : tuple[float, float], color: tuple[int, int, int]=(255, 255, 255)) -> None:
#    pygame.draw.line(renderSurface, color, start, end, 3)
#def drawPoint(center: tuple[float, float], color: tuple[int, int, int]=(255, 255, 255)) -> None:
#    pygame.draw.circle(renderSurface, color, center, 3)

#helper functions
def gameSize() -> tuple[int, int]:
    return renderSurface.get_size()
def displaySize() -> tuple[int, int]:
    return pygame.display.get_window_size()
def display() -> pygame.surface.Surface:
    return pygame.display.get_surface()
def events() -> list[pygame.event.Event]:
    return pygame.event.get()

def getCollision(position: tuple[float, float]) -> list:
    if (isOutofBounds(position)):
        return OoB
    return collision[int(position[0]/(gameSize()[0]/collisionNum))][int(position[1]//(gameSize()[1]/collisionNum))]
def isOutofBounds(position: tuple[float, float]) -> bool:
    if (position[0] < 0 or position[0] > gameSize()[0] or position[1] < 0 or position[1] > gameSize()[1]):
        return True
    return False
    
    
def screenToGame(position:tuple[int, int]) -> tuple[int, int]:
    return (int(position[0]*gameSize()[0]/pygame.display.get_surface().get_size()[0]), int(position[1]*gameSize()[1]/pygame.display.get_surface().get_size()[1]))
def collisionBoxes() -> None:
    for i in range(1, collisionNum+1):
        for j in range(1, collisionNum+1):
            prev = (int((i-1)*(gameSize()[0]/collisionNum)), (j-1)*(gameSize()[1]/collisionNum))
            next = (int(i*(gameSize()[0]/collisionNum)), j*(gameSize()[1]/collisionNum))
            drawRect(prev, (next[0], prev[1]))
            drawRect(prev, (prev[0], next[1]))
            drawRect((next[0], prev[1]), next)
            drawRect((prev[0], next[1]), next)

#setup
renderSurface = pygame.Surface((1920, 1080), pygame.SRCALPHA)
#collision array
collisionNum = 20
collision = []
OoB = []
for i in range(0, collisionNum):
    collision.append([])
    for j in range(0, collisionNum):
        collision[i].append([])

class LineOutofBounds(Exception):
    pass
