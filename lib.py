#imports
from dis import dis
import pygame

#functions

def drawLine(start :tuple[int, int], end : tuple[int, int], color: tuple[int, int, int]=(255, 255, 255)) -> None:
    pygame.draw.line(drawing, color, start, end, 2)
def displaySize() -> tuple[int, int]:
    return drawing.get_size()
def getCollision(position: tuple[int, int]) -> list:
    if ((0>position[0] or position[0]>displaySize()[0]) or (0>position[1] or position[1]>displaySize()[1])):
        return []
    return collision[int(position[0]/(displaySize()[0]/collisionNum))][int(position[1]//(displaySize()[1]/collisionNum))]
def screenToDrawing(position:tuple[int, int]) -> tuple[int, int]:
    return (position[0]*displaySize()[0]/pygame.display.get_surface().get_size()[0],position[1]*displaySize()[1]/pygame.display.get_surface().get_size()[1])
def collisionBoxes() -> None:
    for i in range(1, collisionNum+1):
        for j in range(1, collisionNum+1):
            prev = (int((i-1)*(displaySize()[0]/collisionNum)), (j-1)*(displaySize()[1]/collisionNum))
            next = (int(i*(displaySize()[0]/collisionNum)), j*(displaySize()[1]/collisionNum))
            drawLine(prev, (next[0], prev[1]))
            drawLine(prev, (prev[0], next[1]))
            drawLine((next[0], prev[1]), next)
            drawLine((prev[0], next[1]), next)

#setup
drawing = pygame.Surface((1600, 900))
#collision array
collisionNum = 20
collision = []
for i in range(0, collisionNum):
    collision.append([])
    for j in range(0, collisionNum):
        collision[i].append([])

