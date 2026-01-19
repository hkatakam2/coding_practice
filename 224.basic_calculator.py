"""
given a string s representing a valid expression, implement basic calculator

s can be: digits, +, -, (, ), " "


s = "(1+(4+5+2)-3)+(6 +8)

BODMAS: brackets, of, division, multi, add, sub

ideas:
"""


def calculate(s: str) -> int:
    stack = []
    current_res = 0
    sign = 1
    i = 0

    while i < len(s):
        char = s[i]

        if char.isdigit():
            # val, new_index = get_full_number(s, i)
            val = 0
            while i < len(s) and s[i].isdigit():
                val = val * 10 + int(s[i])
                i += 1

            current_res += val * sign
            i -= 1

        elif char == "+":
            sign = 1
        elif char == "-":
            sign = -1
        elif char == "(":
            # PAUSE: save current state to stack
            stack.append(current_res)
            stack.append(sign)
            # RESET: start fresh for the sub-expression
            current_res = 0
            sign = 1
        elif char == ")":
            # UNPAUSE: retrieve state
            prev_sign = stack.pop()
            prev_res = stack.pop()
            # combine: old_result + (inner_result * old_sign)
            current_res = prev_res + (current_res * prev_sign)

        i += 1
    return current_res
