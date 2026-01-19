"""
We will split the logic into four distinct components (Classes):

Token & Tokenizer: Responsible ONLY for reading the string and cleaning up the input (handling that annoying "unary minus" edge case).

Operator (Strategy Pattern): An abstract base class that defines what an operator is. We can create Add, Subtract, Multiply classes that inherit from this.

InfixToPostfix (Service): Responsible ONLY for reordering the tokens (Shunting Yard Algorithm).

Calculator (Facade): The public face that ties it all together.
"""

from abc import ABC, abstractmethod
from collections import deque
from typing import List, Union

# --- 1. DOMAIN MODELS (Open/Closed Principle) ---
# We define an interface for Operators. To add '*', we just add a new class.
# We don't touch the 'Calculator' logic.


class Operator(ABC):
    @property
    @abstractmethod
    def precedence(self) -> int:
        pass

    @abstractmethod
    def apply(self, a: int, b: int) -> int:
        pass


class Add(Operator):
    @property
    def precedence(self):
        return 1

    def apply(self, a, b):
        return a + b


class Subtract(Operator):
    @property
    def precedence(self):
        return 1

    def apply(self, a, b):
        return a - b


# Simple factory/registry to manage supported operators
class OperatorRegistry:
    def __init__(self):
        self._ops = {"+": Add(), "-": Subtract()}

    def get(self, token: str) -> Operator:
        return self._ops.get(token)

    def is_operator(self, token: str) -> bool:
        return token in self._ops


# --- 2. TOKENIZER (Single Responsibility) ---
# Handles the messy string parsing and "Unary Minus" logic
class Tokenizer:
    def tokenize(self, s: str) -> List[Union[str, int]]:
        s = s.replace(" ", "")
        # The classic "Unary Minus" fix for production:
        # Pre-process the string to make it mathematically standard
        s = s.replace("(-", "(0-")
        if s.startswith("-"):
            s = "0" + s

        tokens = []
        i = 0
        while i < len(s):
            char = s[i]
            if char.isdigit():
                num = 0
                while i < len(s) and s[i].isdigit():
                    num = num * 10 + int(s[i])
                    i += 1
                tokens.append(num)
                continue

            # Parentheses and Operators
            tokens.append(char)
            i += 1
        return tokens


# --- 3. PARSER (The Logic Core) ---
# Converts Infix (1 + 1) to Postfix (1 1 +)
class RPNConverter:
    def __init__(self, registry: OperatorRegistry):
        self.registry = registry

    def to_postfix(self, tokens: List) -> List:
        output_queue = []
        op_stack = []

        for token in tokens:
            if isinstance(token, int):
                output_queue.append(token)
            elif token == "(":
                op_stack.append(token)
            elif token == ")":
                while op_stack and op_stack[-1] != "(":
                    output_queue.append(op_stack.pop())
                op_stack.pop()  # Pop '('
            elif self.registry.is_operator(token):
                current_op = self.registry.get(token)
                while (
                    op_stack
                    and op_stack[-1] != "("
                    and self.registry.get(op_stack[-1]).precedence
                    >= current_op.precedence
                ):
                    output_queue.append(op_stack.pop())
                op_stack.append(token)

        while op_stack:
            output_queue.append(op_stack.pop())

        return output_queue


# --- 4. EVALUATOR (The Calculator) ---
class CalculatorEngine:
    def __init__(self, registry: OperatorRegistry):
        self.registry = registry

    def evaluate(self, postfix_tokens: List) -> int:
        stack = []
        for token in postfix_tokens:
            if isinstance(token, int):
                stack.append(token)
            elif self.registry.is_operator(token):
                # Encapsulated logic: The Engine doesn't know HOW to add,
                # it just asks the Operator object to do it.
                op = self.registry.get(token)
                b = stack.pop()
                a = stack.pop()
                stack.append(op.apply(a, b))
        return stack[0]


# --- MAIN SOLUTION CLASS (The Facade) ---
class Solution:
    def calculate(self, s: str) -> int:
        # 1. Setup Dependencies (Dependency Injection style)
        registry = OperatorRegistry()
        tokenizer = Tokenizer()
        converter = RPNConverter(registry)
        engine = CalculatorEngine(registry)

        # 2. Execute Pipeline
        tokens = tokenizer.tokenize(s)
        postfix = converter.to_postfix(tokens)
        return engine.evaluate(postfix)
