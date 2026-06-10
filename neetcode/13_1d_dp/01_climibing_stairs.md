# question
You are given an integer n representing the number of steps to reach the top of a staircase. You can climb with either 1 or 2 steps at a time.
Return the number of distinct ways to climb to the top of the staircase.

**1. Restating**
Problem: Given $n$ stairs. Can move 1 or 2 stairs per move. Find total unique paths to top.

**2. Clarifying**
Inputs: `n` (integer).
Outputs: `ways` (integer).
Confirmations:

* Can `n` be 0 or negative? (Assume $n \ge 1$).
* Does order matter? (Yes, 1 step then 2 steps differs from 2 steps then 1 step).
* Max `n`? (Assume fits in standard time limits, no big-int overflow needed).

**3. Hand-trace**
Input: `n = 4`
Paths:

1. 1, 1, 1, 1
2. 1, 1, 2
3. 1, 2, 1
4. 2, 1, 1
5. 2, 2
Output: 5.
Observation: To reach step 4, must jump from step 3 (take 1 step) or step 2 (take 2 steps). Thus, `ways(4) = ways(3) + ways(2)`. Matches Fibonacci sequence.

**4. Brainstorming**

* **Recursion (Tree):** Branch paths by 1 or 2. Time $O(2^n)$. Re-evaluates same subproblems. Too slow.
* **Top-Down Memoization:** Cache recursive results. Time $O(n)$, Space $O(n)$. Better, but recursion stack adds overhead.
* **Bottom-Up DP (Array):** Build from step 1 to $n$. Save past results in array. Time $O(n)$, Space $O(n)$.
* **Bottom-Up (Variables):** Only need last two step counts. Time $O(n)$, Space $O(1)$.

**5. Suggest Solutions**
Prefer clear, straightforward approach.

1. Recursive hand-trace simulation (Step 3 logic, unoptimized).
2. Bottom-up DP with array. Highly readable. Directly translates hand-trace into state array. Will implement this first for clarity.

**6. Outline**

```python
def climbStairs(n): 
    """
    Reframe: Current step's total paths equals sum of paths to previous two steps.
    State: Array mapping step index to total paths, chosen because it builds solution iteratively from smallest subproblems.
    Invariant: Current step paths = (current - 1) paths + (current - 2) paths.

    get_prev_sum(history, current) = looks up and adds paths from the two immediately preceding steps.

    Core logic:
    - create tracking list sized n+1
    - seed tracking list for step 1
    - seed tracking list for step 2
    - iterate from step 3 to n:
        - calculate paths using get_prev_sum
        - store paths in tracking list
    - return value at end of tracking list

    Edge cases:
    - n is 1 (array size too small for step 2 seed)
    - n is 2 (loop won't execute, but needs to return safely)
    """

```

**7. Iterative Implementation**

*Iteration 1: Skeleton*

```python
def climbStairs(n):
    # TODO: Handle edge cases 
    
    # create tracking list
    
    # seed step 1 and 2
    
    # loop step 3 to n
        # get prev sum
        # store
        
    # return final step
    pass

```

*Iteration 2: Core Logic with Helper*

```python
def get_prev_sum(history, current):
    # dummy helper to read plain English
    return history[current - 1] + history[current - 2]

def climbStairs(n):
    # TODO: Handle edge cases 
    
    # create tracking list sized n+1 (1-indexed for clarity)
    history = [0] * (n + 1)
    
    # seed step 1 and 2
    history[1] = 1
    history[2] = 2
    
    # loop step 3 to n
    for step in range(3, n + 1):
        # get prev sum and store
        history[step] = get_prev_sum(history, step)
        
    # return final step
    return history[n]

```

*Iteration 3: Inline helper (Core complete)*

```python
def climbStairs(n):
    # TODO: Handle edge cases 
    
    history = [0] * (n + 1)
    
    history[1] = 1
    history[2] = 2
    
    for step in range(3, n + 1):
        # replaced helper with actual array syntax
        history[step] = history[step - 1] + history[step - 2]
        
    return history[n]

```

*Iteration 4: Patching Edge Cases (Final Array Version)*

```python
def climbStairs(n):
    # EDGE CASE PATCH: n=1 breaks history[2] = 2. 
    # n=2 is technically handled by seeds, but early return is cleaner.
    if n == 1:
        return 1
    if n == 2:
        return 2
    
    history = [0] * (n + 1)
    
    history[1] = 1
    history[2] = 2
    
    for step in range(3, n + 1):
        history[step] = history[step - 1] + history[step - 2]
        
    return history[n]

```

**8. Complexity & Optimization**
Current Time: $O(n)$ (single loop).
Current Space: $O(n)$ (array of size $n+1$).

*Commentary on expensive sections:*
Allocating array is $O(n)$ space. We only ever read `step - 1` and `step - 2`. Rest of history is dead memory.
*Optimization:* Replace array with two variables to track just the previous two states. Drops space to $O(1)$.

*Optimized Code:*

```python
def climbStairs(n):
    if n == 1:
        return 1
    if n == 2:
        return 2
        
    # Track only the last two steps
    prev2 = 1  # ways to reach step 1
    prev1 = 2  # ways to reach step 2
    
    for _ in range(3, n + 1):
        # Current ways = sum of last two
        current = prev1 + prev2
        
        # Shift variables forward for next iteration
        prev2 = prev1
        prev1 = current
        
    return prev1

```
