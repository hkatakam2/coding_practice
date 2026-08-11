'''
paranthesis matching

write a function that, given a sentence like the one above, along with the
position of an opening paranthesis, finds the corresponding closing paranthesis

breakdown:
how would you solve this problem by hand?
try looping through the string, keeping track of how many open paranthese we have

'''
def get_closing_paren(sentence, opening_paren_index):
    open_nested_parens = 0

    for position in range(opening_paren_index + 1, len(sentence)):
        char = sentence[position]

        if char == "(":
            open_nested_parens += 1
        elif char == ")":
            if open_nested_parens == 0:
                return position
            else:
                open_nested_parens -= 1
    raise Exception("No closing parenthesis :(")
'''
O(n) time and O(1) space

learning:
many "parsing" questions like this is using a stack to track 
which brackets/phrases/etc are "open" as you go.
So next time you get a parsing question, one of your first thoughts 
should be "use a stack!"
'''