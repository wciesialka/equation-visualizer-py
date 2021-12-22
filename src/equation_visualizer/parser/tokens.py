from abc import ABC, abstractmethod
from typing import List

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