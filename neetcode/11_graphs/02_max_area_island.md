### question
You are given a matrix grid where grid[i] is either a 0 (representing water) or 1 (representing land).

An island is defined as a group of 1's connected horizontally or vertically. You may assume all four edges of the grid are surrounded by water.

The area of an island is defined as the number of cells within the island.

Return the maximum area of an island in grid. If no island exists, return 0.

**1. Restating the Question**
Given 2D matrix of 0s (water) and 1s (land).
Island = 1s connected horizontally/vertically.
Area = count of 1s in an island.
Goal: Find largest island area. Return 0 if none.

**2. Clarifying Questions & I/O**

* Empty grid? Return 0.
* Diagonals count? No, strictly up/down/left/right.
* Can we mutate input grid? Assume yes, saves space for `visited` tracking.

**3. Example by Hand**
Grid:

```
1 1 0
1 0 1

```

* Scan row 0, col 0. Found 1. Area = 1.
* Mark as visited (change to 0). Look neighbors.
* Right is 1. Move there. Area = 1 + 1 = 2. Mark visited.
* Down from (0,0) is 1. Move there. Area = 2 + 1 = 3. Mark visited.
* Island 1 complete. Area = 3. Max = 3.
* Keep scanning. Find 1 at (1,2). Area = 1. No land neighbors. Max = max(3,1) = 3.

**4. Brainstorming & Complexity**

* *Approach A (DFS):* Iterate grid. On land, recursive Depth First Search. Count cells, sink island (set 1 to 0). Time O(R*C), Space O(R*C) call stack.
* *Approach B (BFS):* Same, but iterative queue. Time O(R*C), Space O(min(R,C)) queue.
* *Approach C (Union-Find):* Disjoint set for all 1s. Keep track of set sizes. High overhead, complex code.

**5. Suggest Solutions**

* Prefer Approach A (DFS). Mirrors manual hand-trace. Very clean recursion.
* Approach B (BFS) is good but requires more boilerplate (queue management).
* Will implement Approach A.

**6. Outline**

```python
def maxAreaOfIsland(grid): # -> int
    """
    Reframe: Find the largest connected component of 1s.
    State: Mutating grid in-place (1 -> 0), chosen because avoids O(R*C) external visited set.
    Invariant: Unvisited land cells remain 1; visited land and water are 0.

    calculateIslandArea(row, col) = returns area of connected land starting here, sinking it along the way.

    Core logic:
    - set max area to 0
    - scan every cell in grid
    - if cell is land:
        - get area via calculateIslandArea
        - update max area if larger
    - return max area

    Edge cases:
    - empty grid
    - no land (all water)
    """

```

**7. Iterative Implementation**

*Iteration 1: Skeleton core logic*

```python
def maxAreaOfIsland(grid):
    max_area = 0
    
    # scan every cell
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            # if cell is land
            if grid[row][col] == 1:
                # get area via helper and update max
                current_area = calculateIslandArea(grid, row, col)
                max_area = max(max_area, current_area)
                
    return max_area

# TODO: define calculateIslandArea

```

*Iteration 2: Define helper skeleton*

```python
# Added helper stub for DFS
def calculateIslandArea(grid, row, col):
    # TODO: handle out of bounds or water
    
    # mark visited (sink)
    grid[row][col] = 0
    
    # TODO: traverse 4 directions, sum areas + 1 for current cell
    return 1

```

*Iteration 3: Complete helper logic (Happy path realized)*

```python
def calculateIslandArea(grid, row, col):
    # check bounds and water
    if row < 0 or row >= len(grid) or col < 0 or col >= len(grid[0]) or grid[row][col] == 0:
        return 0
        
    # sink land
    grid[row][col] = 0
    
    # sum 4 directions + current cell
    up = calculateIslandArea(grid, row - 1, col)
    down = calculateIslandArea(grid, row + 1, col)
    left = calculateIslandArea(grid, row, col - 1)
    right = calculateIslandArea(grid, row, col + 1)
    
    return 1 + up + down + left + right

```

*Iteration 4: Patching Edge Cases*

* *Edge case: Empty grid.* If `grid` is empty, `len(grid[0])` throws index error. Let's patch `maxAreaOfIsland`.

```python
def maxAreaOfIsland(grid):
    # PATCH: handle empty grid edge case
    if not grid or not grid[0]:
        return 0
        
    max_area = 0
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == 1:
                max_area = max(max_area, calculateIslandArea(grid, row, col))
                
    return max_area

def calculateIslandArea(grid, row, col):
    if row < 0 or row >= len(grid) or col < 0 or col >= len(grid[0]) or grid[row][col] == 0:
        return 0
        
    grid[row][col] = 0
    
    # Inline summation for brevity
    return (1 + 
            calculateIslandArea(grid, row - 1, col) +
            calculateIslandArea(grid, row + 1, col) +
            calculateIslandArea(grid, row, col - 1) +
            calculateIslandArea(grid, row, col + 1))

```

* *Edge case: No land.* Handled naturally. `grid[row][col] == 1` never hits, returns `max_area` (0).

**8. Complexity & Optimizations**

* **Time Complexity:** $O(R \times C)$. We visit every cell. A land cell triggers DFS, but we immediately sink it (`grid[row][col] = 0`). Thus, no cell is processed by DFS more than once.
* **Space Complexity:** $O(R \times C)$ worst case. If the grid is completely filled with 1s in a snake-like pattern, the recursive call stack goes R*C deep.
* **Optimization:** We optimized space by mutating `grid` in-place (sinking islands). If mutation wasn't allowed, we'd need a `Set` for visited coordinates, costing additional $O(R \times C)$ memory.