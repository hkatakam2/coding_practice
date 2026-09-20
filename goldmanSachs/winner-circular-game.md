### question
There are n friends that are playing a game. The friends are sitting in a circle and are numbered from 1 to n in clockwise order. More formally, moving clockwise from the ith friend brings you to the (i+1)th friend for 1 <= i < n, and moving clockwise from the nth friend brings you to the 1st friend.

The rules of the game are as follows:

Start at the 1st friend.
Count the next k friends in the clockwise direction including the friend you started at. The counting wraps around the circle and may count some friends more than once.
The last friend you counted leaves the circle and loses the game.
If there is still more than one friend in the circle, go back to step 2 starting from the friend immediately clockwise of the friend who just lost and repeat.
Else, the last friend in the circle wins the game.
Given the number of friends, n, and an integer k, return the winner of the game.

**1. Restating the Question**
Given $n$ friends standing in a circle numbered $1$ to $n$ clockwise, eliminate every $k$-th friend starting from friend 1 until only one person remains. Return the 1-indexed label of the winning friend.

---

**2. Clarifying Questions & Confirming I/O**

* **Inputs:** `n` (integer $\ge 1$), `k` (integer $\ge 1$).
* **Output:** `int` (1-indexed survivor label).
* **Constraints/Edge behavior:**
* Can $n = 1$? Yes, survivor is immediately 1.
* Can $k > n$? Yes, counting wraps around multiple times via modulo.
* Can $k = 1$? Yes, people are eliminated in order $1, 2, \dots, n-1$, leaving $n$.



---

**3. Hand-Simulation Example**

* **Input:** `n = 5, k = 2`
* Initial circle: `[1, 2, 3, 4, 5]`, current index = 0 (points to `1`).
* **Round 1:** Count 2 steps from index 0 $\rightarrow$ index $(0 + 2 - 1) = 1$ (`2` eliminated). Remaining: `[1, 3, 4, 5]`. New start index = 1 (`3`).
* **Round 2:** Count 2 steps from index 1 $\rightarrow$ index $(1 + 2 - 1) = 2$ (`4` eliminated). Remaining: `[1, 3, 5]`. New start index = 2 (`5`).
* **Round 3:** Count 2 steps from index 2 $\rightarrow$ index $(2 + 2 - 1) \bmod 3 = 0$ (`1` eliminated). Remaining: `[3, 5]`. New start index = 0 (`3`).
* **Round 4:** Count 2 steps from index 0 $\rightarrow$ index $(0 + 2 - 1) = 1$ (`5` eliminated). Remaining: `[3]`.
* **Result:** `3`.



---

**4. Brainstorming & Complexity**

* **Approach 1: Array-Based Simulation**
* Store $[1 \dots n]$ in a dynamic array. Track current index, step by $(k-1)$ with modulo length, remove person.
* *Time:* $O(n^2)$ due to array shift on deletion. *Space:* $O(n)$.


* **Approach 2: Queue Rotation**
* Pop and push $(k-1)$ elements to back, pop the $k$-th.
* *Time:* $O(n \cdot k)$. *Space:* $O(n)$.


* **Approach 3: Josephus Recurrence (Mathematical)**
* $f(n, k) = (f(n-1, k) + k) \bmod n$ with base $f(1, k) = 0$.
* *Time:* $O(n)$. *Space:* $O(1)$.



---

**5. Suggested Solution**
Proceed with **Approach 1 (Array Simulation)** first: it directly mirrors manual execution, has clear state transitions, and is easy to explain without mathematical leaps.

---

**6. Implementation Outline & Plain-English Core Logic**

```python
def findTheWinner(n: int, k: int) -> int:
    """
    Reframe: Repeatedly remove the (current + k - 1) % size element from a list until size is 1.
    State: Dynamic array `friends` representing active circle, `curr_idx` representing turn start.
        Chosen because array index modulo length natively models circular wrap-around.
    Invariant: At the start of each round, `curr_idx` points to the friend taking the next turn.

    next_elimination_index(curr_idx, k, circle_size) = calculates where count lands with circular wrapping.

    Core logic:
    - Populate circle with friends 1 to n.
    - Start counting at index 0.
    - While more than 1 friend remains:
        - Determine elimination index by moving k - 1 steps clockwise with wrap-around.
        - Remove eliminated friend from circle.
        - Next start index becomes the elimination index (elements shift left automatically).
    - Return the sole remaining friend.

    Edge cases:
    - n = 1: Loop does not execute, returns 1 immediately.
    - k = 1: Eliminates sequentially at curr_idx each time.
    - k > n: Modulo handles multi-lap wrapping automatically.
    """

```

---

**7. Iterative Implementation**

### Iteration 1: Skeleton with stubs

```python
def findTheWinner(n: int, k: int) -> int:
    # 1. Initialize friends circle
    friends = list(range(1, n + 1))
    curr_idx = 0

    # 2. Simulate rounds until 1 left
    while len(friends) > 1:
        # TODO: Calculate next target index
        # TODO: Remove friend at target index
        # TODO: Update curr_idx for next round
        pass

    return friends[0]

```

### Iteration 2: Fleshing out circular index calculation

```python
def findTheWinner(n: int, k: int) -> int:
    friends = list(range(1, n + 1))
    curr_idx = 0

    while len(friends) > 1:
        # Moving (k - 1) steps from curr_idx; % len handles wrapping
        target_idx = (curr_idx + k - 1) % len(friends)
        
        # TODO: Remove element and set next starting index
        friends.pop(target_idx) # + pop target
        curr_idx = target_idx   # + next person shifts into target_idx

    return friends[0]

```

### Iteration 3: Complete Core Implementation

```python
class Solution:
    def findTheWinner(self, n: int, k: int) -> int:
        friends = list(range(1, n + 1))
        curr_idx = 0

        while len(friends) > 1:
            # Advance (k - 1) steps in circle
            curr_idx = (curr_idx + k - 1) % len(friends)
            # Remove the k-th person; next start index is now at curr_idx
            friends.pop(curr_idx)

        return friends[0]

```

### Edge Case Verification against Final Code

* $n = 1$: `friends = [1]`, while loop condition `len > 1` is False $\rightarrow$ returns `1`. Correct.
* $k = 1$: `curr_idx = (0 + 0) % len = 0`. Pops index 0 each round until 1 element left. Correct.
* $k > n$: `(curr_idx + k - 1) % len` handles $k > \text{len}$ via modulo reduction. Correct.

---

**8. Complexity & Optimization**

* **Current Complexity (Simulation):**
* **Time:** $O(n^2)$ — $n-1$ removals, each `pop(idx)` takes $O(n)$ in an array.
* **Space:** $O(n)$ to store list of friends.


* **Optimization ($O(n)$ Time, $O(1)$ Space):**
* When $n$ grows large ($n \ge 10^5$), simulation times out.
* Use the **Josephus recurrence**: in 0-indexed form, survivor index in circle of size $i$ relates to size $i-1$ via:

$$\text{winner}(i) = (\text{winner}(i - 1) + k) \bmod i \quad \text{with } \text{winner}(1) = 0$$





```python
def findTheWinnerOptimal(n: int, k: int) -> int:
    winner_idx = 0  # Base case: 1 person, 0-indexed winner is 0
    for i in range(2, n + 1):
        winner_idx = (winner_idx + k) % i
    return winner_idx + 1  # Convert 0-indexed to 1-indexed

```

* **Optimized Time:** $O(n)$ — single pass loop.
* **Optimized Space:** $O(1)$ — single integer state.