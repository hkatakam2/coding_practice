### question
You are given an array of integers nums containing n + 1 integers. Each integer in nums is in the range [1, n] inclusive.

There is exactly one repeated integer in nums, and every other integer appears at most once.

Return the repeated integer.

**1. Restate**
Given array `nums` of size n+1. Elements restricted to range 1 to n. Exactly one number repeats (possibly multiple times). Find and return it.

**2. Clarify**

* Inputs: List of integers.
* Outputs: Single integer (the duplicate).
* Confirming: Is the array read-only? Do we have space constraints? (Assuming standard constraints first: find it however we can. Will optimize space later).

**3. Example by Hand**
Input: `[1, 3, 4, 2, 2]` (n=4)

* Read 1. Seen before? No. Remember 1.
* Read 3. Seen before? No. Remember 3.
* Read 4. Seen before? No. Remember 4.
* Read 2. Seen before? No. Remember 2.
* Read 2. Seen before? Yes! Return 2.

**4. Brainstorming & Complexity**

* **Idea 1: Hash Set (Mirroring by-hand).** Track seen items. Time: O(N). Space: O(N).
* **Idea 2: Sorting.** Sort array, check adjacent elements. Time: O(N log N). Space: O(1) or O(N). Modifies input array.
* **Idea 3: Math (Sum).** Calculate expected sum vs actual sum. Fails if duplicate appears >2 times (e.g., `[2, 2, 2, 2]`). Discard.
* **Idea 4: Linked List Cycle (Floyd's).** Treat values as pointers to indices. Duplicate creates a cycle. Time: O(N). Space: O(1). Clever, but complex to explain initially.

**5. Suggest Solutions**
Prefer Idea 1 (Hash Set). It is simple, readable, and directly translates the human "by hand" method into code without mutating the array or relying on clever pointer tricks.

**6. Outline**

```python
def findDuplicate(nums): 
    """
    Reframe: Track visited elements; first recurrence is our target.
    State: Hash set `seen`, chosen because it exploits O(1) lookup time.
    Invariant: `seen` contains only unique elements processed so far.

    is_already_seen(num) = checks if num exists in our set
    mark_as_seen(num) = adds num to our set

    Core logic:
    - iterate through each number in array
    - if is_already_seen(number), return number
    - else, mark_as_seen(number)

    Edge cases:
    - duplicate appears more than twice
    - empty array or missing duplicate (ignored per constraints: n+1 size, guaranteed duplicate)
    """

```

**7. Iterative Implementation**

*Iteration 1: Skeleton with stubs*

```python
def findDuplicate(nums):
    # TODO: initialize state
    
    for num in nums:
        # TODO: if is_already_seen(num) return num
        # TODO: mark_as_seen(num)
        pass
        
    return -1 # Fallback

```

*Iteration 2: Fleshing out core logic (Replacing stubs with Python set logic)*

```python
def findDuplicate(nums):
    seen = set() # ADDED: state initialization
    
    for num in nums:
        if num in seen: # ADDED: inline is_already_seen check
            return num
        seen.add(num) # ADDED: inline mark_as_seen action
        
    return -1

```

*Edge Cases Review:*

* **Duplicate appears >2 times:** Core logic handles this. We return immediately upon the *second* sighting. Code requires no patching.

**8. Complexity & Optimization**
*Current Complexity:* Time: O(N) due to single pass. Space: O(N) due to hash set.
*Optimization:* Interviewers often restrict space to O(1) and forbid array modification. To achieve O(1) space, we switch to Idea 4 (Floyd's Tortoise and Hare).

*Optimization Logic:* Map array values to pointers (`next = nums[curr]`). Because multiple indices point to the duplicate value, a cycle forms.

*Optimized Code:*

```python
def findDuplicate_optimized(nums):
    # Phase 1: Intersect in cycle
    slow = nums[0]
    fast = nums[nums[0]]
    
    while slow != fast:
        slow = nums[slow]
        fast = nums[nums[fast]]
        
    # Phase 2: Find cycle entrance (the duplicate)
    slow = 0
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]
        
    return slow

```

*Optimized Complexity:* Time: O(N). Space: O(1). No array mutation.