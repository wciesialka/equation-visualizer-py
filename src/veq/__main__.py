import pygame
from veq.calculator import Calculator
from veq.visualizer import Equation, Visualizer
from math import log, sin
import argparse

def parse_args() -> argparse.Namespace:
    '''Parse command line arguments.

    :returns: Parsed arguments.
    :rtype; argparse.Namespace'''
    parser = argparse.ArgumentParser("veq",description="Visualize an equation.")
    parser.add_argument("equation", type=str.lower)

    return parser.parse_args()


def main():
    args = parse_args()

    domain = [-1, 1]
    range = [-1, 1]

    calc = Calculator(args.equation)

    pygame.init()

    screen = pygame.display.set_mode([900, 900])

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
                # If LMB is /bin/python3down...
                if event.buttons[0] == 1:
                    rel = [x/100 for x in event.rel]
                    eq.domain[0] -= rel[0]
                    eq.domain[1] -= rel[0]
                    eq.range[0]  += rel[1]
                    eq.range[1]  += rel[1]
            elif event.type == pygame.KEYUP:
                if event.key == 114: # r
                    eq.domain = domain.copy()
                    eq.range = range.copy()
        screen.fill((255, 255, 255))
        visualizer.draw_equation()
        visualizer.draw_text()

        pygame.display.flip()

    pygame.quit()



if __name__=="__main__":
    main()