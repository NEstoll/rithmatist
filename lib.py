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
    #https://stackoverflow.com/a/565282
    if (line2[1] == line2[0] and line1[0] == line1[1] and line1[0] == line2[0]): #if single point, return that point
        return line1[0]
    # calculate the delta from start to end for each line
    deltaLine1 = (line1[1][0] - line1[0][0], line1[1][1] - line1[0][1])
    deltaLine2 = (line2[1][0] - line2[0][0], line2[1][1] - line2[0][1])

    #determinant/crossproduct
    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    # divisor, if 0 lines are parallel
    div = det(deltaLine1, deltaLine2)
    if div == 0:
       return None

    diff = (line2[0][0] - line1[0][0], line2[0][1] - line1[0][1])
    if diff == (0, 0):
        return None #lines are co-linear
    t = det(diff, deltaLine2) / div
    u = det(diff, deltaLine1) / div
    if (0 <= t <= 1 and 0 <= u <= 1): #if collision is within segment
        return (line1[0][0]+t*deltaLine1[0], line1[0][1]+t*deltaLine1[1])
    return None

def getCollisions(start: tuple[float, float], end:  tuple[float, float]) -> list[list]:
    s = getCollision(start) 
    e = getCollision(end)
    if (s is e):
        return [s]
    grid_dx = gameSize()[0]/collisionNum
    grid_dy = gameSize()[1]/collisionNum
    line_dx = (end[0]-start[0])
    line_dy = (end[1]-start[1])
    collisions = [s]
    while (line_dx > 0 or line_dy > 0):
        if (line_dx/grid_dx > line_dy/grid_dy):
            line_dx -= grid_dx
        else:
            line_dy -= grid_dy
        collisions.append(getCollision((start[0]+line_dx, start[1]+line_dy)))
    return collisions


def getCollision(position: tuple[float, float]) -> list:
    if (isOutofBounds(position)):
        return OoB
    return collision[int(position[0]/(gameSize()[0]/collisionNum))][int(position[1]//(gameSize()[1]/collisionNum))]
def isOutofBounds(position: tuple[float, float]) -> bool:
    if (position[0] < 0 or position[0] > gameSize()[0] or position[1] < 0 or position[1] > gameSize()[1]):
        return True
    return False
    
    
def screenToGame(position:tuple[float, float]) -> tuple[float, float]:
    return ((position[0]*gameSize()[0]/displaySize()[0]), (position[1]*gameSize()[1]/displaySize()[1]))
def gameToScreen(position:tuple[float, float]) -> tuple[float, float]:
    return ((position[0]*displaySize()[0]/gameSize()[0]), (position[1]*displaySize()[1]/gameSize()[1]))
def collisionBoxes() -> None:
    for i in range(1, collisionNum+1):
        for j in range(1, collisionNum+1):
            prev = (int((i-1)*(gameSize()[0]/collisionNum)), (j-1)*(gameSize()[1]/collisionNum))
            next = (int(i*(gameSize()[0]/collisionNum)), j*(gameSize()[1]/collisionNum))
            drawLine(prev, (next[0], prev[1]))
            drawLine(prev, (prev[0], next[1]))
            # drawLine((next[0], prev[1]), next)
            # drawLine((prev[0], next[1]), next)

#setup
renderSurface = pygame.Surface((1920, 1080), pygame.SRCALPHA)
#collision array
collisionNum = 1
collision = []
OoB = []
for i in range(0, collisionNum):
    collision.append([])
    for j in range(0, collisionNum):
        collision[i].append([])

class LineOutofBounds(Exception):
    pass
