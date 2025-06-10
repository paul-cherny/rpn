import re


class RPNError(Exception):
    pass


def to_rpn(expression: str) -> list[str]:
    output = []
    stack = []
    precedence = {"+": 1, "-": 1, "*": 2, "/": 2}

    tokens = expression.replace("(", " ( ").replace(")", " ) ").split()
    for token in tokens:
        if re.fullmatch(r"\d+(\.\d+)?", token):
            output.append(token)
        elif token in precedence:
            while (
                stack
                and stack[-1] in precedence
                and precedence[token] <= precedence[stack[-1]]
            ):
                output.append(stack.pop())
            stack.append(token)
        elif token == "(":
            stack.append(token)
        elif token == ")":
            while stack and stack[-1] != "(":
                output.append(stack.pop())
            if not stack:
                raise RPNError("Unmatched closing parenthesis")
            stack.pop()
        else:
            raise RPNError(f"Invalid token: '{token}'")

    while stack:
        if stack[-1] in "()":
            raise RPNError("Unmatched opening parenthesis")
        output.append(stack.pop())

    return output


def eval_rpn(rpn_tokens: list[str]) -> float:
    stack = []
    for token in rpn_tokens:
        if re.fullmatch(r"\d+(\.\d+)?", token):
            stack.append(float(token))
        else:
            if len(stack) < 2:
                raise RPNError("Not enough operands")
            b = stack.pop()
            a = stack.pop()
            if token == "+":
                stack.append(a + b)
            elif token == "-":
                stack.append(a - b)
            elif token == "*":
                stack.append(a * b)
            elif token == "/":
                if b == 0:
                    raise ZeroDivisionError("Division by zero")
                stack.append(a / b)
            else:
                raise RPNError(f"Unknown operator: '{token}'")

    if len(stack) != 1:
        raise RPNError("Invalid RPN expression")

    return stack[0]


def calculate(expression: str) -> float:
    rpn = to_rpn(expression)
    return eval_rpn(rpn)
