### question
Given an integer array arr of distinct integers and an integer k.

A game will be played between the first two elements of the array (i.e. arr[0] and arr[1]). In each round of the game, we compare arr[0] with arr[1], the larger integer wins and remains at position 0, and the smaller integer moves to the end of the array. The game ends when an integer wins k consecutive rounds.

Return the integer which will win the game.

It is guaranteed that there will be a winner of the game.

 

Example 1:

Input: arr = [2,1,3,5,4,6,7], k = 2
Output: 5
Explanation: Let's see the rounds of the game:
Round |       arr       | winner | win_count
  1   | [2,1,3,5,4,6,7] | 2      | 1
  2   | [2,3,5,4,6,7,1] | 3      | 1
  3   | [3,5,4,6,7,1,2] | 5      | 1
  4   | [5,4,6,7,1,2,3] | 5      | 2
So we can see that 4 rounds will be played and 5 is the winner because it wins 2 consecutive games.
Example 2:

Input: arr = [3,2,1], k = 10
Output: 3
Explanation: 3 will win the first 10 rounds consecutively.


### 1. Problem Restatement

Given an array of distinct integers and target streak $k$. Two elements at the front duel; larger stays at index 0, smaller goes to the back. First element to reach $k$ consecutive wins wins the game. Find that winning element.

---

### 2. Clarifying Questions & Inputs/Outputs

* **Input:** `arr: list[int]` (length $n \ge 2$, all elements unique), `k: int` ($1 \le k \le 10^9$).
* **Output:** `int` (the value of the winning integer).
* **Constraints/Assumptions:**
* No duplicates in `arr`.
* $k$ can be much larger than $n$ ($10^9$), so simulating every single match for large $k$ will TLE.
* Winner is guaranteed.



---

### 3. Hand Simulation

Input: `arr = [2, 1, 3, 5, 4, 6, 7], k = 2`

| Step | Matchup | Winner | Win Streak | Array State Conceptually |
| --- | --- | --- | --- | --- |
| **Start** | — | — | 0 | `[2, 1, 3, 5, 4, 6, 7]` |
| **Round 1** | `2` vs `1` | `2` | 1 | `[2, 3, 5, 4, 6, 7, 1]` |
| **Round 2** | `2` vs `3` | `3` | 1 (new) | `[3, 5, 4, 6, 7, 1, 2]` |
| **Round 3** | `3` vs `5` | `5` | 1 (new) | `[5, 4, 6, 7, 1, 2, 3]` |
| **Round 4** | `5` vs `4` | `5` | 2 (hit $k=2$) | `[5, 6, 7, 1, 2, 3, 4]` |

Output: `5`

---

### 4. Brainstorming Solutions & Complexity

* **Approach 1: Queue / Deque Simulation**
* Rotate elements via actual queue operations until one hits $k$ wins.
* *Time Complexity:* $O(k)$. When $k = 10^9$, this causes TLE.
* *Space Complexity:* $O(n)$ to store queue.


* **Approach 2: Single-Pass "King of the Hill" (Optimal)**
* Notice: once an element loses, it moves to back and cannot challenge again until all other elements are played.
* If a leader beats every remaining element in a single pass of $arr$, it must be the global maximum. The global maximum can never lose to previously defeated elements cycled to the back.
* Therefore, one linear sweep through `arr[1:]` is sufficient.
* *Time Complexity:* $O(n)$.
* *Space Complexity:* $O(1)$.



---

### 5. Selected Solution

**Single-Pass Sweep:** Track `current_leader` and `consecutive_wins`. Compare `current_leader` with each incoming challenger sequentially.

---

### 6. Outline & Docstring Specification

```python
def getWinner(arr: list[int], k: int) -> int:
    """
    Reframe: Single pass "King of the Hill" sweep; global max wins if no one hits k earlier.
    State: current_winner and consecutive_wins maintained to track reigning champion.
    Invariant: current_winner has defeated all challengers encountered since its streak started.

    Core logic:
    - set first element as initial reigning winner with zero wins
    - for each subsequent challenger in the array:
        - match reigning winner against challenger
        - if reigning winner wins: increment streak
        - if challenger wins: challenger becomes new reigning winner with streak of 1
        - if streak reaches k: target met, return reigning winner
    - if array fully traversed without reaching k: return reigning winner (must be global max)

    Edge cases:
    - k >= len(arr): loop finishes completely and returns global maximum.
    - k = 1: terminates on first comparison.
    """
    pass

```

---

### 7. Iterative Implementation

**Iteration 1: Skeleton with stubs and placeholders**

```python
def getWinner(arr: list[int], k: int) -> int:
    # Setup initial state
    current_winner = arr[0]
    streak = 0
    
    # Iterate through remaining challengers
    for i in range(1, len(arr)):
        challenger = arr[i]
        
        # TODO: compare current_winner and challenger
        # TODO: update streak or reset winner
        # TODO: early return if streak == k
        pass

    # If pass completes without returning, reigning winner is global max
    return current_winner

```

**Iteration 2: Implement core logic comparisons**

```python
def getWinner(arr: list[int], k: int) -> int:
    current_winner = arr[0]
    streak = 0
    
    for i in range(1, len(arr)):
        challenger = arr[i]
        
        # Changed: resolve matchup outcome
        if current_winner > challenger:
            streak += 1
        else:
            current_winner = challenger
            streak = 1  # Beat the previous winner, so streak starts at 1
            
        # Changed: check target streak condition
        if streak == k:
            return current_winner

    return current_winner

```

**Iteration 3: Validate and walk edge cases**

* **Edge Case 1: $k \ge n$ (e.g., $k = 10^9$)**
* Code scans the entire array. The final `current_winner` is guaranteed to be $\max(arr)$. When the loop terminates, `return current_winner` executes correctly.


* **Edge Case 2: $k = 1$**
* On the very first matchup ($i=1$), winner gets `streak = 1 == k` and returns immediately.


* **Edge Case 3: Winner is at index 0 and beats all elements**
* `current_winner` stays `arr[0]`, increments streak until either $k$ is met or array ends. Correct.



*No additional patching required.*

---

### 8. Final Code & Complexity

```python
def getWinner(arr: list[int], k: int) -> int:
    current_winner = arr[0]
    streak = 0
    
    for i in range(1, len(arr)):
        if current_winner > challenger:
            streak += 1
        else:
            current_winner = arr[i]
            streak = 1
            
        if streak == k:
            return current_winner
            
    return current_winner

```

* **Time Complexity:** $O(n)$ where $n = \text{len}(arr)$. We iterate at most through the array once ($n-1$ comparisons).
* **Space Complexity:** $O(1)$ auxiliary space. Only two scalar variables maintained (`current_winner`, `streak`).