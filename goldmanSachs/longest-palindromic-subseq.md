### question
Given a string s, find the longest palindromic subsequence's length in s.

A subsequence is a sequence that can be derived from another sequence by deleting some or no elements without changing the order of the remaining elements.

 

Example 1:

Input: s = "bbbab"
Output: 4
Explanation: One possible longest palindromic subsequence is "bbbb".
Example 2:

Input: s = "cbbd"
Output: 2
Explanation: One possible longest palindromic subsequence is "bb".

## 1. Restate the problem

Given a string `s`, return the **length of the longest subsequence that is a palindrome**.

Important distinction:

* **substring** → characters must be contiguous
* **subsequence** → can skip characters, but order must remain

Example:

```text
s = "bbbab"

"bbbb" is a subsequence:
b b b _ b
```

So answer = `4`.

---

## 2. Clarifying questions

In an interview, I would confirm:

* Can `s` be empty?
* Do we only need the **length**, not the actual subsequence?
* Characters are case-sensitive?
* What are the input constraints?

Assume:

```python
def longestPalindromeSubseq(s: str) -> int:
```

returns an integer.

---

## 3. Work an example by hand

Take:

```text
s = "cbbd"
```

We want the best palindrome inside the whole range:

```text
c b b d
```

Compare the outer characters:

```text
c != d
```

They cannot both belong to the same palindrome as matching endpoints.

So we have two choices:

```text
ignore c → "bbd"
ignore d → "cbb"
```

For `"bbd"`:

```text
b != d
```

Eventually we reach:

```text
"bb"
```

Outer characters match:

```text
b == b
```

So:

```text
2 + palindrome length inside them
= 2
```

Answer:

```text
2
```

---

# 4. Brainstorm solutions

### Solution 1: brute-force subsequences

Generate every possible subsequence.

For a string of length `n`, there are:

```text
2^n
```

subsequences.

For each subsequence, check whether it is a palindrome.

```text
Time: O(n * 2^n)
Space: O(n)
```

Not practical.

---

### Solution 2: recursion

Think in terms of a substring bounded by two positions.

Suppose we are solving:

```text
s[left ... right]
```

Two cases.

### Case 1: endpoints match

```text
s[left] == s[right]
```

We can put both characters around the palindrome formed by the inside:

```text
answer = 2 + solve(left + 1, right - 1)
```

Example:

```text
"bb"

b == b

answer = 2
```

---

### Case 2: endpoints do not match

```text
s[left] != s[right]
```

At least one endpoint cannot be part of our chosen palindrome.

Try both:

```text
ignore left
ignore right
```

Therefore:

```text
answer = max(
    solve(left + 1, right),
    solve(left, right - 1)
)
```

But plain recursion repeats the same ranges.

Worst case:

```text
O(2^n)
```

---

### Solution 3: dynamic programming / memoization

Cache each:

```text
(left, right)
```

There are only:

```text
O(n²)
```

possible ranges.

Each state does constant work.

```text
Time: O(n²)
Space: O(n²)
```

This is the straightforward interview solution.

---

# 5. Key insight

The problem has a natural **interval DP** structure.

For every range of the string:

```text
[left ... right]
```

ask:

> What is the longest palindromic subsequence contained within this range?

The outer characters determine how we reduce the problem.

---

# 6. Implementation outline

```python
def longestPalindromeSubseq(s: str) -> int:
    """
    Reframe:
    Solve the best palindrome inside progressively smaller string ranges.

    State:
    memo[(left, right)] stores the longest palindromic subsequence
    length inside that range.

    Chosen because:
    many recursive branches ask for the same range repeatedly.

    Invariant:
    solve(left, right) always returns the optimal answer using only
    characters inside that range.

    Core logic:
    - If the range is empty, no palindrome exists.
    - If the range contains one character, palindrome length is one.
    - If the two boundary characters match, use both and solve the inside.
    - Otherwise, discard either boundary and take the better result.

    Edge cases:
    - empty string
    - one character
    - two equal characters
    - two different characters
    - all characters equal
    - no repeated characters
    """
```

---

# 7. Iterative implementation

## Iteration 1: skeleton

```python
def longestPalindromeSubseq(s: str) -> int:

    def solve(left, right):
        # base cases

        # matching endpoints

        # non-matching endpoints

        pass

    return solve(0, len(s) - 1)
```

---

## Iteration 2: base cases

What happens when the range becomes invalid?

```text
left > right
```

There are no characters:

```python
return 0
```

What if only one character remains?

```text
left == right
```

Any single character is a palindrome:

```python
return 1
```

Code:

```python
def longestPalindromeSubseq(s: str) -> int:

    def solve(left, right):
        if left > right:
            return 0

        if left == right:
            return 1

        # TODO

    return solve(0, len(s) - 1)
```

