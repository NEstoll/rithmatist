import lib

class Cursor:
    def __init__(self, pos=(0, 0)) -> None:
        self.mouse = pos
        pass
    def draw(self)-> None:
        lib.drawPoint(self.mouse, (255, 0, 0))
        pass