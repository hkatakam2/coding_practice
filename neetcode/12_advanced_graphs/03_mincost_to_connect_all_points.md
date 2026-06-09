# question
You are given a 2-D integer array points, where points[i] = [xi, yi]. Each points[i] represents a distinct point on a 2-D plane.
The cost of connecting two points [xi, yi] and [xj, yj] is the manhattan distance between the two points, i.e. |xi - xj| + |yi - yj|.
Return the minimum cost to connect all points together, such that there exists exactly one path between each pair of points.

### 1. Restate Problem

Given 2D coordinates. Connect all points into a single network. Cost = Manhattan distance: $|x_1 - x_2| + |y_1 - y_2|$. Need exactly one path between any pair. Return minimum total cost.
Essentially: Find the Minimum Spanning Tree (MST) of a fully connected graph.

### 2. Clarifying Questions & I/O

* **Input:** `points = [[x_1, y_1], [x_2, y_2], ...]` (List of integer pairs)
* **Output:** Integer (Minimum total cost)
* **Confirmations:**
* Can points have negative coordinates? Yes.
* Will points fit in memory? Yes.
* What if $N=1$? Cost is 0.



### 3. Hand-Trace Example

Input: `A(0,0), B(2,2), C(3,10), D(5,2), E(7,0)`

1. Start at `A`. Tree = `{A}`. Cost = 0.
2. Evaluate edges from `A`: `B=4`, `C=13`, `D=7`, `E=7`. Cheapest is `B`.
3. Add `B`. Tree = `{A, B}`. Cost = 4.
4. Evaluate new edges from `B`: `C=9`, `D=3`, `E=7`.
5. Cheapest available from `{A, B}` to unvisited is `B-D` (cost 3).
6. Add `D`. Tree = `{A, B, D}`. Cost = 4 + 3 = 7.
7. Evaluate new edges from `D`: `C=10`, `E=4`.
8. Cheapest from `{A, B, D}` to unvisited is `D-E` (cost 4).
9. Add `E`. Tree = `{A, B, D, E}`. Cost = 7 + 4 = 11.
10. Unvisited left: `C`. Cheapest edge is `B-C` (cost 9).
11. Add `C`. Tree = `{A, B, D, E, C}`. Cost = 11 + 9 = 20.
Return 20.

### 4. Brainstorming & Complexity

Graph is fully connected. $N$ vertices, $O(N^2)$ edges.

* **Kruskal's Algorithm:** Generate all $O(N^2)$ edges. Sort them. Use Union-Find to pick $N-1$ edges. Time: $O(N^2 \log(N^2))$. Space: $O(N^2)$.
* **Prim's Algorithm (Min-Heap):** Start at node 0. Keep a min-heap of edges bridging the tree to unvisited nodes. Pop cheapest. Time: $O(N^2 \log N)$. Space: $O(N^2)$.
* **Prim's Algorithm (Array):** Keep track of minimum distance from tree to each unvisited node. Scan array to find minimum. Time: $O(N^2)$. Space: $O(N)$.

### 5. Suggest Solutions

1. **Kruskal's:** Good, but generating and sorting $O(N^2)$ edges is heavy on memory and overhead.
2. **Prim's (Min-Heap):** Intuitive. Directly translates step 3's logic to code. "Always expand using the cheapest ticket."
Prefer Prim's (Min-Heap) for clarity and ease of explanation.

### 6. Outline Core Logic

```python
def minCostConnectPoints(points):
    """
    Reframe: Grow a connected group of points one by one, always adding the cheapest adjacent point.
    State: `visited` set (points in tree), `min_heap` (candidate edges to expand), chosen because heap automatically surfaces the shortest distance.
    Invariant: Heap only produces the shortest path to expand the frontier.

    manhattan(p1, p2) = returns absolute x diff + absolute y diff
    add_edges(node_idx) = calculates distance from node_idx to all unvisited nodes and pushes to heap

    Core logic:
    - Start with point index 0 in tree.
    - Put all its connections into the heap.
    - While visited count is less than total points:
        - Pop the cheapest connection from heap.
        - If destination already visited, skip.
        - Else, add to visited, add cost to total.
        - Put new connections from this destination into heap.
    - Return total cost.

    Edge cases:
    - 0 or 1 point given -> return 0 immediately.
    """

```

### 7. Iterative Implementation

**Iteration 1: Skeleton with stubs**

```python
import heapq

def minCostConnectPoints(points):
    n = len(points)
    visited = set()
    heap = [] # stores (cost, target_node)
    total_cost = 0

    # Start at node 0
    visited.add(0)
    # TODO: add_edges(0) to heap
    
    # Loop until all nodes connected
    while len(visited) < n:
        # TODO: pop min edge
        # TODO: if target visited, continue
        # TODO: process valid target (add to visited, add cost)
        # TODO: add_edges(target)
        pass
        
    return total_cost

```

**Iteration 2: Fleshing out core logic (No edge cases yet)**

```python
import heapq

def minCostConnectPoints(points):
    n = len(points)
    visited = set()
    heap = [] 
    total_cost = 0
    
    # Helper replacing add_edges stub
    # Pushes all unvisited neighbors to heap
    def push_unvisited(curr_node):
        x1, y1 = points[curr_node]
        for next_node in range(n):
            if next_node not in visited:
                x2, y2 = points[next_node]
                dist = abs(x1 - x2) + abs(y1 - y2)
                heapq.heappush(heap, (dist, next_node))

    # Init
    visited.add(0)
    push_unvisited(0)
    
    # Process heap
    while len(visited) < n:
        cost, node = heapq.heappop(heap)
        
        if node in visited:
            continue # stale edge
            
        visited.add(node)
        total_cost += cost
        push_unvisited(node) # expand frontier
        
    return total_cost

```

**Iteration 3: Adding edge cases**

```python
import heapq

def minCostConnectPoints(points):
    # EDGE CASE: 0 or 1 point requires 0 cost to connect
    if not points or len(points) <= 1:
        return 0

    n = len(points)
    visited = set()
    heap = [] 
    total_cost = 0
    
    def push_unvisited(curr_node):
        x1, y1 = points[curr_node]
        for next_node in range(n):
            if next_node not in visited:
                x2, y2 = points[next_node]
                dist = abs(x1 - x2) + abs(y1 - y2)
                heapq.heappush(heap, (dist, next_node))

    visited.add(0)
    push_unvisited(0)
    
    while len(visited) < n:
        cost, node = heapq.heappop(heap)
        
        if node in visited:
            continue 
            
        visited.add(node)
        total_cost += cost
        push_unvisited(node)
        
    return total_cost

```

### 8. Complexity & Optimizations

* **Time Complexity:** $O(N^2 \log N)$. Outer loop runs $N$ times. Inner loop (inside `push_unvisited`) runs $N$ times, pushing to heap takes $\log(N^2)$. Total heap pushes $O(N^2)$.
* **Space Complexity:** $O(N^2)$ because the heap can store up to $N(N-1)/2$ edges.

**Optimization Note:**
Heap operations dominate. Because graph is completely dense, an Array-based Prim's reduces Time to $O(N^2)$ and Space to $O(N)$.
Instead of a heap, maintain a `min_dist` array of size $N$ storing the shortest distance from the current MST to each unvisited node. In each step, linearly scan `min_dist` to find the minimum $O(N)$, add that node, and update `min_dist` with edges from the new node $O(N)$. Over $N$ steps, this is exactly $O(N^2)$. Excellent optimization if interviewer pushes on scaling $N$.