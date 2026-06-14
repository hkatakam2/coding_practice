## question
You are given an input string s consisting of lowercase english letters, and a pattern p consisting of lowercase english letters, as well as '.', and '*' characters.
Return true if the pattern matches the entire input string, otherwise return false.

'.' Matches any single character
'*' Matches zero or more of the preceding element.

**1. Restating the Question**
Goal: Determine if string `s` completely matches pattern `p`.
Rules:

* `.` matches exact one of any character.
* `*` matches zero or more of the immediately preceding character.
Must match the *entire* string, not just a substring.

**2. Clarifying Questions & Confirming Inputs/Outputs**

* Can `p` start with `*`? Assume no, patterns are well-formed (e.g., `a*`, not `*a`).
* Can inputs be empty? Yes. `s=""`, `p=""` -> True. `s=""`, `p="a*"` -> True.
* Valid characters? Lowercase English only, plus `.` and `*`.
* Examples:
* `s="aa", p="a"` -> False.
* `s="aa", p="a*"` -> True.
* `s="ab", p=".*"` -> True (`.` acts as 'a' then 'b').



**3. Hand Tracing Example**
`s = "aab"`, `p = "c*a*b"`

* Look at `p`: `c*`. Can match 0+ 'c's. `s` has 'a'. Choose 0 matches. Drop `c*`. `s` remains `"aab"`, `p` becomes `"a*b"`.
* Look at `p`: `a*`. Can match 0+ 'a's. `s` has 'a'. Match one! `s` becomes `"ab"`, `p` stays `"a*b"`.
* Look at `p`: `a*` again. `s` has 'a'. Match one! `s` becomes `"b"`, `p` stays `"a*b"`.
* Look at `p`: `a*` again. `s` has 'b'. Doesn't match 'a'. Choose 0 matches. Drop `a*`. `s` is `"b"`, `p` becomes `"b"`.
* Look at `p`: `b`. `s` has 'b'. Match! `s` becomes `""`, `p` becomes `""`.
* Both empty -> True.

**4. Brainstorming & Complexity**

* *Approach A: Linear Scan.* Fails because `*` introduces ambiguity (how many to match?).
* *Approach B: Recursion (Backtracking).* Make a choice at `*`: either match 0 chars (skip `*`), or match 1 char (keep `*` for next turn). Time: $O(2^{N+M})$ worst case. Space: $O(N+M)$ call stack.
* *Approach C: Recursion + Memoization (Top-down DP).* Cache results for `(s_index, p_index)`. Time: $O(N \cdot M)$. Space: $O(N \cdot M)$.

**5. Suggesting Solutions**
Prefer Approach C. Simple, clear. Directly mirrors the hand-tracing logic. We step through `s` and `p`. If we see `*`, we branch. We cache the branches. No clever 2D matrix bottom-up math needed; plain English recursion is easiest to explain.

**6. Outline & Core Logic**

```python
def isMatch(s: str, p: str) -> bool:
    """
    Reframe: Match character by character; handle '*' by branching into two paths: skip '*' or consume a character and keep '*'.
    State: current string index and current pattern index, chosen because substring matching depends only on remaining suffixes.
    Invariant: If current indices evaluate to true, the remaining string completely matches the remaining pattern.

    first_char_matches(s_idx, p_idx) = checks if current string char matches current pattern char (or if pattern is '.').
    has_star_next(p_idx) = checks if the next character in pattern is '*'.

    Core logic:
    - Check if first character matches.
    - If pattern has a star next:
        - Branch 1: Skip the star and preceding char (advance pattern by 2).
        - Branch 2: If first char matched, consume one char from string (advance string by 1) and keep pattern same.
        - Return true if either branch is true.
    - If no star next:
        - If first character matched, advance both string and pattern by 1.
        - Return result of continued match.

    Edge cases:
    - Pattern is fully consumed. (Is string also consumed?)
    - String is fully consumed, but pattern still has elements (e.g., "a*b*").
    - Index out of bounds when checking first_char_matches or has_star_next.
    """

```

**7. Iterative Implementation**

*Iteration 1: Core logic skeleton (Happy Path only, no bounds checking yet)*

```python
def isMatch(s: str, p: str) -> bool:
    def dfs(i, j):
        # Helper stubs
        first_char_matches = (s[i] == p[j] or p[j] == '.')
        has_star_next = (p[j + 1] == '*')

        # Core plain English logic
        if has_star_next:
            # Branch 1: skip star | Branch 2: use star (if match)
            skip_star = dfs(i, j + 2)
            use_star = first_char_matches and dfs(i + 1, j)
            return skip_star or use_star
        else:
            # Normal match
            return first_char_matches and dfs(i + 1, j + 1)
            
    return dfs(0, 0)

```

*Iteration 2: Fleshing out edge cases (fixing out-of-bounds errors)*
If `i` or `j` exceed lengths, the above crashes. Let's patch edges.

```python
def isMatch(s: str, p: str) -> bool:
    def dfs(i, j):
        # Edge Case 1: Pattern is fully consumed
        if j >= len(p):
            return i >= len(s) # True only if string is also empty
            
        # Edge Case 3: first_char_matches bounds check. 
        # i can be out of bounds if string is empty but pattern has "a*"
        first_char_matches = (i < len(s)) and (s[i] == p[j] or p[j] == '.')
        
        # Edge Case 3: has_star_next bounds check
        has_star_next = (j + 1 < len(p)) and (p[j + 1] == '*')

        if has_star_next:
            skip_star = dfs(i, j + 2)
            use_star = first_char_matches and dfs(i + 1, j)
            return skip_star or use_star
        else:
            return first_char_matches and dfs(i + 1, j + 1)
            
    return dfs(0, 0)

```

**8. Complexity & Optimizations**

* **Current Complexity:** Exponential time $O(2^{N+M})$ due to branching at every `*` without caching. Overlapping subproblems exist (e.g., reaching the same `i, j` via different matching paths).
* **Optimization:** Memoization. Cache `(i, j)` to avoid re-evaluating the same suffixes.
* **Final Optimized Code:**

```python
def isMatch(s: str, p: str) -> bool:
    cache = {} # Map (i, j) -> bool

    def dfs(i, j):
        if (i, j) in cache:
            return cache[(i, j)]
            
        if j >= len(p):
            return i >= len(s)
            
        first_char_matches = (i < len(s)) and (s[i] == p[j] or p[j] == '.')
        has_star_next = (j + 1 < len(p)) and (p[j + 1] == '*')

        if has_star_next:
            # Try skipping, or try consuming 1 char if matched
            ans = dfs(i, j + 2) or (first_char_matches and dfs(i + 1, j))
        else:
            # Normal character progression
            ans = first_char_matches and dfs(i + 1, j + 1)
            
        cache[(i, j)] = ans
        return ans
            
    return dfs(0, 0)

```

* **Final Complexity:** - Time: $O(N \cdot M)$ where $N$ is length of `s`, $M$ is length of `p`. Each state `(i, j)` is computed exactly once.
* Space: $O(N \cdot M)$ to store the cache and recursion stack.