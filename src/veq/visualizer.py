'''Equation visualization module.'''

from typing import Callable, Tuple, List
import pygame
import logging

from veq.calculator import Calculator

def map(value, input_start, input_end, output_start, output_end):
    # output = output_start + ((output_end - output_start) / (input_end - input_start)) * (input - input_start)
    divisor = input_end - input_start
    dividend = output_end - output_start
    multiplier = value - input_start

    return output_start + (dividend / divisor) * multiplier

class Equation:

    def __init__(self, calculator: Calculator, domain: Tuple[int, int], range: Tuple[int, int]):
        self.domain = domain
        self.range = range
        self.calculator = calculator
        self.calculator.infix_to_postfix()

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

        def y_map(x):
            try:
                y = self.equation.calculator.calculate(x)
            except:
                return None # Error
            else:
                if isinstance(y, float) or isinstance(y, int): # We don't want complex numbers or anything unexpected...
                    return map(y, self.bottom, self.top, self.height, 0)
                return None

        list_of_points = []
        points: List[Tuple[int, float]] = []
        for i in range(0,self.width):
            # Get X and Y
            x = self.left + (dx*i)
            y = y_map(x)
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

        domain_text = self.font.render(f'Domain: [{self.left:1.2f}, {self.right:1.2f}]', True, (0, 0, 0), (255, 255, 255))
        range_text = self.font.render(f'Range: [{self.bottom:1.2f}, {self.top:1.2f}]', True, (0, 0, 0), (255, 255, 255))
        eq_text = self.font.render(f"Equation: {self.equation.calculator.stream}",  True, (0, 0, 0), (255, 255, 255))
        self.screen.blit(domain_text, (0, 12))
        self.screen.blit(range_text, (0, 24))
        self.screen.blit(eq_text, (0, 0))

    def __domain_range(self, step):
        x = (self.left // step) * step 
        while x < self.right:
            x += step
            yield x
        return x

    def __range_range(self, step):
        y = (self.bottom // step) * step 
        while y < self.top:
            y += step
            yield y
        return y

    def draw_grid(self, step):

        if round(step) == step:
            step_precision = 0
        else:
            step_str = str(step)
            step_precision = len(step_str[step_str.index('.')+1:])

        text_format = lambda x : str(round(x,step_precision))

        grid_color = (200, 200, 200)
        text_color = (100, 100, 100)

        for x in self.__domain_range(step):
            screen_x = map(x, self.left, self.right, 0, self.width)
            pygame.draw.line(self.screen, grid_color, (screen_x, 0), (screen_x, self.height))
            text = text_format(x)
            text_surface = self.font.render(text, True, text_color, (255, 255, 255))
            self.screen.blit(text_surface, (screen_x - (len(text)/2)*6, self.height-12))
            

        for y in self.__range_range(step):
            screen_y =  map(y, self.bottom, self.top, self.height, 0)
            pygame.draw.line(self.screen, grid_color, (0, screen_y), (self.width, screen_y))
            text = text_format(y)
            text_surface = self.font.render(text, True, text_color, (255, 255, 255))
            self.screen.blit(text_surface, (12, screen_y - 6))
            
    def draw_axis(self):

        axis_color = (205, 25, 25)
        screen_x = map(0, self.left, self.right, 0, self.width)
        screen_y = map(0, self.bottom, self.top, self.height, 0)
        if 0 <= screen_x <= self.width:
            pygame.draw.line(self.screen, axis_color, (screen_x, 0), (screen_x, self.height))
        if 0 <= screen_y <= self.height:
            pygame.draw.line(self.screen, axis_color, (0, screen_y), (self.width, screen_y))