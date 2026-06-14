## question
You are given an array of integers `nums` of size `n`. The `ith` element represents a balloon with an integer value of `nums[i]`. You must burst all of the balloons.
If you burst the `ith` balloon, you will receive `nums[i - 1] * nums[i] * nums[i + 1]` coins. If `i - 1` or `i + 1` goes out of bounds of the array, then assume the out of bounds value is 1.
Return the maximum number of coins you can receive by bursting all of the balloons.

**1. Restating the Question**
Given an array `nums` representing balloons. Burst them all. Bursting balloon `i` yields `nums[i-1] * nums[i] * nums[i+1]` coins. Edges out of bounds count as `1`. Find max coins possible.

**2. Clarifying Questions & Confirming I/O**

* **Input:** Array of integers `nums`.
* **Output:** Integer representing max coins.
* **Q:** What if `nums` is empty? **A:** Assume return 0.
* **Q:** What if `nums` has 1 element? **A:** Assume boundaries are 1, so `1 * nums[0] * 1`.
* **Q:** Can values be 0? **A:** Yes. Bursting them yields 0, but they still get removed.

**3. Hand Trace Example**
Input: `[3, 1, 5]`
Pad edges: `[1, 3, 1, 5, 1]`

Try bursting left-to-right:

* Burst `3`: `1 * 3 * 1 = 3`. Array left: `[1, 1, 5, 1]`
* Burst `1`: `1 * 1 * 5 = 5`. Array left: `[1, 5, 1]`
* Burst `5`: `1 * 5 * 1 = 5`. Array left: `[1, 1]`
Total: `3 + 5 + 5 = 13`

Try middle first:

* Burst `1`: `3 * 1 * 5 = 15`. Array left: `[1, 3, 5, 1]`
* Burst `5`: `3 * 5 * 1 = 15`. Array left: `[1, 3, 1]`
* Burst `3`: `1 * 3 * 1 = 3`. Array left: `[1, 1]`
Total: `15 + 15 + 3 = 33` -> **Max**

**4. Brainstorming & Complexity**

* **Idea 1: Brute Force (simulate bursts).** Pick any balloon, remove it, recurse on new array.
* *Complexity:* `O(n!)` time. Array shrinks, changing adjacent neighbors. Extremely slow.


* **Idea 2: Divide & Conquer (burst first).** If we burst `i` first, the left sub-array and right sub-array are now adjacent. They are not independent. DP fails.
* **Idea 3: Divide & Conquer (burst *last*).** What if we pick balloon `i` to be the *last* one to burst in a range? Left of `i` and right of `i` become completely independent because `i` stays intact until the very end, serving as their boundary!
* *Complexity:* `O(n^3)` time, `O(n^2)` space. Excellent.



**5. Suggest Solutions**

1. **Brute Force Permutations:** Easy to write by simulating the hand-trace in Step 3. Too slow for interviews.
2. **Top-Down DP (Memoization) with "Burst Last" pattern:** Pad the array. Define a helper that finds max coins for a range. Pick each balloon to be the *last* to burst, splitting into independent left/right subproblems. Simple, elegant, avoids nasty index math. We will proceed with this.

**6. Outline Implementation**

```python
def maxCoins(nums):
    """
    Reframe: Think about which balloon bursts LAST, not first, to keep subproblems independent.
    State: Memoization cache for ranges, chosen because it prevents recalculating the max coins for the same subarray.
    Invariant: Boundaries left and right are strictly alive while evaluating the balloons between them.

    solve(left, right) = computes max coins from bursting all balloons strictly between index 'left' and 'right'.

    Core logic:
    - pad original array with 1s on both ends
    - create a cache for memoization
    - call solve on the entire padded range
    - inside solve:
        - try making every balloon in the range the LAST one to burst
        - coins for this burst = left boundary * this balloon * right boundary
        - total coins = left subproblem + right subproblem + coins for this burst
        - track the maximum total found
    - return max total

    Edge cases:
    - range is empty (no balloons between left and right)
    """

```

**7. Iterative Implementation**

*Iteration 1: Skeleton with helper setup.*

```python
def maxCoins(nums):
    # Setup padded array
    padded_nums = [1] + nums + [1]
    
    def solve(left, right):
        # TODO: return max coins strictly between left and right
        pass
        
    # call solve on the whole range, excluding the artificial 1s
    return solve(0, len(padded_nums) - 1)

```

*Iteration 2: Core logic (looping and recursion).*

```python
def maxCoins(nums):
    padded_nums = [1] + nums + [1]
    
    def solve(left, right):
        max_coins = 0
        
        # 'i' is the balloon we choose to burst LAST
        for i in range(left + 1, right):
            # calculate coins if 'i' is the last to burst
            coins_for_burst = padded_nums[left] * padded_nums[i] * padded_nums[right]
            
            # recursively solve left and right independent halves
            left_coins = solve(left, i)
            right_coins = solve(i, right)
            
            total_coins = left_coins + coins_for_burst + right_coins
            max_coins = max(max_coins, total_coins)
            
        return max_coins
        
    return solve(0, len(padded_nums) - 1)

```

*Iteration 3: Adding Memoization (State).*

```python
def maxCoins(nums):
    padded_nums = [1] + nums + [1]
    cache = {} # ADDED: Cache to store computed ranges
    
    def solve(left, right):
        # ADDED: check cache
        if (left, right) in cache:
            return cache[(left, right)]
            
        max_coins = 0
        for i in range(left + 1, right):
            coins_for_burst = padded_nums[left] * padded_nums[i] * padded_nums[right]
            
            left_coins = solve(left, i)
            right_coins = solve(i, right)
            
            total_coins = left_coins + coins_for_burst + right_coins
            max_coins = max(max_coins, total_coins)
            
        # ADDED: store in cache
        cache[(left, right)] = max_coins
        return max_coins
        
    return solve(0, len(padded_nums) - 1)

```

*Iteration 4: Edge Cases.*
Checking our edge cases from Step 6.

* Empty range: What if `left + 1 == right`? (e.g., adjacent balloons).
* In our current code, `range(left + 1, right)` will just be empty. The loop won't run. `max_coins` remains `0`, which is correctly returned. The happy path implicitly handles the edge case! We just add an explicit base case to short-circuit and save function calls.

```python
def maxCoins(nums):
    padded_nums = [1] + nums + [1]
    cache = {} 
    
    def solve(left, right):
        # PATCH: Explicit base case for empty range
        if left + 1 == right:
            return 0
            
        if (left, right) in cache:
            return cache[(left, right)]
            
        max_coins = 0
        for i in range(left + 1, right):
            coins_for_burst = padded_nums[left] * padded_nums[i] * padded_nums[right]
            total_coins = solve(left, i) + coins_for_burst + solve(i, right)
            max_coins = max(max_coins, total_coins)
            
        cache[(left, right)] = max_coins
        return max_coins
        
    return solve(0, len(padded_nums) - 1)

```

**8. Complexity & Optimization**

* **Time Complexity:** `O(n^3)`. There are `O(n^2)` possible `(left, right)` pairs for states. For each state, we iterate through up to `n` balloons.
* **Space Complexity:** `O(n^2)` for the memoization cache and call stack.
* **Optimization Comment:** Removing `0` values from the input array upfront can safely optimize execution time since bursting a `0` yields `0` coins and shrinks the array faster without penalty. We omitted this to keep the core logic perfectly clear, but in a production environment, filtering `nums = [n for n in nums if n > 0]` before padding is a great quick win. Converting this top-down logic to bottom-up DP saves recursion overhead, but top-down is far more readable for interviews.