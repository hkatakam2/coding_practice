### 1. Restate the problem

We are given a 2D array of integers (a matrix) with dimensions $m \times n$.
We need to traverse the matrix starting from the top-left corner, moving in a spiral pattern (right, then down, then left, then up, repeating).
We must return a 1D list containing all the elements in the exact order they are encountered during this spiral walk.

### 2. Ask clarifying questions

In a real interview, I would confirm these details:

* **Input dimensions:** Can the matrix be empty? (I will assume `matrix` might be empty or null, which should return an empty list.)
* **Aspect ratio:** Can it be non-square? (Yes, $m \times n$ means it could be $1 \times 5$ or $4 \times 2$.)
* **Input modification:** Am I allowed to mutate the matrix to mark cells as visited? (I will assume the input should remain pristine. Mutating arguments is generally discouraged unless explicitly permitted.)
* **Value bounds:** Are there specific constraints on the integer values? (If values were restricted to positive numbers, we could mark visited cells by making them negative. Assuming no constraints, we cannot safely mutate them to a "magic number".)

### 3. Work through an example by hand

Let's trace a $3 \times 3$ matrix:

**Input:**

```text
[ 1, 2, 3 ]
[ 4, 5, 6 ]
[ 7, 8, 9 ]

```

* **State:** Start at `(0,0)`, facing **Right**.
* **Step 1:** Walk right. Take `1, 2, 3`.
* *Next cell* is out of bounds (hit the right wall).
* *Action:* Turn 90 degrees right (now facing **Down**).


* **Step 2:** Walk down. Take `6, 9`.
* *Next cell* is out of bounds (hit the bottom floor).
* *Action:* Turn 90 degrees right (now facing **Left**).


* **Step 3:** Walk left. Take `8, 7`.
* *Next cell* is out of bounds (hit the left wall).
* *Action:* Turn 90 degrees right (now facing **Up**).


* **Step 4:** Walk up. Take `4`.
* *Next cell* is `(0,0)`, which contains `1`. We already visited it!
* *Action:* Turn 90 degrees right (now facing **Right**).


* **Step 5:** Walk right. Take `5`.
* *Next cell* is `(1,2)`, which contains `6` (already visited).
* *Action:* Turn 90 degrees right... wait, we have collected exactly $3 \times 3 = 9$ elements. We are done.


* **Final Result:** `[1, 2, 3, 6, 9, 8, 7, 4, 5]`.

### 4. Brainstorm solutions aloud

**Approach 1: Boundary Tracking (Layer Peeling)**

* *Core idea:* Maintain four pointers (`top`, `bottom`, `left`, `right`) and peel off the outer perimeter using four sequential loops, shrinking the boundaries inward.
* *Tradeoffs:* It operates in $O(1)$ auxiliary space, but the loop control logic and inner boundary checks can sometimes feel abstract or prone to off-by-one errors.

**Approach 2: Simulation with Direction Vectors (The Intuitive Path)**

* *Core idea:* Exactly as we traced by hand. We start at `(0,0)` moving right. If our next step would take us out of bounds or into an already-visited cell, we turn 90 degrees clockwise. We repeat this exactly $m \times n$ times because there are exactly that many elements in the matrix.
* *Data structures:* An array of direction vectors for row and column changes, and a `boolean[][] visited` matrix to track where we have been.
* *Time complexity:* $O(m \times n)$, as we process each cell once and do constant-time boundary checks.
* *Space complexity:* $O(m \times n)$ auxiliary space for the `visited` matrix.
* *Tradeoffs:* It uses extra memory for the `boolean` matrix, but the control flow is incredibly straightforward and mirrors physical intuition perfectly.

### 5. Select the solution

As you prefer, I will proceed with **Approach 2: Simulation with Direction Vectors**.
It aligns perfectly with the mental model of physically walking through the matrix. The code naturally explains itself through state transitions (moving forward vs. turning). I will use a `boolean[][]` array to keep the original matrix pristine, ensuring no destructive side effects.

### 6. Write the implementation outline

