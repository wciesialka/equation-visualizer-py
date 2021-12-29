'''Equation visualization module.'''

import logging
from typing import Tuple, List, Union
from time import time
import pygame
from veq.calculator import CalculationError, Calculator

def remap(value: float, input_range: Tuple[float, float], output_range: Tuple[float, float]) -> float:
    '''Map a value from an input range to an output range.

    :param value: Value to map.
    :type value: float
    :param input_range: Input range to map from.
    :type input_range: tuple(float, float)
    :param output_range: Output range to map to.
    :type output_range: tuple(float, float)
    :returns: Mapped value.
    :rtype: float
    '''
    # f(x) = o_s + ((o_e - o_s) / (i_e - i_s)) * (x - i_s)
    input_start, input_end = input_range
    output_start, output_end = output_range
    divisor = input_end - input_start
    dividend = output_end - output_start
    multiplier = value - input_start

    return output_start + (dividend / divisor) * multiplier

class Equation:

    '''An equation with an expression, domain, and range.

    :attribute calculator: The calculator holding the postfix expression to calculate.
    :type calculator: veq.calculator.Calculator
    :attribute domain: Domain of the equation.
    :type domain: tuple(float, float)
    :attribute range: Range of the equation.
    :type range: tuple(float, float)'''

    def __init__(self, calculator: Calculator, \
        domain: Tuple[float, float], range: Tuple[float, float]):

        self.domain = domain
        self.range = range
        self.calculator = calculator
        self.calculator.infix_to_postfix()

    def zoom(self, increase: float):
        '''Adjust the domain and range by a given number to give the illusion of zooming in/out.

        :param increase: Number to adjust by. Half will be subtracted\
            from the left bound of the domain and range, while \
                another half will be added to the right bound.
        :type increase: float'''
        if (self.range[0] - increase/2 < self.range[1] + increase/2) and\
             (self.domain[0] - increase/2 < self.domain[1] + increase/2):
            self.range[0] -= increase/2
            self.range[1] += increase/2
            self.domain[0] -= increase/2
            self.domain[1] += increase/2

    def shift(self, shift_by: Tuple[float, float]):
        '''Shift the domain and range of the equation.

        :param shift_by: What values to adjust by.
        :type shift_by: tuple(float, float)'''
        self.domain[0] += shift_by[0]
        self.domain[1] += shift_by[0]
        self.range[0] += shift_by[1]
        self.range[1] += shift_by[1]

