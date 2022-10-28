#imports
import pygame

#drawing functions
def drawLine(start :tuple[float, float], end : tuple[float, float], color=(255, 255, 255)) -> None:
    pygame.draw.line(renderSurface, color, start, end, 3)
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

def linesColliding(line1:tuple[tuple[float, float], tuple[float, float]], line2:tuple[tuple[float, float], tuple[float, float]]) -> tuple[float, float] | None:
    a = ((line1[0][0]-line1[1][0])*(line2[0][1]-line1[1][1]) - (line1[0][1]-line1[1][1])*(line2[0][0]-line1[1][0])) / ((line1[0][1]-line1[1][1])*(line2[1][0]-line2[0][0]) - (line1[0][0]-line1[1][0])*(line2[1][1]-line2[0][1]))
    b = ((line2[1][0]-line2[0][0])*(line2[0][1]-line1[1][1]) - (line2[1][1]-line2[0][1])*(line2[0][0]-line1[1][0])) / ((line1[0][1]-line1[1][1])*(line2[1][0]-line2[0][0]) - (line1[0][0]-line1[1][0])*(line2[1][1]-line2[0][1]))
    if (0 <= a <= 1) and (0 <= b <= 1):
        intersection = (line2[0][0] + a*(line2[1][0]-line2[0][0]), line2[0][1] + (a*(line2[1][1]+line2[0][1])))
        return intersection
    else:
        return None

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
            drawLine(prev, (next[0], prev[1]))
            drawLine(prev, (prev[0], next[1]))
            drawLine((next[0], prev[1]), next)
            drawLine((prev[0], next[1]), next)

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
