## question:
You are given a rectangular island heights where heights[r][c] represents the height above sea level of the cell at coordinate (r, c).
The islands borders the Pacific Ocean from the top and left sides, and borders the Atlantic Ocean from the bottom and right sides.
Water can flow in four directions (up, down, left, or right) from a cell to a neighboring cell with height equal or lower. Water can also flow into the ocean from cells adjacent to the ocean.
Find all cells where water can flow from that cell to both the Pacific and Atlantic oceans. Return it as a 2D list where each element is a list [r, c] representing the row and column of the cell. You may return the answer in any order.

### 1. Restating the Question

Given 2D matrix. Cells: 0 (empty), 1 (fresh), 2 (rotten).
Rotten fruits infect 4-directionally adjacent fresh fruits every minute.
Goal: Find min minutes to rot all fresh fruits. Return -1 if impossible.

### 2. Clarifying Questions & I/O

* **Input:** `List[List[int]]`
* **Output:** `int`
* **Q:** Grid empty? **A:** Assume at least 1x1.
* **Q:** Zero fresh fruits initially? **A:** Return 0. Time elapsed is zero.
* **Q:** Zero rotten initially but some fresh? **A:** Return -1. Will never rot.

### 3. Example Input to Output by Hand

**Input:**
[2, 1, 1]
[1, 1, 0]
[0, 1, 1]

**Simulation:**

* **Min 0:** Rotten at (0,0). Fresh = 6.
* **Min 1:** (0,0) rots (0,1) and (1,0). Fresh = 4.
* **Min 2:** (0,1) rots (0,2). (1,0) rots (1,1). Fresh = 2.
* **Min 3:** (1,1) rots (2,1). Fresh = 1.
* **Min 4:** (2,1) rots (2,2). Fresh = 0.
**Output:** 4.

### 4. Brainstorming & Complexity

* **Idea 1: Full grid scan per minute.** Scan entire grid for 2s. Mark adjacent 1s as "to be rotten". Update grid. Repeat until no changes.
* *Complexity:* Worst case fruit is in a snake-like line. $O(M \times N)$ scans $\times$ $O(M \times N)$ cells = $O((M \times N)^2)$. Too slow.


* **Idea 2: Multi-source Breadth-First Search (BFS).** Exactly like the manual simulation. Find all 2s initially. Put in queue. Expand layer by layer. Track fresh count. Stop when queue empty.
* *Complexity:* Visit each cell once. Time $O(M \times N)$. Space $O(M \times N)$ for queue. Optimal.



### 5. Suggested Solutions

Prefer Idea 2 (Multi-source BFS). It directly models the physical spread of rot minute-by-minute. Idea 1 is brute force. Idea 2 matches the "by hand" simulation.

### 6. Outline of Implementation

```python
def orangesRotting(grid): # -> int
    """
    Reframe: Multi-source shortest path problem.
    State: Queue holding coordinates of newly rotten fruits, int tracking fresh fruit count. Chosen because BFS naturally models simultaneous step-by-step layer expansion.
    Invariant: Queue only contains fruits that rotted in the current or previous minute.

    get_fresh_neighbors(grid, cell) = returns adjacent cell coordinates containing fresh fruit.

    Core logic:
    - count total fresh fruits and enqueue all initially rotten fruits
    - loop while queue has fruits and fresh fruits remain:
        - for each fruit currently in queue (representing current minute):
            - get its fresh neighbors
            - mark them rotten in grid
            - enqueue them for next minute
            - decrement fresh count
        - increment minutes passed
    
    Edge cases:
    - zero fresh fruits at start (return 0 immediately)
    - unreachable fresh fruits remain after queue empties (return -1)
    """

```

### 7. Iterative Implementation

**Iteration 1: Skeleton**

```python
def orangesRotting(grid):
    # TODO: init queue and count fresh
    # TODO: loop queue layer by layer
        # TODO: process neighbors
    # TODO: return minutes or -1
    pass

```

**Iteration 2: Fleshing out core logic with helpers**

```python
def orangesRotting(grid):
    # Added state variables and main loop structure
    queue, fresh_count = setup_state(grid)
    minutes = 0

    while queue and fresh_count > 0:
        layer_size = len(queue)
        for _ in range(layer_size):
            r, c = queue.pop(0) # dequeue
            
            neighbors = get_fresh_neighbors(grid, r, c)
            for nr, nc in neighbors:
                grid[nr][nc] = 2 # mark rotten
                queue.append((nr, nc))
                fresh_count -= 1
                
        minutes += 1

    return minutes

```

**Iteration 3: Realizing helpers & full core logic**

```python
def orangesRotting(grid):
    # Replaced setup_state with actual iteration
    queue = []
    fresh_count = 0
    rows, cols = len(grid), len(grid[0])
    
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                queue.append((r, c))
            elif grid[r][c] == 1:
                fresh_count += 1

    minutes = 0
    directions = [(1,0), (-1,0), (0,1), (0,-1)]

    while queue and fresh_count > 0:
        layer_size = len(queue)
        for _ in range(layer_size):
            r, c = queue.pop(0)
            
            # Replaced get_fresh_neighbors with inline logic
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                # Check bounds and if fresh
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                    grid[nr][nc] = 2 
                    queue.append((nr, nc))
                    fresh_count -= 1
                    
        minutes += 1

    return minutes

```

**Iteration 4: Patching Edge Cases**

```python
def orangesRotting(grid):
    queue = []
    fresh_count = 0
    rows, cols = len(grid), len(grid[0])
    
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                queue.append((r, c))
            elif grid[r][c] == 1:
                fresh_count += 1

    # Edge case 1: No fresh fruits to begin with
    if fresh_count == 0:
        return 0

    minutes = 0
    directions = [(1,0), (-1,0), (0,1), (0,-1)]

    while queue and fresh_count > 0:
        layer_size = len(queue)
        for _ in range(layer_size):
            r, c = queue.pop(0)
            
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                    grid[nr][nc] = 2 
                    queue.append((nr, nc))
                    fresh_count -= 1
                    
        minutes += 1

    # Edge case 2: Queue empty but fresh fruits remain (unreachable)
    return minutes if fresh_count == 0 else -1

```

### 8. Complexity & Optimizations

**Complexity:**

* **Time:** $O(M \times N)$. Every cell visited once during setup. Every cell added to queue at most once.
* **Space:** $O(M \times N)$. Queue size worst case holds all cells. Space saved by modifying grid in-place instead of `visited` set.

**Optimization:**
`queue.pop(0)` on standard Python list is $O(K)$ time, forcing elements to shift. Expensive.
Fix: Use `collections.deque` for $O(1)$ `popleft()`.

**Final Optimized Code:**

```python
from collections import deque

def orangesRotting(grid):
    queue = deque() # Optimized
    fresh_count = 0
    rows, cols = len(grid), len(grid[0])
    
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                queue.append((r, c))
            elif grid[r][c] == 1:
                fresh_count += 1

    if fresh_count == 0:
        return 0

    minutes = 0
    directions = [(1,0), (-1,0), (0,1), (0,-1)]

    while queue and fresh_count > 0:
        layer_size = len(queue)
        for _ in range(layer_size):
            r, c = queue.popleft() # O(1) operation now
            
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                    grid[nr][nc] = 2 
                    queue.append((nr, nc))
                    fresh_count -= 1
                    
        minutes += 1

    return minutes if fresh_count == 0 else -1

```