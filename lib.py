#imports
import pygame

#functions

def drawLine(start :tuple[int, int], end : tuple[int, int]) -> None:
    pygame.draw.line(drawing, (255, 255, 255), start, end)
def displaySize() -> tuple[int, int]:
    return drawing.get_size()
def getCollision(position: tuple[int, int]) -> list:
    if (0>position[0]>displaySize()[0] or 0>position[1]>displaySize()[1]):
        return []
    return collision[int(position[0]/(displaySize()[0]/collisionNum))][int(position[1]//(displaySize()[1]/collisionNum))]
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
drawing = pygame.Surface((1280, 720))
#collision array
collisionNum = 20
collision = []
for i in range(0, collisionNum):
    collision.append([])
    for j in range(0, collisionNum):
        collision[i].append([])

