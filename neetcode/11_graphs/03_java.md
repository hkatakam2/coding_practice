### 1. Restate the problem

We are given a reference to a node in a connected, undirected graph. Our task is to return a deep copy (clone) of the entire graph.

* **Given:** A `Node` object containing an integer value and a list of neighboring `Node` objects.
* **Must return:** A new `Node` object that represents the start of a completely cloned graph.
* **Main constraint:** The new graph must be structurally identical, but every single node and list must be newly instantiated. We cannot reuse any references from the original graph.
* **Cycles:** Because the graph is undirected, there are mutual connections (A points to B, B points to A). We must handle cycles properly to avoid infinite loops.

### 2. Ask clarifying questions

Before writing code, I would normally confirm a few details with the interviewer:

* *Null input:* Can the input node be `null`? (I will assume yes, and returning `null` is the expected behavior).
* *Max size:* What is the maximum number of nodes? (If it's in the millions, a deep recursive approach might cause a `StackOverflowError`, but typically graph problems in interviews have $V \le 1000$, making recursion safe. I'll assume standard limits).
* *Uniqueness:* Are node values unique? (The prompt states nodes are numbered 1 to $n$, so yes).

### 3. Work through an example by hand

Let's consider a simple square graph (4 nodes).
Node 1 is connected to 2 and 4.
Node 2 is connected to 1 and 3.
Node 3 is connected to 2 and 4.
Node 4 is connected to 1 and 3.

**Trace:**

1. Start at Node 1. Has it been copied yet? No.
* Create `Clone 1`.
* Record that Node 1 maps to `Clone 1` so we don't copy it again.
* Look at Node 1's neighbors: Node 2 and Node 4.


2. Process neighbor Node 2. Has it been copied? No.
* Create `Clone 2`. Map Node 2 to `Clone 2`.
* Look at Node 2's neighbors: Node 1 and Node 3.


3. Process Node 2's neighbor Node 1. Has it been copied? Yes!
* Retrieve `Clone 1` from our record.
* Add `Clone 1` to `Clone 2`'s neighbors. (Breaks the cycle).


4. Process Node 2's neighbor Node 3. Copied? No.
* Create `Clone 3`. Map it.
* Neighbors: Node 2, Node 4.
* ... this continues until the entire structure is explored and reconstructed.



### 4. Brainstorm solutions aloud

**Approach 1: Depth-First Search (DFS) with Recursion**
Like my manual trace, we can traverse the graph using recursion. Whenever we visit a node, we immediately clone it and store the mapping of `Original Node -> Cloned Node` in a `HashMap`. Then, we iterate over the original node's neighbors. If a neighbor is in the map, we add its clone to our current clone's neighbors. If not, we recursively call the clone function on that neighbor, and add the returned clone.

* *Time complexity:* O(V + E) where V is vertices and E is edges.
* *Space complexity:* O(V) for the map and O(V) for the recursion stack.

**Approach 2: Breadth-First Search (BFS) with a Queue**
We could also do this iteratively. We start by cloning the first node, putting it in a `HashMap`, and enqueuing the original node. While the queue isn't empty, we pop a node, look at its neighbors, and if a neighbor hasn't been cloned, we clone it, map it, and enqueue it. Then we link the clones.

* *Time complexity:* O(V + E).
* *Space complexity:* O(V) for the map and O(W) for the queue (where W is the maximum width of the graph).

### 5. Select the solution

I will use **Depth-First Search (DFS) with a HashMap**.

* It is concise and directly models the structural dependencies of the graph.
* The `HashMap` provides expected O(1) lookups to instantly determine if we've already visited and cloned a node, effectively breaking cycles.
* Unless the graph is an extreme straight-line linked list of tens of thousands of nodes (which would risk a `StackOverflowError`), DFS is the cleanest, most maintainable approach for interview settings.

### 6. Write the implementation outline

```java
Node cloneGraph(Node node) {
    /*
     * Reframe:
     * Traverse the original graph, creating a copy of each node and wiring up 
     * the new nodes exactly as the original was wired.
     *
     * State:
     * Map<Node, Node> visited
     * Chosen because:
     * We need O(1) lookups to map an original node to its new clone, 
     * preventing infinite loops in cyclic graphs.
     *
     * Invariant:
     * By the time a recursive call processes a node's neighbors, that node 
     * has already been added to the map.
     *
     * Helpers:
     * dfs(node, visited)
     * - clones the current node
     * - adds it to the visited map
     * - recursively clones all unvisited neighbors
     * - returns the cloned node
     *
     * Core logic:
     * - Handle null input
     * - Initialize the tracking map
     * - Kick off the recursive DFS traversal from the starting node
     * - Return the cloned starting node
     *
     * Edge cases:
     * - Null starting node.
     * - Graph with only 1 node (no neighbors).
     */
}

```

### 7. Implement iteratively

**Iteration 1: Method skeleton**
First, I'll set up the main method, the state map, and the helper stub.

