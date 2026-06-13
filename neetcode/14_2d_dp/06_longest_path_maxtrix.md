## question
You are given a 2-D grid of integers matrix, where each integer is greater than or equal to 0.
Return the length of the longest strictly increasing path within matrix.
From each cell within the path, you can move either horizontally or vertically. You may not move diagonally.

### 1. Restating the Question

Find the maximum number of steps you can take in a 2D grid of non-negative integers. Rules:

* Move up, down, left, or right.
* No diagonals.
* Next cell must be strictly greater than current cell.

### 2. Clarifying Questions & Inputs/Outputs

**Inputs:** `matrix` (2D array of integers $\ge 0$).
**Outputs:** `integer` representing max path length.
**Questions:**

* Empty matrix possible? (Assume yes, return 0).
* Can we revisit cells? (Strictly increasing rule naturally prevents cycles; it's a Directed Acyclic Graph).
* Minimum size? (1x1 matrix returns 1).

### 3. Example Input to Output by Hand

**Input:**

```text
9 9 4
6 6 8
2 1 1

```

**By Hand:**
Start at `1` (bottom middle).
`1` -> up to `6` -> up to `9`. Length = 3.
Wait, `1` -> left to `2` -> up to `6` -> up to `9`. Length = 4.
Check `4` (top right) -> `8`. Length = 2.
Max path is 4.

### 4. Brainstorming & Complexity

* **Approach 1: Naive DFS.** Start a Depth-First Search from every cell.
* *Complexity:* Time $O(4^{mn})$ worst case (branching factor 4). Space $O(mn)$ for recursion stack. Too slow.


* **Approach 2: DFS + Memoization (Cache).** Since we can't cycle (strictly increasing), overlapping subproblems exist (e.g., reaching `6` from `1` or `2` yields the same subsequent path to `9`). Cache the longest path starting from each cell.
* *Complexity:* Time $O(mn)$. Space $O(mn)$.


* **Approach 3: Topological Sort (Kahn's).** Treat grid as a DAG. Calculate in-degrees, peel off cells with 0 out-degrees.
* *Complexity:* Time $O(mn)$. Space $O(mn)$.



### 5. Suggest Solutions

Approach 2 (DFS + Memoization) is best. It maps perfectly to how we intuitively solved it by hand: trace paths, but remember the longest path from any "choke point" cell so we don't recalculate it. Simple, clear, easy to explain.

### 6. Outline of Selected Implementation

```python
def longest_increasing_path(matrix):
    """
    Reframe: Treat matrix as a DAG where edges point to strictly greater neighbors; find longest path.
    State: Memoization cache mapping cell coordinates to max path length, chosen because it prevents recomputing overlapping subproblems.
    Invariant: The cached value for a cell is the absolute maximum path length originating from that cell.

    dfs(cell) = computes and returns the longest increasing path starting from 'cell'.
    get_valid_neighbors(cell) = returns adjacent cells.

    Core logic:
    - initialize a cache
    - iterate through every cell in the grid
    - for each cell, calculate longest path using dfs
    - keep track of the maximum path seen so far
    - inside dfs: check cache first
    - if not in cache, check all neighbors
    - if neighbor is strictly greater, recursively call dfs on neighbor
    - path length is 1 + max of valid neighbor paths
    - save to cache and return

    Edge cases:
    - matrix is empty or None
    - neighbor is out of bounds
    - neighbor is not strictly greater (<= current)
    """
    pass

```

### 7. Iterative Implementation

**Iteration 1: Skeleton with stubs**
Map the plain English to a barebones structure.

```python
def longest_increasing_path(matrix):
    # TODO: handle empty matrix later (edge case)
    
    rows = len(matrix)
    cols = len(matrix[0])
    global_max = 0
    cache = {}

    def dfs(r, c):
        # return longest path from r, c
        pass 

    # check every cell
    for r in range(rows):
        for c in range(cols):
            path_len = dfs(r, c)
            global_max = max(global_max, path_len)

    return global_max

```

**Iteration 2: Expanding DFS core logic**
Focus on exploring paths. Defer caching and strict boundary checks.

```python
def longest_increasing_path(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    global_max = 0
    cache = {}

    def dfs(r, c):
        max_path_from_here = 1 # base case: just the cell itself
        
        # Directions: up, down, left, right
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            
            # TODO: add boundary checks (edge case)
            # Core logic check: strictly increasing
            if matrix[nr][nc] > matrix[r][c]:
                # NEW: recursively find path length of valid neighbor
                neighbor_path = dfs(nr, nc)
                max_path_from_here = max(max_path_from_here, 1 + neighbor_path)
                
        return max_path_from_here

    for r in range(rows):
        for c in range(cols):
            global_max = max(global_max, dfs(r, c))

    return global_max

```

**Iteration 3: Adding Memoization**
Make it efficient by using the `cache`.

```python
def longest_increasing_path(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    global_max = 0
    cache = {}

    def dfs(r, c):
        # NEW: Return cached result if already computed
        if (r, c) in cache:
            return cache[(r, c)]

        max_path_from_here = 1 
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            # TODO: add boundary checks (edge case)
            if matrix[nr][nc] > matrix[r][c]:
                max_path_from_here = max(max_path_from_here, 1 + dfs(nr, nc))
                
        # NEW: Store result in cache before returning
        cache[(r, c)] = max_path_from_here
        return max_path_from_here

    for r in range(rows):
        for c in range(cols):
            global_max = max(global_max, dfs(r, c))

    return global_max

```

**Iteration 4: Patching Edge Cases (Final)**
Add empty matrix check and out-of-bounds neighbor checks.

```python
def longest_increasing_path(matrix):
    # EDGE CASE PATCH: empty matrix
    if not matrix or not matrix[0]:
        return 0

    rows = len(matrix)
    cols = len(matrix[0])
    global_max = 0
    cache = {}

    def dfs(r, c):
        if (r, c) in cache:
            return cache[(r, c)]

        max_path_from_here = 1 
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            
            # EDGE CASE PATCH: boundary checks added before matrix access
            is_in_bounds = 0 <= nr < rows and 0 <= nc < cols
            
            # Valid neighbor: in bounds AND strictly greater
            if is_in_bounds and matrix[nr][nc] > matrix[r][c]:
                max_path_from_here = max(max_path_from_here, 1 + dfs(nr, nc))
                
        cache[(r, c)] = max_path_from_here
        return max_path_from_here

    for r in range(rows):
        for c in range(cols):
            global_max = max(global_max, dfs(r, c))

    return global_max

```

### 8. Complexity & Optimizations

**Time Complexity:** $O(mn)$. We visit every cell. Thanks to memoization, `dfs(r, c)` computes fully only once per cell. Checking 4 neighbors is $O(1)$ work.
**Space Complexity:** $O(mn)$. The `cache` dictionary stores exactly $mn$ entries. The recursion stack can also go $mn$ deep in the worst-case scenario (a single continuous snake-like path through the entire grid).

**Optimizations:** Code is optimal for time. Space optimization is minimal—could use a 2D array initialized to 0 instead of a dictionary for slightly faster lookup overhead, but asymptotic space remains $O(mn)$.