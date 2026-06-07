# 6. Outline

```python
def pacificAtlantic(heights):  # -> list[list[int]]
    """
    Reframe: don't trace water OUT of each cell; flood INWARD from
        each ocean, climbing to equal-or-higher neighbors. A cell the
        flood touches is a cell that can drain to that ocean.
    State: two sets of cells, pacific_reachable & atlantic_reachable,
        chosen because we just need membership + final intersection.
    Invariant: a cell is in a set IFF water can flow from it to that ocean.

    oceanBorderCells(ocean) = the grid cells physically touching that ocean.
    canFlowUphill(from, to) = to is in-bounds and height[to] >= height[from]
        (reverse of real flow).
    floodFrom(startCells) = set of all cells reachable by repeatedly
        stepping to canFlowUphill neighbors, starting from startCells.

    Core logic:
    - pacific_reachable  = floodFrom(oceanBorderCells(Pacific))
    - atlantic_reachable = floodFrom(oceanBorderCells(Atlantic))
    - answer = every cell present in BOTH sets

    Edge cases:
    - single cell / single row / single col: touches both oceans -> included
    - empty grid: return []
    - plateaus (equal heights): canFlowUphill allows equal, so flood spreads
    """
```

# 7. Iterative implementation

**Iter 1 — skeleton with stubs**

```python
def pacificAtlantic(heights):
    pacific = flood(pacific_border())     # stub
    atlantic = flood(atlantic_border())   # stub
    return [[r, c] for (r, c) in pacific & atlantic]
```

**Iter 2 — fill the borders (plain English -> coords)**

```python
def pacificAtlantic(heights):
    rows, cols = len(heights), len(heights[0])

    # Pacific = top row + left col ; Atlantic = bottom row + right col
    pacific_start = [(0, c) for c in range(cols)] + [(r, 0) for r in range(rows)]
    atlantic_start = [(rows-1, c) for c in range(cols)] + [(r, cols-1) for r in range(rows)]

    pacific = flood(pacific_start)        # still stub
    atlantic = flood(atlantic_start)
    return [[r, c] for (r, c) in pacific & atlantic]
```

**Iter 3 — implement `flood` (DFS, uphill rule inline)**

```python
def pacificAtlantic(heights):
    rows, cols = len(heights), len(heights[0])

    def flood(starts):
        seen = set()
        def dfs(r, c):
            seen.add((r, c))
            for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
                nr, nc = r+dr, c+dc
                # reverse flow: step only to equal-or-HIGHER neighbor
                if 0 <= nr < rows and 0 <= nc < cols \
                   and (nr, nc) not in seen \
                   and heights[nr][nc] >= heights[r][c]:
                    dfs(nr, nc)
        for r, c in starts:
            if (r, c) not in seen:
                dfs(r, c)
        return seen

    pacific_start = [(0, c) for c in range(cols)] + [(r, 0) for r in range(rows)]
    atlantic_start = [(rows-1, c) for c in range(cols)] + [(r, cols-1) for r in range(rows)]

    pacific = flood(pacific_start)
    atlantic = flood(atlantic_start)
    return [[r, c] for (r, c) in pacific & atlantic]
```

Core logic complete.

**Edge cases walk:**
- Single cell / row / col: in both `pacific_start` and `atlantic_start`, flood adds it to both sets, intersection includes it. ✔ no patch.
- Empty grid: `heights[0]` crashes. **Patch:**

```python
    if not heights or not heights[0]:
        return []
```

- Plateaus: `>=` already permits equal-height steps. ✔ no patch.

Final adds only the guard line at top.

# 8. Complexity

- `flood`: each cell pushed once (`seen` guard), each looks at 4 neighbors → **O(mn)** per ocean, two oceans → **O(mn)**.
- Space: `seen` sets + recursion stack → **O(mn)**.

Possible optimization: convert recursive DFS to iterative stack to avoid Python recursion-limit blowup on large grids (~big m*n). Same asymptotics, only safety:

```python
        def dfs(r0, c0):
            stack = [(r0, c0)]
            seen.add((r0, c0))
            while stack:
                r, c = stack.pop()
                for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
                    nr, nc = r+dr, c+dc
                    if 0 <= nr < rows and 0 <= nc < cols \
                       and (nr, nc) not in seen \
                       and heights[nr][nc] >= heights[r][c]:
                        seen.add((nr, nc))
                        stack.append((nr, nc))
```

Recursive version is clearer; swap to iterative only if stack depth is a concern.