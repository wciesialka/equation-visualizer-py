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
        color: Tuple[int, int, int] = (0, 0, 0), precision = 2):

        pygame.font.init()
        self.__font = pygame.font.SysFont("Courier New", 12)
        self.equation = equation
        self.screen = screen
        self.color = color
        self.__saved = None

        self.__t = 0
        self.__last_render = 0
        self.precision = precision

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

    @property
    def precision(self):
        '''Precision of numbers in text format.'''
        return self.__precision

    @property
    def dx(self) -> float:
        '''Change of x in pixels.'''
        return (self.right-self.left)/self.width

    @precision.setter
    def precision(self, new_precision: int):
        '''Force precision on text formatted.

        :param new_precision: New precision to be forced.
        :type new_precision: int
        :raises TypeError: Raises TypeError if new_precision is not castable to int.
        :raises ValueError: Raises ValueError if new_precision is less than zero.'''
        try:
            new_precision = int(new_precision)
        except (TypeError, ValueError):
            raise TypeError(f'Expected type int to force_precision, not type {new_precision.__class__.__name__}.')
        if new_precision < 0:
            raise ValueError(f"Precision must be greater than or equal to zero, not {new_precision}.")
        self.__precision = new_precision

    def __format_text(self, text: str, *values) -> str:
        '''Format text with floating point numbers to the correct level of precision.'''
        f_string = f"{{:0.{self.precision}f}}"

        return text.format(*[f_string.format(x) for x in values])

    def reset_t(self):
        '''Reset the internal t variable.'''
        self.__last_render = 0
        self.__t = 0

    def draw_equation(self):
        '''Plot the equation to the screen.'''
        outside_range = False
        render_start = time()

        list_of_points = []
        points: List[Tuple[int, float]] = []
        for i in range(0, self.width):
            # Get X and Y
            x = remap(i, (0, self.width), (self.left, self.right))
            y = self.execute(x)
            if y is None:
                list_of_points.append(points)
                points = []
            else:
                screen_y = remap(y, (self.bottom, self.top), (self.height, 0))

                if screen_y > self.height or screen_y < 0:
                    if not outside_range:
                        if screen_y > self.height:
                            screen_y = self.height
                        else:
                            screen_y = 0
                        points.append((i, screen_y))
                    else:
                        list_of_points.append(points)
                        points = []
                    outside_range = True
                else:
                    outside_range = False
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
            elif len(points) == 1:
                try:
                    self.screen.set_at([round(x) for x in points[0]], self.color)
                except Exception as ex:
                    logging.debug("Error encountered rendering points %s.", points[0])
                    raise ex

        current_time = time()
        if self.__last_render == 0:
            self.__t = current_time - render_start
        else:
            self.__t += current_time - self.__last_render
        self.__last_render = current_time

    def draw_text(self):
        '''Draw text onto the screen.'''

        domain_text = self.__format_text("Domain: [{}, {}]", self.left, self.right)
        range_text = self.__format_text("Range: [{}, {}]", self.bottom, self.top)
        equation_text = f"Equation: {self.equation.calculator.stream}"
        t_text = self.__format_text("t: {}", self.__t)

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

        text_format = lambda x: f"{{:.{step_precision}f}}".format(x)

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
            location_text = self.__format_text("Location: ({}, {})", x, y)

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
                saved_text = self.__format_text("Saved: ({}, {})", x, y)
                text_surface = self.__font.render(saved_text, True, (0, 0, 0), (255, 255, 255))
                self.screen.blit(text_surface, (0, 36))
                if self.on_screen((screen_x, screen_y)):
                    pygame.draw.circle(self.screen, color, (screen_x, screen_y), 4, width=1)
