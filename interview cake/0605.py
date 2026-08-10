'''
brackets validator

breakdown:

'''
def is_valid(code):
    openers_to_closers = {
        '(':')',
        '[':']',
        '{':'}',
    }
    openers = set(openers_to_closers.keys())
    closers = set(openers_to_closers.values())
    
    openers_stack = []

    for char in code:
        if char in openers:
            openers_stack.append(char)
        elif char in closers:
            if not openers_stack:
                return False
            else:
                last_closed_opener = openers_stack.pop()
                # if this closer doesn't correspond to the most recently
                # seen unclosed opener, return False
                if not openers_to_closers[last_closed_opener] == char:
                    return False
    return openers_stack == []

'''
O(n) time and O(n) space 

what we learned:
two common uses fro stacks are:
1. parsing (like in this problem)
2. tree or graph traversal (like depth first traversal)
'''
def is_valid(code):
    closers_to_openers = {
        "}":"{",
        ")":"(",
        "]":"["
    }

    openers_stack = []
    for char in code:
        # if char is closing bracket
        if char in closers_to_openers.keys():
            if not openers_stack: 
                return False
            else: 
                last_closed_opener = openers_stack.pop()
                if closers_to_openers[char] != last_closed_opener: 
                    return False
        # if char is a opening bracket
        elif char in closers_to_openers.values():
            openers_stack.append(char)
    return openers_stack == []
'''
simpler version, O(n) time and O(n) space
'''