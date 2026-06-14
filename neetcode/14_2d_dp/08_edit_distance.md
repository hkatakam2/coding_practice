## question
You are given two strings word1 and word2, each consisting of lowercase English letters.
You are allowed to perform three operations on word1 an unlimited number of times:

Insert a character at any position
Delete a character at any position
Replace a character at any position
Return the minimum number of operations to make word1 equal word2.

### 1. Restating the Question

Given string `word1` and string `word2`. Convert `word1` to `word2`.
Allowed operations (cost = 1 each): Insert char, Delete char, Replace char.
Find absolute minimum operations required.

### 2. Clarifying Questions & Confirmations

* **Inputs:** Two strings. Lowercase English letters only? *Assume yes.*
* **Empty strings:** Can `word1` or `word2` be empty? *Assume yes.*
* **Output:** Integer representing minimum operation count.
* **In-place modification:** Do we need to return the actual string? *No, just the count.*

### 3. Example by Hand

`word1` = "horse", `word2` = "ros"

* Compare 'h' and 'r'. Mismatch. Best path: replace 'h' with 'r'. (Cost: 1, `word1` effectively "rorse").
* Compare 'o' and 'o'. Match. (Cost: 0).
* Compare 'r' and 's'. Mismatch. Best path: delete 'r'. (Cost: 1, `word1` effectively "rose").
* Compare 's' and 's'. Match. (Cost: 0).
* Compare 'e' and end of word. Mismatch. Best path: delete 'e'. (Cost: 1).
* Total cost = 3.

### 4. Brainstorming & Complexity

* **Brute Force (Recursion):** Compare char by char from left to right. If match, move to next. If mismatch, branch into 3 parallel universes (try insert, try delete, try replace). Find min of branches.
* *Time Complexity:* $O(3^{\max(M, N)})$ where $M, N$ are string lengths. Terrible.
* *Space Complexity:* $O(\max(M, N))$ for call stack.


* **Top-Down Dynamic Programming (Memoization):** Same recursion, but we see overlapping subproblems (e.g., deleting then inserting reaches the same string state as replacing). Cache results based on index pair `(i, j)`.
* *Time Complexity:* $O(M \times N)$ - every index pair computed once.
* *Space Complexity:* $O(M \times N)$ for cache + recursion stack.


* **Bottom-Up DP (Tabulation):** 2D grid of size $(M+1) \times (N+1)$. Fill iteratively.
* *Time Complexity:* $O(M \times N)$.
* *Space Complexity:* $O(M \times N)$.



### 5. Suggested Solutions

1. **Recursive Memoization:** Models the "by hand" branching directly. Simple to read, clear logical flow.
2. **Bottom-Up 2D DP:** Standard iterative approach. Avoids recursion overhead.
*Decision:* Proceed with Recursive Memoization for maximum clarity, matching the step 3 logic perfectly. We'll optimize space later.

### 6. Outline

```python
def minDistance(word1: str, word2: str) -> int:
    """
    Reframe: Find shortest path of edits by comparing character pairs left-to-right.
    State: Memo dictionary caching min operations for index pair (index1, index2), chosen because it eliminates evaluating identical substring pairs multiple times.
    Invariant: The minimum operations required for the remaining substrings are optimal and independent of previous edits.

    compute_cost(index1, index2) = returns edit distance for substrings starting at index1 and index2.

    Core logic:
    - check if current characters match.
    - if they match, cost is just the cost of the remaining substrings.
    - if they mismatch, simulate inserting, deleting, and replacing.
    - cost is 1 plus the minimum cost among those three simulated paths.
    - cache the result for the current indices.
    - return cached result.
    
    Edge cases:
    - index1 reaches end of word1 (must insert all remaining word2 chars).
    - index2 reaches end of word2 (must delete all remaining word1 chars).
    """

```

### 7. Iterative Implementation

**Iteration 1: Skeleton code**

```python
def minDistance(word1: str, word2: str) -> int:
    # TODO: add memoization dictionary
    
    def compute_cost(i, j):
        # TODO: handle edge cases (end of strings)
        
        # TODO: compare characters and branch
        pass
        
    return compute_cost(0, 0)

```

