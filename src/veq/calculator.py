'''Containing module for the Calculator class.'''

from typing import List, Dict, Union
from veq.tokens import TokenBuilder, Token, TokenStream, VariableToken, FunctionToken

class CalculationError(Exception):

    '''An exception that indicates there was an error in calculating the user's equation.'''
    
    def __init__(self, expression: str):
        self.__expression = expression
        super().__init__(expression)

    def __str__(self):
        return f"Error in equation \"f(x) = {self.__expression}\""

class Calculator:

    '''Class responsible for converting infix to postfix and calculating expressions.

    :attribute stream: Expression in infix format for reading expressions.
    :type stream: str or TokenStream
    :attribute stack: Calculation stack.
    :type stack: List(float)
    :value stack: []'''

    def __init__(self, stream: Union[str, TokenStream], stack: List[float] = []):
        self.stack = stack
        self.__builder = TokenBuilder(self.stack)

        if isinstance(stream, str):
            self.stream = TokenStream(stream)
        else:
            self.stream = stream

        self.expression = []

    def infix_to_postfix(self):
        '''Convert infix stream to postfix list of tokens.

        :param expression: String to tokenize.
        :type expression: str
        :returns: List of tokens
        :rtype: list(Token)'''

        lookup: Dict[str, Token] = {
            "+":   self.__builder.build_add,
            "-":   self.__builder.build_subtract,
            "*":   self.__builder.build_multiply,
            "/":   self.__builder.build_divide,
            "^":   self.__builder.build_power,
            "sin(": self.__builder.build_sin,
            "cos(": self.__builder.build_cos,
            "tan(": self.__builder.build_tan,
            "log(": self.__builder.build_log,
        }

        stack: List[Token] = []

        token: Token = None

        for match in self.stream:
            if match in lookup:
                token = lookup[match]()
            elif match == "x":
                token = self.__builder.build_x()
                self.expression.append(token)
                continue
            elif match == '(':
                self.infix_to_postfix()
                continue
            elif match == ')':
                while len(stack) > 0:
                    self.expression.append(stack.pop())
                return
            elif match == 'pi':
                token = self.__builder.build_pi()
                self.expression.append(token)
                continue
            elif match == 'e':
                token = self.__builder.build_e()
                self.expression.append(token)
                continue
            else:
                try:
                    x = float(match)
                except:
                    raise TypeError(f"Invalid Token \"{match}\"")
                else:
                    token = self.__builder.build_value(x)
                    self.expression.append(token)
                    continue

            if isinstance(token, FunctionToken):
                self.infix_to_postfix()
                self.expression.append(token)
                continue

            while len(stack) > 0 and stack[-1].precedence >= token.precedence:
                self.expression.append(stack.pop())
            stack.append(token)

        while len(stack) > 0:
            self.expression.append(stack.pop())

    def calculate(self, x: float) -> float:
        '''Calculate the Calculator's expression.

        :param x: Value to substitute for x in the expression.
        :type x: float
        :returns: The result of the equation.
        :rtype: float'''
        if len(self.expression) == 0:
            self.infix_to_postfix()

        self.stack.clear()

        try:
            for token in self.expression:
                if isinstance(token, VariableToken):
                    token.execute(x)
                else:
                    token.execute()
        except:
            pass
        else:
            if len(self.stack) > 0:
                result = self.stack[-1]
                if isinstance(result, (float, int)):
                    return result
        raise CalculationError(self.stream.text)
