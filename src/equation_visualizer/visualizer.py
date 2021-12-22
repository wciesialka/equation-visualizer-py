'''Equation visualization module.'''

from typing import Callable, Tuple, List
import pygame
import logging

from equation_visualizer.calculator import Calculator

class Equation:

    def __init__(self, calculator: Calculator, domain: Tuple[int, int], range: Tuple[int, int]):
        self.domain = domain
        self.range = range
        self.calculator = calculator
        self.calculator.infix_to_postfix()

    def f(self, x):
        self.calculator.calculate(x)

    def zoom(self, by):
        if self.range[0] - by/2 < self.range[1] + by/2 and self.domain[0] - by/2 < self.domain[1] + by/2:
            self.range[0] -=   by/2
            self.range[1] +=   by/2
            self.domain[0] -=  by/2
            self.domain[1] +=  by/2

class Visualizer:

    def __init__(self, equation: Equation, screen: pygame.Surface, *, color: Tuple[int, int, int] = (0, 0, 0)):
        pygame.font.init()
        self.font = pygame.font.SysFont("Courier New", 12)
        self.equation = equation
        self.screen = screen
        self.color = color

    @property
    def left(self):
        return self.equation.domain[0]
    
    @property
    def right(self):
        return self.equation.domain[1]

    def f(self, x):
        return self.equation.f(x)

    @property
    def width(self):
        return self.screen.get_width()

    @property
    def height(self):
        return self.screen.get_height()

    @property
    def top(self):
        return self.equation.range[1]

    @property
    def bottom(self):
        return self.equation.range[0]

    def draw_equation(self):

        dx: float = (self.right-self.left)/self.width

        def map(x):
            try:
                y = self.f(x)
            except:
                return None # Error
            else:
                # output = output_start + ((output_end - output_start) / (input_end - input_start)) * (input - input_start)
                divisor = (self.top - self.bottom)

                return (self.height + ((0 - self.height) / divisor) * (y - self.bottom))

        list_of_points = []
        points: List[Tuple[int, float]] = []
        for i in range(0,self.width):
            x = self.left + (dx*i)
            y = map(x)
            # If undefined...
            if y is None or abs(y) > self.height * 4:
                list_of_points.append(points)
                points = []
                if y is None:
                    continue
            point: Tuple[int, float] = (i, y)
            points.append(point)
        list_of_points.append(points)

        for points in list_of_points:
            if(len(points) >= 2):
                try:
                    pygame.draw.lines(self.screen, self.color, False, points, 1)
                except Exception as ex:
                    logging.debug(points)
                    raise ex

    def draw_text(self):

        domain_text = self.font.render(f'Domain: [{self.left}, {self.right}]', True, (0, 0, 0), (255, 255, 255))
        range_text = self.font.render(f'Range: [{self.bottom}, {self.top}]', True, (0, 0, 0), (255, 255, 255))
        self.screen.blit(domain_text, (0, 0))
        self.screen.blit(range_text, (0, 12))