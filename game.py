import pygame
from client import Client
import lib

from forbiddance import Forbiddance
from line import Line
from player import Player
from vigor import Vigor
from warding import Warding

class Game:
    # Instance of a game
    # Holds references to all currently instantiated game objects
    # No distinction between server/client
    # TODO seperate graphics code/make optional

    def __init__(self) -> None:
        #variable instantiation
        self.objects = []
        self.undrawn = []
        self.players = []
        self.time = 0

    def update(self) -> None:
        self.time += 1
        for o in reversed(self.objects):
            try:
                o.update()
            except lib.LineOutofBounds:
                self.objects.remove(o)

    def createLine(self, line: Line, player: Player):
        if not player in self.players:
            return False
        else:
            pass


    def isRunning(self) -> bool:
        return True

    def draw(self, display) -> None:
        #draw each object, and then handle render -> display trasform
        lib.renderSurface.fill(0)
        display.fill(0)
        for o in self.objects:
            o.draw()
        for o in self.undrawn:
            o.draw()
        lib.collisionBoxes()
        frame = lib.pygame.transform.smoothscale(lib.renderSurface, lib.displaySize())
        display.blit(frame, frame.get_rect())
        lib.pygame.display.flip()




if __name__ == "__main__": #temp runner code
    pygame.init()
    pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    game = Game()
    # game.objects.append(Forbiddance((100, 300), (300, 100)))
    # game.objects.append(Forbiddance((200, 200), (200, 600)))
    game.objects.append(Forbiddance((400, 600), (1900, 600)))
    # game.objects.append(Forbiddance((600, 600), (600, 200)))
    # game.objects.append(Forbiddance((600, 200), (200, 200)))
    # game.objects.append(Vigor((400, 400), (800, 800), True))
    game.objects.append(Vigor((500, 700), (500, 1000), True))
    # game.objects.append(Vigor((600, 300), (800, 300), True))
    # game.objects.append(Vigor((300, 300), (400, 200), True))
    game.objects.append(Warding((1500, 800), 100))

    game.draw(pygame.display.get_surface())
    
    running = True
    start = None
    button = None
    while running:
        for evt in lib.pygame.event.get(): #todo, add event handling to seperate class/game class
            if evt.type == lib.pygame.quit:
                lib.pygame.quit()
                running = False
                break
            elif evt.type == lib.pygame.MOUSEBUTTONDOWN:
                #starting to draw a line
                start = lib.screenToGame(lib.pygame.mouse.get_pos())
                button = lib.pygame.mouse.get_pressed()
            elif evt.type == lib.pygame.MOUSEBUTTONUP and start != None:
                #line drawn
                if button[0]:
                    line = Vigor(start, lib.screenToGame(lib.pygame.mouse.get_pos()))
                elif button[2]:
                    line = Forbiddance(start, lib.screenToGame(lib.pygame.mouse.get_pos()))
                else:
                    # line = Vigor(start, lib.screenToGame(lib.pygame.mouse.get_pos()))
                    continue
                game.objects.append(line)
                start = None 
            else:
                if lib.pygame.key.get_pressed()[lib.pygame.K_SPACE]:
                    # game.update()
                    # game.draw(pygame.display.get_surface())
                    pass
        game.update()
        game.draw(pygame.display.get_surface())
        lib.pygame.time.delay(10)
