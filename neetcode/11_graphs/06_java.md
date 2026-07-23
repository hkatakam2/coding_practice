### 1. Restate the problem

We are given a 2D rectangular grid where each cell's value represents its height above sea level.

* The top and left edges of the grid touch the Pacific Ocean.
* The bottom and right edges touch the Atlantic Ocean.
* Water can flow from any cell to a neighboring cell (up, down, left, right) if the neighboring cell's height is **less than or equal to** the current cell's height.

Our goal is to find all the grid coordinates `[r, c]` from which water can flow to **both** the Pacific and Atlantic oceans. We need to return these coordinates as a list of lists.

### 2. Ask clarifying questions

Before writing code, I would confirm a few details with the interviewer:

* **Grid size:** Can the grid be empty, or have 0 rows/columns? *(Assumption: The grid will have at least 1 row and 1 column, but I will handle empty grids defensively.)*
* **Negative values:** Can heights be negative? *(Assumption: Heights are non-negative integers, though negative values wouldn't break relative comparisons.)*
* **Output ordering:** Does the order of the output coordinates matter? *(Assumption: As stated, any order is acceptable.)*
* **Recursion depth:** If I use a recursive approach, could the grid be large enough (e.g., 1000x1000) to cause a `StackOverflowError`? *(Assumption: Standard interview bounds usually allow O(N) recursion depth, but I will keep this in mind.)*

### 3. Work through an example by hand

Let's use a 3x3 grid to understand the flow:

```text
      Pacific (Top)
      [ 2,  2,  2 ]
(Left)[ 1,  4,  1 ] (Right - Atlantic)
      [ 1,  1,  3 ]
      Atlantic (Bottom)

```

If we trace the flow *forward* (downhill) from each cell:

* `(1, 1)` has height `4`.
* It can flow up to `(0, 1)` height `2` -> Pacific!
* It can flow down to `(2, 1)` height `1` -> Atlantic!
* So `(1, 1)` is in the result.


* `(0, 2)` has height `2`.
* It touches the Pacific (top).
* It cannot flow to `(1, 2)` (height `1`) and then further down because `(2, 2)` is height `3` (uphill). However, wait, it touches the Atlantic on the right edge! So it actually reaches both just by its position.


* `(2, 0)` has height `1`.
* Touches Pacific (left) and Atlantic (bottom). It's in the result.



This forward simulation works, but doing it for every single cell independently feels repetitive.

### 4. Brainstorm solutions aloud

**Approach 1: Forward Traversal (Brute Force)**

* **Core idea:** For every single cell in the grid, run a Breadth-First Search (BFS) or Depth-First Search (DFS) looking for paths to both oceans.
* **Why it works:** It literally simulates water flowing downhill from each starting point.
* **Complexity:** Time is $O((M \times N)^2)$ because in the worst case (a completely flat grid), a DFS from one cell will visit every other cell, and we do this $M \times N$ times. Space is $O(M \times N)$ for the visited set.

**Approach 2: Reverse Traversal (Water flowing uphill)**

* **Core idea:** Instead of asking "Where can water flow *from* here?", we ask "What cells can *reach* the ocean?". We can start at the ocean borders and run a search **uphill** (or flat).
* **Data structures:** We can maintain two boolean matrices: `pacificReachable` and `atlanticReachable`.
* **Why it works:** If a cell can be reached by climbing uphill from the Pacific, it means water can flow downhill from that cell to the Pacific. We do this for both oceans. A cell that is `true` in both matrices is part of our answer.
* **Complexity:** Time is $O(M \times N)$ because we only visit each cell at most once per ocean. Space is $O(M \times N)$ for the boolean matrices and the traversal call stack.

### 5. Select the solution

I will go with **Approach 2 (Reverse Traversal)**.
It is optimal in time complexity, easy to explain, and avoids redundant work. I will use DFS for the traversal because it is straightforward to implement and reads very cleanly without needing to manage a queue explicitly. If the grid were excessively large, I might choose BFS with an `ArrayDeque` to prevent stack overflows, but DFS is generally the standard expectation for this problem size.

### 6. Write the implementation outline

```java
List<List<Integer>> pacificAtlantic(int[][] heights) {
    /*
     * Reframe:
     * Start at the ocean borders and flow "uphill" to find all cells 
     * that can drain into each ocean. Find the intersection of these two sets.
     *
     * State:
     * Two boolean matrices: pacificReachable and atlanticReachable.
     * Chosen because we need fast O(1) intersection checking at the end.
     *
     * Invariant:
     * A cell is marked true in a reachable matrix only if there is a 
     * monotonically descending path from that cell to the respective ocean.
     *
     * Helpers:
     * dfs(row, col, reachableMatrix, previousHeight)
     * - Marks the current cell as reachable.
     * - Recursively visits valid neighbors (within bounds, unvisited, and >= previousHeight).
     *
     * Core logic:
     * - Handle empty grid edge cases.
     * - Launch DFS from the top and left borders for the Pacific.
     * - Launch DFS from the bottom and right borders for the Atlantic.
     * - Scan the grid: if a cell is true in both matrices, add it to the result.
     *
     * Edge cases:
     * - Empty input grid.
     * - 1x1 grid.
     * - All heights are the same (flat terrain).
     */
}

```

### 7. Implement iteratively

#### Iteration 1: Method skeleton

First, I'll set up the main structures, the borders, and the intersection loop.

```java
public List<List<Integer>> pacificAtlantic(int[][] heights) {
    List<List<Integer>> result = new ArrayList<>();
    if (heights == null || heights.length == 0 || heights[0].length == 0) {
        return result;
    }

    int numRows = heights.length;
    int numCols = heights[0].length;

    boolean[][] pacificReachable = new boolean[numRows][numCols];
    boolean[][] atlanticReachable = new boolean[numRows][numCols];

    // TODO: Launch DFS from top/left borders for Pacific
    // TODO: Launch DFS from bottom/right borders for Atlantic

    // Find the intersection
    for (int row = 0; row < numRows; row++) {
        for (int col = 0; col < numCols; col++) {
            if (pacificReachable[row][col] && atlanticReachable[row][col]) {
                result.add(List.of(row, col));
            }
        }
    }

    return result;
}

```

*Explanation:* I've established the output container, handled the null/empty edge case immediately, and set up the matrices. The nested loops at the end handle our intersection requirement.

#### Iteration 2: Adding the boundary loops

Now I will add the logic to initiate the DFS from the ocean borders.

```java
public List<List<Integer>> pacificAtlantic(int[][] heights) {
    List<List<Integer>> result = new ArrayList<>();
    if (heights == null || heights.length == 0 || heights[0].length == 0) {
        return result;
    }

    int numRows = heights.length;
    int numCols = heights[0].length;

    boolean[][] pacificReachable = new boolean[numRows][numCols];
    boolean[][] atlanticReachable = new boolean[numRows][numCols];

    // Added: Launch DFS from the vertical borders (left and right)
    for (int row = 0; row < numRows; row++) {
        dfs(row, 0, pacificReachable, heights[row][0], heights);
        dfs(row, numCols - 1, atlanticReachable, heights[row][numCols - 1], heights);
    }

    // Added: Launch DFS from the horizontal borders (top and bottom)
    for (int col = 0; col < numCols; col++) {
        dfs(0, col, pacificReachable, heights[0][col], heights);
        dfs(numRows - 1, col, atlanticReachable, heights[numRows - 1][col], heights);
    }

    // Find the intersection
    for (int row = 0; row < numRows; row++) {
        for (int col = 0; col < numCols; col++) {
            if (pacificReachable[row][col] && atlanticReachable[row][col]) {
                result.add(List.of(row, col));
            }
        }
    }

    return result;
}

// TODO: Implement dfs helper

```

*Explanation:* The loops iterate along the perimeter of the grid. `0` indices touch the Pacific, while `numRows - 1` and `numCols - 1` touch the Atlantic. I pass the starting cell's height as the "previous height" to the DFS.

#### Iteration 3: Complete the DFS Helper (Happy Path)

Now I'll implement the `dfs` traversal logic. I'll use a `DIRECTIONS` array to keep the neighbor discovery readable.

```java
// Added: Directional vectors to avoid dense index arithmetic
private static final int[][] DIRECTIONS = {{0, 1}, {0, -1}, {1, 0}, {-1, 0}};

private void dfs(int row, int col, boolean[][] reachable, int previousHeight, int[][] heights) {
    // Check bounds
    if (row < 0 || row >= heights.length || col < 0 || col >= heights[0].length) {
        return;
    }
    
    // Check if visited already to prevent infinite loops
    if (reachable[row][col]) {
        return;
    }

    // Water is flowing UPHILL in our simulation. 
    // If the current cell is lower than the previous one, water couldn't have flowed down.
    if (heights[row][col] < previousHeight) {
        return;
    }

    // Mark as reachable from this ocean
    reachable[row][col] = true;

    // Visit all 4 neighbors
    for (int[] direction : DIRECTIONS) {
        int newRow = row + direction[0];
        int newCol = col + direction[1];
        dfs(newRow, newCol, reachable, heights[row][col], heights);
    }
}

```

*Explanation:* The DFS does bounds checking, prevents cyclic loops via the `reachable` boolean array (which doubles as our `visited` set), and enforces the reverse-flow constraint (current height `>=` previous height).

### 8. Edge-case pass and optimization

Let's review the edge cases:

1. **Empty input:** Handled gracefully at the beginning of the main method.
2. **1x1 grid:** The loops will just process `row = 0` and `col = 0`. Both `pacificReachable` and `atlanticReachable` will be marked `true`. The intersection finds it, returning `[[0, 0]]`. This is correct.
3. **Flat terrain (all 1s):** The DFS will traverse the entire grid for both oceans since `heights[row][col] >= previousHeight` evaluates to `1 >= 1` (true). All cells will be marked `true` in both matrices. This is correct.
4. **Recursion Depth:** The maximum depth of the call stack is $O(M \times N)$. In Java, the default stack size can handle around 7,000 to 10,000 deep recursive calls. If a grid is explicitly massive (e.g., $1000 \times 1000$ and perfectly flat), a `StackOverflowError` could occur. If requested, we could switch `dfs` to `bfs` using a `Queue`, but DFS is acceptable for typical grid boundaries (often up to $200 \times 200$).

*Bottlenecks:* Time complexity is strictly linear with respect to the number of cells. There are no redundant scans because the `reachable` array immediately halts duplicate DFS paths. Therefore, further algorithmic optimization is unnecessary.

### 9. Final Code

```java
import java.util.ArrayList;
import java.util.List;

public class PacificAtlanticWaterFlow {

    // Represents movement: Right, Left, Down, Up
    private static final int[][] DIRECTIONS = {{0, 1}, {0, -1}, {1, 0}, {-1, 0}};

    public List<List<Integer>> pacificAtlantic(int[][] heights) {
        List<List<Integer>> result = new ArrayList<>();
        
        // Edge case: empty grid
        if (heights == null || heights.length == 0 || heights[0].length == 0) {
            return result;
        }

        int numRows = heights.length;
        int numCols = heights[0].length;

        boolean[][] pacificReachable = new boolean[numRows][numCols];
        boolean[][] atlanticReachable = new boolean[numRows][numCols];

        // Launch DFS from the vertical borders
        for (int row = 0; row < numRows; row++) {
            // Left edge touches Pacific
            dfs(row, 0, pacificReachable, heights[row][0], heights);
            // Right edge touches Atlantic
            dfs(row, numCols - 1, atlanticReachable, heights[row][numCols - 1], heights);
        }

        // Launch DFS from the horizontal borders
        for (int col = 0; col < numCols; col++) {
            // Top edge touches Pacific
            dfs(0, col, pacificReachable, heights[0][col], heights);
            // Bottom edge touches Atlantic
            dfs(numRows - 1, col, atlanticReachable, heights[numRows - 1][col], heights);
        }

        // Find cells capable of reaching both oceans
        for (int row = 0; row < numRows; row++) {
            for (int col = 0; col < numCols; col++) {
                if (pacificReachable[row][col] && atlanticReachable[row][col]) {
                    result.add(List.of(row, col));
                }
            }
        }

        return result;
    }

    private void dfs(int row, int col, boolean[][] reachable, int previousHeight, int[][] heights) {
        // Stop if out of grid bounds
        if (row < 0 || row >= heights.length || col < 0 || col >= heights[0].length) {
            return;
        }
        
        // Stop if we already visited this cell from this ocean
        if (reachable[row][col]) {
            return;
        }

        // Stop if terrain goes downhill (since we are searching uphill backwards from the ocean)
        if (heights[row][col] < previousHeight) {
            return;
        }

        // Mark current cell as reachable from the ocean
        reachable[row][col] = true;

        // Traverse all four adjacent neighbors
        for (int[] direction : DIRECTIONS) {
            int newRow = row + direction[0];
            int newCol = col + direction[1];
            dfs(newRow, newCol, reachable, heights[row][col], heights);
        }
    }
}

```

### 10. Complexity

* **Time Complexity:** $O(M \times N)$ where $M$ is the number of rows and $N$ is the number of columns. We visit every cell at most once during the Pacific DFS and at most once during the Atlantic DFS.
* **Space Complexity:** $O(M \times N)$ for the two boolean state matrices `pacificReachable` and `atlanticReachable`. Additionally, the recursion call stack could go as deep as $O(M \times N)$ in the worst-case scenario (e.g., a grid where every cell is identical height).

### 11. Test walkthrough

Let's test it mentally with a 2x2 grid to stress the invariants:

```text
[2, 1]
[1, 2]

```

1. **Pacific DFS Setup:**
* Row 0 touches Pacific. We start DFS at `(0,0)=2` and `(0,1)=1`.
* Col 0 touches Pacific. We start DFS at `(0,0)=2` and `(1,0)=1`.
* `(0,0)` marks itself `true`. Its neighbor `(1,0)=1` is strictly less than 2, so water wouldn't flow *up* from `(1,0)` to `(0,0)`. DFS stops going down.
* `(0,1)` marks itself `true`. Its neighbor `(1,1)=2` is `>= 1`, so `(1,1)` is marked Pacific reachable.
* *Resulting Pacific reachable:* `(0,0), (0,1), (1,0), (1,1)` (Actually, all are reachable!).


2. **Atlantic DFS Setup:**
* Row 1 touches Atlantic. DFS at `(1,0)=1`, `(1,1)=2`.
* Col 1 touches Atlantic. DFS at `(0,1)=1`, `(1,1)=2`.
* Similar logic, all cells end up marked `true` for Atlantic as well because there is an uphill path from the borders to every interior cell.


3. **Intersection:**
* All cells are returned: `[[0, 0], [0, 1], [1, 0], [1, 1]]`.
* This matches expectations: from any cell, water can flow directly into an ocean or across flat neighbors. The state tracking and direction correctly handle equality.