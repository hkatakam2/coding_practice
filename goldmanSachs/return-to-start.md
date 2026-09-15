### question
There is a robot starting at the position (0, 0), the origin, on a 2D plane. Given a sequence of its moves, judge if this robot ends up at (0, 0) after it completes its moves.

You are given a string moves that represents the move sequence of the robot where moves[i] represents its ith move. Valid moves are 'R' (right), 'L' (left), 'U' (up), and 'D' (down).

Return true if the robot returns to the origin after it finishes all of its moves, or false otherwise.

Note: The way that the robot is "facing" is irrelevant. 'R' will always make the robot move to the right once, 'L' will always make it move left, etc. Also, assume that the magnitude of the robot's movement is the same for each move.

 

Example 1:

Input: moves = "UD"
Output: true
Explanation: The robot moves up once, and then down once. All moves have the same magnitude, so it ended up at the origin where it started. Therefore, we return true.
Example 2:

Input: moves = "LL"
Output: false
Explanation: The robot moves left twice. It ends up two "moves" to the left of the origin. We return false because it is not at the origin at the end of its moves.

**1. Restating the Question**
Given string of directional steps (`'U'`, `'D'`, `'L'`, `'R'`) starting at origin $(0, 0)$, determine if cumulative vector sum of all unit displacements results in zero vector $(0, 0)$.

---

**2. Clarifying Questions & Confirming Inputs/Outputs**

* **Input:** `moves: str` containing move characters.
* **Output:** `bool` (`True` if final position is $(0, 0)$, else `False`).
* **Assumptions:**
* Empty string $\implies$ 0 moves $\implies$ returns `True`.
* Input characters strictly bounded to `'U'`, `'D'`, `'L'`, `'R'`.
* Step size is fixed unit length $1$.
* Move order executes sequentially from index $0$ to $N-1$.



---

**3. Hand Execution (Input $\to$ Output)**

* Vector mappings: `'U': (0, 1)`, `'D': (0, -1)`, `'L': (-1, 0)`, `'R': (1, 0)`.
* **Test Case 1:** `moves = "UDLR"`
* Start: $(0, 0)$
* Move 1 `'U'`: $(0, 0) + (0, 1) = (0, 1)$
* Move 2 `'D'`: $(0, 1) + (0, -1) = (0, 0)$
* Move 3 `'L'`: $(0, 0) + (-1, 0) = (-1, 0)$
* Move 4 `'R'`: $(-1, 0) + (1, 0) = (0, 0)$
* Final: $(0, 0) == (0, 0) \implies \text{True}$


* **Test Case 2:** `moves = "LL"`
* Start: $(0, 0)$
* Move 1 `'L'`: $(0, 0) + (-1, 0) = (-1, 0)$
* Move 2 `'L'`: $(-1, 0) + (-1, 0) = (-2, 0)$
* Final: $(-2, 0) \ne (0, 0) \implies \text{False}$



---

**4. Brainstorming & Complexity**

* **Option A: Conditional Scalar Mutation:** Branch on each character with `if/elif` blocks modifying scalar variables $x$ and $y$. Time: $O(N)$, Space: $O(1)$.
* **Option B: Character Frequency Counting:** Count occurrences of each character. Check if $\text{count}(U) == \text{count}(D)$ and $\text{count}(L) == \text{count}(R)$. Time: $O(N)$, Space: $O(1)$.
* **Option C: Vector Summation (Requested):** Map each character to static 2D displacement vector $(dx, dy)$. Aggregate vectors component-wise across sequence. Decouples direction semantics from summation logic. Time: $O(N)$, Space: $O(1)$.

---

**5. Suggested Solution: Option C (Vector Summation)**

* Model each move as 2D displacement tuple.
* Accumulate components into running total vector.
* Check if accumulated vector equals zero vector $(0, 0)$.

---

**6. Implementation Outline**

```python
def judgeCircle(moves: str) -> bool:
    """
    Reframe: Total displacement is the vector sum of all individual step vectors.
    State: A 2D coordinate vector (x, y) representing accumulated displacement, chosen because vector addition directly tracks Euclidean position across moves.
    Invariant: At step i, (x, y) holds the cumulative vector sum of moves[0...i].

    get_vector(move) = maps directional character to its unit displacement tuple (dx, dy).
    add_vectors(v1, v2) = computes component-wise sum of two 2D vectors.
    is_zero_vector(v) = checks if both components of a vector evaluate to 0.

    Core logic:
    - initialize net vector to zero vector
    - for each move in input string:
        - get step vector for current move
        - add step vector to net vector
    - return whether net vector is zero vector

    Edge cases:
    - empty string: returns True immediately (0 total displacement).
    - odd length string: odd number of unit vectors cannot cancel out to zero vector.
    """

```

---

**7. Iterative Implementation**

**Iteration 1: Skeleton with helper stubs & placeholders**

```python
def judgeCircle(moves: str) -> bool:
    # Helper stubs
    def get_vector(move: str) -> tuple[int, int]:
        # TODO: map 'U', 'D', 'L', 'R' to (dx, dy)
        pass

    def add_vectors(
        v1: tuple[int, int], v2: tuple[int, int]
    ) -> tuple[int, int]:
        # TODO: return component-wise sum
        pass

    def is_zero_vector(v: tuple[int, int]) -> bool:
        # TODO: check if (0, 0)
        pass

    # Core flow skeleton
    current_pos = (0, 0)
    for move in moves:
        step = get_vector(move)
        current_pos = add_vectors(current_pos, step)

    return is_zero_vector(current_pos)

```

**Iteration 2: Realize helper implementations**

```python
def judgeCircle(moves: str) -> bool:
    # Static vector lookup table
    DIR_VECTORS = {
        "U": (0, 1),
        "D": (0, -1),
        "L": (-1, 0),
        "R": (1, 0),
    }

    # Inline vector accumulation to avoid tuple allocation overhead
    x, y = 0, 0
    for move in moves:
        dx, dy = DIR_VECTORS[move]
        x += dx
        y += dy

    return x == 0 and y == 0

```

**Iteration 3: Walk & integrate edge cases**

* **Edge Case Walkthrough:**
* *Empty String (`moves = ""`):* Parity check `0 % 2 != 0` is `False`. Loop skips. Returns `0 == 0 and 0 == 0` $\to$ `True` (Correct).
* *Odd Length String (`len(moves) % 2 != 0`):* Each positive displacement requires matching negative displacement. Odd count cannot sum to $(0, 0)$. Short-circuit return `False` in $O(1)$.



```python
def judgeCircle(moves: str) -> bool:
    # Edge case: odd number of unit steps can never return to origin
    if len(moves) % 2 != 0:
        return False

    # Pre-defined vector mapping table
    DIR_VECTORS = {
        "U": (0, 1),
        "D": (0, -1),
        "L": (-1, 0),
        "R": (1, 0),
    }

    x, y = 0, 0
    for move in moves:
        dx, dy = DIR_VECTORS[move]
        x += dx
        y += dy

    return x == 0 and y == 0

```

---

**8. Complexity & Optimization Analysis**

* **Time Complexity:**
* Parity check: $O(1)$.
* Dictionary lookup & addition: $O(1)$ per step.
* Loop sweeps $N$ characters: $O(N)$ total runtime.


* **Space Complexity:**
* $O(1)$ auxiliary space. `DIR_VECTORS` table has fixed size $4$. No dynamic allocations per step.


* **Performance Note:** Inlining $(dx, dy)$ addition directly to scalar accumulators avoids creating temporary tuple objects on every step, minimizing garbage collection overhead during large inputs ($N = 10^5$).