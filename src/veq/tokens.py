'''Module containing all tokens and classes needed to tokenize expressions.

:data TOKEN_REGEX: Regular Expression used for extracting specific token characters.
:type TOKEN_REGEX: Pattern'''

import re
from abc import ABC, abstractmethod
from typing import Callable, Dict, List, Pattern
from math import acos, acosh, asin, asinh, atan, atanh, cosh, degrees, e, fabs, fmod, pi, radians, sin, cos, sinh, tan, log, tanh

class Token(ABC):

    '''Token Abstract Base Class.'''

    def __init__(self, stack: List):
        self._stack = stack

    @abstractmethod
    def execute(self):
        '''Execute the function.'''
        pass

    @property
    def precedence(self):
        '''Precedence of a token.'''
        try:
            return self.__class__.PRECEDENCE
        except NameError: # If value isn't set
            return -1

    def __str__(self):
        return self.__class__.__name__

class VariableToken(Token):

    '''Variable token.'''

    def __init__(self, stack:List, name:str):
        super().__init__(stack)
        self.__name = name

    @property
    def name(self) -> str:
        '''Return the read-only name property.'''
        return self.__name

    def execute(self, value: float):
        '''Push given value to top of stack.

        :param value: What value to push.
        :type value: float'''
        self._stack.append(value)

    def __str__(self):
        return f"VariableToken({self.name})"

class ValueToken(Token):

    '''Token representing a number.'''

    def __init__(self, stack: List, value: float):
        super().__init__(stack)
        self.__value = value

    def execute(self):
        '''Push value to top of stack.'''
        self._stack.append(self.__value)
    
    def __str__(self):
        return f"ValueToken({self.__value})"

class TokenBuilder:

    '''Build tokens.'''

    TOKENS: Dict[str, Callable[[], Token]] = {}

    def __init__(self, stack: List):
        self._stack = stack

    def build_value(self, value: float) -> ValueToken:
        '''Build a value token.'''
        return ValueToken(self._stack, value)

    def build_variable(self, name: str) -> VariableToken:
        '''Build a variable token.'''
        return VariableToken(self._stack, name)

def add_builder(function_name:str, key: str):
    '''This decorator allows us to dynamically add tokens to the TokenBuilder.

    :param function_name: Name of the function to add.
    :type function_name: str
    :param key: What represents the function in an equation.
    :type key: str'''

    def decorate(cls):
        def func(self, *args, **kwargs):
            return cls(self._stack, *args, **kwargs)

        setattr(TokenBuilder, function_name, func)
        TokenBuilder.TOKENS[key] = function_name

        return cls

    return decorate
class BinaryToken(Token):

    '''Binary Operation token.'''

    @abstractmethod
    def operation(self, a, b):
        '''What operation to execute.'''
        pass

    def execute(self):
        '''Pop two items from the stack, run an operation on them,\
            and push the result to the stack.'''
        b = self._stack.pop()
        a = self._stack.pop()
        result = self.operation(a, b)
        self._stack.append(result)

@add_builder("build_add", "+")
class AddToken(BinaryToken):

    '''Addition token.'''

    PRECEDENCE = 1

    def operation(self, a, b):
        '''Add a and b'''
        return a + b

@add_builder("build_subtract", "-")
class SubtractToken(BinaryToken):

    '''Subtraction token.'''

    PRECEDENCE = 1

    def operation(self, a, b):
        '''Subtract a and'''
        return a - b

@add_builder("build_multiply", "*")
class MultiplyToken(BinaryToken):

    '''Multiplication token.'''

    PRECEDENCE = 2

    def operation(self, a, b):
        '''Multiply a and b'''
        return a * b

@add_builder("build_divide", "/")
class DivideToken(BinaryToken):

    '''Division token.'''

    PRECEDENCE = 2

    def operation(self, a, b):
        '''Divide a and b.'''
        return a / b

@add_builder("build_modulo", "%")
class ModuloToken(BinaryToken):

    '''Modulo token.'''

    PRECEDENCE = 2

    def operation(self, a, b):
        return fmod(a, b)

@add_builder("build_power", "^")
class PowerToken(BinaryToken):

    '''Exponation token.'''

    PRECEDENCE = 3

    def operation(self, a, b):
        '''Exponate a to the power of b'''
        return a ** b

class FunctionToken(Token):

    '''Token representing a unary function.'''

    @abstractmethod
    def operation(self, a):
        pass

    def execute(self):
        '''Pop an item from the stack, run a function on it,\
            and push the result to the stack.'''
        a = self._stack.pop()
        result = self.operation(a)
        self._stack.append(result)

@add_builder("build_sin", "sin(")
class SinToken(FunctionToken):

    '''Sine token.'''

    PRECEDENCE = 4

    def operation(self, a):
        '''Run sin'''
        return sin(a)