```java
class Solution {
    public Node cloneGraph(Node node) {
        // State: Map from Original Node -> Cloned Node
        Map<Node, Node> visited = new HashMap<>();
        
        // TODO: Handle null input
        // TODO: Call DFS to start the cloning process
        
        return null;
    }

    private Node dfs(Node node, Map<Node, Node> visited) {
        // TODO: Implement clone, register to map, and recurse on neighbors
        return null;
    }
}

```

**Iteration 2: Implement easiest core section**
Now I'll implement the basic node cloning and mapping inside the `dfs` method, deferring the neighbor relationships.

```java
class Solution {
    public Node cloneGraph(Node node) {
        Map<Node, Node> visited = new HashMap<>();
        // Added: trigger the recursive clone
        return dfs(node, visited);
    }

    private Node dfs(Node node, Map<Node, Node> visited) {
        // Added: base case to stop cycle
        if (visited.containsKey(node)) {
            return visited.get(node);
        }

        // Added: create the clone
        Node clone = new Node(node.val, new ArrayList<>());
        
        // Added: register the clone immediately to prevent infinite loops
        visited.put(node, clone);

        // TODO: recursively populate clone.neighbors
        
        return clone;
    }
}

```

**Iteration 3: Complete the happy path**
Now I will wire up the neighbors.

```java
class Solution {
    public Node cloneGraph(Node node) {
        Map<Node, Node> visited = new HashMap<>();
        return dfs(node, visited);
    }

    private Node dfs(Node node, Map<Node, Node> visited) {
        if (visited.containsKey(node)) {
            return visited.get(node);
        }

        Node clone = new Node(node.val, new ArrayList<>());
        visited.put(node, clone);

        // Added: Iterate through original neighbors. 
        // DFS ensures we get a fully constructed clone back.
        for (Node neighbor : node.neighbors) {
            clone.neighbors.add(dfs(neighbor, visited));
        }

        return clone;
    }
}

```

### 8. Edge-case pass

Let's review the edge cases identified earlier:

* *Null starting node:* If `node` is `null`, `dfs(null, visited)` will throw a `NullPointerException` when trying to evaluate `visited.containsKey(node)` or accessing `node.val`. I must add an explicit check for this in the main method.
* *Graph with 1 node:* The loops will cleanly bypass since `node.neighbors` is empty, returning just the single cloned node. This works fine.

Let's patch the `null` case.

### 9. Analyze expensive sections and optimize (Final Code)

The graph traversal touches every vertex $V$ and every edge $E$ exactly once. There are no expensive redundant operations, no unnecessary sorting, and no intermediate stream objects being created in a tight loop.

* **Time Complexity:** $O(V + E)$. We visit every node once, and iterate through all the edges across the entire traversal.
* **Space Complexity:** $O(V)$ for the `HashMap` storing the mapping. In the worst-case scenario (a long linear chain of nodes), the recursion stack will also go $V$ levels deep, taking $O(V)$ space.

Here is the final, clean code:

```java
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

// Definition for a Node provided by the environment.
class Node {
    public int val;
    public List<Node> neighbors;
    
    public Node() {
        val = 0;
        neighbors = new ArrayList<Node>();
    }
    
    public Node(int _val) {
        val = _val;
        neighbors = new ArrayList<Node>();
    }
    
    public Node(int _val, ArrayList<Node> _neighbors) {
        val = _val;
        neighbors = _neighbors;
    }
}

class Solution {
    public Node cloneGraph(Node node) {
        // Handle edge case of empty graph
        if (node == null) {
            return null;
        }
        
        Map<Node, Node> visited = new HashMap<>();
        return dfs(node, visited);
    }

    private Node dfs(Node node, Map<Node, Node> visited) {
        // If we have already cloned this node, return the clone to break the cycle
        if (visited.containsKey(node)) {
            return visited.get(node);
        }

        // Create the clone. It's crucial we map it BEFORE iterating neighbors 
        // to handle mutual connections (A -> B and B -> A).
        Node clone = new Node(node.val, new ArrayList<>());
        visited.put(node, clone);

        // Recursively clone and link all neighbors
        for (Node neighbor : node.neighbors) {
            clone.neighbors.add(dfs(neighbor, visited));
        }

        return clone;
    }
}

```

**Brief test walkthrough:**

* `cloneGraph(null)`: Fails the first `if` check, returns `null`. Correct.
* `cloneGraph(Node(1))` (no neighbors): `visited` map created. `dfs` creates `clone(1)`, maps it. Loop over neighbors skips (it's empty). Returns `clone(1)`. Correct.
* `cloneGraph(1 <-> 2)`:
* `dfs(1)` clones `1`, maps `1 -> c1`. Iterates neighbors.
* Calls `dfs(2)` on neighbor. Clones `2`, maps `2 -> c2`. Iterates neighbors.
* Calls `dfs(1)` on neighbor. `visited` has `1`, returns `c1`.
* `c2` adds `c1` to neighbors.
* `dfs(2)` finishes, returns `c2` to `dfs(1)`.
* `c1` adds `c2` to neighbors.
* Returns `c1`. Both nodes cloned, pointers correctly reference the new instances. Correct.