### 1. Restatement

We are given a 2D grid made of characters, where `'1'` represents land and `'0'` represents water. Our goal is to count the total number of distinct islands.
An island is defined as a group of `'1'`s connected vertically or horizontally. We can assume that anything outside the bounds of the grid is water, meaning islands won't wrap around the edges. We need to return an integer representing this count.

### 2. Clarifying questions and assumptions

Before writing code, I would clarify a few details with the interviewer:

* **Input size:** How large can the grid be? (Assumption: Typical interview constraints, e.g., up to 300x300. This helps evaluate recursion depth limits).
* **Null or empty input:** Can the grid be null or empty? (Assumption: Yes, I should handle `null` or a `0x0` grid safely by returning 0).
* **Grid mutation:** Can I modify the input `grid` in place to mark visited land? (Assumption: Yes. If the caller needs the original grid preserved, I would allocate a separate `boolean[][] visited` matrix, but mutating in place is a common, space-efficient approach for this specific problem).
* **Data type:** The prompt mentions `'1'` and `'0'`, so the input is a `char[][]`. The return type will be an `int`.

### 3. Manual example

Let's trace a representative grid:

```text
Grid:
[ 1, 1, 0, 0 ]
[ 1, 0, 0, 1 ]
[ 0, 0, 1, 1 ]

```

**Process:**

1. Scan top-left to bottom-right.
2. `(0, 0)` is `'1'`. This is a new island! `count = 1`.
3. To avoid double-counting, we "sink" this island by finding all connected `'1'`s and turning them to `'0'`.
* Sink `(0,0)`, then look around.
* Sink `(0,1)`, then look around.
* Sink `(1,0)`, then look around.
* The grid now looks like:
```text
[ 0, 0, 0, 0 ]
[ 0, 0, 0, 1 ]
[ 0, 0, 1, 1 ]

```




4. Continue scanning from `(0, 1)`. It's now `'0'`, so we skip.
5. Reach `(1, 3)`. It's `'1'`. `count = 2`. Sink it and its neighbors. (Grid mutates again).
6. Reach `(2, 2)`. It's `'1'`. `count = 3`. Sink it and its neighbor at `(2, 3)`.
7. Finish scanning the grid.

**Result:** `3`.

### 4. Candidate solutions

**Approach 1: Depth-First Search (DFS)**

* **Core idea:** Iterate through the grid. When we find a `'1'`, increment our island count, then immediately recursively visit its neighbors to change them to `'0'`.
* **Time complexity:** O(M × N), where M is rows and N is columns. Every cell is visited a constant number of times.
* **Space complexity:** O(M × N) worst case for the recursion call stack if the grid is filled with a "snake-like" island.
* **Tradeoffs:** Very easy to implement and read. The risk of StackOverflow exists for massive grids, but fits standard constraints perfectly.

**Approach 2: Breadth-First Search (BFS)**

* **Core idea:** Similar to DFS, but we use a `Queue` to iteratively sink the island level by level.
* **Time complexity:** O(M × N).
* **Space complexity:** O(min(M, N)) for the maximum size of the queue.
* **Tradeoffs:** Prevents StackOverflow on deep grids, but requires more boilerplate code (managing a queue, creating a state object or coordinate arithmetic for queue entries).

**Approach 3: Union-Find (Disjoint Set)**

* **Core idea:** Treat the grid as a graph, union adjacent `'1'`s, and count the distinct sets.
* **Time complexity:** O(M × N × α(M × N)).
* **Space complexity:** O(M × N) for the parent and rank arrays.
* **Tradeoffs:** Overkill for this problem unless we are dealing with a dynamic grid where islands are added over time.

### 5. Selected solution and justification

I will use **Approach 1 (DFS)**.
It directly models the human process of discovering a piece of land and tracing its boundaries until the whole island is accounted for. Modifying the grid in place by changing `'1'`s to `'0'`s acts as our "visited" state. It requires the least amount of boilerplate, is highly readable, and perfectly fits standard interview grid sizes.

### 6. Plain-English implementation outline

```java
int numIslands(char[][] grid) {
    /*
     * Reframe:
     * Scan the grid cell by cell. Count each newly discovered piece of land, 
     * and immediately "sink" the entire island so it isn't counted again.
     *
     * State:
     * The grid itself acts as our visited tracker, mutated in-place ('1' -> '0').
     * Chosen because it saves O(M*N) auxiliary space.
     *
     * Invariant:
     * Any '1' encountered in the main loop is strictly the first cell of a 
     * previously undiscovered island.
     *
     * Helpers:
     * sinkIsland(grid, row, col)
     * - recursively visits the cell and its orthogonal neighbors, turning 
     *   all connected '1's into '0's.
     *
     * Core logic:
     * - check for a null or empty grid
     * - initialize an island count to 0
     * - loop through every row and column
     * - if the current cell is '1':
     *     - increment the island count
     *     - call sinkIsland to erase the connected land
     * - return the count
     *
     * Edge cases:
     * - null or empty grid
     * - recursive calls going out of bounds
     * - cells that are already '0'
     */
}

```

### 7. Iterative Java implementation