```java
List<Integer> spiralOrder(int[][] matrix) {
    /*
     * Reframe:
     * Simulate a walk through the matrix, changing direction 90 degrees 
     * clockwise whenever we hit a wall or a previously visited cell.
     *
     * State:
     * - boolean[][] visited: tracks which cells we have already collected.
     *   Chosen because it cleanly separates visitation logic from the data.
     * - dr, dc arrays: represent the row/col changes for Right, Down, Left, Up.
     * - Current position (r, c) and current direction index (di).
     *
     * Invariant:
     * The loop runs exactly (rows * cols) times. Every iteration, the current 
     * cell is valid and unvisited.
     *
     * Core logic:
     * - calculate total elements (rows * cols)
     * - loop exactly that many times
     * - record the current cell and mark it visited
     * - calculate the proposed next coordinates
     * - if the next coordinates are out of bounds or already visited:
     *   - turn 90 degrees right (increment direction index modulo 4)
     *   - recalculate next coordinates
     * - move current position to the next coordinates
     *
     * Edge cases:
     * - null matrix or 0 rows/cols
     */
}

```

### 7. Implement iteratively

**Iteration 1: Method skeleton and state setup**
First, we establish our safety checks, state variables, and the direction vectors that map to Right, Down, Left, Up.

```java
public List<Integer> spiralOrder(int[][] matrix) {
    List<Integer> result = new ArrayList<>();
    if (matrix == null || matrix.length == 0 || matrix[0].length == 0) {
        return result;
    }

    int rows = matrix.length;
    int cols = matrix[0].length;
    boolean[][] visited = new boolean[rows][cols];

    // Direction vectors: Right, Down, Left, Up
    int[] dr = {0, 1, 0, -1};
    int[] dc = {1, 0, -1, 0};

    int r = 0;
    int c = 0;
    int di = 0; // Starts at 0 (Right)

    // TODO: loop through all elements and simulate the walk

    return result;
}

```

*Why this setup:* The `dr` and `dc` arrays are a standard trick in grid-traversal problems. `dr[0], dc[0]` is `(0, 1)`, meaning row stays the same, column increases (moving Right).

**Iteration 2: The main traversal loop**
Now we add the loop that runs exactly `rows * cols` times. We'll capture the current element and compute the next step.

```java
public List<Integer> spiralOrder(int[][] matrix) {
    List<Integer> result = new ArrayList<>();
    if (matrix == null || matrix.length == 0 || matrix[0].length == 0) {
        return result;
    }

    int rows = matrix.length;
    int cols = matrix[0].length;
    boolean[][] visited = new boolean[rows][cols];

    int[] dr = {0, 1, 0, -1};
    int[] dc = {1, 0, -1, 0};

    int r = 0;
    int c = 0;
    int di = 0;

    // Added: We need exactly rows * cols elements.
    int totalElements = rows * cols;
    for (int i = 0; i < totalElements; i++) {
        result.add(matrix[r][c]);
        visited[r][c] = true;

        // Added: Propose the next cell to move into
        int nextR = r + dr[di];
        int nextC = c + dc[di];

        // TODO: Validate nextR and nextC, turn if necessary

        r = nextR;
        c = nextC;
    }

    return result;
}

```

**Iteration 3: The turn logic (Complete Happy Path)**
Finally, we add the boundary and visited checks. If the proposed cell is invalid, we turn.

```java
public List<Integer> spiralOrder(int[][] matrix) {
    List<Integer> result = new ArrayList<>();
    if (matrix == null || matrix.length == 0 || matrix[0].length == 0) {
        return result;
    }

    int rows = matrix.length;
    int cols = matrix[0].length;
    boolean[][] visited = new boolean[rows][cols];

    int[] dr = {0, 1, 0, -1};
    int[] dc = {1, 0, -1, 0};

    int r = 0;
    int c = 0;
    int di = 0;

    int totalElements = rows * cols;
    for (int i = 0; i < totalElements; i++) {
        result.add(matrix[r][c]);
        visited[r][c] = true;

        int nextR = r + dr[di];
        int nextC = c + dc[di];

        // Added: Check if we hit a boundary OR a previously visited cell
        if (nextR < 0 || nextR >= rows || nextC < 0 || nextC >= cols || visited[nextR][nextC]) {
            // Turn 90 degrees clockwise
            di = (di + 1) % 4;
            // Recalculate next step in the new direction
            nextR = r + dr[di];
            nextC = c + dc[di];
        }

        r = nextR;
        c = nextC;
    }

    return result;
}

```

