
from os import remove

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

    def update(self) -> None:
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

        frame = lib.pygame.transform.smoothscale(lib.renderSurface, lib.displaySize())
        display.blit(frame, frame.get_rect())
        lib.pygame.display.flip()




if __name__ == "__main__": #temp runner code
    pygame.init()
    pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    game = Game()
    game.objects.append(Forbiddance((300, 100), (100, 300)))
    game.objects.append(Vigor((400, 400), (800, 800)))
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
                game.objects.append(Vigor(lib.screenToGame(lib.pygame.mouse.get_pos()), start))
                start = None
        game.update()
        game.draw(pygame.display.get_surface())
        lib.pygame.time.delay(100)