@add_builder("build_cos", "cos(")
class CosToken(FunctionToken):

    '''Cosine token.'''

    PRECEDENCE = 4

    def operation(self, a):
        '''Run cosine'''
        return cos(a)

@add_builder("build_tan", "tan(")
class TanToken(FunctionToken):

    '''Tangent token.'''

    PRECEDENCE = 4

    def operation(self, a):
        '''Run tangent'''
        return tan(a)

@add_builder("build_log", "log(")
class LogToken(FunctionToken):

    '''Logarithm token.'''

    PRECEDENCE = 4

    def operation(self, a):
        '''Run natural logarithm.'''
        return log(a)

@add_builder("build_sinh", "sinh(")
class SinhToken(FunctionToken):

    '''Hyperbolic Sine Token.'''

    PRECEDENCE = 4

    def operation(self, a):
        return sinh(a)

@add_builder("build_cosh", "cosh(")
class CoshToken(FunctionToken):

    '''Hyperbolic Cosine Token.'''

    PRECEDENCE = 4

    def operation(self, a):
        return cosh(a)

@add_builder("build_tanh", "tanh(")
class TanhToken(FunctionToken):

    '''Hyperbolic Tangent Token.'''

    PRECEDENCE = 4

    def operation(self, a):
        return tanh(a)

@add_builder("build_sign", "sign(")
class SignToken(FunctionToken):

    '''Sign Token.'''

    PRECEDENCE = 4

    def operation(self, a):
        if a < 0:
            return -1
        elif a > 0:
            return 1
        return 0

@add_builder("build_abs", "abs(")
class AbsToken(FunctionToken):

    '''Absolute Value token.'''

    PRECEDENCE = 4

    def operation(self, a):
        return fabs(a)

@add_builder("build_round", "round(")
class RoundToken(FunctionToken):

    '''Round Token.'''

    PRECEDENCE = 4

    def operation(self, a):
        return round(a)

@add_builder("build_rad", "rad(")
class RadiansToken(FunctionToken):

    '''Radian Conversion Token.'''

    PRECEDENCE = 4

    def operation(self, a):
        return radians(a)

@add_builder("build_deg", "deg(")
class DegreesToken(FunctionToken):

    '''Degrees Conversion Token.'''

    PRECEDENCE = 4

    def operation(self, a):
        return degrees(a)

@add_builder("build_acos", "acos(")
class ArcCosToken(FunctionToken):

    '''Arc Cosine token.'''

    PRECEDENCE = 4

    def operation(self, a):
        return acos(a)

@add_builder("build_asin", "asin(")
class ArcSinToken(FunctionToken):

    '''Arc Sine token.'''

    PRECEDENCE = 4

    def operation(self, a):
        return asin(a)

@add_builder("build_atan", "atan(")
class ArcTanToken(FunctionToken):

    '''Arc Tangent token.'''

    PRECEDENCE = 4

    def operation(self, a):
        return atan(a)

@add_builder("build_acosh", "acosh(")
class ArcCosHToken(FunctionToken):

    '''inverse hyperbolic cosine token.'''

    PRECEDENCE = 4

    def operation(self, a):
        return acosh(a)

@add_builder("build_asinh", "asinh(")
class ArcSinHToken(FunctionToken):

    '''inverse hyperbolic sine token.'''

    PRECEDENCE = 4

    def operation(self, a):
        return asinh(a)

@add_builder("build_atanh", "atanh(")
class ArcTanHToken(FunctionToken):

    '''inverse hyperbolic tangent token.'''

    PRECEDENCE = 4

    def operation(self, a):
        return atanh(a)

TOKEN_REGEX_STRING: str = r"\d+.?\d*|"
TOKEN_REGEX_STRING += "|".join([re.escape(token) for token in TokenBuilder.TOKENS.keys()]) 
TOKEN_REGEX_STRING += r"|\(|\)|[a-z]+"
TOKEN_REGEX: Pattern[str] = re.compile(TOKEN_REGEX_STRING) 

class TokenStream:

    '''A read-only representation of a stream of strings representing individual tokens.

    :property text: The infix represenetation of the full expression.
    :type text: str'''

    def __init__(self, expression: str):
        self.__expression: List[str] = TOKEN_REGEX.findall(expression)
        self.__iteration = 0

    @property
    def text(self) -> str:
        '''The infix representation of the full expression.'''
        return "".join(self.__expression)

    def reset(self):
        '''Reset the stream to the beginning.'''
        self.__iteration = 0

    def __iter__(self): 
        return self

    def __next__(self):
        if self.__iteration < len(self.__expression):
            value = self.__expression[self.__iteration]
            self.__iteration += 1
            return value
        raise StopIteration

    def __str__(self):
        return self.text
