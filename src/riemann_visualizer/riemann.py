'''Calculate Riemann sums.'''

from typing import Callable, Tuple, List
from math import sin


def __midpoint_generator(left: float, right: float, dx: float):
    '''Generator for the riemann function.'''
    x: float = left + (dx/2)
    while x < right:
        yield x
        x += dx

def riemann(f: Callable[[float], float], left: float, right: float, subdivisions: int) -> float:
    '''Calculate the midpoint Riemann sum of function f over domain [left, right] with n subdivisions.

    :param f: Function f.
    :type f: callable(float) -> float
    :param left: Left domain.
    :type left: float
    :param right: Right domain.
    :type right: float
    :param subdivisions: How many subdivisions to calculate.
    :type subdivisions: int'''


    if not callable(f):
        raise TypeError(f"f must be callable.")
    
    if left > right:
        raise ValueError("Left domain must not be greater than right domain.")
    
    if subdivisions <= 0:
        raise ValueError("Cannot have less than or equal to zero subdivisions.")

    riemann_sum = 0

    dx: float = (right-left)/subdivisions
    for x in __midpoint_generator(left, right, dx):
        y: float = f(x)
        area = dx * y
        riemann_sum += area

    return riemann_sum