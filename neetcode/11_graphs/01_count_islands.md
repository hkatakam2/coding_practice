### question
Given a 2D grid grid where '1' represents land and '0' represents water, count and return the number of islands.

An island is formed by connecting adjacent lands horizontally or vertically and is surrounded by water. You may assume water is surrounding the grid (i.e., all the edges are water).

**1. Restating the question**
Given a 2D matrix of '1's (land) and '0's (water). Need to count distinct islands. Island = horizontally or vertically connected '1's. Grid boundaries surrounded by water.

**2. Clarifying questions, confirming I/O**

* Input: `List[List[str]]` (matrix of strings)? Yes.
* Output: `int` (total count)? Yes.
* Diagonal connections? No, only horizontal/vertical.
* Mutating the input grid allowed? Assuming yes to save space.
* Empty grid possible? Yes, should return 0.

**3. Example input to output by hand**
Input:
1 1 0
0 1 0
0 0 1

* Scan left-to-right, top-to-bottom.
* Hit '1' at top-left. Count = 1.
* "Sink" this island so we don't double count. Convert connected '1's to '0's.
Grid becomes:
0 0 0
0 0 0
0 0 1
* Keep scanning. Hit next '1' at bottom-right. Count = 2.
* Sink it.
* Finish scan. Output: 2.

**4. Brainstorming solutions & complexity**

* **Idea 1: DFS Sinking.** Scan grid. On hitting land, increment count, run Depth First Search to turn all connected lands to water.
* Time: O(M*N) to visit every cell.
* Space: O(M*N) worst-case call stack (if grid is one giant snake-like island).


* **Idea 2: BFS Sinking.** Same sweep, but use a Queue to sink.
* Time: O(M*N).
* Space: O(min(M,N)) for queue max width.


* **Idea 3: Union-Find.** Treat lands as nodes, union adjacent lands. Count disjoint sets.
* Time O(M*N * α(M*N)).
* Space O(M*N) for parent arrays. Overkill.



**5. Suggest solutions**
Prefer Idea 1 (DFS Sinking). Mirrors the by-hand logic perfectly. Very clean to explain. BFS is also good but requires queue boilerplate. We'll go with DFS.

**6. Outline of selected implementation**

```python
def numIslands(grid): 
    """
    Reframe: Count connected components by sinking them as we count.
    State: Grid itself (mutated to track visited), chosen because saves O(M*N) auxiliary space.
    Invariant: Any land encountered during the main sweep is the start of a previously unseen island.

    sinkIsland(cell) = recursively turns the current piece of land and all connected land into water.

    Core logic:
    - start a counter at zero
    - sweep through every cell in the grid
    - if cell is land:
        - increase island count
        - sinkIsland(cell)
    - return count

    Edge cases:
    - empty grid or null grid -> return zero
    - sinkIsland goes out of bounds -> stop sinking
    - sinkIsland hits water -> stop sinking
    """

```

**7. Iterative implementation**

**Iteration 1: Skeleton**
Translate plain English core logic directly.

```python
def numIslands(grid):
    count = 0
    
    # sweep through every cell in the grid
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            # if cell is land
            if grid[r][c] == '1':
                # increase island count
                count += 1
                # sinkIsland(cell)
                sinkIsland(grid, r, c)
                
    return count

def sinkIsland(grid, r, c):
    # recursively turns connected land into water
    pass

```

**Iteration 2: Fleshing out the helper (Core Logic)**
Implement `sinkIsland` assuming happy path (only hitting valid land).

```python
def sinkIsland(grid, r, c):
    # turn current land to water
    grid[r][c] = '0' 
    
    # visit neighbors (up, down, left, right)
    sinkIsland(grid, r - 1, c) # up
    sinkIsland(grid, r + 1, c) # down
    sinkIsland(grid, r, c - 1) # left
    sinkIsland(grid, r, c + 1) # right

```

**Iteration 3: Patching Edge Cases**
Now address the edge cases listed in step 6.

* *Edge case 1: empty grid.*
* *Edge case 2 & 3: out of bounds or hitting water in DFS.*

```python
def numIslands(grid):
    # PATCH: empty grid edge case
    if not grid or not grid[0]:
        return 0

    count = 0
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == '1':
                count += 1
                sinkIsland(grid, r, c)
                
    return count

def sinkIsland(grid, r, c):
    # PATCH: out of bounds or hits water -> stop sinking
    if r < 0 or r >= len(grid) or c < 0 or c >= len(grid[0]) or grid[r][c] == '0':
        return
        
    grid[r][c] = '0' 
    
    sinkIsland(grid, r - 1, c)
    sinkIsland(grid, r + 1, c)
    sinkIsland(grid, r, c - 1)
    sinkIsland(grid, r, c + 1)

```

**8. Complexity & Optimizations**

* **Time Complexity:** O(M*N). Each cell visited essentially twice (once in main loop, once during DFS checks).
* **Space/Expensive sections:** Space is O(M*N) in worst case due to call stack (e.g., spiral shaped island). Recursion limit in Python might be hit for huge grids.
* **Optimization:** If we expect massive grids, swap DFS for BFS (using `collections.deque`). Space drops to max queue size O(min(M,N)). If mutating the input array is forbidden by interviewer, instantiate a `visited = set()` and pass it through, checking `if (r,c) not in visited` instead of mutating to '0'.