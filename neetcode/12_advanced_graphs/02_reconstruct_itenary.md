# question
You are given a list of flight tickets tickets where tickets[i] = [from_i, to_i] represent the source airport and the destination airport.
Each from_i and to_i consists of three uppercase English letters.
Reconstruct the itinerary in order and return it.
All of the tickets belong to someone who originally departed from "JFK". Your objective is to reconstruct the flight path that this person took, assuming each ticket was used exactly once.
If there are multiple valid flight paths, return the lexicographically smallest one.

For example, the itinerary ["JFK", "SEA"] has a smaller lexical order than ["JFK", "SFO"].
You may assume all the tickets form at least one valid flight path.

### 1. Restate

Given list of directed flight segments. Find exact full route starting at "JFK". Must use all tickets exactly once. Tie-breaker: lexicographical order. Guaranteed valid path exists.

### 2. Clarify

* **Inputs:** `tickets` = array of arrays of strings. e.g., `[["JFK", "SFO"], ...]`.
* **Outputs:** Array of strings representing ordered path. e.g., `["JFK", "SFO", ...]`.
* **Cycles:** Graph can have cycles.
* **Dead ends:** Graph can have terminal nodes.
* **Empty input:** Possible? Assume at least one ticket based on problem description.

### 3. By Hand

Input: `[["JFK","ATL"], ["JFK","SFO"], ["SFO","ATL"], ["ATL","JFK"], ["ATL","SFO"]]`
Graph:

* `JFK -> ATL, SFO`
* `SFO -> ATL`
* `ATL -> JFK, SFO`

Simulation (Greedy + Backtrack / DFS):

1. Start `JFK`. Choices: `ATL, SFO`. Pick alphabetical: `ATL`. Path: `JFK -> ATL`.
2. From `ATL`. Choices: `JFK, SFO`. Pick `JFK`. Path: `JFK -> ATL -> JFK`.
3. From `JFK`. Only `SFO` left. Path: `JFK -> ATL -> JFK -> SFO`.
4. From `SFO`. Only `ATL` left. Path: `JFK -> ATL -> JFK -> SFO -> ATL`.
5. From `ATL`. Only `SFO` left. Path: `JFK -> ATL -> JFK -> SFO -> ATL -> SFO`.
All tickets used. Return path.

### 4. Brainstorm & Complexity

* **Approach A: DFS with Backtracking.** Sort adjacency list. DFS picking smallest lexical edge. If stuck before using all tickets, backtrack (un-mark edge, try next).
* *Complexity:* Worst-case $O(E^d)$ (exponential backtracking), though practically fast with sorted edges. Space $O(E)$ for recursion and graph.


* **Approach B: Hierholzer's Algorithm (Post-order DFS).** Build graph. Sort adjacency lists descending. DFS traversing available edges. When a node has no more outgoing unvisited edges, push to a result stack. Reverse stack at end.
* *Complexity:* $O(E \log E)$ to sort edges. $O(E)$ for traversal. Time $O(E \log E)$. Space $O(E)$.



### 5. Suggest Solutions

1. **DFS with Backtracking:** Literally the "by hand" approach. Intuitive but heavy on recursion and potential worst-case time complexity.
2. **Hierholzer's (Post-order DFS):** Simpler to implement, clearer, linear time traversal, no explicit un-marking edges needed.

**Selected:** Hierholzer's. It relies on a very simple mechanic: "fly until you get stuck, write down where you got stuck, step back."

### 6. Outline

```python
def findItinerary(tickets):
    """
    Reframe: Find Eulerian path in directed graph, greedily picking lexical smallest edge, recording nodes post-order.
    State: Adjacency list of descending-sorted arrays, chosen because popping from the end gives smallest lexical destination in O(1) time and removes the edge.
    Invariant: Nodes are only added to the path when all their outgoing edges are exhausted, ensuring dead-ends are processed last and end up at the end of the reversed result.

    buildGraph(tickets) = creates mapping of src -> sorted list of destinations (descending)
    dfs(airport) = greedily visits neighbors, then appends airport to result

    Core logic:
    - build graph from tickets.
    - initialize empty result path.
    - start dfs at "JFK".
    - inside dfs: while current airport has outgoing flights, pop the next flight and recursively call dfs on it.
    - inside dfs: once loop finishes, append airport to result path.
    - return reversed result path.

    Edge cases:
    - empty tickets array.
    - airport with zero outgoing flights (dead end) encountered mid-traversal.
    """

```

### 7. Iterative Implementation

**Iteration 1: Skeleton**

```python
def findItinerary(tickets):
    # TODO: buildGraph(tickets) -> dict of src: [dst1, dst2] (sorted descending)
    
    result = []
    
    # def dfs(airport):
        # TODO: while airport has neighbors, pop neighbor, dfs(neighbor)
        # TODO: append airport to result
        
    # dfs("JFK")
    # return reversed result

```

**Iteration 2: Graph Building**

```python
import collections

def findItinerary(tickets):
    # CHANGED: Implemented graph building and descending sort
    graph = collections.defaultdict(list)
    for src, dst in tickets:
        graph[src].append(dst)
        
    for src in graph:
        graph[src].sort(reverse=True)
    
    result = []
    
    # def dfs(airport):
        # TODO: while airport has neighbors, pop neighbor, dfs(neighbor)
        # TODO: append airport to result
        
    # dfs("JFK")
    # return reversed result

```

**Iteration 3: Core Logic Realized**

```python
import collections

def findItinerary(tickets):
    graph = collections.defaultdict(list)
    for src, dst in tickets:
        graph[src].append(dst)
        
    for src in graph:
        graph[src].sort(reverse=True)
    
    result = []
    
    # CHANGED: Implemented DFS and final return
    def dfs(airport):
        while graph[airport]:
            next_dest = graph[airport].pop()
            dfs(next_dest)
        result.append(airport)
        
    dfs("JFK")
    return result[::-1]

```

**Edge Case Patching:**

1. *Empty tickets array:* Handled. Loop skipped, returns `[]`.
2. *Airport with zero outgoing flights (dead end):* Handled safely. `collections.defaultdict` ensures that `graph[airport]` evaluates to an empty list `[]` without throwing a `KeyError`. The while loop skips, and it safely appends.
No code patches required. The core logic inherently covers the edge cases due to Python's robust standard library choices (`defaultdict`).

### 8. Complexity & Optimization

* **Time:** Graph building and sorting takes $O(E \log E)$ where $E$ is number of tickets. Traversal touches each edge exactly once, taking $O(E)$. Total Time: $O(E \log E)$.
* **Space:** Graph stores $E$ edges. Result stores $E+1$ nodes. Recursion stack can go $E$ deep in worst case. Total Space: $O(E)$.
* **Optimization noted:** Sorting in reverse (`reverse=True`) is a deliberate optimization. If we sorted normally (ascending), we would need to do `graph[airport].pop(0)` to get the lexicographically smallest. `pop(0)` on a Python list is an $O(N)$ operation, destroying our linear time traversal. Popping from the end (`pop()`) is $O(1)$.