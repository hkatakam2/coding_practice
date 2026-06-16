### question
Given an array of integers `nums`, return the length of the longest consecutive sequence of elements that can be formed.
A consecutive sequence is a sequence of elements in which each element is exactly `1` greater than the previous element. The elements do not have to be consecutive in the original array.
You must write an algorithm that runs in `O(n)` time.

### 1. Restating the Question

Given unordered array `nums`. Find length of longest sequence of numbers that increase by exactly 1. Must run in $O(n)$ time. Elements don't need to be adjacent in input.

### 2. Clarifying Questions & Confirming I/O

* **Input:** `[100, 4, 200, 1, 3, 2]`
* **Output:** `4` (Sequence: 1, 2, 3, 4)
* **Q:** Can array be empty? **A:** Yes. Output `0`.
* **Q:** Are there duplicates? **A:** Yes. Sequence length counts unique values only.
* **Q:** Negative numbers? **A:** Yes.

### 3. Manual Trace (Example Input)

Input: `[100, 4, 200, 1, 3, 2]`

1. Look for a starting point. 1 looks like a start.
2. Does 2 exist? Yes. 3? Yes. 4? Yes. 5? No. Sequence from 1 has length 4.
3. Look at 100. Start? Yes. 101? No. Length 1.
4. Look at 200. Start? Yes. 201? No. Length 1.
5. Look at 4. Start? No, 3 exists. Skip.
Max length found is 4.

### 4. Brainstorming & Complexity

* **Approach 1: Sorting.** Sort array. Iterate and count adjacent increasing elements. Time: $O(n \log n)$. Space: $O(1)$ or $O(n)$ depending on sort. Fails $O(n)$ constraint.
* **Approach 2: Brute Force Set Lookup.** Put all in a hash set. For each number, check if num+1, num+2... exists. Time: $O(n^2)$ worst case (e.g., already sorted array).
* **Approach 3: Optimized Set Lookup.** (Matches manual trace). Put in hash set. Only build sequence if number is a "start" (i.e., `num - 1` is not in set). If it's a start, count upwards. Time: $O(n)$. Space: $O(n)$.

### 5. Suggest Solutions

Prefer simple over clever.

1. **Sorting:** Easy to explain, but violates time constraint.
2. **Optimized Set Lookup (Selected):** Directly translates the manual trace. Find sequence starts, count up. Very readable, meets constraints.

### 6. Outline Selected Implementation

```python
def longestConsecutive(nums):
    """
    Reframe: Only build sequences from their true start to avoid redundant work.
    State: Hash Set, chosen because $O(1)$ lookups allow checking neighbors instantly.
    Invariant: Each number is visited exactly once inside the inner sequence-building loop across the entire run.

    is_sequence_start(num, num_set) = returns True if num - 1 is not in set.
    count_consecutive(num, num_set) = returns length of consecutive streak starting at num.

    Core logic:
    - Convert array to hash set to remove duplicates and enable fast lookup.
    - Initialize max sequence length to 0.
    - Iterate through each number in the set.
    - If the number is a sequence start:
        - Count consecutive sequence length starting from this number.
        - Update max sequence length if current length is larger.
    - Return max sequence length.

    Edge cases:
    - Empty input array: should return 0 directly to save time.
    """
    pass

```

### 7. Iterative Implementation

**Iteration 1: Skeleton with stubs**

```python
def longestConsecutive(nums):
    num_set = set(nums)
    max_len = 0
    
    for num in num_set:
        # TODO: check if num is start
        # TODO: if start, find length and update max_len
        pass
        
    return max_len

```

**Iteration 2: Implementing the `is_sequence_start` logic inline**

```python
def longestConsecutive(nums):
    num_set = set(nums)
    max_len = 0
    
    for num in num_set:
        # ADDED: check if start (left neighbor missing)
        if (num - 1) not in num_set:
            # TODO: find length and update max_len
            pass
            
    return max_len

```

**Iteration 3: Implementing the `count_consecutive` logic**

```python
def longestConsecutive(nums):
    num_set = set(nums)
    max_len = 0
    
    for num in num_set:
        if (num - 1) not in num_set:
            # ADDED: loop to count consecutive numbers
            current_num = num
            current_len = 1
            
            while (current_num + 1) in num_set:
                current_num += 1
                current_len += 1
                
            # ADDED: update max
            max_len = max(max_len, current_len)
            
    return max_len

```

**Iteration 4: Edge cases**
Reviewing Step 6 edge cases. Empty array.
If `nums` is `[]`, `num_set` is empty, loop skips, returns `0`. Core logic actually handles it gracefully. But explicitly checking early saves a set allocation.

```python
def longestConsecutive(nums):
    # ADDED: Early exit for empty array (Edge case patched)
    if not nums:
        return 0
        
    num_set = set(nums)
    max_len = 0
    
    for num in num_set:
        if (num - 1) not in num_set:
            current_num = num
            current_len = 1
            
            while (current_num + 1) in num_set:
                current_num += 1
                current_len += 1
                
            max_len = max(max_len, current_len)
            
    return max_len

```

### 8. Complexity & Optimizations

* **Time Complexity:** $O(n)$. Creating the set takes $O(n)$. In the main loop, we iterate through the set $O(n)$. The inner `while` loop only triggers on sequence starts and only visits each sequence element once. Total time is strictly $O(n)$.
* **Space Complexity:** $O(n)$ to store elements in the hash set.
* **Optimization Comment:** No major algorithmic optimization needed as we hit the theoretical lower bound. Micro-optimizations could include checking if `max_len > len(nums) / 2` to early exit (if we found a sequence larger than half the array, it's mathematically impossible to find a longer one), but this complicates code for minimal real-world gain. Keep it clean.