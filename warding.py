import lib
from line import Line

class Warding(Line):
    def __init__(self, center:tuple[int, int], radius:float) -> None:
        super().__init__()
        self.centerx = center[0]
        self.centery = center[1]
        self.radius = radius