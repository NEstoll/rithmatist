
from os import remove
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

        #display
        #self.window = lib.pygame.display.set_mode((320, 240))
        self.window = lib.pygame.display.set_mode((0, 0), lib.pygame.FULLSCREEN)
        lib.pygame.display.update()

    def update(self):
        self.objects = [o for o in self.objects if not o.update()]
        
    def draw(self):
        #update and draw each object, and then handle render -> display trasform
        lib.pygame.draw.rect(lib.drawing, (0, 0, 0), lib.pygame.Rect(0, 0, lib.displaySize()[0], lib.displaySize()[1]))
        remove = []
        for o in self.objects:
            # if o.update():
            #     remove.append(o)
            #     continue
            o.draw()
        # for o in remove:
        #     self.objects.remove(o)
        #lib.collisionBoxes()

        frame = lib.pygame.transform.scale(lib.drawing, self.window.get_size())
        self.window.blit(frame, frame.get_rect())
        lib.pygame.display.flip()



if __name__ == "__main__": #temp runner code
    game = Game()
    game.objects.append(Forbiddance((300, 100), (100, 300)))
    game.objects.append(Vigor((400, 400), (800, 800)))
    game.draw()
    
    running = True
    while running:
        for evt in lib.pygame.event.get(): #todo, add event handling to seperate class/game class
            if evt.type == lib.pygame.quit:
                lib.pygame.quit()
                running = False
                break
            elif evt.type == lib.pygame.MOUSEBUTTONDOWN:
                start = lib.screenToDrawing(lib.pygame.mouse.get_pos())
            elif evt.type == lib.pygame.MOUSEBUTTONUP and start:
                game.objects.append(Vigor(lib.screenToDrawing(lib.pygame.mouse.get_pos()), start))
        game.update()
        game.draw()
        lib.pygame.time.delay(10)
