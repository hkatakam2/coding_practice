### question
You are given an array of length n which was originally sorted in ascending order. It has now been rotated between 1 and n times. For example, the array nums = [1,2,3,4,5,6] might become:

[3,4,5,6,1,2] if it was rotated 4 times.
[1,2,3,4,5,6] if it was rotated 6 times.
Given the rotated sorted array nums and an integer target, return the index of target within nums, or -1 if it is not present.

You may assume all elements in the sorted rotated array nums are unique,

### 1. Restating the Question

Given an array of unique integers initially sorted in ascending order but rotated an unknown number of times. Given a `target` integer. Find the index of `target` in the array. Return `-1` if not found.

### 2. Clarifying Questions & Confirming Inputs/Outputs

* **Input:** `nums` (array of integers), `target` (integer).
* **Output:** Integer (index or `-1`).
* **Constraints:** Can `nums` be empty? (Assume yes, lengths 0 to n). Are there duplicates? (Prompt says no, all unique). Will it fit in memory? (Assume yes).

### 3. Manual Trace

**Input:** `nums = [4, 5, 6, 7, 0, 1, 2]`, `target = 0`

* Look at middle: `7`. Not `0`.
* Left half `[4, 5, 6, 7]` is strictly sorted. Right half `[0, 1, 2]` contains the rotation pivot.
* Is `0` between `4` and `7`? No. So it must be in the right half.
* New search space: `[0, 1, 2]`. Middle is `1`. Not `0`.
* Left half `[0, 1]` is sorted. Is `0` between `0` and `1`? Yes.
* New space: `[0]`. Middle is `0`. Found it.
**Output:** `4` (index of `0`).

### 4. Brainstorming & Complexity

* **Approach 1: Linear Scan.** Iterate through `nums`, check each element.
* *Time Complexity:* $O(n)$.
* *Space Complexity:* $O(1)$.


* **Approach 2: Binary Search.** Array is mostly sorted. Binary search splits array in half. One half will *always* be perfectly sorted. We can use the sorted half to determine if the target is inside it.
* *Time Complexity:* $O(\log n)$.
* *Space Complexity:* $O(1)$.



### 5. Suggested Solutions

1. **Linear Scan:** Simple, straightforward $O(n)$ loop. Good fallback.
2. **Modified Binary Search:** Optimal $O(\log n)$ approach. Mimics the manual trace above.

We will proceed with the Modified Binary Search as it exploits the partially sorted nature of the input.

### 6. Outline & Core Logic

```python
def search(nums, target):
    """
    Reframe: At least one half of any divided rotated-array is strictly sorted.
    State: left and right bounds, chosen because binary search requires bounding the active search space.
    Invariant: The target, if it exists, is always located between the left and right bounds.

    is_left_half_sorted() = checks if elements from left to mid are strictly ascending.
    is_target_in_left_half() = checks if target lies between the values at the left bound and mid bound.
    is_target_in_right_half() = checks if target lies between the values at the mid bound and right bound.

    Core logic:
    - Loop while search space is valid.
    - Find middle element.
    - If middle is target, return its index.
    - Check if left half is sorted.
        - If yes: check if target is inside left half.
            - If yes, narrow search to left half.
            - If no, narrow search to right half.
        - If no (meaning right half is sorted): check if target is inside right half.
            - If yes, narrow search to right half.
            - If no, narrow search to left half.
    
    Edge cases:
    - Empty array.
    - Array of length 1.
    """
    pass

```

### 7. Iterative Implementation

**Iteration 1: Outline with Stubs**
Translating the plain English logic directly into a structural skeleton.

```python
def search(nums, target):
    left = 0
    right = len(nums) - 1

    while left <= right:
        mid = (left + right) // 2
        
        if nums[mid] == target:
            return mid
            
        # Helper: is_left_half_sorted
        if nums[left] <= nums[mid]:
            # Left half is sorted
            # Helper: is_target_in_left_half
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:
            # Right half is sorted
            # Helper: is_target_in_right_half
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1
                
    return -1

```

**Iteration 2: Resolving Logic & Edge Cases**
The core logic in Iteration 1 is fully realized and robust. Let's walk the edge cases to see if they break it.

* *Edge Case 1: Empty Array.* If `nums = []`, `len(nums) - 1` is `-1`. `left (0) <= right (-1)` is False. Loop skips. Returns `-1`. Safe.
* *Edge Case 2: Array of length 1.* `nums = [5], target = 5`. `left=0`, `right=0`, `mid=0`. Returns `0`. Safe.
* *Edge Case 3: Target not found.* Loop exhausts when `left > right`. Returns `-1`. Safe.

**Final Code (Polished):**

```python
def search(nums: list[int], target: int) -> int:
    left, right = 0, len(nums) - 1

    while left <= right:
        mid = left + (right - left) // 2 # Optimization: prevents integer overflow
        
        if nums[mid] == target:
            return mid
            
        # Check if left half is the sorted half
        if nums[left] <= nums[mid]:
            # Target is mathematically inside the sorted left half
            if nums[left] <= target < nums[mid]:
                right = mid - 1 # Search left
            else:
                left = mid + 1  # Search right
                
        # Otherwise, right half must be the sorted half
        else:
            # Target is mathematically inside the sorted right half
            if nums[mid] < target <= nums[right]:
                left = mid + 1  # Search right
            else:
                right = mid - 1 # Search left
                
    return -1

```

### 8. Complexity & Optimizations

* **Time Complexity:** $O(\log n)$. We halve the search space on every iteration.
* **Space Complexity:** $O(1)$. We only store pointers (`left`, `right`, `mid`), allocating no additional structures.
* **Optimization included:** `mid = left + (right - left) // 2`. In Python, integers have arbitrary precision, so `(left + right) // 2` won't overflow. However, calculating `mid` this way is a standard best practice borrowed from C/Java to prevent integer overflow when adding two massive indices. Kept for interview rigor.