import pygame
import lib

from forbiddance import Forbiddance
from vigor import Vigor

class Game:
    # Instance of a game
    # Holds references to all currently instantiated game objects
    # No distinction between server/client
    # TODO seperate graphics code/make optional

    def __init__(self) -> None:
        #variable instantiation
        self.objects = []
        self.undrawn = []
        self.time = 0

    def update(self) -> None:
        self.time += 1
        for o in reversed(self.objects):
            try:
                o.update()
            except IndexError:
                self.objects.remove(o)

    def isRunning(self) -> bool:
        return True

    def draw(self, display) -> None:
        #update and draw each object, and then handle render -> display trasform
        lib.renderSurface.fill(0)
        display.fill(0)
        for o in self.objects:
            o.draw()
        for o in self.undrawn:
            o.draw()
        # lib.collisionBoxes()
        frame = lib.pygame.transform.smoothscale(lib.renderSurface, lib.displaySize())
        display.blit(frame, frame.get_rect())
        lib.pygame.display.flip()




if __name__ == "__main__": #temp runner code
    pygame.init()
    pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    game = Game()
    game.objects.append(Forbiddance((200, 200), (200, 600)))
    game.objects.append(Forbiddance((200, 600), (600, 600)))
    game.objects.append(Forbiddance((600, 600), (600, 200)))
    game.objects.append(Forbiddance((600, 200), (200, 200)))
    # game.objects.append(Vigor((400, 400), (800, 800), True))
    # game.objects.append(Vigor((210, 700), (210, 1000), True))
    # game.objects.append(Vigor((600, 300), (800, 300), True))
    # game.objects.append(Vigor((300, 300), (400, 200), True))
    game.draw(pygame.display.get_surface())
    
    running = True
    start = None
    while running:
        for evt in lib.pygame.event.get(): #todo, add event handling to seperate class/game class
            if evt.type == lib.pygame.quit:
                lib.pygame.quit()
                running = False
                break
            elif evt.type == lib.pygame.MOUSEBUTTONDOWN:
                start = lib.screenToGame(lib.pygame.mouse.get_pos())
            elif evt.type == lib.pygame.MOUSEBUTTONUP and start != None:
                game.objects.append(Vigor(start, lib.screenToGame(lib.pygame.mouse.get_pos()), True))
                start = None
            else:
                if lib.pygame.key.get_pressed()[lib.pygame.K_SPACE]:
                    # game.update()
                    # game.draw(pygame.display.get_surface())
                    pass
        game.update()
        game.draw(pygame.display.get_surface())
        lib.pygame.time.delay(10)
