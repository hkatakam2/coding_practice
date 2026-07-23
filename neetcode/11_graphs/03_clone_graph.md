### question
Given a node in a connected undirected graph, return a deep copy of the graph.

Each node in the graph contains an integer value and a list of its neighbors.

class Node {
    public int val;
    public List<Node> neighbors;
}
The graph is shown in the test cases as an adjacency list. An adjacency list is a mapping of nodes to lists, used to represent a finite graph. Each list describes the set of neighbors of a node in the graph.

For simplicity, nodes values are numbered from 1 to n, where n is the total number of nodes in the graph. The index of each node within the adjacency list is the same as the node's value (1-indexed).

The input node will always be the first node in the graph and have 1 as the value.

**1. Restate**
Given a reference to a single node in a connected, undirected graph. Return a deep copy (clone). New node instances, exact same connectivity.

**2. Clarify & I/O**

* Input: `Node` (original start node, or null).
* Output: `Node` (cloned start node, or null).
* Questions: Can graph be empty? Yes (input is null). Cycles? Yes, undirected graphs have cycles inherently. Self-loops? Assume possible, deep copy handles it naturally.

**3. Hand-Trace Example**
Input graph: 1 -- 2
Start at 1.
Create `Copy_1`. Store in memory: `Map[1] = Copy_1`.
Look at 1's neighbors: Node 2.
Is 2 in map? No.
Create `Copy_2`. Store: `Map[2] = Copy_2`.
Link: `Copy_1.neighbors.add(Copy_2)`.
Look at 2's neighbors: Node 1.
Is 1 in map? Yes (`Copy_1`).
Link: `Copy_2.neighbors.add(Copy_1)`.
Done. Return `Copy_1`.

**4. Brainstorm & Complexity**

* Need to traverse every node and edge.
* Must track visited nodes to avoid infinite cycles. Best way: Hash Map mapping `OriginalNode -> ClonedNode`.
* Approach A: Depth First Search (DFS). Recursively visit neighbors. Implicit call stack. Time: O(V+E), Space: O(V) for map and recursion stack.
* Approach B: Breadth First Search (BFS). Queue-based. Time: O(V+E), Space: O(V) for map and queue.

**5. Suggest Solutions**

1. Recursive DFS. (Handled exactly like the hand-trace in step 3. Simple, highly readable).
2. Iterative BFS.
*Selection*: Recursive DFS. Easiest to explain and write cleanly.

**6. Outline**

```python
def cloneGraph(node: 'Node') -> 'Node':
    """
    Reframe: Graph traversal mapping old memory references to new memory references.
    State: Hash map (old_node -> new_node), chosen because it tracks visited nodes and provides O(1) access to previously created copies for wiring cyclical edges.
    Invariant: Any node added to the map has a cloned instance, and its edges are being actively processed or fully resolved.

    dfs_clone(current_node) = Recursively creates a copy of the node, saves it to the map, and populates its neighbors.

    Core logic:
    - check if current node is already in map
    - if yes, return the mapped clone
    - create new clone node with current node's value
    - save clone in map using current node as key
    - for every neighbor of current node:
        - recursively call dfs_clone on neighbor
        - append the returned cloned neighbor to clone's neighbor list
    - return the clone

    Edge cases:
    - input node is null (empty graph)
    """

```

**7. Iterative Implementation**

*Iteration 1: Skeleton with stubs*

```python
class Solution:
    def cloneGraph(self, node: 'Node') -> 'Node':
        cloned_map = {}
        
        def dfs_clone(curr):
            # TODO: base case (already visited)
            # TODO: clone curr
            # TODO: add to map
            # TODO: iterate neighbors and recurse
            pass
            
        # TODO: handle start node and return

```

*Iteration 2: Core logic (Happy path)*

```python
class Solution:
    def cloneGraph(self, node: 'Node') -> 'Node':
        cloned_map = {}
        
        def dfs_clone(curr):
            # check if visited
            if curr in cloned_map:
                return cloned_map[curr]
            
            # create clone, add to map IMMEDIATELY to prevent cycles
            clone = Node(curr.val)
            cloned_map[curr] = clone
            
            # wire neighbors via recursion
            for neighbor in curr.neighbors:
                cloned_neighbor = dfs_clone(neighbor)
                clone.neighbors.append(cloned_neighbor)
                
            return clone
            
        # kick off DFS
        return dfs_clone(node)

```

*Iteration 3: Patching edge cases (null input)*

```python
class Solution:
    def cloneGraph(self, node: 'Node') -> 'Node':
        # EDGE CASE PATCH: empty graph
        if not node:
            return None
            
        cloned_map = {}
        
        def dfs_clone(curr):
            if curr in cloned_map:
                return cloned_map[curr]
            
            clone = Node(curr.val, []) # init empty neighbors array
            cloned_map[curr] = clone
            
            for neighbor in curr.neighbors:
                clone.neighbors.append(dfs_clone(neighbor))
                
            return clone
            
        return dfs_clone(node)

```

**8. Complexity & Optimizations**

* **Time Complexity**: O(V + E) where V is vertices, E is edges. We visit each node exactly once and iterate through every edge exactly once (twice total for undirected graph). No way to optimize time further; must touch all data to copy it.
* **Space Complexity**: O(V). The `cloned_map` stores exactly V nodes. The recursion stack goes at most V deep (in a linked-list-like graph).
* **Optimizations**:
* If the graph is extremely deep (e.g., $10^5$ nodes in a straight line), recursion might hit Python's stack limit (`RecursionError`).
* *Fix for deep graphs*: Switch to iterative BFS using `collections.deque`. However, for standard interview constraints, recursive DFS is preferred for pure readability.