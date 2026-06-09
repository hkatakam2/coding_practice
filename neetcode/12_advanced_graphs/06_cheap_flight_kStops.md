# question
There are n airports, labeled from 0 to n - 1, which are connected by some flights. You are given an array flights where flights[i] = [from_i, to_i, price_i] represents a one-way flight from airport from_i to airport to_i with cost price_i. You may assume there are no duplicate flights and no flights from an airport to itself.
You are also given three integers src, dst, and k where:

src is the starting airport
dst is the destination airport
src != dst
k is the maximum number of stops you can make (not including src and dst)
Return the cheapest price from src to dst with at most k stops, or return -1 if it is impossible.

### 1. Restating the Question

Find the cheapest path from source A to destination B in a directed, weighted graph. Constraint: Path can have at most `k` intermediate nodes (which means at most `k + 1` edges/flights).

### 2. Clarifying Questions & Confirming I/O

* **Interviewer:** Are flight prices always positive?
* *Assumption:* Yes. No negative cycles to worry about.


* **Interviewer:** Can `src` and `dst` be disconnected?
* *Assumption:* Yes. Should return `-1` in that case.


* **Inputs:** `n = 3`, `flights = [[0,1,100],[1,2,100],[0,2,500]]`, `src = 0`, `dst = 2`, `k = 1`.
* **Outputs:** `200` (Route: 0 -> 1 -> 2. One stop, cost 200).

### 3. Example Trace By Hand

* `src = 0`, `dst = 2`, `k = 1`. Allowed edges = `k + 1 = 2`.
* Start at `0`. Cost: 0. Stops: 0.
* From `0`, check outgoing flights:
* To `1`: Cost 100. Stops: 1.
* To `2`: Cost 500. Stops: 1. (Valid route found, current min = 500).


* From `1`, check outgoing flights:
* To `2`: Cost 100 + 100 = 200. Stops: 2. (Valid route found, update min = 200).


* Max stops reached. Cheapest is 200.

### 4. Brainstorming Solutions & Complexity

* **Depth-First Search (DFS) with backtracking:** Explore all paths. Very slow. Time: Exponential. Space: O(n) for recursion.
* **Dijkstra's Algorithm:** Standard for shortest path. But modifying it for a "stops" limit is tricky; a cheaper path might have too many stops, masking a slightly pricier path with fewer stops. Time: O(E log V).
* **Breadth-First Search (BFS):** Process level by level. Naturally tracks stops. Stop searching after `k + 1` levels. Time: O(V + E * K). Space: O(V + E).
* **Bellman-Ford:** Relax all edges `k + 1` times. Time: O(E * K). Space: O(V).

### 5. Suggest Solutions

Prefer simple and straightforward.

1. **Level-order BFS (matches step 3 trace):** Explores outward one flight at a time. Very intuitive. We track the minimum cost to reach each node to prune useless paths.
2. **Bellman-Ford:** Extremely short code, but sometimes less intuitive to explain if the candidate isn't familiar with graph algorithms.

**Selection:** Level-order BFS. It's literally the manual trace turned into code.

### 6. Outline of Implementation

```python
def findCheapestPrice(n: int, flights: list[list[int]], src: int, dst: int, k: int) -> int:
    """
    Reframe: Find shortest path bounded by depth in a directed graph.
    State: A queue tracking active flights, and an array tracking the cheapest known cost to each airport. Chosen because queue handles level-by-level traversal naturally, and the array prunes redundant, more expensive paths.
    Invariant: Processing the queue strictly level-by-level ensures the stop count never exceeds the current depth.

    build_graph(flights) = creates adjacency list mapping airport to list of (neighbor, price).

    Core logic:
    - Build graph mapping airports to their destinations and costs.
    - Initialize queue with starting airport and zero cost.
    - Initialize best_cost array with infinity for all airports.
    - Loop up to k+1 times (representing max allowed edges):
        - Take snapshot of current queue size to process only this level.
        - Process each airport in the current level:
            - Look at all its connecting flights.
            - Calculate the new total cost to reach the next airport.
            - If new cost is cheaper than the known best_cost to that airport:
                - Update best_cost.
                - Add next airport and new cost to the queue for the next level.
    - Return best_cost of destination.

    Edge cases:
    - Destination never reached.
    - Graph is completely disconnected.
    - Zero stops allowed (direct flights only).
    """

```

