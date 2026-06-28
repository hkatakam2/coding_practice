### question
You are given an array of length n which was originally sorted in ascending order. It has now been rotated between 1 and n times. For example, the array nums = [1,2,3,4,5,6] might become:

[3,4,5,6,1,2] if it was rotated 4 times.
[1,2,3,4,5,6] if it was rotated 6 times.
Notice that rotating the array 4 times moves the last four elements of the array to the beginning. Rotating the array 6 times produces the original array.

Assuming all elements in the rotated sorted array nums are unique, return the minimum element of this array.

### 1. Restating

* **Input:** Array `nums`, length `n`. Originally sorted ascending, rotated $1$ to $n$ times. All elements unique.
* **Output:** Minimum element in `nums`.
* **Goal:** Find smallest number in a shifted sorted list.

---

### 2. Clarifying Questions

* **Input type:** List of integers? (Assume yes).
* **Output type:** Integer? (Assume yes).
* **Empty array possible?** (Assume length >= 1).
* **Duplicates?** (Prompt confirms all unique).

---

### 3. Example by Hand

* **Input:** `nums = [3, 4, 5, 6, 1, 2]`
* Scan from left to right.
* 3 -> 4 (Up)
* 4 -> 5 (Up)
* 5 -> 6 (Up)
* 6 -> 1 (Drop!)
* Drop indicates the rotation point. The number immediately following the drop is the minimum.
* **Output:** `1`

---

### 4. Brainstorming & Complexity

* **Approach A: Linear Scan.** Iterate left to right, track minimum.
* *Time:* O(N)
* *Space:* O(1)


* **Approach B: Binary Search.** Exploit the "mostly sorted" property. Compare middle element to rightmost element to determine which half contains the drop (the minimum).
* *Time:* O(log N)
* *Space:* O(1)



---

### 5. Suggesting Solutions

Prefer **Approach B (Binary Search)**. While Approach A is exactly how we did it by hand in step 3, Approach B is vastly more efficient for large inputs and directly exploits the unique structural clue given in the prompt (sorted then rotated). It is clean, avoids linear time, and is easy to explain.

---

### 6. Outline & Core Logic

```python
def findMin(nums):
    """
    Reframe: Find the inflection point where the array drops, or return the first element if fully sorted.
    State: left pointer and right pointer, chosen because binary search exploits the partially sorted property.
    Invariant: The minimum element is always within the inclusive range [left, right].

    midpoint(left, right) = calculates the middle index safely.

    Core logic:
    - Setup left and right boundaries at array ends.
    - Loop while search space is larger than 1 element.
    - Calculate midpoint.
    - Compare midpoint value to right boundary value.
    - If midpoint value > right boundary value: minimum must be in right half (excluding mid).
    - Else: minimum must be in left half (including mid).
    - Narrow boundaries.
    - Return value at remaining pointer.

    Edge cases:
    - Array size of 1.
    - Array size of 2 (testing loop condition).
    - Array fully sorted (0 or n rotations).
    """

```

---

### 7. Iterative Implementation

**Iteration 1: Skeleton**
Translating plain English outline into code stubs.

```python
def findMin(nums):
    # setup left and right boundaries
    
    # loop while left < right
        
        # calculate midpoint
        
        # if midpoint value > right value:
            # move left boundary to mid + 1
            
        # else:
            # move right boundary to mid
            
    # return remaining element
    pass

```

**Iteration 2: Core Logic (Happy Path)**
Filling in the stubs with actual Python logic.

```python
def findMin(nums):
    left = 0                               # setup left boundary
    right = len(nums) - 1                  # setup right boundary
    
    while left < right:                    # loop while search space > 1
        mid = (left + right) // 2          # calculate midpoint
        
        if nums[mid] > nums[right]:        # if midpoint > right value
            left = mid + 1                 # min is to the right
        else:                              
            right = mid                    # min is to the left (or is mid)
            
    return nums[left]                      # return remaining element

```

**Iteration 3: Edge Case Walkthrough & Patching**

* **Edge Case 1: Array size 1 `[5]**`
* `left = 0`, `right = 0`.
* `while 0 < 0` is False. Loop skips.
* Returns `nums[0] = 5`. (Works, no patch needed).


* **Edge Case 2: Array size 2 `[2, 1]**`
* `left = 0`, `right = 1`.
* `mid = 0`. `nums[0] (2) > nums[1] (1)` is True.
* `left = mid + 1 = 1`.
* Next loop: `while 1 < 1` is False. Loop ends.
* Returns `nums[1] = 1`. (Works, no patch needed).


* **Edge Case 3: Fully sorted array `[1, 2, 3, 4]**`
* `left = 0`, `right = 3`.
* `mid = 1`. `nums[1] (2) > nums[3] (4)` is False.
* `right = mid = 1`.
* Next loop: `left = 0, right = 1`. `mid = 0`. `nums[0] (1) > nums[1] (2)` is False.
* `right = mid = 0`.
* Loop ends. Returns `nums[0] = 1`. (Works, no patch needed).



*Note: Core logic holds perfectly against all listed edge cases because `left < right` prevents infinite loops when `right = mid`, and checking against `nums[right]` accurately identifies the unsorted half.*

---

### 8. Complexity & Optimization

* **Time Complexity:** O(log N). The search space is halved every iteration.
* **Space Complexity:** O(1). Only using three pointer variables (`left`, `right`, `mid`) regardless of array size.
* **Optimization:** The solution is theoretically optimal for this problem. No expensive sections exist. Integer division `(left + right) // 2` is fine in Python as it handles arbitrarily large integers automatically, preventing the standard integer overflow bug found in languages like Java or C++ (where `left + (right - left) // 2` would be required).