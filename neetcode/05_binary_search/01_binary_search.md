### question
You are given an array of distinct integers nums, sorted in ascending order, and an integer target.

Implement a function to search for target within nums. If it exists, then return its index, otherwise, return -1.

### 1. Restate

Find index of `target` in sorted array `nums` of unique integers. Return -1 if absent.

### 2. Clarifying Questions & I/O

* **Input**: `nums` (Array of ints, sorted, distinct), `target` (int).
* **Output**: `int` (Index or -1).
* **Constraints/Questions**: Can `nums` be empty? (Assume yes). Do numbers fit in standard memory? (Assume yes).

### 3. Example by Hand

* `nums = [0, 2, 4, 6, 8]`, `target = 6`
* Middle is 4. `6 > 4`. Look right.
* Right half is `[6, 8]`. Middle is 6. Matches `target`.
* Found at index 3.

### 4. Brainstorming & Complexity

* **Linear Scan**: Check each item left to right. Time: $O(N)$. Space: $O(1)$.
* **Binary Search**: Exploit sorted nature. Pick middle. If target is larger, discard left half. Repeat. Time: $O(\log N)$. Space: $O(1)$.

### 5. Suggest Solutions

* **Solution A**: Linear scan. Simple, slow.
* **Solution B**: Binary Search (the by-hand method). Fast, straightforward logical elimination. We will implement Solution B.

### 6. Outline

```python
def search(nums, target):
    """
    Reframe: Exploit sorted property to eliminate half the search space per step.
    State: left and right boundary pointers, chosen because they track the active search window.
    Invariant: If target exists, it is strictly between left and right boundaries inclusive.

    get_mid(left, right) = finds the center item of the active window.
    check_target(mid_val) = compares mid value to target.

    Core logic:
    - while search window is valid:
        - get_mid of window
        - if check_target is exact match, return mid index
        - if check_target is smaller, shrink window to right half
        - if check_target is larger, shrink window to left half
    - if window closes empty, return not found

    Edge cases:
    - empty array
    - target smaller than smallest element
    - target larger than largest element
    - array of size 1
    """

```

### 7. Iterative Implementation

**Iteration 1: Skeleton**

```python
def search(nums, target):
    # init left and right boundaries
    # loop while window valid
        # get mid
        # check mid vs target
            # return if match
            # adjust left boundary if mid too small
            # adjust right boundary if mid too big
    # return not found
    return -1

```

**Iteration 2: Core Logic Chunking**

```python
def search(nums, target):
    left = 0                           # added: init left
    right = len(nums) - 1              # added: init right
    
    while left <= right:               # added: valid window loop
        mid = (left + right) // 2      # added: get mid
        mid_val = nums[mid]
        
        if mid_val == target:          # added: match check
            return mid
        elif mid_val < target:         # added: target is strictly to the right
            left = mid + 1
        else:                          # added: target is strictly to the left
            right = mid - 1
            
    return -1

```

**Iteration 3: Walk Edge Cases**

* *Empty array*: `right` becomes `-1`. `0 <= -1` is False. Loop skips. Returns `-1`. (Safe).
* *Target smaller than all*: `right` shrinks until `< left`. Loop exits. Returns `-1`. (Safe).
* *Target larger than all*: `left` grows until `> right`. Loop exits. Returns `-1`. (Safe).
* *Size 1*: `left=0`, `right=0`. `mid=0`. Matches or adjusts pointers and exits. (Safe).

### 8. Complexity & Optimization

* **Time Complexity**: $O(\log N)$. Search space halves each iteration.
* **Space Complexity**: $O(1)$. Only pointer variables used.
* **Optimization**: In Python, integers have arbitrary precision so `(left + right)` won't overflow. In strict-typed languages (Java/C++), `left + right` can overflow max integer limits.
* **Patch**: Compute `mid` safely.

**Final Polished Code:**

```python
def search(nums, target):
    left = 0
    right = len(nums) - 1
    
    while left <= right:
        # safe mid calculation to prevent integer overflow
        mid = left + (right - left) // 2 
        mid_val = nums[mid]
        
        if mid_val == target:
            return mid
        elif mid_val < target:
            left = mid + 1
        else:
            right = mid - 1
            
    return -1

```