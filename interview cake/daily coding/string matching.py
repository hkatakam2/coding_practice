'''
given a string of length N and a pattern of length k, write a program that searches for the pattern in the string.

If the pattern is found, return the start index of its location. If not, return False.

Breakdown:
take all the substrings of len k and check if any of them matches pattern

'''
def pattern_found(string, pattern):
    # base cases: pattern is '', string is ''
    if pattern == '':
        return True
    
    if string == '':
        return False

    n = len(string)
    k = len(pattern)

    def same_string(start_index):
        return string[start_index: start_index + k] == pattern
    
    start_index = 0
    while (start_index + k < n): 
        if same_string(start_index):
            return start_index
        else:
            start_index += 1
    return False 
'''
feedback:
The condition start_index + k < n should be start_index + k <= n
The last possible substring isn't checked
The base case for empty pattern returning True might not be the best choice
'''

'''
0. is my implementation correct? help me reason through my approch and how I could correct errors
1. this question belongs to what kind of problems and how to use this pattern of thinking in other problems, list some of these problems 
2. I want to understand how to think about similar problems, starting from brute force soution and then thinking about improving the solution for time and space
3. i think the O(n) time complexity and O(1) additional space for my implementation, is this correct?
4. we are returning boolean sometimes and integer sometimes, how to handle such scenarios
5. 
'''
def pattern_found(string, pattern):
    # returns index if found, -1 if not found
    # base cases: pattern is '', string is ''
    if pattern == '':
        return 0
    
    if string == '':
        return -1

    n = len(string)
    k = len(pattern)
    
    if k > n:
        return -1
    
    for start_index in range(n - k + 1):
        if string[start_index: start_index + k] == pattern:
            return start_index
    
    return False
'''
O(n * k) time, becuase string slicing and comparison takes O(k) time
O(1) space

Bonus: with less than O(N * k) worst-case time complexity

Optimization Techniques:

Rolling hash (Rabin-Karp)
Pattern preprocessing (KMP)
Suffix arrays
Time: Can reach O(n+k)


'''
# KMP (Knuth-Morris-Pratt) algorithm
def build_pattern_table(pattern):
    # Build the pattern table for KMP algorithm
    table = [0] * len(pattern)
    i = 1
    j = 0
    
    while i < len(pattern):
        if pattern[i] == pattern[j]:
            table[i] = j + 1
            i += 1
            j += 1
        elif j > 0:
            j = table[j - 1]
        else:
            table[i] = 0
            i += 1
    
    return table

def pattern_found(string, pattern):
    # Handle base cases
    if not pattern:
        return 0
    if not string:
        return -1
    if len(pattern) > len(string):
        return -1

    # Build pattern table - O(K) time
    pattern_table = build_pattern_table(pattern)
    
    # Search pattern - O(N) time
    i = 0  # index for string
    j = 0  # index for pattern
    
    while i < len(string):
        if string[i] == pattern[j]:
            if j == len(pattern) - 1:
                return i - j  # Pattern found, return starting index
            i += 1
            j += 1
        elif j > 0:
            j = pattern_table[j - 1]
        else:
            i += 1
    
    return -1  # Pattern not found
'''
Key improvements:

Time complexity is O(N + K) where:

N is the length of the string
K is the length of the pattern
O(K) for building pattern table
O(N) for searching the pattern
Space complexity is O(K) for storing the pattern table

How it works:

First builds a pattern table that helps skip unnecessary comparisons
Uses the pattern table to avoid backtracking in the main string
When a mismatch occurs, uses the pattern table to know how many characters to skip
'''

'''
This is a String Matching/Searching problem. Similar problems include:

KMP Algorithm implementation
Rabin-Karp string matching
Finding all anagrams in a string
Implement strStr() (Leetcode 28)
Longest repeating substring
Longest common substring
'''
