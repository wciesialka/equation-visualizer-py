'''Riemann Sum visualization module.'''

from typing import Callable, Tuple, List
import pygame

class RiemannSum:

    def __init__(self, f:Callable[[float], float], domain: Tuple[int, int], range: Tuple[int, int]):
        self.left, self.right = domain
        self.top, self.bottom = range
        self.f = f

class Visualizer:

    def __init__(self, equation: RiemannSum, screen: pygame.Surface, *, color: Tuple[int, int, int] = (0, 0, 0)):
        self.equation = equation
        self.screen = screen
        self.color = color

    @property
    def left(self):
        return self.equation.left
    
    @property
    def right(self):
        return self.equation.right

    @property
    def f(self):
        return self.equation.f

    @property
    def width(self):
        return self.screen.get_width()

    @property
    def height(self):
        return self.screen.get_height()

    @property
    def top(self):
        return self.equation.top

    @property
    def bottom(self):
        return self.equation.bottom

    def draw_equation(self):

        dx: float = (self.right-self.left)/self.width

        def map(x):
            y = self.f(x)
            # output = output_start + ((output_end - output_start) / (input_end - input_start)) * (input - input_start)
            return self.height - (self.height + ((0 - self.height) / (self.top - self.bottom)) * (y - self.bottom))

        points: List[Tuple[int, float]] = [(0, map(self.left))]
        for i in range(1,self.width):
            x = self.left + (dx*i)
            point: Tuple[int, float] = (i, map(x))
            points.append(point)

        pygame.draw.lines(self.screen, self.color, False, points, 1)