class Visualizer:

    '''Graphical visualization of an equation.

    :attribute equation: What equation to plot.
    :type equation: veq.visualizer.Equation
    :attribute screen: pygame surface to plot on.
    :type screen: pygame.Surface
    :attribute color: What color of line to plot.
    :type color: tuple(int, int, int)
    :value color: tuple(0, 0, 0)
    :property width: Width of the screen in pixels.
    :type width: int
    :property height: Height of the screen in pixels.
    :type height: int
    :property left: Left bound of the equation's domain.
    :type left: float
    :property right: Right bound of the equation's domain.
    :type right: float
    :property top: Left bound of the equation's range.
    :type top: float
    :property bottom: Right bound of the equation's range.
    :type bottom: float'''

    def __init__(self, equation: Equation, screen: pygame.Surface, *,\
         color: Tuple[int, int, int] = (0, 0, 0)):

        pygame.font.init()
        self.__font = pygame.font.SysFont("Courier New", 12)
        self.equation = equation
        self.screen = screen
        self.color = color
        self.__saved = None

        self.__t = 0
        self.__last_render = 0

    @property
    def left(self):
        '''Left bound of the equation.'''
        return self.equation.domain[0]

    @property
    def right(self):
        '''Right bound of the equation.'''
        return self.equation.domain[1]

    def execute(self, x: float) -> Union[float, None]:
        '''Calculate the Calculator's expression with value x.

        :param x: Value to substitute x for in the Visualizer's equation.
        :type x: float
        :returns: The resulting expression, or None if there is no valid\
             calculation for that x value.
        :rtype: float or None'''
        try:
            y = self.equation.calculator.calculate(x = x, t = self.__t)
        except CalculationError:
            return None
        else:
            return y

    @property
    def width(self):
        '''Width of the screen.'''
        return self.screen.get_width()

    @property
    def height(self):
        '''Height of the screen.'''
        return self.screen.get_height()

    @property
    def top(self):
        '''Top bound of the equation.'''
        return self.equation.range[1]

    @property
    def bottom(self):
        '''Bottom bound of the equation.'''
        return self.equation.range[0]

    def reset_t(self):
        '''Reset the internal t variable.'''
        self.__last_render = 0
        self.__t = 0

    def draw_equation(self):
        '''Plot the equation to the screen.'''
        render_start = time()

        dx: float = (self.right-self.left)/self.width

        list_of_points = []
        points: List[Tuple[int, float]] = []
        for i in range(0, self.width):
            # Get X and Y
            x = self.left + (dx*i)
            y = self.execute(x)
            if y is None:
                continue
            else:
                screen_y = remap(y, (self.bottom, self.top), (self.height, 0))

                # If considerably enough on screen...
                if abs(screen_y) > self.height * 4:
                    list_of_points.append(points)
                    points = []

                point: Tuple[int, float] = (i, screen_y)
                points.append(point)

        list_of_points.append(points)

        for points in list_of_points:
            if len(points) >= 2:
                try:
                    pygame.draw.lines(self.screen, self.color, False, points, 1)
                except Exception as ex:
                    logging.debug(points)
                    raise ex

        current_time = time()
        if self.__last_render == 0:
            self.__t = current_time - render_start
        else:
            self.__t += current_time - self.__last_render
        self.__last_render = current_time

    def draw_text(self):
        '''Draw text onto the screen.'''

        domain_text = f'Domain: [{self.left:1.2f}, {self.right:1.2f}]'
        range_text = f'Range: [{self.bottom:1.2f}, {self.top:1.2f}]'
        equation_text = f"Equation: {self.equation.calculator.stream}"
        t_text = f"t: {self.__t:1.2f}"

        domain_surface = self.__font.render(domain_text, True, (0, 0, 0), (255, 255, 255))
        range_surface = self.__font.render(range_text, True, (0, 0, 0), (255, 255, 255))
        equation_surface = self.__font.render(equation_text, True, (0, 0, 0), (255, 255, 255))

        t_surface = self.__font.render(t_text, True, (0, 0, 0), (255, 255, 255))
        t_width = t_surface.get_size()[0]

        self.screen.blit(domain_surface, (0, 12))
        self.screen.blit(range_surface, (0, 24))
        self.screen.blit(equation_surface, (0, 0))
        self.screen.blit(t_surface, (self.width - t_width, 0))

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

    def draw_grid(self, step: float):
        '''Draw a grid onto the screen, with the lines seperated\
             by a certain step.

        :param step: What amount to seperate gridlines by.
        :type step: float'''

        if round(step) == step:
            step_precision = 0
        else:
            step_str = str(step)
            step_precision = len(step_str[step_str.index('.')+1:])

        text_format = lambda x: str(round(x, step_precision))

        grid_color = (200, 200, 200)
        text_color = (100, 100, 100)

        for x in self.__domain_range(step):
            screen_x = remap(x, (self.left, self.right), (0, self.width))
            pygame.draw.line(self.screen, grid_color, (screen_x, 0), (screen_x, self.height))
            text = text_format(x)
            text_surface = self.__font.render(text, True, text_color, (255, 255, 255))
            self.screen.blit(text_surface, (screen_x - (len(text)/2)*6, self.height-12))

        for y in self.__range_range(step):
            screen_y = remap(y, (self.bottom, self.top), (self.height, 0))
            pygame.draw.line(self.screen, grid_color, (0, screen_y), (self.width, screen_y))
            text = text_format(y)
            text_surface = self.__font.render(text, True, text_color, (255, 255, 255))
            self.screen.blit(text_surface, (12, screen_y - 6))

    def draw_axis(self):
        '''Draw the axis lines onto the screen.'''

        axis_color = (205, 25, 25)
        screen_x = remap(0, (self.left, self.right), (0, self.width))
        screen_y = remap(0, (self.bottom, self.top), (self.height, 0))
        if 0 <= screen_x <= self.width:
            pygame.draw.line(self.screen, axis_color, (screen_x, 0), (screen_x, self.height))
        if 0 <= screen_y <= self.height:
            pygame.draw.line(self.screen, axis_color, (0, screen_y), (self.width, screen_y))

    def draw_location(self, mouse_pos: Tuple[int, int]):
        '''Draw the location text information onto the screen.

        :param mouse_pos: Position of the mouse on the screen.
        :type mouse_pos: tuple(int, int)'''

        color = (0, 0, 175)

        mouse_x, mouse_y = mouse_pos
        x = remap(mouse_x, (0, self.width), (self.left, self.right))
        y = self.execute(x)
        if not y is None:
            screen_y = remap(y, (self.bottom, self.top), (self.height, 0))
            location_text = f"Location: ({x:.2f}, {y:.2f})"

            pygame.draw.circle(self.screen, color, (mouse_x, screen_y), 5, width=2)
            text_surface = self.__font.render(location_text, True, (0, 0, 0), (255, 255, 255))
            self.screen.blit(text_surface, (0, 48))

    def save(self, mouse_pos: Tuple[int, int]):
        '''Save the current location into the visualizer.

        :param mouse_pos: Position of the mouse on the screen.
        :type mouse_pos: tuple(int, int)'''
        mouse_x, mouse_y = mouse_pos
        x = remap(mouse_x, (0, self.width), (self.left, self.right))
        self.__saved = x

    def on_screen(self, pixel: Tuple[int, int]) -> bool:
        '''Returns whether the given pixel is within the bounds of the screen.

        :param pixel: What pixel to check.
        :type pixel: tuple(int, int)
        :returns: true if the pixel is within the bounds of the screen, and false if it isn't.
        :rtype: bool'''
        return 0 <= pixel[0] <= self.width and 0 <= pixel[1] <= self.height

    def draw_saved(self):
        '''Draw the saved location onto the screen.'''
        color = (25, 175, 25)

        if not self.__saved is None:
            x = self.__saved
            y = self.execute(x)
            if not y is None:
                screen_x = remap(x, (self.left, self.right), (0, self.width))
                screen_y = remap(y, (self.bottom, self.top), (self.height, 0))
                saved_text = f"Saved: ({x:.2f}, {y:.2f})"
                text_surface = self.__font.render(saved_text, True, (0, 0, 0), (255, 255, 255))
                self.screen.blit(text_surface, (0, 36))
                if self.on_screen((screen_x, screen_y)):
                    pygame.draw.circle(self.screen, color, (screen_x, screen_y), 4, width=1)
