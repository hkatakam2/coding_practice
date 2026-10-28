# question
Maximize Distance to Closest Person (LeetCode 849) & Longest Common Subsequence (LeetCode 1143): Reported in August 2026 loop experiences, where interviewers explicitly required walking through recursion $\rightarrow$ memoization $\rightarrow$ bottom-up DP $\rightarrow$ space optimization.

# restate
Given two strings, find the length of the longest sequence of characters that appears in both, in the same relative order, but not necessarily contiguously. For example, "ace" is a subsequence of "abcde".

# clarify:
1. return the length or actual subseq? number now
2. subseq or substring? seq meaning skip characters
3. can strings be empty?
4. character set and size? Lowercase letters, length up to 1000 each
   1. Size matters here. 1000 × 1000 is fine for O(m·n), but exponential is not.

# ideas
1. Compare the last characters of both strings. If they match, that character can safely be part of an optimal answer, so I take it and shrink both strings by one. If they don’t match, at least one of the two last characters isn’t used, so I try dropping each and take the better result.
2. That’s a recursion over prefix pairs (i, j). Without caching it’s exponential, but there are only m × n distinct pairs, so the subproblems overlap heavily. That points to memoization.
3. Recursion depth is up to m + n, around 2000, which exceeds Python’s default limit of 1000. That’s a concrete reason to go bottom-up.
4. Each table row depends only on the row above it, so I only need two rows. Space drops from O(m·n) to O(min(m, n)).

# outline
lcs_length(i, j) = longest common subsequence of the first i chars of text_a and the first j chars of text_b

lcs_length(i, j):
    if either prefix is empty:          return 0
    if the last chars match:            return 1 + lcs_length(i-1, j-1)
    otherwise:                          return max(lcs_length(i-1, j), lcs_length(i, j-1))

answer = lcs_length(len(text_a), len(text_b))

```python
# plain recursion
# Time is O(2^(m+n)) in the worst case. Space is O(m+n) for the call stack.
def lcs_recursive(text_a, text_b):
    def lcs_length(i, j):
        # if either prefix is empty: return 0
        if i == 0 or j == 0:
            return 0
        # if the last chars match: return 1 + lcs_length(i-1, j-1)
        if text_a[i - 1] == text_b[j - 1]:
            return 1 + lcs_length(i - 1, j - 1)
        # otherwise: max(drop last char of text_a, drop last char of text_b)
        return max(lcs_length(i - 1, j), lcs_length(i, j - 1))

    # answer = lcs_length(len(text_a), len(text_b))
    return lcs_length(len(text_a), len(text_b))

# memoization
# The same function, with each (i, j) computed once. Time and space are O(m·n), plus the O(m+n) call stack.
def lcs_memo(text_a, text_b):
    memo = {}                                  # (i, j) -> lcs_length(i, j)

    def lcs_length(i, j):
        if i == 0 or j == 0:                   # either prefix empty: 0
            return 0
        if (i, j) in memo:                     # NEW: reuse a solved prefix pair
            return memo[(i, j)]
        if text_a[i - 1] == text_b[j - 1]:     # last chars match: 1 + lcs_length(i-1, j-1)
            result = 1 + lcs_length(i - 1, j - 1)
        else:                                  # otherwise: max of the two drops
            result = max(lcs_length(i - 1, j), lcs_length(i, j - 1))
        memo[(i, j)] = result                  # NEW: save before returning
        return result

    return lcs_length(len(text_a), len(text_b))

# @lru_cache does the same thing, but the explicit dict makes the idea visible.

# bottom up DP
# This removes the recursion and the stack-depth risk. Time and space are O(m·n).
# The recursion called smaller prefix pairs first, so I fill the table in that order: increasing i, then increasing j.

def lcs_bottom_up(text_a, text_b):
    m, n = len(text_a), len(text_b)
    # table[i][j] = lcs_length(i, j); row 0 and column 0 stay 0 (the "empty prefix" base case)
    table = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            # if the last chars match: 1 + lcs_length(i-1, j-1)
            if text_a[i - 1] == text_b[j - 1]:
                table[i][j] = table[i - 1][j - 1] + 1
            # otherwise: max(lcs_length(i-1, j), lcs_length(i, j-1))
            else:
                table[i][j] = max(table[i - 1][j], table[i][j - 1])

    # answer = lcs_length(len(text_a), len(text_b))
    return table[m][n]

# space optimized
# table[i][*] reads only table[i-1][*] and itself, so two rows suffice. Time is O(m·n) and space is O(n).
def lcs_two_rows(text_a, text_b):
    n = len(text_b)
    previous_row = [0] * (n + 1)               # row i-1 (starts as the empty-prefix row)

    for i in range(1, len(text_a) + 1):
        current_row = [0] * (n + 1)            # row i; column 0 stays 0 (empty prefix)
        for j in range(1, n + 1):
            if text_a[i - 1] == text_b[j - 1]:                          # last chars match
                current_row[j] = previous_row[j - 1] + 1                #   1 + lcs_length(i-1, j-1)
            else:                                                       # otherwise
                current_row[j] = max(previous_row[j], current_row[j - 1])  # max of the two drops
        previous_row = current_row

    return previous_row[n]                      # lcs_length(len(text_a), len(text_b))

```

# edge cases
```python
def longest_common_subsequence(text_a, text_b):
    # EDGE: an empty string has no common subsequence with anything
    if not text_a or not text_b:
        return 0

    # EDGE: make text_b the shorter string so the rows are as small as possible (LCS is symmetric)
    if len(text_b) > len(text_a):
        text_a, text_b = text_b, text_a

    n = len(text_b)
    previous_row = [0] * (n + 1)                # row for the empty prefix of text_a

    # lcs_length(i, j), filled bottom-up, one row at a time
    for i in range(1, len(text_a) + 1):
        current_row = [0] * (n + 1)
        for j in range(1, n + 1):
            if text_a[i - 1] == text_b[j - 1]:  # last chars match: 1 + lcs_length(i-1, j-1)
                current_row[j] = previous_row[j - 1] + 1
            else:                               # otherwise: max of the two drops (this is also what handles no-match and subsequence-vs-substring)
                current_row[j] = max(previous_row[j], current_row[j - 1])
        previous_row = current_row

    # answer = lcs_length(len(text_a), len(text_b))
    return previous_row[n]
```
