## question
There are `n` gas stations along a circular route. You are given two integer arrays `gas` and `cost` where:

* `gas[i]` is the amount of gas at the `ith` station.
* `cost[i]` is the amount of gas needed to travel from the `ith` station to the `(i + 1)th` station. (The last station is connected to the first station)
You have a car that can store an unlimited amount of gas, but you begin the journey with an empty tank at one of the gas stations.
Return the starting gas station's index such that you can travel around the circuit once in the clockwise direction. If it's impossible, then return `-1`.
It's guaranteed that at most one solution exists.

### 1. Restating the Question

N gas stations in a circle.
Station gives `gas[i]`, costs `cost[i]` to reach the next.
Start with empty tank. Unlimited capacity.
Find starting index to complete full loop clockwise. Return -1 if impossible.
Guaranteed max one valid start.

---

### 2. Clarifying Questions & Confirming I/O

**Interviewer:** Let's lock down the inputs and expected outputs.

* **Input:** Two arrays, `gas` and `cost`. Both integers, same length.
* **Output:** Integer representing starting index, or -1.
* **Constraints:** Can arrays be empty? Assume $N \ge 1$. Are values non-negative? Yes.
* **Example 1:**
`gas = [1, 2, 3, 4, 5]`
`cost = [3, 4, 5, 1, 2]`
Returns `3`.
* **Example 2:**
`gas = [2, 3, 4]`
`cost = [3, 4, 3]`
Returns `-1`.

---

### 3. Hand-Tracing Example

Let's trace Example 1 manually.
`gas = [1, 2, 3, 4, 5]`
`cost = [3, 4, 5, 1, 2]`
Net gas per station (`gas - cost`): `[-2, -2, -2, 3, 3]`

* Try start 0: net is -2. Tank negative. Fails.
* Try start 1: net is -2. Tank negative. Fails.
* Try start 2: net is -2. Tank negative. Fails.
* Try start 3: net is 3. Tank positive.
* Go to 4: tank = 3 + 3 = 6.
* Go to 0: tank = 6 - 2 = 4.
* Go to 1: tank = 4 - 2 = 2.
* Go to 2: tank = 2 - 2 = 0.
* Loop complete. Returns 3.



---

### 4. Brainstorming & Complexity

**Approach A: Brute Force**
Try every station as a start point. Simulate the loop.
Time: O(N^2) for nested loops. Space: O(1).
Too slow. We do redundant checks.

**Approach B: Greedy / One-Pass**
Two key insights:

1. If total gas < total cost, completion is impossible. Return -1.
2. If we start at station A and run out of gas at station B, *no station between A and B can reach B+1*. Why? Because starting at A gave us a positive buffer. If even with that buffer we couldn't pass B, starting anywhere after A with a 0 buffer will fail even faster.
Therefore, the next viable start point is `B + 1`.
Time: O(N). Space: O(1).

---

### 5. Suggesting Solutions

We will implement **Approach B**. It is clean, requires only a single pass, and relies on simple logic rather than complex data structures. Approach A (our manual hand-trace method) is good for intuition but fails scale tests.

---

### 6. Outline Implementation

```python
def canCompleteCircuit(gas: list[int], cost: list[int]) -> int:
    """
    Reframe: Total gas must >= total cost. A failed segment means no start point in it works.
    State: `total_surplus` to check if journey is possible overall. `current_surplus` to check validity of current start point.
    Invariant: `current_surplus` remains >= 0 from the chosen start point onwards.

    Core logic:
    - calculate net gas for each station.
    - accumulate total net gas across all stations.
    - accumulate current net gas for the active trip.
    - if the trip's tank drops below zero:
        - current start point is invalid.
        - reset tank.
        - set next station as the new start point candidate.
    - return the candidate start point.

    Edge cases:
    - if total net gas across the entire array is negative, return -1.
    """

```

---

### 7. Iterative Implementation

**Iteration 1: Skeleton with Plain English Logic**
Set up placeholders. Focus entirely on flow.

```python
def canCompleteCircuit(gas: list[int], cost: list[int]) -> int:
    # TODO: track current tank and candidate start station
    
    # loop over stations:
        # calculate net gas for this stop
        # add to current tank
        
        # if tank empty/negative:
            # this start candidate failed
            # move start candidate to next station
            # reset current tank to 0
            
    # return candidate start station
    pass

```

**Iteration 2: Core Logic (Happy Path)**
Assume a valid route exists. Turn outline into code.

```python
def canCompleteCircuit(gas: list[int], cost: list[int]) -> int:
    current_tank = 0
    start_station = 0
    
    for i in range(len(gas)):
        net_gas = gas[i] - cost[i]
        current_tank += net_gas
        
        # If we run out of gas, this start point (and all prior) is invalid
        if current_tank < 0:
            start_station = i + 1  # Next station is the new candidate
            current_tank = 0       # Reset tank for the new candidate
            
    return start_station

```

**Iteration 3: Edge Cases**
Patch code to handle the impossible route (total gas < total cost). Add `total_tank` tracking.

```python
def canCompleteCircuit(gas: list[int], cost: list[int]) -> int:
    total_tank = 0       # Added: Track overall net gas
    current_tank = 0
    start_station = 0
    
    for i in range(len(gas)):
        net_gas = gas[i] - cost[i]
        
        total_tank += net_gas      # Added: Update overall sum
        current_tank += net_gas
        
        if current_tank < 0:
            start_station = i + 1
            current_tank = 0
            
    # Added: Edge case check. If overall we don't have enough gas, impossible.
    if total_tank < 0:
        return -1
        
    return start_station

```

---

### 8. Complexity & Optimization

* **Time Complexity:** O(N). We iterate through the arrays exactly once.
* **Space Complexity:** O(1). We only store three integer variables (`total_tank`, `current_tank`, `start_station`).
* **Optimization check:** The single loop doing simultaneous candidate-checking and total-summation is optimal. No further algorithmic improvements exist. Skipping ahead (`start_station = i + 1`) is mathematically sound and saves us from nested loops. The solution is complete.