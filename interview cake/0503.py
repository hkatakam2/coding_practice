'''
write a recursive function for generating all
permutations of an input string, return them as a set

assume: every character in the input string is unique

breakdown:
how to re-phrase the problem of getting all permutations
for 'cats' in terms of a smaller but similar subproblem?

if we had all the permutations for all characters
except the last i.e. 'cat', how could we
use tht to generate all permutations for 'cats'?

what is the base case?
'''
def get_permutations(string):
    # base case
    if len(string) <= 1:
        return set([string])
    
    all_chars_except_last = string[:-1]
    last_char = string[-1]

    # recursive call: get all possible permutations for all chars except last
    permutations_of_all_chars_except_last = get_permutations(all_chars_except_last)

    # put the last char in all possible positions for each
    # of the above permutations
    permutations = set()
    for permutation_of_all_chars_except_last in permutations_of_all_chars_except_last:
        for position in range(len(all_chars_except_last) + 1):
            permutation = (
                permutation_of_all_chars_except_last[:position]
                + last_char
                + permutation_of_all_chars_except_last[position:]
            )
            permutations.add(permutation)
    return permutations

'''
learning:
first figure out how you would solve the problem "by hand"
and then translate that process into code 
'''
'''
Bonus: what if the input has string has duplicate chars?
some permutations will be identical, set avoids this problem

how to improve?
current implementation has 
Time Complexity: O(n!), as it generates all possible permutations.
Space Complexity: O(n!), as it stores all permutations in memory.


Avoid constructing duplicate permutations upfront: 
Instead of using a set, directly filter duplicates by keeping track of 
used characters.

'''
def get_permutations(string):
    def backtrack(path, remaining, result):
        if not remaining:
            result.append("".join(path))
            return

        used = set()  # To avoid duplicate permutations in the same recursive branch
        for i, char in enumerate(remaining):
            if char in used:
                continue
            used.add(char)
            backtrack(path + [char], remaining[:i] + remaining[i + 1:], result)

    result = []
    backtrack([], list(string), result)
    return result
'''
The time complexity is still O(n!) for generating all unique permutations, 
as that’s the lower bound for this problem. However, avoiding duplicate 
computations reduces redundant work

The algorithm avoids explicitly storing all permutations in memory, 
reducing space usage to O(n) for the recursion stack
'''
'''
how this code works:

Initial call: path=[], remaining=['a','b','c']
├─ Choose 'a': path=['a'], remaining=['b','c']
│  ├─ Choose 'b': path=['a','b'], remaining=['c']
│  │  └─ Choose 'c': path=['a','b','c'] ✓ (add to result)
│  └─ Choose 'c': path=['a','c'], remaining=['b']
│     └─ Choose 'b': path=['a','c','b'] ✓ (add to result)
└─ Choose 'b': path=['b'], remaining=['a','c']
   ... and so on

Uses backtracking to explore all possibilities
Handles duplicates using a used set
Builds permutations character by character
Time complexity: O(n! * n) where n is string length
Space complexity: O(n! * n) for storing all permutations
'''