**Iteration 1: Method skeleton**
I will set up the main traversal loop and stub out the helper method.

```java
public int numIslands(char[][] grid) {
    int islandCount = 0;
    int rows = grid.length;
    int cols = grid[0].length;
    
    for (int r = 0; r < rows; r++) {
        for (int c = 0; c < cols; c++) {
            // TODO: check if land, increment count, and sink island
        }
    }
    
    return islandCount;
}

private void sinkIsland(char[][] grid, int row, int col) {
    // TODO: implement DFS
}

```

**Iteration 2: Completing the main loop**
Now, I'll translate the core logic into the main loop. Whenever we see a `'1'`, it guarantees a new island due to our invariant.

```java
public int numIslands(char[][] grid) {
    int islandCount = 0;
    int rows = grid.length;
    int cols = grid[0].length;
    
    for (int r = 0; r < rows; r++) {
        for (int c = 0; c < cols; c++) {
            // Added: check for land
            if (grid[r][c] == '1') {
                islandCount++;
                sinkIsland(grid, r, c);
            }
        }
    }
    
    return islandCount;
}

private void sinkIsland(char[][] grid, int row, int col) {
    // TODO: implement DFS
}

```

**Iteration 3: Implementing the DFS helper**
Next, I'll implement `sinkIsland` to recursively clear the board. I must ensure the recursive steps safely stop when hitting water or grid boundaries.

```java
public int numIslands(char[][] grid) {
    int islandCount = 0;
    int rows = grid.length;
    int cols = grid[0].length;
    
    for (int r = 0; r < rows; r++) {
        for (int c = 0; c < cols; c++) {
            if (grid[r][c] == '1') {
                islandCount++;
                sinkIsland(grid, r, c);
            }
        }
    }
    
    return islandCount;
}

private void sinkIsland(char[][] grid, int row, int col) {
    // Added: boundary checks to prevent ArrayOutOfBounds
    if (row < 0 || row >= grid.length || col < 0 || col >= grid[0].length) {
        return;
    }
    
    // Added: base case for water or already visited land
    if (grid[row][col] == '0') {
        return;
    }
    
    // Mutate state to prevent infinite loops
    grid[row][col] = '0';
    
    // Sink all 4 neighbors
    sinkIsland(grid, row - 1, col); // up
    sinkIsland(grid, row + 1, col); // down
    sinkIsland(grid, row, col - 1); // left
    sinkIsland(grid, row, col + 1); // right
}

```

**Edge-case pass and patches**

* *Empty or Null Grid:* If `grid` is null or `grid.length == 0`, `grid[0].length` will throw an exception. I must patch this at the beginning of the main method.
* *Out of bounds:* My helper gracefully handles negative indices and indices beyond grid boundaries via the base case.
* *Already '0':* Handled by the second `if` block in the helper.

I'll add the defensive check for the null/empty grid at the top of the function.

### 8. Final code

```java
public class Solution {
    
    public int numIslands(char[][] grid) {
        if (grid == null || grid.length == 0) {
            return 0;
        }

        int islandCount = 0;
        int rows = grid.length;
        int cols = grid[0].length;
        
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                if (grid[r][c] == '1') {
                    islandCount++;
                    sinkIsland(grid, r, c);
                }
            }
        }
        
        return islandCount;
    }

    private void sinkIsland(char[][] grid, int row, int col) {
        if (row < 0 || row >= grid.length || col < 0 || col >= grid[0].length) {
            return;
        }
        
        if (grid[row][col] == '0') {
            return;
        }
        
        // Mark as visited by sinking it
        grid[row][col] = '0';
        
        // Recursively visit all 4 orthogonal directions
        sinkIsland(grid, row - 1, col); 
        sinkIsland(grid, row + 1, col); 
        sinkIsland(grid, row, col - 1); 
        sinkIsland(grid, row, col + 1); 
    }
}

```

### Complexity

* **Time Complexity: O(M × N).** We iterate through every cell in the nested loop exactly once. During the DFS, a cell is visited at most 4 times by its neighbors before hitting the base case and returning. Thus, total operations scale linearly with the number of cells in the grid.
* **Space Complexity: O(M × N).** Modifying the grid in place allows us to achieve O(1) auxiliary space *excluding* the recursion stack. In the worst-case scenario (e.g., the entire grid is one zig-zagging continuous piece of land), the depth of the recursive call stack will be O(M × N).

### Brief test walkthrough

Let's mentally test the smallest valid input: a `1x1` grid with `[['1']]`.

1. `grid` is not null or empty. `rows = 1`, `cols = 1`.
2. Loop starts at `(0,0)`. `grid[0][0] == '1'`.
3. `islandCount` becomes `1`.
4. `sinkIsland(grid, 0, 0)` is called.
5. Bounds are valid. It's not `'0'`.
6. `grid[0][0]` becomes `'0'`.
7. The four recursive calls are made for `(-1,0)`, `(1,0)`, `(0,-1)`, `(0,1)`.
8. Every single recursive call triggers the `row < 0 || row >= grid.length ...` base case and returns immediately.
9. DFS completes. Loops terminate. Returns `1`.

This is exactly the expected output, confirming the boundary checks and base cases are completely solid.