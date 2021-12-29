'''Main module.'''

import argparse
import logging
import pygame
from veq.calculator import Calculator
from veq.visualizer import Equation, Visualizer

def parse_args() -> argparse.Namespace:
    '''Parse command line arguments.

    :returns: Parsed arguments.
    :rtype; argparse.Namespace'''
    parser = argparse.ArgumentParser("veq", description="Visualize an equation.")
    parser.add_argument("equation", type=str.lower, help="Equation to plot.")
    parser.add_argument("-d", "--debug", dest="level", action="store_const",\
         const=logging.DEBUG, default=logging.INFO, help="Enable debug logging.")
    parser.add_argument("-s", "--step", metavar='n', type=float, default=None,\
         help="Enable gridlines with step n")
    parser.add_argument("-a", "--noaxis", dest="axis", action="store_false", help="Disable axis.")

    return parser.parse_args()

def main():
    '''Run the main functionality of the program.'''
    args = parse_args()

    logging.basicConfig(level=args.level)

    domain = [-1, 1]
    range_ = [-1, 1]
    mouse_x, mouse_y = (0, 0)

    calculator = Calculator(args.equation)

    pygame.init()

    screen = pygame.display.set_mode([900, 900])
    pygame.display.set_caption('veq')

    equation = Equation(calculator, domain.copy(), range_.copy())
    visualizer = Visualizer(equation, screen)

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
                    rel = (-event.rel[0]/100, event.rel[1]/100)
                    equation.shift(rel)
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
