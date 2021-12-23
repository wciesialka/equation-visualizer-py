from typing import List, Dict
from veq.parser.tokens import TokenBuilder, Token, TokenStream, VariableToken, FunctionToken

class Calculator:

    def __init__(self, stream: TokenStream, stack: List[float] = []):
        self.stack = stack
        self.builder = TokenBuilder(self.stack)

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

        REPRESENTATIONS: Dict[str, Token] = {
            "+":   self.builder.build_add,
            "-":   self.builder.build_subtract,
            "*":   self.builder.build_multiply,
            "/":   self.builder.build_divide,
            "^":   self.builder.build_power,
            "sin(": self.builder.build_sin,
            "cos(": self.builder.build_cos,
            "tan(": self.builder.build_tan,
            "log(": self.builder.build_log,
        }

        stack: List[Token] = []

        token: Token = None

        for match in self.stream:
            if match in REPRESENTATIONS:
                token = REPRESENTATIONS[match]()
            elif match == "x":
                token = self.builder.build_x()
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
                token = self.builder.build_pi()
                self.expression.append(token)
                continue
            elif match == 'e':
                token = self.builder.build_e()
                self.expression.append(token)
                continue
            else:
                try:
                    x = float(match)
                except:
                    raise TypeError(f"Invalid Token \"{match}\"")
                else:
                    token = self.builder.build_value(x)
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
        if len(self.expression) == 0:
            self.infix_to_postfix()

        self.stack.clear()

        for token in self.expression:
            if isinstance(token, VariableToken):
                token.execute(x)
            else:
                token.execute()

        return self.stack[-1]