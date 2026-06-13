## question
You are given two strings `s` and `t`, both consisting of english letters.
Return the number of distinct subsequences of `s` which are equal to `t`.

### 1. Restating the Question

Given two strings `s` and `t`. Find total distinct ways to form `t` by deleting characters from `s`. Order must remain unchanged.

### 2. Clarifying Questions

* **Case sensitivity?** Assume sensitive.
* **Empty inputs?** If `t` is empty, answer is 1 (delete all of `s`). If `s` is empty and `t` isn't, answer is 0.
* **Scale?** If `s` and `t` are large, answer might overflow 32-bit integer. Assume environment handles large ints (like Python).

### 3. Hand-Tracing Example

Input: `s` = "caat", `t` = "cat"
Output: 2

Trace by hand:

* Match 'c' in both. `s` remaining: "aat", `t` remaining: "at".
* Look at first 'a' in `s`. Matches 'a' in `t`.
* Path 1: Use it. `s` remaining: "at", `t` remaining: "t". Next match 't'. Found "cat". (Count = 1)
* Path 2: Skip it. `s` remaining: "at", `t` remaining: "at". Next 'a' matches. Then 't' matches. Found "cat". (Count = 2)



### 4. Brainstorming & Complexity

* **Brute Force (DFS):** Try matching each char. If match, branch into two paths: "include char" or "exclude char". If mismatch, "exclude char".
* *Time:* $O(2^{|s|})$ worst case. Too slow.


* **Memoization (Top-Down DP):** DFS visits same `(s_index, t_index)` states repeatedly. Cache results.
* *Time:* $O(|s| \times |t|)$. *Space:* $O(|s| \times |t|)$ for cache and recursion stack.


* **Tabulation (Bottom-Up DP):** Build 2D matrix. `dp[i][j]` = ways to form `t[:j]` from `s[:i]`.
* *Time:* $O(|s| \times |t|)$. *Space:* $O(|s| \times |t|)$.



### 5. Suggesting Solutions

Prefer Top-Down Memoization. It directly mirrors the logical by-hand breakdown (Step 3). Simple to write, easy to explain. Tabulation is fine but indices can get confusing to explain upfront. We will implement Memoization.

### 6. Outline & Core Logic

```python
def numDistinct(s: str, t: str) -> int:
    """
    Reframe: Count successful paths through 's' that construct 't'.
    State: Cache mapping (s_index, t_index) to successful path counts, chosen because 
           overlapping subproblems occur when skipping different characters leads to same suffixes.
    Invariant: For any (s_index, t_index), function returns total valid subsequences of t[t_index:] in s[s_index:].

    count_ways(s_index, t_index) = counts ways to match remaining t in remaining s.

    Core logic:
    - Check if current character in s matches current character in t.
    - If match: we have two choices. 
        1. Use character (advance both indices) 
        2. Skip character (advance only s index to find another match later). 
        Add ways from both choices.
    - If mismatch: we have one choice.
        1. Skip character (advance only s index).

    Edge cases:
    - Target t is fully matched: returning 1 (found a valid subsequence).
    - Source s is fully exhausted, but t is not: returning 0 (failed to form t).
    """
    pass

```

### 7. Iterative Implementation

**Iteration 1: Skeleton & Core Logic (Happy Path)**
Translating plain English into structural code. No edge cases or caching yet.

```python
def numDistinct(s: str, t: str) -> int:
    
    def count_ways(s_idx, t_idx):
        # TODO: Add base cases
        
        # If characters match, branch: use it OR skip it
        if s[s_idx] == t[t_idx]:
            use_char = count_ways(s_idx + 1, t_idx + 1)
            skip_char = count_ways(s_idx + 1, t_idx)
            return use_char + skip_char
            
        # If characters mismatch, only option: skip it
        else:
            skip_char = count_ways(s_idx + 1, t_idx)
            return skip_char

    return count_ways(0, 0)

```

**Iteration 2: Adding Edge Cases**
Patching the base cases from Step 6. Code will now logically terminate, but still slow.

```python
def numDistinct(s: str, t: str) -> int:
    
    def count_ways(s_idx, t_idx):
        # Edge Case 1: Target t fully matched. Success.
        if t_idx == len(t):
            return 1
            
        # Edge Case 2: Source s exhausted before t. Failure.
        if s_idx == len(s):
            return 0
        
        if s[s_idx] == t[t_idx]:
            use_char = count_ways(s_idx + 1, t_idx + 1)
            skip_char = count_ways(s_idx + 1, t_idx)
            return use_char + skip_char
        else:
            skip_char = count_ways(s_idx + 1, t_idx)
            return skip_char

    return count_ways(0, 0)

```

**Iteration 3: Full Realization (Adding Memoization)**
Adding cache to fix $O(2^N)$ time complexity.

```python
def numDistinct(s: str, t: str) -> int:
    cache = {} # Map (s_idx, t_idx) -> count
    
    def count_ways(s_idx, t_idx):
        if t_idx == len(t):
            return 1
        if s_idx == len(s):
            return 0
            
        # Check cache
        if (s_idx, t_idx) in cache:
            return cache[(s_idx, t_idx)]
        
        if s[s_idx] == t[t_idx]:
            cache[(s_idx, t_idx)] = count_ways(s_idx + 1, t_idx + 1) + count_ways(s_idx + 1, t_idx)
        else:
            cache[(s_idx, t_idx)] = count_ways(s_idx + 1, t_idx)
            
        return cache[(s_idx, t_idx)]

    return count_ways(0, 0)

```

### 8. Complexity & Optimizations

* **Current Time:** $O(|s| \times |t|)$ due to cached states.
* **Current Space:** $O(|s| \times |t|)$ for cache dictionary and recursion depth.

**Optimization Note:**
Recursion stack takes memory. Can optimize to $O(|t|)$ space using 1D Bottom-Up DP.
Since current state only depends on the previous row (or previous character in `s`), we only need a 1D array of size $|t| + 1$.

*Brief 1D DP Implementation (for completeness):*

```python
def numDistinct_optimized(s: str, t: str) -> int:
    # dp[j] stores ways to form t[:j]
    dp = [0] * (len(t) + 1)
    dp[0] = 1 # Empty string matches 1 way
    
    for i in range(len(s)):
        # Traverse backwards to prevent using same character twice
        for j in range(len(t) - 1, -1, -1):
            if s[i] == t[j]:
                # Add ways without this char to ways with it
                dp[j + 1] += dp[j]
                
    return dp[len(t)]

```

Time remains $O(|s| \times |t|)$. Space drops to $O(|t|)$.