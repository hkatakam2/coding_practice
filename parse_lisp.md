### question
You are given a string expression representing a Lisp-like expression to return the integer value of.

The syntax for these expressions is given as follows.

An expression is either an integer, let expression, add expression, mult expression, or an assigned variable. Expressions always evaluate to a single integer.
(An integer could be positive or negative.)
A let expression takes the form "(let v1 e1 v2 e2 ... vn en expr)", where let is always the string "let", then there are one or more pairs of alternating variables and expressions, meaning that the first variable v1 is assigned the value of the expression e1, the second variable v2 is assigned the value of the expression e2, and so on sequentially; and then the value of this let expression is the value of the expression expr.
An add expression takes the form "(add e1 e2)" where add is always the string "add", there are always two expressions e1, e2 and the result is the addition of the evaluation of e1 and the evaluation of e2.
A mult expression takes the form "(mult e1 e2)" where mult is always the string "mult", there are always two expressions e1, e2 and the result is the multiplication of the evaluation of e1 and the evaluation of e2.
For this question, we will use a smaller subset of variable names. A variable starts with a lowercase letter, then zero or more lowercase letters or digits. Additionally, for your convenience, the names "add", "let", and "mult" are protected and will never be used as variable names.
Finally, there is the concept of scope. When an expression of a variable name is evaluated, within the context of that evaluation, the innermost scope (in terms of parentheses) is checked first for the value of that variable, and then outer scopes are checked sequentially. It is guaranteed that every expression is legal. Please see the examples for more details on the scope.
 

 class Solution:
    def evaluate(self, expression: str) -> int:
        tokens = (
            expression
            .replace("(", " ( ")
            .replace(")", " ) ")
            .split()
        )

        # variable -> stack of active values
        values = {}

        def is_integer(token):
            return token[0].isdigit() or token[0] == "-"

        def push(variable, value):
            values.setdefault(variable, []).append(value)

        def pop(variable):
            values[variable].pop()

            if not values[variable]:
                del values[variable]

        def parse(i):
            token = tokens[i]

            # -------------------------
            # Atom: integer / variable
            # -------------------------
            if token != "(":
                if is_integer(token):
                    return int(token), i + 1

                return values[token][-1], i + 1

            operator = tokens[i + 1]

            # -------------------------
            # add
            # -------------------------
            if operator == "add":
                left, j = parse(i + 2)
                right, j = parse(j)

                # j currently points after second expression,
                # which means at the closing ')'
                return left + right, j + 1

            # -------------------------
            # mult
            # -------------------------
            if operator == "mult":
                left, j = parse(i + 2)
                right, j = parse(j)

                return left * right, j + 1

            # -------------------------
            # let
            # -------------------------
            assigned = []
            j = i + 2

            while True:
                token = tokens[j]

                # Final expression of the let
                if (
                    token == "("
                    or is_integer(token)
                    or tokens[j + 1] == ")"
                ):
                    result, j = parse(j)

                    # Leave this lexical scope
                    for variable in reversed(assigned):
                        pop(variable)

                    return result, j + 1

                # Otherwise:
                # variable expression pair
                variable = token

                value, j = parse(j + 1)

                push(variable, value)
                assigned.append(variable)

        result, _ = parse(0)
        return result