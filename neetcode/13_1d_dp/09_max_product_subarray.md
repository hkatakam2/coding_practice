## question
Given an integer array nums, find a subarray that has the largest product within the array and return it.
A subarray is a contiguous non-empty sequence of elements within an array.
You can assume the output will fit into a 32-bit integer.

# 6. Outline

```python
def max_product(nums):  # -> int
    """
    Reframe: a running negative product is an asset, not garbage — another
        negative flips it to the largest positive. So at each position track
        BOTH the largest and smallest product ending here.
    State: cur_max, cur_min (best & worst product of subarray ending at i),
        best (global answer). chosen because the sign-flip property means the
        future max can come from today's min × a negative.
    Invariant: after processing i, cur_max/cur_min = max/min product over all
        subarrays ending exactly at i; best = max product over all subarrays
        ending at or before i.

    candidates(x) = the three options for the subarray ending here:
        start fresh at x, or extend prev max by x, or extend prev min by x.

    Core logic:
    - seed cur_max, cur_min, best with first element
    - sweep rest: for each x, new cur_max = biggest of candidates(x),
        new cur_min = smallest of candidates(x)
    - fold cur_max into best
    Edge cases:
    - single element -> seeding already returns it
    - zero -> all candidates collapse toward 0, naturally resets the run
    - negative -> handled because we kept cur_min around to flip
    - all negatives -> min-tracking finds the even-count product
    """
```

# 7. Iterative implementation

**Skeleton**

```python
def max_product(nums):  # -> int
    cur_max = cur_min = best = nums[0]        # seed
    for x in nums[1:]:
        cur_max, cur_min = update(x, cur_max, cur_min)  # TODO
        best = max(best, cur_max)
    return best
```

**Iter 1 — fill `candidates`, inline the update**

```python
def max_product(nums):  # -> int
    cur_max = cur_min = best = nums[0]
    for x in nums[1:]:
        cands = (x, cur_max * x, cur_min * x)   # start fresh / extend max / extend min
        cur_max = max(cands)
        cur_min = min(cands)
        best = max(best, cur_max)
    return best
```

**Iter 2 — fix the ordering bug**

`cur_max` reassigned before `cur_min` uses it → must snapshot. `cands` already snapshots before either reassignment, so we're fine. But note: if we'd written `cur_max = max(...)` then `cur_min = min(x, cur_max*x, ...)` it'd be wrong. Keeping the tuple computed first is the safe move. Core logic done.

# Edge cases (walk one by one)

- **single element** `[5]`: loop body never runs, returns seed `5`. ✓ no patch.
- **zero** `[2,0,3]`: at `x=0`, cands `(0, 0, 0)` → cur_max=cur_min=0, run resets. next `x=3` cands `(3,0,0)` → 3. ✓ no patch.
- **negative / two negatives** `[-2,3,-4]`: cur_min carries the negative so `-4` flips it to 24. ✓ no patch.
- **all negatives** `[-2,-3,-1]`: min-tracking captures the even-length subarray. ✓ no patch.

No patches needed — the max/min seeding + tuple-of-candidates handles every edge.

# 8. Complexity

- Time **O(n)**: single pass, constant work per element.
- Space **O(1)**: three scalars (no `dp` array needed since each step only depends on previous).
- `nums[1:]` makes a copy → O(n) extra space. Cheap fix: iterate `for x in nums[1:]` → use index `for i in range(1, len(nums))` if you want strict O(1):

```python
def max_product(nums):  # -> int
    cur_max = cur_min = best = nums[0]
    for i in range(1, len(nums)):
        x = nums[i]
        cands = (x, cur_max * x, cur_min * x)
        cur_max, cur_min = max(cands), min(cands)
        best = max(best, cur_max)
    return best
```

Already optimal; nothing further to squeeze.