---

## Iteration 3: matching endpoints

If:

```python
s[left] == s[right]
```

use both:

```python
return 2 + solve(left + 1, right - 1)
```

Now:

```python
def longestPalindromeSubseq(s: str) -> int:

    def solve(left, right):
        if left > right:
            return 0

        if left == right:
            return 1

        if s[left] == s[right]:
            return 2 + solve(left + 1, right - 1)

        # TODO

    return solve(0, len(s) - 1)
```

---

## Iteration 4: non-matching endpoints

If:

```text
s[left] != s[right]
```

try:

```text
remove left
remove right
```

and take the maximum.

```python
def longestPalindromeSubseq(s: str) -> int:

    def solve(left, right):
        if left > right:
            return 0

        if left == right:
            return 1

        if s[left] == s[right]:
            return 2 + solve(left + 1, right - 1)

        skip_left = solve(left + 1, right)
        skip_right = solve(left, right - 1)

        return max(skip_left, skip_right)

    return solve(0, len(s) - 1)
```

Logically correct.

But inefficient because states repeat.

---

## Iteration 5: add memoization

```python
def longestPalindromeSubseq(s: str) -> int:
    memo = {}

    def solve(left, right):
        if left > right:
            return 0

        if left == right:
            return 1

        if (left, right) in memo:
            return memo[(left, right)]

        if s[left] == s[right]:
            result = 2 + solve(left + 1, right - 1)
        else:
            skip_left = solve(left + 1, right)
            skip_right = solve(left, right - 1)

            result = max(skip_left, skip_right)

        memo[(left, right)] = result
        return result

    return solve(0, len(s) - 1)
```

This is already a good interview answer.

---

# 8. Walk through edge cases

### Empty string

```text
s = ""
```

Initial call:

```text
solve(0, -1)
```

Hits:

```python
if left > right:
    return 0
```

Correct.

---

### One character

```text
"a"
```

```text
solve(0, 0) = 1
```

Correct.

---

### Two equal characters

```text
"aa"
```

Endpoints match:

```text
2 + solve(1, 0)
= 2
```

Correct.

---

### Two different characters

```text
"ab"
```

Try skipping either side:

```text
max(1, 1) = 1
```

Correct.

---

### All characters identical

```text
"aaaa"
```

Every outer pair matches:

```text
4
```

Correct.

---

### No repeating characters

```text
"abcd"
```

Any single character is the longest palindrome:

```text
1
```

Correct.

---

# 9. Bottom-up version

An interviewer may ask:

> Can you avoid recursion?

Yes.

Define:

```text
dp[left][right]
```

as the LPS length within that range.

Base case:

```text
every single character has answer 1
```

Then solve shorter ranges before longer ranges.

```python
def longestPalindromeSubseq(s: str) -> int:
    n = len(s)

    if n == 0:
        return 0

    dp = [[0] * n for _ in range(n)]

    # Single characters.
    for i in range(n):
        dp[i][i] = 1

    # Build from right to left so smaller inner ranges
    # are already available.
    for left in range(n - 1, -1, -1):
        for right in range(left + 1, n):

            if s[left] == s[right]:
                dp[left][right] = 2 + dp[left + 1][right - 1]
            else:
                dp[left][right] = max(
                    dp[left + 1][right],
                    dp[left][right - 1]
                )

    return dp[0][n - 1]
```

One subtle point:

```python
dp[left + 1][right - 1]
```

for adjacent matching characters refers to an empty interior. Since the table is initialized with `0`, this naturally gives:

```text
"bb" → 2 + 0 = 2
```

---

# Complexity

For memoized recursion or bottom-up DP:

```text
States: O(n²)

Work per state: O(1)

Time:  O(n²)
Space: O(n²)
```

---

## What I would present in the interview

I would start with the memoized recursive solution because the recurrence follows directly from the definition:

```python
def longestPalindromeSubseq(s: str) -> int:
    memo = {}

    def solve(left, right):
        if left > right:
            return 0

        if left == right:
            return 1

        if (left, right) in memo:
            return memo[(left, right)]

        if s[left] == s[right]:
            result = 2 + solve(left + 1, right - 1)
        else:
            result = max(
                solve(left + 1, right),
                solve(left, right - 1)
            )

        memo[(left, right)] = result
        return result

    return solve(0, len(s) - 1)
```

The interview explanation is essentially:

> “For each range, if its endpoints match, I can include both and solve the interior. If they don't match, I must exclude at least one endpoint, so I try excluding each and take the better result. There are only `O(n²)` distinct ranges, so memoization reduces the exponential recursion to `O(n²)`.”
