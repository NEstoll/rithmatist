#imports
import pygame
import math
import random
from pygame.locals import *


#drawing functions
def drawRect(start :tuple[float, float], end : tuple[float, float]):  

    # checks highest point
    if start[1] > end[1]:
        topY = start[1]
        topX = start[0]
        botY = end[1]
        botX = end[0]
    else:
        topY = end[1]
        topX = end[0]
        botY = start[1]
        botX = start[0]
    
    length = math.sqrt((topY-botY)**2 + (topX-botX)**2)
    # Draw rect
    rect = Rect(topX - 5, topY, 10, length)
    pygame.draw.rect(renderSurface, (255, 255, 255), rect)

    # Setting image rect
    imageRect = Rect(127, 34, 10, length)

    # blit image over rect
    renderSurface.blit(pygame.image.load("images.jfif").convert(), rect, imageRect)





#def drawLine(start :tuple[float, float], end : tuple[float, float], color: tuple[int, int, int]=(255, 255, 255)) -> None:
#    pygame.draw.line(renderSurface, color, start, end, 3)
def drawPoint(center: tuple[float, float], color: tuple[int, int, int]=(255, 255, 255)) -> None:
    pygame.draw.circle(renderSurface, color, center, 3)

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
