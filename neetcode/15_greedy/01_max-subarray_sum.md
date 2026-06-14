## question
Given an array of integers `nums`, find the subarray with the largest sum and return the sum.
A subarray is a contiguous non-empty sequence of elements within an array.

**1. Restate**
Find contiguous non-empty slice of `nums` with max sum; return that sum.

**2. Clarifying Qs**
- Empty array possible? Assume no (non-empty array, non-empty subarray).
- All negatives? Then answer is the largest single element (subarray must be non-empty).
- Integer overflow concern? Assume fits in standard int.
- Need indices or just the sum? Just the sum.

Input: `list[int]` → Output: `int`.

**3. Example by hand**
`nums = [-2,1,-3,4,-1,2,1,-5,4]`
Walk left→right, track running sum; drop it when it goes negative (a negative prefix only hurts what follows):
```
-2 → running -2 (negative, drop → 0), best -2
 1 → running 1,  best 1
-3 → running -2 (drop → 0), best 1
 4 → running 4,  best 4
-1 → running 3,  best 4
 2 → running 5,  best 5
 1 → running 6,  best 6   <- subarray [4,-1,2,1]
-5 → running 1,  best 6
 4 → running 5,  best 6
```
Answer: **6**.

**4. Brainstorm + complexity**
- Brute force: all subarrays, sum each → O(n²) or O(n³) naive.
- Prefix sums: max(prefix[j] - min prefix before j) → O(n).
- Kadane (the by-hand method from step 3): running sum, reset when it'd hurt → O(n) time, O(1) space.
- Divide & conquer: O(n log n), more code, harder to explain.

**5. Solutions**
- (A) Brute force O(n²) — clearest to reason about, slow.
- (B) Kadane O(n)/O(1) — exactly the by-hand walk in step 3, simple + optimal.
- (C) Divide & conquer O(n log n) — clever, not worth it.

Recommend **(B) Kadane** — matches your hand-trace and is both simple and optimal.

**6. Outline**

```python
def max_subarray(nums):  # -> int
    """
    Reframe: a negative running sum can only hurt what comes after, so drop it and start fresh.
    State: running_sum (best sum of a subarray ending at current element),
           best (max running_sum seen so far). Chosen because the optimal subarray
           ending here is either (this element) or (this element + best ending at prev).
    Invariant: after processing index i, running_sum = max subarray sum ending exactly at i,
               and best = max over all subarrays ending at or before i.

    extend_or_restart(running_sum, x) = whichever is bigger: x alone, or running_sum + x.

    Core logic:
    - start running_sum and best at the first element
    - for each later element: running_sum = extend_or_restart(running_sum, element)
    - best = the larger of best and running_sum
    - return best

    Edge cases:
    - single element -> loop never runs, best = that element
    - all negatives -> extend_or_restart keeps picking the lone element (never forced to add); best ends as max element
    - empty array -> undefined (assume non-empty per clarifying Qs)
    """
```

**7. Iterative implementation**

Iteration 1 — skeleton from the plain English:
```python
def max_subarray(nums):
    running_sum = nums[0]          # best subarray ending at current
    best = nums[0]                 # best seen anywhere
    for x in nums[1:]:
        running_sum = extend_or_restart(running_sum, x)  # TODO
        best = max(best, running_sum)
    return best
```

Iteration 2 — fill the helper:
```python
def max_subarray(nums):
    def extend_or_restart(running_sum, x):   # new: inline the helper
        return max(x, running_sum + x)       # x alone, or extend prev
    running_sum = nums[0]
    best = nums[0]
    for x in nums[1:]:
        running_sum = extend_or_restart(running_sum, x)
        best = max(best, running_sum)
    return best
```

Iteration 3 — inline helper for tightness (optional), core logic complete:
```python
def max_subarray(nums):
    running_sum = best = nums[0]
    for x in nums[1:]:
        running_sum = max(x, running_sum + x)  # extend or restart
        best = max(best, running_sum)
    return best
```

Edge-case walk:
- single element → `nums[1:]` empty, returns `nums[0]`. ✓ no patch.
- all negatives → `max(x, running_sum + x)` picks lone `x` when sum hurts; `best` tracks max element. ✓ no patch.
- empty → would crash on `nums[0]`; out of scope per Qs. No guard added (could add `if not nums: return 0/None` if required).

**8. Complexity**

Time O(n): single pass, each element O(1) work.
Space O(1): two scalars.
Optimal — can't beat O(n) since every element must be inspected at least once. No further optimization warranted.