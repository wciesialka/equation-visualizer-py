'''Main module.'''

import argparse
import logging
from typing import Pattern
import pygame
from veq.calculator import Calculator
from veq.visualizer import Equation, Visualizer
import re

INTERVAL_REGEX: str = r"^\[(-?\d+\.?\d*),\s*(-?\d+\.?\d*)\]$"
INTERVAL_PATTERN: Pattern = re.compile(INTERVAL_REGEX)

class PrecisionAction(argparse.Action):

    def __call__(self, parser, namespace, values, option_string = ...) -> None:
        if values < 0:
            parser.error("Minimum precision is zero.")

        setattr(namespace, self.dest, values)

class IntervalAction(argparse.Action):

    def __call__(self, parser, namespace, values, option_string = ...) -> None:

        if not INTERVAL_PATTERN.match(values):
            parser.error(f"Invalid {option_string} format: {values}")

        setattr(namespace, self.dest, values)

def parse_args() -> argparse.Namespace:
    '''Parse command line arguments.

    :returns: Parsed arguments.
    :rtype: argparse.Namespace'''
    parser = argparse.ArgumentParser("veq", description="Visualize an equation.")
    parser.add_argument("equation", type=str.lower, help="Equation to plot.")
    parser.add_argument("--debug", dest="level", action="store_const",\
         const=logging.DEBUG, default=logging.INFO, help="Enable debug logging.")
    parser.add_argument("-s", "--step", metavar='n', type=float, default=None,\
         help="Enable gridlines with step n")
    parser.add_argument("-a", "--noaxis", dest="axis", action="store_false", help="Disable axis.")
    parser.add_argument("-p", "--precision", type=int, default=2, action=PrecisionAction, help="Number precision for text formatting.")
    parser.add_argument("-d", "--domain", default="[-1, 1]", action=IntervalAction, help="Initial domain.")
    parser.add_argument("-r", "--range", default="[-1, 1]", action=IntervalAction, help="Initial range.")


    return parser.parse_args()

def main():
    '''Run the main functionality of the program.'''
    args = parse_args()

    logging.basicConfig(level=args.level)

    domain = [float(x) for x in INTERVAL_PATTERN.findall(args.domain)[0]]
    range_ = [float(x) for x in INTERVAL_PATTERN.findall(args.range)[0]]
    mouse_x, mouse_y = (0, 0)

    calculator = Calculator(args.equation)

    pygame.init()

    screen = pygame.display.set_mode([900, 900])
    pygame.display.set_caption('veq')

    equation = Equation(calculator, domain.copy(), range_.copy())
    visualizer = Visualizer(equation, screen, precision=args.precision)

    running = True
    while running: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEWHEEL:
                if event.y != 0:
                    equation.zoom(-event.y)
            elif event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = event.pos

                # If RMB is down...
                if event.buttons[2] == 1:
                    move_x = -event.rel[0] * visualizer.dx
                    move_y = event.rel[1] * visualizer.dx
                    equation.shift((move_x, move_y))
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    visualizer.save(event.pos)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                    equation.zoom(1)
                elif event.key == pygame.K_PLUS or event.key == 61 or event.key == pygame.K_KP_PLUS:
                    # 61 = Plus. For some reason pygame.K_PLUS wasn't wanting to work
                    equation.zoom(-1)
                elif event.key == pygame.K_r:
                    if event.mod & pygame.KMOD_SHIFT:
                        visualizer.reset_t()
                    else:
                        equation.domain = domain.copy()
                        equation.range = range_.copy()
                elif event.key == pygame.K_UP:
                    equation.shift((0, 0.5))
                elif event.key == pygame.K_DOWN:
                    equation.shift((0, -0.5))
                elif event.key == pygame.K_LEFT:
                    equation.shift((-0.5, 0))
                elif event.key == pygame.K_RIGHT:
                    equation.shift((0.5, 0))
            elif event.type == pygame.ACTIVEEVENT:
                focus = (event.gain == 1)

        screen.fill((255, 255, 255))
        if not args.step is None:
            visualizer.draw_grid(args.step)
        if args.axis:
            visualizer.draw_axis()
        visualizer.draw_equation()
        visualizer.draw_text()

        if focus:
            visualizer.draw_location((mouse_x, mouse_y))
        visualizer.draw_saved()

        pygame.display.flip()

    pygame.quit()



if __name__ == "__main__":
    main()
