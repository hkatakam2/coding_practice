### question
You are given a string s consisting of lowercase english letters.
We want to split the string into as many substrings as possible, while ensuring that each letter appears in at most one substring.
Return a list of integers representing the size of these substrings in the order they appear in the string.

### 1. Restating

Problem: Cut string into maximum possible pieces. Rule: all copies of any letter must stay in exactly one piece. Return list of piece sizes.

### 2. Clarifying Questions

* **Input:** Only lowercase English letters? (Assume yes).
* **Edge cases:** Empty string? (Assume possible, return empty list). Single character string? (Return `[1]`).
* **Output:** Order matters? (Assume yes, from left to right as they appear).

### 3. Example by Hand

Input: `s = "abacdefeg"`

1. Trace last positions: `a`->2, `b`->1, `c`->3, `d`->4, `e`->7, `f`->6, `g`->8.
2. Start scan at index 0 (`a`). Must include index 2. Furthest requirement = 2.
3. Move to index 1 (`b`). Last `b` is 1. Doesn't extend furthest (still 2).
4. Move to index 2 (`a`). Reached furthest. Cut! Substring "aba". Size = 3.
5. Move to index 3 (`c`). Furthest = 3. Reached furthest. Cut! Substring "c". Size = 1.
6. Move to index 4 (`d`). Furthest = 4. Reached. Cut! "d". Size = 1.
7. Move to index 5 (`e`). Furthest = 7.
8. Move to index 6 (`f`). Furthest = max(7, 6) = 7.
9. Move to index 7 (`e`). Reached furthest. Cut! "efe". Size = 3.
10. Move to index 8 (`g`). Reached furthest. Cut! "g". Size = 1.
Result: `[3, 1, 1, 3, 1]`

### 4. Brainstorming & Complexity

* **Idea 1 (Naive):** Try all splits. Check left and right of split for shared chars. Very slow. O(N^2) or worse.
* **Idea 2 (Two-pass trace):** Do what we did by hand. We need to know the "farthest limit" of every character we encounter.
* Pass 1: Record last index of every char in a map/array.
* Pass 2: Walk string. Track `max_limit` of current piece. If `current_index == max_limit`, close piece.
* Complexity: Time O(N) (two linear passes). Space O(1) (only 26 letters max in map).



### 5. Suggest Solutions

Prefer Idea 2. Simple, mimics human intuition (the by-hand trace), straight forward tracking. No clever tricks, just maintaining an invariant boundary.

### 6. Outline

```python
def partitionLabels(s):
    """
    Reframe: A partition boundary safely closes only when no characters inside it appear later in the string.
    State: Hash map of last seen positions, chosen because it gives O(1) lookup to find a character's absolute limit.
    Invariant: Current partition must extend to at least the maximum last-seen position of any character currently within it.

    findLastOccurrences(string) = returns dictionary mapping each char to its final index.

    Core logic:
    - get last occurrences for all characters
    - initialize empty list for results
    - initialize trackers for current partition start and end boundaries
    - iterate through characters one by one
    - update partition end boundary if current character appears later
    - if current position matches partition end boundary, we can safely cut
    - record partition size using start and end, then move start to next character

    Edge cases:
    - string is empty -> return empty list
    """

```

### 7. Iterative Implementation

**Iteration 1: Skeleton with plain English flow**

```python
def partitionLabels(s):
    # helpers
    last_occurrences = findLastOccurrences(s)
    
    # state
    results = []
    partition_start = 0
    partition_end = 0
    
    # core logic
    for each character in s:
        # update furthest boundary needed for current character
        # if current position matches furthest boundary:
            # calculate size and append to results
            # reset partition_start for the next piece
            
    return results

```

**Iteration 2: Translating core logic to code**

```python
def partitionLabels(s):
    # TO DO: implement findLastOccurrences
    last_occurrences = findLastOccurrences(s)
    
    results = []
    partition_start = 0
    partition_end = 0
    
    # changed: actual loop syntax and variable names
    for current_index, char in enumerate(s):
        # changed: tracking max boundary using helper map
        partition_end = max(partition_end, last_occurrences[char])
        
        # changed: cut condition met
        if current_index == partition_end:
            size = partition_end - partition_start + 1
            results.append(size)
            partition_start = current_index + 1
            
    return results

```

**Iteration 3: Fleshing out the helper function**

```python
def partitionLabels(s):
    # changed: fully inline the helper for simplicity. 
    # Dictionary comprehension gets last index cleanly.
    last_occurrences = {char: idx for idx, char in enumerate(s)}
    
    results = []
    partition_start = 0
    partition_end = 0
    
    for current_index, char in enumerate(s):
        partition_end = max(partition_end, last_occurrences[char])
        
        if current_index == partition_end:
            size = partition_end - partition_start + 1
            results.append(size)
            partition_start = current_index + 1
            
    return results

```

**Iteration 4: Edge cases patching**
Reviewing Step 6 edge cases. Empty string breaks logic? `enumerate("")` skips loop entirely. Returns `[]`. Correct. But to be explicitly safe and avoid unnecessary dictionary creation, handle at the top.

```python
def partitionLabels(s):
    # edge case: empty string
    if not s:
        return []

    last_occurrences = {char: idx for idx, char in enumerate(s)}
    
    results = []
    partition_start = 0
    partition_end = 0
    
    for current_index, char in enumerate(s):
        partition_end = max(partition_end, last_occurrences[char])
        
        if current_index == partition_end:
            size = partition_end - partition_start + 1
            results.append(size)
            partition_start = current_index + 1
            
    return results

```

### 8. Complexity & Optimization

* **Time Complexity:** O(N). First pass (dict comprehension) touches every char once. Second pass touches every char once. `max()` is O(1). Total time is strictly linear.
* **Space Complexity:** O(1). `last_occurrences` map stores at most 26 key-value pairs because input is constrained to lowercase English letters.
* **Optimization:** Logic is perfectly optimal. No expensive sections. Instead of a hash map, could use a fixed-size array of length 26 (`ord(char) - ord('a')`), but dictionary overhead in Python is negligible here and code readability is vastly superior. No change needed.