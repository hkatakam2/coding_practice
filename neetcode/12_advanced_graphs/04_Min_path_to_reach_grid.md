# question
You are given a square 2-D matrix of distinct integers grid where each integer grid[i][j] represents the elevation at position (i, j).
Rain starts to fall at time = 0, which causes the water level to rise. At time t, the water level across the entire grid is t.
You may swim either horizontally or vertically in the grid between two adjacent squares if the original elevation of both squares is less than or equal to the water level at time t.
Starting from the top left square (0, 0), return the minimum amount of time it will take until it is possible to reach the bottom right square (n - 1, n - 1).

**1. Restating the Question**
Find path from top-left `(0,0)` to bottom-right `(n-1, n-1)`. Time `t` equals water level. Can only step on cell if its elevation is `<= t`. Goal: Find a path that minimizes the maximum elevation encountered along the way.

**2. Clarifying Questions & Confirming I/O**

* **Inputs:** `grid` (list of lists of ints). Size $N \times N$. Elements distinct.
* **Outputs:** `int` (minimum time `t` to reach end).
* **Movement:** 4-directional (up, down, left, right).
* **Start/End:** Always start at `(0,0)`. Always end at `(N-1, N-1)`.
* **Wait:** We can "wait" at any cell for water to rise. The cost of a path is strictly the maximum elevation node in that path.

**3. Hand-Tracing Example**
Grid:

```
0  1  2
4  8  3
7  6  5

```

* Start `0`. Current max path cost = `0`. Neighbors: `1`, `4`.
* Best path forward is `1` (cost becomes max(0, 1) = `1`).
* From `1`, neighbors: `2`, `8`. Pick `2` (cost = `2`).
* From `2`, neighbor: `3` (cost = `3`).
* From `3`, neighbor: `5` (cost = `5`). End reached.
* Path: `0 -> 1 -> 2 -> 3 -> 5`. Max elevation = `5`. Answer: `5`.

**4. Brainstorming Solutions**

* **Approach A:** Binary Search + BFS/DFS.
* Guess a time `t` between $0$ and $N^2-1$.
* Run BFS/DFS. Only traverse cells `<= t`.
* Complexity: $O(N^2 \log(\text{max value}))$. Simple, but does redundant traversals.


* **Approach B:** Modified Dijkstra (Min-Heap).
* Track `max_elevation_so_far` for each path.
* Always expand the frontier using the cell with the lowest `max_elevation_so_far`.
* Complexity: $O(N^2 \log N)$. State space is $N^2$, heap ops take $\log(N^2) \approx \log N$.



**5. Suggested Solution**
Approach B (Modified Dijkstra) is preferred. It's direct, avoids guessing via binary search, and the manual trace in Step 3 exactly mirrors how Dijkstra dynamically picks the next lowest-cost node to expand.

**6. Implementation Outline**

```python
def swimInWater(grid):  # -> int
    """
    Reframe: Find path from start to end minimizing the maximum node value along it.
    State: Min-heap storing tuples of (max_elevation_so_far, row, col); Visited matrix/set. Chosen because min-heap guarantees we always expand the easiest/lowest-water-level paths first.
    Invariant: The top of the heap always represents the absolute lowest possible water level required to reach the extracted cell from the start.

    get_neighbors(cell) = yields adjacent valid coordinates not yet visited.
    is_end(cell) = true if cell is the bottom-right corner.

    Core logic:
    - initialize heap with starting cell and its elevation, mark start as visited
    - while heap has items:
        - pop cell with smallest max_elevation_so_far
        - if cell is the end, return max_elevation_so_far
        - for each unvisited neighbor:
            - calculate new max elevation (max of current path's elevation and neighbor's elevation)
            - add neighbor to heap and mark visited
    Edge cases:
    - Grid is 1x1 size (start is end).
    """

```

**7. Iterative Implementation**

*Iteration 1: Skeleton with helper stubs.*

```python
import heapq

def swimInWater(grid):
    n = len(grid)
    
    # Stubs
    def get_neighbors(r, c):
        # TODO: yield valid r, c
        pass
        
    def is_end(r, c):
        return r == n - 1 and c == n - 1

    # Core logic skeleton
    # pq stores (max_elevation, r, c)
    pq = []
    visited = set()
    
    # TODO: Push start node to pq and visited
    
    while pq:
        # TODO: pop min element
        # TODO: check if end
        # TODO: explore neighbors and push to pq
        pass

```

*Iteration 2: Fleshing out core logic (happy path).*

```python
import heapq

def swimInWater(grid):
    n = len(grid)
    
    def get_neighbors(r, c):
        # TODO: yield valid r, c
        pass
        
    def is_end(r, c):
        return r == n - 1 and c == n - 1

    # Initialize heap and visited
    pq = [(grid[0][0], 0, 0)] # Changed: Add start node
    visited = {(0, 0)}        # Changed: Track visited
    
    while pq:
        current_max, r, c = heapq.heappop(pq) # Changed: Pop smallest barrier path
        
        if is_end(r, c):                      # Changed: Terminate if end reached
            return current_max
            
        for nr, nc in get_neighbors(r, c):    # Changed: Explore neighbors
            if (nr, nc) not in visited:
                visited.add((nr, nc))
                # Calculate new max elevation needed
                new_max = max(current_max, grid[nr][nc])
                heapq.heappush(pq, (new_max, nr, nc))

```

*Iteration 3: Fleshing out helpers and finalizing core.*

```python
import heapq

def swimInWater(grid):
    n = len(grid)
    
    def get_neighbors(r, c):
        # Changed: Implement actual 4-directional boundary checks
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n:
                yield nr, nc
        
    def is_end(r, c):
        return r == n - 1 and c == n - 1

    pq = [(grid[0][0], 0, 0)]
    visited = {(0, 0)}
    
    while pq:
        current_max, r, c = heapq.heappop(pq)
        
        if is_end(r, c):
            return current_max
            
        for nr, nc in get_neighbors(r, c):
            if (nr, nc) not in visited:
                visited.add((nr, nc))
                new_max = max(current_max, grid[nr][nc])
                heapq.heappush(pq, (new_max, nr, nc))

```

*Iteration 4: Edge Cases check.*
Let's check the $1 \times 1$ grid. `n = 1`.
Start node is pushed: `(grid[0][0], 0, 0)`.
Loop starts. Popped `r=0, c=0`. `is_end(0, 0)` evaluates to `True`. Returns `grid[0][0]`.
Logic holds perfectly. No structural patching required.

**8. Complexity & Optimizations**

* **Time Complexity:** $O(N^2 \log N)$. In the worst case, we push every cell into the priority queue once. There are $N^2$ cells. Each heap insertion/extraction takes $O(\log(N^2)) = O(2 \log N) = O(\log N)$.
* **Space Complexity:** $O(N^2)$. The `visited` set and the priority queue `pq` can both store up to $N^2$ elements.
* **Optimization:** Hashing tuples in a Python `set` has a small constant factor overhead. We can optimize space and lookup speed slightly by replacing `visited = set()` with a 2D boolean array: `visited = [[False] * n for _ in range(n)]`.

*Optimized Final Code Snippet:*

```python
import heapq

def swimInWater(grid):
    n = len(grid)
    pq = [(grid[0][0], 0, 0)]
    visited = [[False] * n for _ in range(n)]
    visited[0][0] = True
    
    while pq:
        current_max, r, c = heapq.heappop(pq)
        
        if r == n - 1 and c == n - 1:
            return current_max
            
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and not visited[nr][nc]:
                visited[nr][nc] = True
                heapq.heappush(pq, (max(current_max, grid[nr][nc]), nr, nc))

```