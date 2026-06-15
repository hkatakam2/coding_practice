## question
Given an integer array nums, return true if any value appears more than once in the array, otherwise return false.

### 1. Restate

Goal: Find duplicates in an array. Return `True` if any number repeats. Return `False` if all numbers are strictly unique.

### 2. Clarifying Questions

* **Inputs:** Array of integers (`nums`). Can contain negatives? (Assume yes).
* **Outputs:** Boolean (`True` or `False`).
* **Edge states:** Empty array? (Assume returns `False`). Single element array? (Assume returns `False`). Huge array? (Need to watch time complexity).

### 3. By Hand Example

Input: `[1, 2, 3, 1]`

* Read 1. Have I seen 1? No. Remember 1.
* Read 2. Have I seen 2? No. Remember 1, 2.
* Read 3. Have I seen 3? No. Remember 1, 2, 3.
* Read 1. Have I seen 1? Yes. -> **Return True**.

### 4. Brainstorming & Complexity

* **Approach A (Brute Force):** Nested loop. Compare every number to every other number. Time: **O(N^2)**. Space: **O(1)**. Too slow for large inputs.
* **Approach B (Sorting):** Sort array first. Duplicates will be adjacent. Loop once checking `nums[i] == nums[i+1]`. Time: **O(N log N)**. Space: **O(1)** (if in-place sort). Better, but modifies input.
* **Approach C (Hash Set):** Track "seen" numbers as we read. Exact match to step 3 manual logic. Time: **O(N)**. Space: **O(N)**. Fast, requires extra memory.

### 5. Suggest Solutions

Suggest **Approach C (Hash Set)**. It's the simplest, clearest, and directly maps to the manual "by hand" translation in step 3. Trades a bit of memory for an optimal linear time complexity. Highly readable.

### 6. Implementation Outline

```python
def contains_duplicate(nums): 
    """
    Reframe: Check if any item exists in our historical 'seen' record.
    State: Hash set `seen`, chosen because O(1) average lookup time.
    Invariant: Set always contains strictly unique numbers processed so far.

    has_been_seen(num, set) = checks if num exists in the set.
    add_to_seen(num, set) = adds num to the set.

    Core logic:
    - Iterate through each number in the array.
    - If has_been_seen(num, seen), we found a duplicate, return True.
    - Otherwise, add_to_seen(num, seen).
    - If iteration finishes without returning True, return False.

    Edge cases:
    - Array is empty (returns False, loop never runs).
    - Array has 1 element (returns False, loop finishes cleanly).
    """

```

### 7. Iterative Implementation

**Iteration 1: Skeleton Structure**

```python
def contains_duplicate(nums):
    # init seen record
    # loop over nums
        # if seen, return True
        # else store in seen
    # return False

```

**Iteration 2: Adding Helpers (Translating Plain English)**

```python
def contains_duplicate(nums):
    seen = set() # init seen record
    for num in nums: # loop over nums
        if has_been_seen(num, seen): 
            return True
        add_to_seen(num, seen)
    return False

```

**Iteration 3: Fleshing Out Helpers (Final Core Logic)**

```python
def contains_duplicate(nums):
    seen = set()
    for num in nums:
        # Replaced has_been_seen with native Python 'in' operator
        if num in seen: 
            return True
        # Replaced add_to_seen with native set.add()
        seen.add(num)
    return False

```

**Edge Case Check:** * Empty array `[]`: For-loop skips. Hits `return False`. Correct.

* Single element `[1]`: Loop runs once. Adds `1` to set. Finishes. Hits `return False`. Correct.
* No patches needed. Core logic naturally handles edges.

### 8. Complexity & Optimization

* **Time Complexity:** **O(N)**. Loop runs N times. Set lookup is **O(1)** on average.
* **Space Complexity:** **O(N)**. In worst case (no duplicates), set stores all N elements.

**Alternative Pythonic Optimization:**
A common "clever" optimization in Python is `return len(set(nums)) != len(nums)`.

* *Pros:* One line, executes in fast C-backend.
* *Cons:* Always iterates entire array to build the set first, meaning no "early exit" (short-circuiting). If duplicate is at the 2nd index of a 1-million item array, the loop method finds it instantly; the `len(set())` method processes all 1-million items first.
* *Verdict:* Keep the loop method for interviews to demonstrate early exit logic and control flow, though mentioning the one-liner shows language fluency.