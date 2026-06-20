### question
You are given an array of strings `tokens` that represents a valid arithmetic expression in [Reverse Polish Notation](https://en.wikipedia.org/wiki/Reverse_Polish_notation).
Return the integer that represents the evaluation of the expression.

* The operands may be integers or the results of other operations.
* The operators include `'+'`, `'-'`, `'*'`, and `'/'`.
* Assume that division between integers always truncates toward zero.

## 1. Restate

Evaluate a valid Reverse Polish Notation expression.

In RPN:

- numbers go onto a stack
- operator consumes the latest two numbers
- result goes back onto stack
- final stack value = answer

## 2. Clarify

Assumptions:

- `tokens` is non-empty and valid
- operators: `+ - * /`
- operands may be negative
- division truncates toward zero
- return an integer

Important: for `-` and `/`, operand order matters.  
For stack values `left, right`, compute `left operator right`.

## 3. Example by hand

```text
tokens = ["2", "1", "+", "3", "*"]

"2"  -> stack [2]
"1"  -> stack [2, 1]
"+"  -> 2 + 1 = 3   -> stack [3]
"3"  -> stack [3, 3]
"*"  -> 3 * 3 = 9   -> stack [9]

answer = 9
```

## 4. Possible solutions

### Expression tree

Build a tree, then evaluate recursively.

- Time: `O(n)`
- Space: `O(n)`
- unnecessary structure

### Stack

Process tokens left to right:

- number: push
- operator: pop right, then left; calculate; push result

- Time: `O(n)`
- Space: `O(n)`

Selected: stack. Directly matches the by-hand process.

## 5. Implementation outline

```python
def evalRPN(tokens):  # -> int
    """
    Reframe: Each operator reduces the two latest completed expressions
    into one completed expression.

    State: stack of evaluated operands/results, chosen because RPN operators
    always use the two most recent values.

    Invariant: after each token, the stack contains all completed values
    not yet consumed by an operator.

    apply(left, right, operator) =
    evaluate left operator right.

    Core logic:
    - create an empty stack
    - visit each token
    - if token is a number, push its integer value
    - otherwise pop the right operand
    - pop the left operand
    - apply the operator
    - push the result
    - return the remaining value

    Edge cases:
    - one number and no operators
    - negative operands
    - subtraction operand order
    - division operand order
    - negative division must truncate toward zero
    """
```

## 6. Iterative implementation

### Iteration 1: skeleton

```python
def evalRPN(tokens):
    stack = []

    for token in tokens:
        if is_operator(token):
            right = stack.pop()
            left = stack.pop()
            result = apply(left, right, token)
            stack.append(result)
        else:
            stack.append(int(token))

    return stack.pop()
```

### Iteration 2: identify operators

```python
def evalRPN(tokens):
    stack = []
    operators = {"+", "-", "*", "/"}

    for token in tokens:
        if token in operators:  # implemented operator detection
            right = stack.pop()
            left = stack.pop()
            result = apply(left, right, token)
            stack.append(result)
        else:
            stack.append(int(token))

    return stack.pop()
```

### Iteration 3: implement operations

```python
def evalRPN(tokens):
    stack = []
    operators = {"+", "-", "*", "/"}

    def apply(left, right, operator):
        if operator == "+":
            return left + right
        if operator == "-":
            return left - right
        if operator == "*":
            return left * right

        return int(left / right)  # truncates toward zero

    for token in tokens:
        if token in operators:
            right = stack.pop()
            left = stack.pop()
            stack.append(apply(left, right, token))
        else:
            stack.append(int(token))

    return stack.pop()
```

## 7. Edge-case walk

- Single number: pushed, then returned. Works.
- Negative token such as `"-11"`: not equal to an operator, converted with `int`. Works.
- Subtraction: pop `right` first, then `left`. Works.
- Division: same operand ordering. Works.
- Negative division: `int(-7 / 3)` gives `-2`, truncating toward zero.

## Final code

```python
from typing import List


class Solution:
    def evalRPN(self, tokens: List[str]) -> int:
        stack = []
        operators = {"+", "-", "*", "/"}

        def apply(left: int, right: int, operator: str) -> int:
            if operator == "+":
                return left + right
            if operator == "-":
                return left - right
            if operator == "*":
                return left * right

            return int(left / right)

        for token in tokens:
            if token in operators:
                right = stack.pop()
                left = stack.pop()
                stack.append(apply(left, right, token))
            else:
                stack.append(int(token))

        return stack.pop()
```

Time: `O(n)`  
Space: `O(n)` worst case.