**Edge-case pass**

* *Empty array:* Handled at the top via `matrix == null || matrix.length == 0`. Returns empty list.
* *1x1 matrix:* `totalElements = 1`. Loop runs once. Takes `matrix[0][0]`, marks visited. `nextR`/`nextC` goes out of bounds, turns down, recalculates. Loop finishes before using the new coordinates. Works perfectly.
* *Single Row (e.g., $1 \times 3$):* Moves right twice, hits right wall, turns down. Fails because down is out of bounds? Wait! Because total elements is 3, the loop runs exactly 3 times. On the third iteration (the last element of the row), it hits the right wall, turns down, recalculates `nextR` to be out of bounds. But then the loop immediately terminates because `i` hits `totalElements`. The invalid state is never accessed. **The fixed loop count implicitly protects us from infinite turns or out-of-bounds crashes.**

### 8. Analyze expensive sections and optimize

* **Time Complexity:** $O(m \times n)$. We iterate exactly $m \times n$ times. Inside the loop, array lookups and arithmetic operations are $O(1)$. This is optimal, as we must read every element.
* **Space Complexity:** $O(m \times n)$ auxiliary space due to the `boolean[][] visited` matrix.
* *Note on optimization:* If we were allowed to mutate the input array, and we knew the integer values were restricted to a specific range (e.g., $1 \le \text{matrix}[i][j] \le 100$), we could avoid the `visited` array by setting elements to a magic number like `-1000` once visited. Since we don't have those constraints, allocating a `boolean[][]` is the correct, safe software engineering choice.



### Final Code

```java
import java.util.ArrayList;
import java.util.List;

public class Solution {
    
    public List<Integer> spiralOrder(int[][] matrix) {
        List<Integer> result = new ArrayList<>();
        
        if (matrix == null || matrix.length == 0 || matrix[0].length == 0) {
            return result;
        }

        int rows = matrix.length;
        int cols = matrix[0].length;
        boolean[][] visited = new boolean[rows][cols];

        // Directions: Right, Down, Left, Up
        int[] dr = {0, 1, 0, -1};
        int[] dc = {1, 0, -1, 0};

        int r = 0;
        int c = 0;
        int di = 0; // Starts pointing Right

        int totalElements = rows * cols;
        for (int i = 0; i < totalElements; i++) {
            // Process current cell
            result.add(matrix[r][c]);
            visited[r][c] = true;

            // Propose the next cell
            int nextR = r + dr[di];
            int nextC = c + dc[di];

            // If out of bounds or already visited, turn 90 degrees right
            if (nextR < 0 || nextR >= rows || nextC < 0 || nextC >= cols || visited[nextR][nextC]) {
                di = (di + 1) % 4; // 0->1->2->3->0
                
                nextR = r + dr[di];
                nextC = c + dc[di];
            }

            // Move to the valid next cell
            r = nextR;
            c = nextC;
        }

        return result;
    }
}

```

### Brief test walkthrough

Let's stress test a $2 \times 2$ matrix.
`[[1, 2],`
`[3, 4]]`

* `totalElements = 4`.
* **i = 0:** Add `1`. `visited[0][0] = true`. `nextR=0, nextC=1`. Valid. Move to `(0,1)`.
* **i = 1:** Add `2`. `visited[0][1] = true`. `nextR=0, nextC=2`. Out of bounds (hit right wall). Turn `di` to 1 (Down). Recalculate: `nextR=1, nextC=1`. Valid. Move to `(1,1)`.
* **i = 2:** Add `4`. `visited[1][1] = true`. `nextR=2, nextC=1`. Out of bounds (hit bottom wall). Turn `di` to 2 (Left). Recalculate: `nextR=1, nextC=0`. Valid. Move to `(1,0)`.
* **i = 3:** Add `3`. `visited[1][0] = true`. `nextR=1, nextC=-1`. Out of bounds (hit left wall). Turn `di` to 3 (Up). Recalculate: `nextR=0, nextC=0`. Loop finishes.
* **Result:** `[1, 2, 4, 3]`. Correct! The simulation elegantly handles the traversal.