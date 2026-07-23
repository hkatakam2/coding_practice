**1. Restating the question**
Given `m x n` grid.
Values: `-1` (water/obstacle), `0` (treasure), `INF` (land).
Goal: Replace `INF` with shortest distance to nearest `0`.
Movement: Up, down, left, right.
Constraints: Update grid in-place. If unreachable, keep `INF`.

**2. Clarifying questions & I/O**

* Input: `grid`, List of List of ints. `INF` is `2^31 - 1`.
* Output: None. Mutate `grid` in-place.
* Q: Can grid be empty? A: Assume possible, handle it.
* Q: Multiple treasures? A: Yes.
* Q: Disconnected land? A: Yes, should remain `INF`.

**3. Example by hand**
Input grid:
`INF  -1  0  INF`
`INF INF INF  -1`
`INF  -1 INF  -1`
`  0  -1 INF INF`

Trace:
Find treasures: (0,2) and (3,0).
Step 1 (dist 1):
From (0,2) -> (0,3) becomes 1, (1,2) becomes 1.
From (3,0) -> (2,0) becomes 1.
Step 2 (dist 2):
From (1,2) -> (1,1) becomes 2, (2,2) becomes 2.
From (2,0) -> (1,0) becomes 2.
Step 3 (dist 3):
From (2,2) -> (3,2) becomes 3.
From (1,0) -> (0,0) becomes 3.
Step 4 (dist 4):
From (3,2) -> (3,3) becomes 4.

Output:
`  3  -1   0   1`
`  2   2   1  -1`
`  1  -1   2  -1`
`  0  -1   3   4`

**4. Brainstorming & Complexity**

* Idea 1 (Brute force): For every `INF`, run BFS to find nearest `0`.
Complexity: O(K * M * N) where K is number of `INF` cells. Very slow.
* Idea 2 (Multi-source BFS): Same as manual trace. Start at all `0`s simultaneously. Radiate outwards layer by layer. First time we hit an `INF`, it's the shortest path.
Complexity: O(M * N) time. Each cell visited once. O(M * N) space for queue.

**5. Suggest solutions**
Prefer Idea 2. Multi-source BFS is simple, mimics the manual trace perfectly, and is optimal. No clever tricks, just standard queue-based BFS.

**6. Outline selected implementation**

```python
def fill_distances(grid): # -> None
    """
    Reframe: Instead of searching from land to treasure, flow water from all treasures to land simultaneously.
    State: Queue of grid coordinates, chosen because BFS naturally processes layer-by-layer for shortest paths.
    Invariant: When a cell is popped from queue, its shortest distance is finalized.

    get_treasures(grid) = scans grid, returns list of all (row, col) with value 0.
    get_valid_neighbors(r, c) = returns adjacent (row, col) that are inside grid bounds and currently equal to INF.

    Core logic:
    - Find all treasure coordinates and put them in a queue
    - While queue is not empty:
        - Take the next cell from queue
        - For each of its valid neighbors:
            - Set neighbor's grid value to current cell's grid value + 1
            - Add neighbor to queue
            
    Edge cases:
    - Empty grid or empty rows
    - No treasures in grid
    - No land in grid
    - Land surrounded by water (unreachable, remains INF)
    """

```

**7. Iterative implementation**

*Iteration 1: Skeleton with stubs*

```python
from collections import deque

def fill_distances(grid):
    # TODO: Handle edge cases later
    
    queue = deque()
    
    # 1. Find treasures
    # queue.extend(get_treasures(grid))
    
    # 2. Process queue
    while queue:
        # curr = queue.popleft()
        # for neighbor in get_valid_neighbors(curr):
            # update neighbor distance
            # queue.append(neighbor)
    pass

```

*Iteration 2: Fill queue and core loop*

```python
from collections import deque

def fill_distances(grid):
    # TODO: edge cases
    
    queue = deque()
    ROWS, COLS = len(grid), len(grid[0])
    
    # Find treasures
    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c] == 0:
                queue.append((r, c))
                
    # Process queue
    while queue:
        r, c = queue.popleft()
        
        # TODO: inline get_valid_neighbors
        # for nr, nc in get_valid_neighbors(r, c):
        #    grid[nr][nc] = grid[r][c] + 1
        #    queue.append((nr, nc))

```

*Iteration 3: Inline neighbor logic (Full Core Logic)*

```python
from collections import deque

def fill_distances(grid):
    # TODO: edge cases
    
    queue = deque()
    ROWS, COLS = len(grid), len(grid[0])
    INF = 2147483647
    
    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c] == 0:
                queue.append((r, c))
                
    directions = [(1,0), (-1,0), (0,1), (0,-1)]
    
    while queue:
        r, c = queue.popleft()
        
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            
            # Check bounds and if it is unvisited land
            if 0 <= nr < ROWS and 0 <= nc < COLS and grid[nr][nc] == INF:
                grid[nr][nc] = grid[r][c] + 1
                queue.append((nr, nc))

```

*Iteration 4: Walk edge cases*

* *Empty grid or empty rows:* `len(grid)` will fail or `len(grid[0])` will fail. Need early exit.
* *No treasures / no land / isolated land:* Core logic handles perfectly. Queue just empties or isolated cells fail `if grid[nr][nc] == INF` check.

*Final patched code:*

```python
from collections import deque

def fill_distances(grid):
    # Edge case: empty grid
    if not grid or not grid[0]:
        return
        
    queue = deque()
    ROWS, COLS = len(grid), len(grid[0])
    INF = 2147483647
    
    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c] == 0:
                queue.append((r, c))
                
    directions = [(1,0), (-1,0), (0,1), (0,-1)]
    
    while queue:
        r, c = queue.popleft()
        
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            
            if 0 <= nr < ROWS and 0 <= nc < COLS and grid[nr][nc] == INF:
                grid[nr][nc] = grid[r][c] + 1
                queue.append((nr, nc))

```

**8. Complexity comments & optimizations**

* **Time Complexity:** O(M * N). We iterate over grid once to find `0`s. Then, in BFS, every cell is added to queue at most once and processed at most once (because we immediately change `INF` to a smaller integer, preventing re-queuing).
* **Space Complexity:** O(M * N) for the `deque` in the worst case (e.g., all `0`s or maximum perimeter layer).
* **Optimizations:** Using `collections.deque` instead of a list ensures `popleft()` is O(1) instead of O(N). `directions` array prevents duplicate boundary check code. Modifying in-place avoids allocating a new grid. Code is optimal as is.