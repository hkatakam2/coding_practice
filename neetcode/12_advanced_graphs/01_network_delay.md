# question
You are given a network of n directed nodes, labeled from 1 to n. You are also given times, a list of directed edges where times[i] = (ui, vi, ti).

ui is the source node (an integer from 1 to n)
vi is the target node (an integer from 1 to n)
ti is the time it takes for a signal to travel from the source to the target node (an integer greater than or equal to 0).
You are also given an integer k, representing the node that we will send a signal from.
Return the minimum time it takes for all of the n nodes to receive the signal. If it is impossible for all the nodes to receive the signal, return -1 instead.

### 1. Restate

Given directed graph of `n` nodes (1 to `n`) and weighted edges `times` where `(u, v, t)` means travel from `u` to `v` takes `t`.
Signal starts at node `k`.
Find time when *all* nodes receive signal. Return max shortest path from `k`, or `-1` if any node is unreachable.

### 2. Clarify

* **Cyclic?** Yes, graph can have cycles.
* **Negative weights?** No, constraints say `t >= 0`.
* **Disconnected?** Yes, handle by returning `-1`.
* **Inputs:** `times` (list of tuples), `n` (int), `k` (int).
* **Outputs:** integer (max time or -1).

### 3. By Hand Example

`times = [[2,1,1], [2,3,1], [3,4,1]]`, `n = 4`, `k = 2`.

1. Start at `2`, time `0`.
2. Neighbors of `2`: `1` (time 1), `3` (time 1).
3. Shortest next is `1` or `3`.
4. Visit `1` at time `1`. Done with `1`.
5. Visit `3` at time `1`. Neighbors of `3`: `4` (time 1+1=2).
6. Visit `4` at time `2`. Done with `4`.
7. All 4 nodes visited. Max time taken: `2`.
Output: `2`.

### 4. Brainstorm & Complexity

* **DFS:** Explores deeply. Bad for shortest paths. Need to backtrack. $O(V!)$ in worst case.
* **Bellman-Ford:** Relax all edges `V-1` times. $O(V \times E)$. Simple, handles negatives, but slow for this.
* **Dijkstra's Algorithm (Min-Heap):** Always expand closest unvisited node. Maps perfectly to the "by hand" example. $O(E \log V)$ time. $O(V + E)$ space.

### 5. Suggest Solutions

Prefer simple, clear Dijkstra's algorithm. It mirrors the manual tracing: greedily visit the next closest reachable node and update its neighbors.

### 6. Outline

```python
def networkDelayTime(times, n, k):
    """
    Reframe: Find the maximum of all shortest paths from source to all other nodes.
    State: Min-heap storing (current_time, node) to prioritize closest nodes. Visited set to avoid cycles and redundant work. Exploits non-negative weights (first pop is guaranteed shortest).
    Invariant: Min-heap always surfaces the absolutely closest unfinalized node.

    buildGraph(times) = maps nodes to list of (neighbor, travel_time).

    Core logic:
    - build adjacency list graph
    - initialize min-heap with start node at time 0
    - initialize visited tracker
    - track maximum time seen so far
    - while min-heap has nodes:
        - pop node with smallest time
        - if node already finalized, skip
        - mark node as finalized
        - update maximum time seen
        - for each neighbor of current node:
            - if neighbor not finalized, push (current_time + travel_time, neighbor) to heap
            
    Edge cases:
    - graph is disconnected; visited count at the end is less than n
    """

```

### 7. Iterative Implementation

**Iteration 1: Skeleton code**

```python
import collections
import heapq

def networkDelayTime(times, n, k):
    # TODO: build graph 
    
    # TODO: initialize heap and state vars
    
    # TODO: process heap (core logic)
            
    # TODO: return result
    return 0

```

**Iteration 2: Core logic (Happy Path)**

```python
import collections
import heapq

def networkDelayTime(times, n, k):
    # build graph
    graph = collections.defaultdict(list)
    for u, v, t in times:
        graph[u].append((v, t))
        
    # initialize heap and state vars
    min_heap = [(0, k)]
    visited = set()
    max_time = 0
    
    # process heap
    while min_heap:
        curr_time, node = heapq.heappop(min_heap)
        
        if node in visited:
            continue
            
        visited.add(node)
        max_time = curr_time # Heap guarantees increasing order of times
        
        for neighbor, travel_time in graph[node]:
            if neighbor not in visited:
                heapq.heappush(min_heap, (curr_time + travel_time, neighbor))
                
    return max_time 

```

**Iteration 3: Patching Edge Cases**

```python
import collections
import heapq

def networkDelayTime(times, n, k):
    graph = collections.defaultdict(list)
    for u, v, t in times:
        graph[u].append((v, t))
        
    min_heap = [(0, k)]
    visited = set()
    max_time = 0
    
    while min_heap:
        curr_time, node = heapq.heappop(min_heap)
        
        if node in visited:
            continue
            
        visited.add(node)
        max_time = curr_time
        
        for neighbor, travel_time in graph[node]:
            if neighbor not in visited:
                heapq.heappush(min_heap, (curr_time + travel_time, neighbor))
                
    # EDGE CASE PATCH: Check if all nodes were reached
    if len(visited) == n:
        return max_time
    else:
        return -1

```

### 8. Complexity & Optimization

* **Time Complexity:** $O(E \log V)$. We push at most $E$ edges into the min-heap. Heap operations take $O(\log E)$, which simplifies to $O(\log V^2)$ = $O(2 \log V)$ = $O(\log V)$. Total time $O(E \log V)$.
* **Space Complexity:** $O(V + E)$ to store the adjacency list graph, plus $O(E)$ worst-case for the heap queue.
* **Optimization:** The standard Python `heapq` approach is optimal for this problem constraints. No clever optimizations required; early exits or alternative heap structures (Fibonacci heap) add unnecessary complexity for interview settings and general inputs.