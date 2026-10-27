# question
Shortest Path in a Grid / Warehouse Obstacle Navigation: Variation of Shortest Path to Get Food or Rotting Oranges—finding the minimum steps for a robot/associate to move through a 4-directional grid with obstacles, or handling multi-source BFS

# clarifications
1. R = robot, T= target, X = obsticle, O = open floor
2. does every move cost one step or weighted? 1 step
3. can there be multiple targets? do I have to return the path taken? possible, yes
4. can there be multiple robots? 1 to start
5. what if no target is reachable? return -1
6. how big is the grid? 

# ideas?
1. DFS/Backtracking: it tries every path and keeps minimum. it is exponential, the first path it finds need not be shrtest
2. Dijkstra: it handles weighted edges; for 1 cost edges, heap adds un necessary log factor
3. A*. It’s useful with a single known target, but I have multiple targets and the nearest one isn’t known up front. A heuristic would be awkward.
4. BFS: with unit cost BFS explores in rings of increasing distance. the first time it touches the target, that is the shortest

# outline
I will process the queue level by level, so I know the current step count without storing distanc eper cell
I'll mark cells visited while I enque, not when I deque them. otherwise the same cell can be queued many times

Complexity: O(R·C) time and space, since each cell is enqueued at most once.

Follow-up thought: BFS handles multiple sources for free. If I seed the queue with all sources instead of one, the rings expand from all of them simultaneously. That’s the Rotting Oranges pattern.

shortest_steps(grid):
    starts = findall(grid, START)
    queue, seen = seed(starts)
    steps = 0

    while queue:
        for each cell in the current level:
            if is_target(cell): return steps
            for each neighbor in 4 directions:
                if in_bounds and not wall and not seen:
                    mark seen, enque
        steps += 1
    return -1

```python
START, TARGET, WALL = 'S', 'T', 'X'
directions = [(1,0), (-1,0), (0,1), (0,-1)]
def find_all(grid, ch):
    return [(r,c) for r, row in enumerate(grid)
                    for c, v in enumerate(row) if v == ch]

def is_target(grid, r, c):
    return grid[r][c] == "T"

def in_bouds(grid, r,c):
    rows = len(grid)
    cols = len(grid[0])
    return 0<= r < rows and 0<= c < cols

from collections import deque

def shortest_steps(grid):
    starts = find_all(grid, START)
    if not starts: return -1
    
    queue = deque(starts)
    seen = set(starts)

    steps = 0

    while queue:
        for _ in range(len(queue)):
            r, c = queue.popleft()
            if is_target(grid,r,c): return steps
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if in_bounds(grid, nr, nc) and grid[nr][nc] != "X" and (nr, nc) not in seen:
                    seen.add((nr, nc))
                    queue.append((nr,nc))
        steps += 1
    return -1
    


```