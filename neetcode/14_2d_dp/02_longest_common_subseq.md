## question
Given two strings text1 and text2, return the length of the longest common subsequence between the two strings if one exists, otherwise return 0.
A subsequence is a sequence that can be derived from the given sequence by deleting some or no elements without changing the relative order of the remaining characters.

For example, "cat" is a subsequence of "crabt".
A common subsequence of two strings is a subsequence that exists in both strings.

# Step 1 — Restate

Given two strings, find length of longest sequence of chars that appears in both, in same relative order (not necessarily contiguous). Return that length, or 0 if none.

# Step 2 — Clarifying questions

- Chars only, or unicode? assume lowercase ascii.
- Case sensitive? assume yes.
- Empty strings allowed? assume yes → answer 0.
- Need the subsequence itself or just length? just length.
- Duplicates in strings? yes, allowed.

# Step 3 — Example by hand

`text1 = "abcde"`, `text2 = "ace"`.

Walk: `a` matches (in both) → take it. `b` not in remaining of text2 → skip. `c` matches → take. `d` skip. `e` matches → take. LCS = `"ace"`, length **3**.

Note the choice structure: at each pair of positions, either the chars match (take both, advance both) or they don't (skip one of the two — try both, keep better).

# Step 4 — Brainstorm

**Brute force / recursion (the by-hand method):** compare from front. If `text1[i]==text2[j]` → 1 + solve(i+1,j+1). Else → max(solve(i+1,j), solve(i,j+1)). Exponential `O(2^(m+n))` — recomputes same (i,j) pairs.

**Memoized recursion (top-down DP):** same recursion + cache on (i,j). Each pair solved once → `O(m·n)` time, `O(m·n)` space. Reads exactly like the by-hand logic.

**Bottom-up table (2D DP):** fill grid `dp[i][j]` = LCS of suffixes. Same complexity, iterative.

**Space-optimized:** keep only 2 rows → `O(min(m,n))` space. Clever, harder to explain.

Recommend **memoized recursion** — mirrors the hand-walk directly, easiest to explain.

# Step 5 — Pick a solution

Which do you want to implement?

- **Memoized recursion (top-down)** — closest to the by-hand walk, recommended
- **Bottom-up 2D table** — classic, fully iterative
- **Space-optimized 2D→1D** — best space, trickier to explain

# Step 6 — Outline

```python
def longest_common_subsequence(text1, text2):  # -> int
    """
    Reframe: at each (i,j) the answer is local choice + best of subproblems;
        same (i,j) recurs many times, so cache it.
    State: memo mapping (i,j) -> LCS length of text1[i:] and text2[j:],
        chosen because suffix pair fully determines the answer (overlapping subproblems).
    Invariant: lcs(i,j) always returns the true LCS length of the two suffixes,
        whether freshly computed or cached.

    lcs(i, j) = LCS length of text1 from i onward and text2 from j onward.
    isCached(i,j) / remember(i,j,val) = read/write the memo.

    Core logic:
    - lcs(i,j): if either suffix empty -> 0
    - if chars at i and j match -> 1 + lcs(next i, next j)
    - else -> better of (skip char i) and (skip char j)
    - answer = lcs(start, start)
    Edge cases:
    - either string empty -> falls out of base case as 0
    - no common chars at all -> recursion bottoms out to 0
    - repeated chars -> handled, match branch only fires on equal chars
    """
```

# Step 7 — Iterative implementation

**Iteration 1 — skeleton from the English:**

```python
def longest_common_subsequence(text1, text2):  # -> int
    def lcs(i, j):
        if base_case(i, j):          # TODO: a suffix is empty
            return 0
        if chars_match(i, j):        # TODO: text1[i] == text2[j]
            return 1 + lcs(i + 1, j + 1)
        return max(skip_i(i, j), skip_j(i, j))  # TODO
    return lcs(0, 0)
```

**Iteration 2 — fill the stubs (still no cache):**

```python
def longest_common_subsequence(text1, text2):  # -> int
    def lcs(i, j):
        if i == len(text1) or j == len(text2):   # base: ran off either string
            return 0
        if text1[i] == text2[j]:                 # match -> consume both
            return 1 + lcs(i + 1, j + 1)
        return max(lcs(i + 1, j), lcs(i, j + 1)) # mismatch -> skip one
    return lcs(0, 0)
```

Core logic now fully correct (just slow).

**Iteration 3 — add memo:**

```python
from functools import lru_cache

def longest_common_subsequence(text1, text2):  # -> int
    @lru_cache(maxsize=None)          # cache on (i,j); each pair computed once
    def lcs(i, j):
        if i == len(text1) or j == len(text2):
            return 0
        if text1[i] == text2[j]:
            return 1 + lcs(i + 1, j + 1)
        return max(lcs(i + 1, j), lcs(i, j + 1))
    return lcs(0, 0)
```

**Edge-case walk:**
- Empty string → first call hits base case → 0. ✓ no patch.
- No common chars → every match branch fails, recursion drains to 0. ✓ no patch.
- Repeated chars → equality check is per-position, correct. ✓ no patch.

All edges already covered by base case + recursion; nothing breaks.

# Step 8 — Complexity

- Distinct `(i,j)` states: `m·n`. Each computed once, `O(1)` work each → **time `O(m·n)`**.
- **Space `O(m·n)`** for memo + up to `O(m+n)` recursion depth.

Possible optimizations (not needed, but noting): bottom-up table removes recursion-depth risk (Python default recursion limit can blow on long strings ~1000+); 1D rolling array cuts space to `O(min(m,n))`. If interviewer flags recursion depth, switch to iterative table. Current top-down is optimal in time and clearest to explain.