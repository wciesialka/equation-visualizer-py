import pygame
from veq.calculator import Calculator
from veq.visualizer import Equation, Visualizer
from math import log, sin
import argparse
import logging

def parse_args() -> argparse.Namespace:
    '''Parse command line arguments.

    :returns: Parsed arguments.
    :rtype; argparse.Namespace'''
    parser = argparse.ArgumentParser("veq",description="Visualize an equation.")
    parser.add_argument("equation", type=str.lower, help="Equation to plot.")
    parser.add_argument("-d","--debug", dest="level", action="store_const", const=logging.DEBUG, default=logging.INFO, help="Enable debug logging.")
    parser.add_argument("-s","--step", metavar='n', type=float, default=None, help="Enable gridlines with step n")
    parser.add_argument("-a","--noaxis", dest="axis", action="store_false", help="Disable axis.")

    return parser.parse_args()

def main():
    args = parse_args()

    logging.basicConfig(level=args.level)

    domain = [-1, 1]
    range = [-1, 1]

    calc = Calculator(args.equation)

    pygame.init()

    screen = pygame.display.set_mode([900, 900])
    pygame.display.set_caption('veq')

    eq = Equation(calc, domain.copy(), range.copy())
    visualizer = Visualizer(eq, screen)

    running = True
    while running: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEWHEEL:
                if event.y != 0:
                    eq.zoom(-event.y)
            elif event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = event.pos

                # If RMB is down...
                if event.buttons[2] == 1:
                    rel = [x/100 for x in event.rel]
                    eq.domain[0] -= rel[0]
                    eq.domain[1] -= rel[0]
                    eq.range[0]  += rel[1]
                    eq.range[1]  += rel[1]
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    visualizer.save(event.pos)
            elif event.type == pygame.KEYUP:
                logging.debug("Key pressed: %i", event.key)
                if event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                    eq.zoom(1)
                elif event.key == pygame.K_PLUS or event.key == 61 or event.key == pygame.K_KP_PLUS: 
                    # 61 = Plus. For some reason pygame.K_PLUS wasn't wanting to work
                    eq.zoom(-1)
                elif event.key == pygame.K_r:
                    eq.domain = domain.copy()
                    eq.range = range.copy()
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



if __name__=="__main__":
    main()