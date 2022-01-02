'''Containing module for the Calculator class.'''

import logging
from typing import List, Dict, Union
from math import pi, e
from veq.tokens import BinaryToken, TokenBuilder, Token, TokenStream, VariableToken, FunctionToken

class ParsingError(Exception):

    '''An exception that indicates there was an error in parsing the user's equation.'''

    def __init__(self):
        super().__init__()

    def __str__(self):
        return f"Error in parsing equation."

class CalculationError(Exception):

    '''An exception that indicates there was an error in calculating the user's equation.'''
    
    def __init__(self, expression: str):
        self.__expression = expression
        super().__init__(expression)

    def __str__(self):
        return f"Error in equation \"f(x) = {self.__expression}\""

class VariableUndefinedError(Exception):

    '''An exception that indicates the user used an undefined variable.'''

    def __init__(self, variable: str):
        self.__variable = variable
        super().__init__(variable)

    def __str__(self):
        return f"Variable undefined: \"{self.__variable}\""

class Calculator:

    '''Class responsible for converting infix to postfix and calculating expressions.

    :attribute stream: Expression in infix format for reading expressions.
    :type stream: str or TokenStream
    :attribute stack: Calculation stack.
    :type stack: List(float)
    :value stack: []'''

    CONSTANTS = {
        "pi": pi,
        "e": e,
        "g": 9.80665
    }

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

        lookup = TokenBuilder.TOKENS

        stack: List[Token] = []

        value_is_placeable: bool = True
        last_token = None
        token: Token = None

        for match in self.stream:
            if match in lookup:
                # This is really wonky. Basically: Look up what the name of function is.
                function_name = lookup[match]
                # Get the function with that name from the instance of our class.
                build_function = getattr(self.__builder, function_name)
                # Execute that function.
                token = build_function()
                value_is_placeable = True
            elif match == '-':
                if last_token:
                    if isinstance(last_token, BinaryToken):
                        token = self.__builder.build_negate()
                    else:
                        token = self.__builder.build_subtract()
                else:
                    token = self.__builder.build_negate()
                value_is_placeable = True
            elif match == '(':
                self.infix_to_postfix()
                continue
            elif match == ')':
                while len(stack) > 0:
                    self.expression.append(stack.pop())
                return
            elif match.isalpha():
                if value_is_placeable:
                    token = self.__builder.build_variable(name = match)
                    self.expression.append(token)
                    value_is_placeable = False
                    last_token = token
                    continue
                raise ParsingError()
            else:
                if value_is_placeable:
                    token = self.__builder.build_value(value = float(match))
                    self.expression.append(token)
                    value_is_placeable = False
                    last_token = token
                    continue
                raise ParsingError()

            last_token = token

            if isinstance(token, FunctionToken):
                self.infix_to_postfix()
                self.expression.append(token)
                value_is_placeable = False
                continue

            while len(stack) > 0 and stack[-1].precedence >= token.precedence:
                self.expression.append(stack.pop())
            stack.append(token)

        while len(stack) > 0:
            self.expression.append(stack.pop())

    def calculate(self, **variables) -> float:
        '''Calculate the Calculator's expression.

        :param variables: Values to substitute for x in the expression.
        :type variables: dict
        :returns: The result of the equation.
        :rtype: float'''
        if len(self.expression) == 0:
            self.infix_to_postfix()

        self.stack.clear()

        try:
            for token in self.expression:
                if isinstance(token, VariableToken):
                    if token.name in variables:
                        token.execute(variables[token.name])
                    elif token.name in Calculator.CONSTANTS:
                        token.execute(Calculator.CONSTANTS[token.name])
                    else:
                        raise VariableUndefinedError(token.name)
                else:
                    token.execute()
        except:
            pass
        else:
            if len(self.stack) > 0:
                while len(self.stack) > 1:
                    a = self.stack.pop()
                    b = self.stack.pop()
                    self.stack.append(a+b)
                result = self.stack[-1]
                if isinstance(result, (float, int)):
                    return result
        raise CalculationError(self.stream.text)
