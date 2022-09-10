from line import Line
import pygame


class Forbiddance(Line):
    def __init__(self, start : tuple[int, int], end: tuple[int, int]) -> None:
        super().__init__()
        self.start = start
        self.end = end
    def draw(self):
        pygame.draw.line(pygame.display.get_surface(), (0, 0, 255), self.start, self.end)
    def update(self):
        pass
