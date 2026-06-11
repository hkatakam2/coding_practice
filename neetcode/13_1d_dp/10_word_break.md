## question
Given a string s and a dictionary of strings wordDict, return true if s can be segmented into a space-separated sequence of dictionary words.
You are allowed to reuse words in the dictionary an unlimited number of times. You may assume all dictionary words are unique.

### 1. Restate

Given string `s` and list `wordDict`. Return `True` if `s` can be perfectly split into words found in `wordDict`. Words can be reused.

### 2. Clarify

* Inputs: Lowercase English letters only? (Assume yes).
* Can `s` be empty? (Assume no, length >= 1).
* Can `wordDict` be empty? (Assume no, but worth handling).
* Outputs: Boolean.

### 3. Hand-Trace

Input: `s = "catsandog"`, `wordDict = ["cats", "dog", "sand", "and", "cat"]`

* Prefix "cat" in dict. Remaining: "sandog".
* Prefix "sand" in dict. Remaining: "og".
* No prefix in dict for "og". Backtrack.




* Prefix "cats" in dict. Remaining: "andog".
* Prefix "and" in dict. Remaining: "og".
* No prefix in dict for "og". Backtrack.




* Exhausted all paths. Return `False`.

### 4. Brainstorm & Complexity

* **Brute Force (DFS/Recursion)**: Exactly like the hand-trace. Try prefix, recurse on suffix. Complexity: $O(2^n)$ worst case (e.g., `s = "aaaaab"`, dict = `["a", "aa"]`). Too slow. Space: $O(n)$ call stack.
* **BFS**: Treat indices as graph nodes. Edge from $i$ to $j$ if $s[i:j]$ is in dict. Queue stores indices to visit. Complexity: $O(n^3)$ with visited set.
* **Top-Down Memoization**: Brute force, but cache suffixes we've already checked. Complexity: $O(n^3)$ (n states, loop size n, slice takes n). Space: $O(n^2)$ for cache.
* **Bottom-Up DP**: `dp[i]` represents if $s[0:i]$ can be segmented. Complexity $O(n^3)$.

### 5. Suggest Solutions

Prefer **Top-Down Memoization**. It maps perfectly to human intuition (the hand-trace in step 3). It directly asks: "If I slice off a valid word, can I word-break the rest?" Caching the "rest" fixes the exponential time complexity trivially. Bottom-Up DP is also great, but Top-Down reads more naturally as English.

### 6. Outline

```python
def wordBreak(s: str, wordDict: list[str]) -> bool:
    """
    Reframe: Can string be split into a valid prefix and a recursively valid suffix?
    State: Cache of previously checked string suffixes, chosen because overlapping subproblems (many paths lead to same suffix).
    Invariant: If a suffix is in the cache, its breakability is absolutely known and never changes.

    can_segment(suffix) = recursively checks if the remaining string can be broken down.
    is_in_dict(word) = checks if a word exists in the dictionary.

    Core logic:
    - If string is empty, we successfully broke everything down. Return true.
    - Try splitting the string into two parts at every possible position.
    - If the first part is a valid word AND the second part can be segmented, return true.
    - If we try all splits and none work, return false.

    Edge cases:
    - Dictionary is empty.
    - String is impossible to break (characters not in dict).
    """

```

### 7. Iterative Implementation

**Iteration 1: Skeleton with stubs**

```python
def wordBreak(s: str, wordDict: list[str]) -> bool:
    word_set = set(wordDict) # fast lookup

    def can_segment(remaining_str):
        # TODO: Base case
        # TODO: Loop over splits
        pass

    return can_segment(s)

```

**Iteration 2: Core logic (Brute force)**

```python
def wordBreak(s: str, wordDict: list[str]) -> bool:
    word_set = set(wordDict) 

    def can_segment(remaining_str):
        # Base case: nothing left means success
        if not remaining_str:
            return True
        
        # Loop over every possible split point
        for i in range(1, len(remaining_str) + 1):
            prefix = remaining_str[:i]
            suffix = remaining_str[i:]
            
            # If prefix valid AND rest is valid
            if prefix in word_set and can_segment(suffix):
                return True
                
        return False

    return can_segment(s)

```

**Iteration 3: Add memoization (Happy Path Complete)**

```python
def wordBreak(s: str, wordDict: list[str]) -> bool:
    word_set = set(wordDict) 
    memo = {} # Added: cache

    def can_segment(remaining_str):
        # Added: check cache
        if remaining_str in memo:
            return memo[remaining_str]

        if not remaining_str:
            return True
        
        for i in range(1, len(remaining_str) + 1):
            prefix = remaining_str[:i]
            suffix = remaining_str[i:]
            
            if prefix in word_set and can_segment(suffix):
                memo[remaining_str] = True # Added: populate cache
                return True
                
        memo[remaining_str] = False # Added: populate cache
        return False

    return can_segment(s)

```

**Iteration 4: Edge Cases**

* *Edge case*: Empty dict? `set()` handles it, loop naturally fails.
* *Edge case*: Very long unmatchable string? Memoization handles the timeout risk. No code changes strictly required, but passing `memo` as an argument or using `@cache` is cleaner in Python. Code holds up against edge cases.

### 8. Complexity & Optimization

**Current Complexity**:

* **Time**: $O(n^3)$. $n$ states in memo, loop runs $n$ times, string slicing `remaining_str[:i]` takes $O(n)$.
* **Space**: $O(n^2)$ to store string suffixes in the hash map.

**Optimization**:
String slicing is expensive. Instead of passing new strings, pass the *start index*. This reduces space complexity to $O(n)$ and speeds up the slicing step by operating on the original string in place.

```python
def wordBreak(s: str, wordDict: list[str]) -> bool:
    word_set = set(wordDict)
    memo = {}
    
    def can_segment(start_index):
        if start_index == len(s):
            return True
            
        if start_index in memo:
            return memo[start_index]
            
        # Only iterate from start_index to end of string
        for end_index in range(start_index + 1, len(s) + 1):
            # Slicing still happens here, but cache keys are just integers now
            word = s[start_index:end_index] 
            
            if word in word_set and can_segment(end_index):
                memo[start_index] = True
                return True
                
        memo[start_index] = False
        return False
        
    return can_segment(0)

```

*Optimized Space*: $O(n)$ for call stack and memo keys. Slicing still makes Time $O(n^3)$ worst-case, but overhead is drastically reduced.