**Iteration 2: Core logic (Happy Path)**
Translating plain English to code. Ignoring bounds/edge cases temporarily.

```python
def minDistance(word1: str, word2: str) -> int:
    
    def compute_cost(i, j):
        # If chars match, advance both pointers (no cost added)
        if word1[i] == word2[j]:
            return compute_cost(i + 1, j + 1)
        
        # Mismatch: try all 3 operations
        # Insert: move word2 pointer (imagine char inserted into word1 to match word2[j])
        insert_cost = compute_cost(i, j + 1)
        
        # Delete: move word1 pointer (skip char in word1)
        delete_cost = compute_cost(i + 1, j)
        
        # Replace: move both pointers (force match)
        replace_cost = compute_cost(i + 1, j + 1)
        
        # Return 1 (the current operation) + best path forward
        return 1 + min(insert_cost, delete_cost, replace_cost)
        
    return compute_cost(0, 0)

```

**Iteration 3: Patching Edge Cases**
Adding bounds checking. If `i` or `j` exceed string lengths, the happy path crashes.

```python
def minDistance(word1: str, word2: str) -> int:
    
    def compute_cost(i, j):
        # EDGE CASE: word1 exhausted. Must insert remaining word2 chars.
        if i == len(word1):
            return len(word2) - j
            
        # EDGE CASE: word2 exhausted. Must delete remaining word1 chars.
        if j == len(word2):
            return len(word1) - i
            
        if word1[i] == word2[j]:
            return compute_cost(i + 1, j + 1)
        
        insert_cost = compute_cost(i, j + 1)
        delete_cost = compute_cost(i + 1, j)
        replace_cost = compute_cost(i + 1, j + 1)
        
        return 1 + min(insert_cost, delete_cost, replace_cost)
        
    return compute_cost(0, 0)

```

**Iteration 4: Adding Memoization**
Code is correct but slow. Patching in the cache to achieve $O(M \times N)$ time.

```python
def minDistance(word1: str, word2: str) -> int:
    memo = {} # Added cache
    
    def compute_cost(i, j):
        if i == len(word1): return len(word2) - j
        if j == len(word2): return len(word1) - i
        
        # Check cache
        if (i, j) in memo:
            return memo[(i, j)]
            
        if word1[i] == word2[j]:
            ans = compute_cost(i + 1, j + 1)
        else:
            insert_cost = compute_cost(i, j + 1)
            delete_cost = compute_cost(i + 1, j)
            replace_cost = compute_cost(i + 1, j + 1)
            ans = 1 + min(insert_cost, delete_cost, replace_cost)
            
        # Write to cache
        memo[(i, j)] = ans
        return ans
        
    return compute_cost(0, 0)

```

### 8. Complexity & Optimizations

**Current Complexity:**

* **Time:** $O(M \times N)$. Each pair evaluated once.
* **Space:** $O(M \times N)$. Dictionary stores states, plus recursion depth $O(M+N)$.

**Optimization Target:** Space complexity. Using a 2D Bottom-Up approach still uses $O(M \times N)$ space. However, notice that computing any cell in a DP grid only requires the *current row* and the *previous row*.

We can optimize space to $O(N)$ by keeping only two arrays of size $N$ in memory.

**Optimized Code (1D Bottom-Up DP):**

```python
def minDistance(word1: str, word2: str) -> int:
    m, n = len(word1), len(word2)
    
    # prev_row represents distances from empty word1 prefix
    prev_row = list(range(n + 1))
    
    for i in range(1, m + 1):
        # curr_row starts with cost of deleting all characters up to i
        curr_row = [i] + [0] * n
        
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                curr_row[j] = prev_row[j - 1]
            else:
                curr_row[j] = 1 + min(
                    curr_row[j - 1],   # Insert
                    prev_row[j],       # Delete
                    prev_row[j - 1]    # Replace
                )
        prev_row = curr_row
        
    return prev_row[n]

```

* *Time:* $O(M \times N)$
* *Space:* $O(N)$