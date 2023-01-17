import math
import pygame
import lib
from cursor import Cursor

from forbiddance import Forbiddance, Segment
from line import Line
from player import Player
from vigor import Vigor
from warding import Warding

class Game:
    # Instance of a game
    # Holds references to all currently instantiated game objects
    # No distinction between server/client

    def __init__(self) -> None:
        #variable instantiation
        self.objects = []
        self.drawOnly = []
        self.players = []
        self.time = 0

    def update(self) -> None:
        self.time += 1
        for o in reversed(self.objects):
            try:
                o.update()
            except lib.LineOutofBounds:
                self.objects.remove(o)

    def createLine(self, line: Line, player: Player) -> bool:
        if not player in self.players:
            return False
        else:
            #TODO check if player can draw line
            self.objects.append(line)
            return True

    def addPlayer(self, player) -> int:
        self.players.append(player)
        return self.players.index(player)


    def isRunning(self) -> bool:
        return True

    def draw(self, display) -> None:
        #draw each object, and then handle render -> display trasform
        lib.renderSurface.fill(0)
        display.fill(0)
        #TODO add real cursor (default can't be moved)
        # lib.drawPoint(lib.screenToGame(lib.pygame.mouse.get_pos()))
        for o in self.objects:
            o.draw()
        for o in self.drawOnly:
            o.draw()
        lib.collisionBoxes()
        frame = lib.pygame.transform.smoothscale(lib.renderSurface, lib.displaySize())
        display.blit(frame, frame.get_rect())
        lib.pygame.display.flip()




if __name__ == "__main__": #temp runner code
    pygame.init()
    pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    pygame.mouse.set_visible(False)
    game = Game()
    game.objects.append(Forbiddance((100, 300), (300, 100)))
    # game.objects.append(Forbiddance((200, 200), (200, 600)))
    # game.objects.append(Forbiddance((400, 600), (1900, 600)))
    # game.objects.append(Forbiddance((600, 600), (600, 200)))
    # game.objects.append(Forbiddance((600, 200), (200, 200)))
    # game.objects.append(Vigor((400, 400), (800, 800), True))
    # game.objects.append(Vigor((500, 700), (500, 1000), True))
    # game.objects.append(Vigor((600, 300), (800, 300), True))
    # game.objects.append(Vigor((300, 300), (400, 200), True))
    game.objects.append(Warding((1500, 800), 100))
    # game.objects.append(Vigor((1800, 800), (2000, 800)))

    game.draw(pygame.display.get_surface())
    player = Player(Warding((1500, 800), 100))
    game.addPlayer(player)

    mouse = Cursor()
    game.drawOnly.append(mouse)

    running = True
    start = (0, 0)
    currLine = None
    prevMouse:tuple[float, float] | None = None
    while running:
        count = 0
        for evt in lib.pygame.event.get(): #todo, add event handling to seperate class/game class
            count += 1
            if evt.type == lib.pygame.quit:
                lib.pygame.quit()
                running = False
                break
            elif evt.type == lib.pygame.MOUSEBUTTONDOWN:
                #starting to draw a line
                start = lib.screenToGame(lib.pygame.mouse.get_pos())
                buttons = lib.pygame.mouse.get_pressed()
                if buttons is not None:
                    if buttons[0]:
                        currLine = Vigor(start, lib.screenToGame(lib.pygame.mouse.get_pos()))
                        game.drawOnly.append(currLine)
                    elif buttons[2]:
                        currLine = Forbiddance(start, lib.screenToGame(lib.pygame.mouse.get_pos()))
                        currLine.setCollision(False)
                        game.drawOnly.append(currLine)
                    else:
                        currLine = None
                        continue
            elif evt.type == lib.pygame.MOUSEBUTTONUP and currLine != None:
                #line drawn
                if isinstance(currLine, Forbiddance):
                    currLine.setCollision(True)
                game.createLine(currLine, player)
                game.drawOnly.remove(currLine)
                currLine = None
            elif evt.type == lib.pygame.MOUSEMOTION:
                #handle mouse motion
                currMouse = lib.screenToGame(lib.pygame.mouse.get_pos())
                if prevMouse is not None and not prevMouse == currMouse:
                    #handle collision with LoF
                    collision = []
                    [collision.extend(x) for x in lib.getCollisions(prevMouse, currMouse)]
                    #TODO actually get all possible collision boxes
                    for line in set(collision):
                        if isinstance(line, Segment):
                            intersection = lib.linesColliding((prevMouse, currMouse), (line.start, line.end))  # type: ignore
                            if (intersection is not None):
                                #TODO line is a segment, need to get the parent line for accurate movement.
                                l = math.dist(intersection, currMouse)
                                otherAngle = line.angle()
                                selfAngle = math.atan2(-currMouse[1]+prevMouse[1], -currMouse[0]+prevMouse[0])
                                angle = otherAngle-selfAngle
                                print("angles: ", (math.degrees(otherAngle), math.degrees(selfAngle), math.degrees(angle)))
                                mouseDirection = ((currMouse[0]-prevMouse[0])/math.dist(prevMouse, currMouse), (currMouse[1]-prevMouse[1])/math.dist(prevMouse, currMouse))
                                lineDirection = ((line.end[0]-line.start[0])/math.dist(line.start, line.end), (line.end[1]-line.start[1])/math.dist(line.start, line.end))
                                end = ((intersection[0]+lineDirection[0]*l*math.cos(angle)), (intersection[1]+lineDirection[1]*l*math.cos(angle)))
                                if (math.cos(angle) > 0):
                                    extra = math.dist(intersection, end)-math.dist(intersection, line.parent.end)
                                else:
                                    extra = math.dist(intersection, end)-math.dist(intersection, line.parent.start)

                                if (angle <= math.pi and angle >= 0):
                                    offsetDir = 1
                                else:
                                    offsetDir = -1

                                if (extra > 0):
                                    # end = (end[0]+extra*mouseDirection[0], end[1]+extra*mouseDirection[1])
                                    pass
                                else:
                                    offset = math.dist(intersection, prevMouse)
                                    end = (end[0]-lineDirection[1]*line.width*offsetDir, end[1]+lineDirection[0]*line.width*offsetDir)
                                    # end = (end[0], end[1])
                                bad = lib.linesColliding((prevMouse, end), (line.start, line.end))
                                if (bad is not None):
                                    print("Bad: ", (prevMouse, end), (line.start, line.end), intersection, bad, currMouse)
                                currMouse = end
                                lib.pygame.mouse.set_pos(lib.gameToScreen(currMouse))
                                break
                prevMouse = currMouse
                mouse.mouse = currMouse
                

                #update line
                if currLine is not None:
                    currLine.instantiate(start, lib.screenToGame(lib.pygame.mouse.get_pos()))
                    

            else:
                if lib.pygame.key.get_pressed()[lib.pygame.K_SPACE]:
                    # game.update()
                    # game.draw(pygame.display.get_surface())
                    pass
        if count != 0:
            # print("evts: ", count)
            pass
        game.update()
        game.draw(pygame.display.get_surface())
        lib.pygame.time.delay(1)