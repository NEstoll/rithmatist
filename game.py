
import lib

from forbiddance import Forbiddance
from vigor import Vigor

class Game:

    def __init__(self) -> None:
        #variable instantiation
        self.objects = []

        #display
        # self.window = lib.pygame.display.set_mode((320, 240))
        self.window = lib.pygame.display.set_mode((0, 0), lib.pygame.FULLSCREEN)
        lib.pygame.display.update()

        
    def draw(self):
        lib.pygame.draw.rect(lib.drawing, (0, 0, 0), lib.pygame.Rect(0, 0, lib.pygame.display.get_window_size()[0], lib.pygame.display.get_window_size()[1]))
        for o in self.objects:
            o.update()
            o.draw()
        lib.collisionBoxes()

        frame = lib.pygame.transform.scale(lib.drawing, self.window.get_size())
        self.window.blit(frame, frame.get_rect())
        lib.pygame.display.flip()



if __name__ == "__main__":
    game = Game()
    game.objects.append(Forbiddance((10, 10), (100, 30)))
    game.objects.append(Vigor((1000, 200), (900, 60)))
    game.draw()
    
    running = True
    while running:
        for evt in lib.pygame.event.get():
            if evt.type == lib.pygame.quit:
                lib.pygame.quit()
                running = False
                break
        game.draw()
        lib.pygame.time.delay(10)
