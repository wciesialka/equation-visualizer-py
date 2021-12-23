import re
from abc import ABC, abstractmethod
from typing import List, Dict
from math import e, pi, sin, cos, tan, log

class Token(ABC):

    def __init__(self, stack: List):
        self._stack = stack

    @abstractmethod
    def execute(self):
        pass

    @property
    def precedence(self):
        try:
            return self.__class__.PRECEDENCE
        except: # If value isn't set
            return -1

class OpenToken(Token):

    def execute(self):
        pass

class CloseToken(Token):

    def execute(self):
        pass

class VariableToken(Token):

    def execute(self, value):
        self._stack.append(value)

class ValueToken(Token):

    def __init__(self, stack: List, value: float):
        super().__init__(stack)
        self.__value = value

    def execute(self):
        self._stack.append(self.__value)

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
        b = self._stack.pop()
        a = self._stack.pop()
        result = self.operation(a,b)
        self._stack.append(result)

class AddToken(BinaryToken):

    PRECEDENCE = 1

    def operation(self, a, b):
        return a + b
        
class SubtractToken(BinaryToken):

    PRECEDENCE = 1

    def operation(self, a, b):
        return a - b

class MultiplyToken(BinaryToken):

    PRECEDENCE = 2

    def operation(self, a, b):
        return a * b

class DivideToken(BinaryToken):

    PRECEDENCE = 2

    def operation(self, a, b):
        return a / b

class PowerToken(BinaryToken):

    PRECEDENCE = 4

    def operation(self, a, b):
        return a ** b

class FunctionToken(Token):

    @abstractmethod
    def operation(self, a):
        pass

    def execute(self):
        a = self._stack.pop()
        result = self.operation(a)
        self._stack.append(result)

class SinToken(FunctionToken):

    PRECEDENCE = 3

    def operation(self, a):
        return sin(a)

class CosToken(FunctionToken):

    PRECEDENCE = 3

    def operation(self, a):
        return cos(a)

class TanToken(FunctionToken):

    PRECEDENCE = 3

    def operation(self, a):
        return tan(a)

class LogToken(FunctionToken):

    PRECEDENCE = 3

    def operation(self, a):
        return log(a)

class TokenBuilder:

    def __init__(self, stack: List):
        self._stack = stack

    def build_value(self, value: float):
        return ValueToken(self._stack, value)

    def build_add(self):
        return AddToken(self._stack)

    def build_subtract(self):
        return SubtractToken(self._stack)

    def build_multiply(self):
        return MultiplyToken(self._stack)

    def build_divide(self):
        return DivideToken(self._stack)

    def build_power(self):
        return PowerToken(self._stack)

    def build_pi(self):
        return PiToken(self._stack)

    def build_e(self):
        return EulerToken(self._stack)

    def build_sin(self):
        return SinToken(self._stack)

    def build_cos(self):
        return CosToken(self._stack)

    def build_tan(self):
        return TanToken(self._stack)

    def build_log(self):
        return LogToken(self._stack)

    def build_open(self):
        return OpenToken(self._stack)

    def build_close(self):
        return CloseToken(self._stack)

    def build_x(self):
        return VariableToken(self._stack)

TOKEN_REGEX = re.compile(r"\d+\.?\d*|\+|-|\*|/|\)|\^|tan\(|cos\(|sin\(|log\(|pi|e|x|\(")

class TokenStream:

    def __init__(self, expression: str):
        self.expression: List[str] = TOKEN_REGEX.findall(expression)
        self.i = 0

    def reset(self):
        self.i = 0

    def __iter__(self): 
        return self

    def __next__(self):
        if self.i < len(self.expression):
            value = self.expression[self.i]
            self.i += 1
            return value
        else:
            raise StopIteration

    def __str__(self):
        return "".join(self.expression)