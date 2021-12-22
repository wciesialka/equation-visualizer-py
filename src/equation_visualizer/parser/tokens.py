import re
from abc import ABC, abstractmethod
from typing import List, Dict
from math import e, pi, sin, cos, tan, log10

class TokenBuilder:

    def __init__(self, stack: List):
        self.__stack = stack

    def build_value(self, value: float):
        return ValueToken(self.__stack, value)

class Token(ABC):

    def __init__(self, stack: List):
        self.__stack = stack

    @abstractmethod
    def execute(self):
        pass

class ValueToken(Token):

    def __init__(self, stack: List, value: float):
        super().__init__(stack)
        self.__value = value

    def execute(self):
        self.__stack.append(self.__value)

class PiToken(ValueToken):

    def __init__(self, stack: List):
        super().__init__(stack, pi)

class EulerToken(ValueToken):

    def __init__(self, stack: List, value: float):
        super().__init__(stack, e)

class BinaryToken(Token):

    @abstractmethod
    def operation(self, a, b):
        pass

    def execute(self):
        b = self.__stack.pop()
        a = self.__stack.pop()
        result = self.operation(a,b)
        self.__stack.append(result)

class AddToken(BinaryToken):

    def operation(self, a, b):
        return a + b
        
class SubtractToken(BinaryToken):

    def operation(self, a, b):
        return a - b

class MultiplyToken(BinaryToken):

    def operation(self, a, b):
        return a * b

class DivideToken(BinaryToken):

    def operation(self, a, b):
        return a / b

class PowerToken(BinaryToken):

    def operation(self, a, b):
        return a ** b

class UnaryToken(Token):

    @abstractmethod
    def operation(self, a,):
        pass

    def execute(self):
        a = self.__stack.pop()
        result = self.operation(a)
        self.__stack.append(result)

class SinToken(UnaryToken):

    def operation(self, a):
        return sin(a)

class CosToken(UnaryToken):

    def operation(self, a):
        return cos(a)

class TanToken(UnaryToken):

    def operation(self, a):
        return tan(a)

class LogToken(UnaryToken):

    def operation(self, a):
        return log10(a)

TOKEN_REGEX = re.compile(r"\d+.?\d*|\+|-|\*|\(|\)|\^|tan|cos|sin|log|pi|e")

def tokenize(expression: str, stack: List[float]) -> List[Token]:
    '''Tokenize a string.
    
    :param expression: String to tokenize.
    :type expression: str
    :returns: List of tokens
    :rtype: list(Token)'''

    builder: TokenBuilder = TokenBuilder(stack)

    REPRESENTATIONS: Dict[str, Token] = {
    }

    matches: List = TOKEN_REGEX.findall(expression)
    tokens: List[Token] = []

    for match in matches:
        if match in REPRESENTATIONS:
            tokens.append(REPRESENTATIONS[match]())
        else:
            try:
                x = float(match)
            except:
                raise TypeError(f"Invalid Token \"{match}\"")
            else:
                tokens.append(builder.build_value(x))

    return tokens