### 7. Iterative Implementation

**Iteration 1: Skeleton with stubs**

```python
def findCheapestPrice(n, flights, src, dst, k):
    # TODO: Build graph
    
    # TODO: Setup queue and tracking
    
    # TODO: Level-order BFS up to k+1 levels
        # TODO: Process current level
            # TODO: check neighbors and update
            
    # TODO: Return result
    pass

```

**Iteration 2: Core structure (Graph + Queue setup)**

```python
import collections

def findCheapestPrice(n, flights, src, dst, k):
    # Build graph: adjacency list
    graph = collections.defaultdict(list)
    for u, v, w in flights:
        graph[u].append((v, w))
        
    # Setup queue: (current_node, current_cost)
    queue = collections.deque([(src, 0)])
    
    # Track min cost to each node to prune bad paths
    min_cost = [float('inf')] * n
    
    stops = 0
    
    # BFS up to k + 1 edges (which means k stops)
    while queue and stops <= k:
        level_size = len(queue)
        
        # Process only nodes at the current depth
        for _ in range(level_size):
            node, cost = queue.popleft()
            # TODO: check neighbors and add to next level
            
        stops += 1
        
    # TODO: return min_cost[dst]

```

**Iteration 3: Filling in core logic (Neighbors & Pruning)**

```python
import collections

def findCheapestPrice(n, flights, src, dst, k):
    graph = collections.defaultdict(list)
    for u, v, w in flights:
        graph[u].append((v, w))
        
    queue = collections.deque([(src, 0)])
    min_cost = [float('inf')] * n
    stops = 0
    
    while queue and stops <= k:
        level_size = len(queue)
        for _ in range(level_size):
            node, cost = queue.popleft()
            
            # Check neighbors
            for neighbor, price in graph[node]:
                next_cost = cost + price
                
                # Prune: only add to queue if this path is strictly cheaper
                # than the best path we've found to this neighbor so far
                if next_cost < min_cost[neighbor]:
                    min_cost[neighbor] = next_cost
                    queue.append((neighbor, next_cost))
                    
        stops += 1
        
    # Return destination cost
    return min_cost[dst] # Note: Needs edge case patch if unreachable

```

**Iteration 4: Patching Edge Cases**

* *Edge case:* Destination unreachable (returns `inf` currently, needs to be `-1`).

```python
import collections

def findCheapestPrice(n, flights, src, dst, k):
    graph = collections.defaultdict(list)
    for u, v, w in flights:
        graph[u].append((v, w))
        
    queue = collections.deque([(src, 0)])
    min_cost = [float('inf')] * n
    stops = 0
    
    while queue and stops <= k:
        level_size = len(queue)
        for _ in range(level_size):
            node, cost = queue.popleft()
            
            for neighbor, price in graph[node]:
                next_cost = cost + price
                if next_cost < min_cost[neighbor]:
                    min_cost[neighbor] = next_cost
                    queue.append((neighbor, next_cost))
                    
        stops += 1
        
    # PATCH: Check if destination was ever reached
    return min_cost[dst] if min_cost[dst] != float('inf') else -1

```

### 8. Complexity & Optimizations

* **Time Complexity:** O(V + E * K). We process at most `E` edges for each of the `K` levels. Very efficient for small `K`.
* **Space Complexity:** O(V + E) for the adjacency list and the queue.

**Optimization Commentary:**
The BFS is highly readable, but we could theoretically drop the queue and just iterate over the `flights` array directly `k+1` times (Bellman-Ford algorithm). That would drop our space complexity down to O(V) because we wouldn't need to build an adjacency list or maintain a queue at all. However, BFS is often faster in practice for sparse graphs or small `k` because Bellman-Ford blindly checks every single edge every iteration, whereas BFS only explores outward from currently active nodes.