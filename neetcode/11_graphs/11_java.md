### 1. Restate the problem

We are given a number `n`, representing nodes in a graph labeled from `0` to `n - 1`. We are also given a list of undirected `edges`, where each edge connects two nodes. Our goal is to determine the total number of distinct, disconnected subgraphs (connected components).

* **Given:** An integer `n` (number of nodes) and a 2D integer array `edges`.
* **Return:** An integer representing the number of connected components.
* **Constraint:** The graph is undirected. We must group all nodes that are connected (directly or transitively) and count the resulting groups.

### 2. Ask clarifying questions

In a real interview, I would quickly confirm a few details to ensure no hidden surprises:

* **Are the nodes strictly 0-indexed from 0 to n-1?** (Assuming yes).
* **Can there be isolated nodes with no edges?** (Assuming yes, which means they each count as their own component).
* **Can there be duplicate edges or self-loops?** (Assuming yes, our algorithm should safely ignore them).
* **What are the bounds of `n` and `edges.length`?** (Assuming `n` can be up to 100,000, meaning an $O(n^2)$ approach will time out).
* **Can `edges` be empty?** (Assuming yes, in which case the answer is simply `n`).

### 3. Work through an example by hand

Let's trace an example to solidify the logic.

* **Input:** `n = 5`, `edges = [[0, 1], [1, 2], [3, 4]]`

**Step-by-step:**

1. Start with 5 isolated components: `{0}, {1}, {2}, {3}, {4}`. (Count = 5)
2. Process `[0, 1]`: Nodes 0 and 1 are in different components. Merge them.
* Current sets: `{0, 1}, {2}, {3}, {4}`. (Count = 4)


3. Process `[1, 2]`: Node 1 is in `{0, 1}`, node 2 is in `{2}`. Merge them.
* Current sets: `{0, 1, 2}, {3}, {4}`. (Count = 3)


4. Process `[3, 4]`: Nodes 3 and 4 are in different components. Merge them.
* Current sets: `{0, 1, 2}, {3, 4}`. (Count = 2)



**Output:** 2 components.

### 4. Brainstorm solutions aloud

**Approach 1: Graph Traversal (DFS or BFS)**

* **Core idea:** Build an adjacency list from the edges. Iterate through all nodes from `0` to `n-1`. Whenever we find an unvisited node, increment our component count and run a full DFS/BFS to mark all reachable nodes as visited.
* **Time Complexity:** O(V + E) where V is `n` and E is the number of edges.
* **Space Complexity:** O(V + E) to store the adjacency list, plus O(V) for the `visited` array and recursion stack/queue.
* **Tradeoffs:** Very standard, but building the adjacency list requires extra memory and boilerplate. DFS can also risk stack overflow on highly unbalanced graphs if not careful, though usually fine in Java for typical constraints.

**Approach 2: Union-Find (Disjoint Set)**

* **Core idea:** Treat each node as its own component initially. Iterate through the edges and "union" the two endpoints. If the endpoints were in different sets, we successfully merged two components, so we decrement our total component count.
* **Time Complexity:** O(V + E * α(V)), where α is the inverse Ackermann function. Practically, this is O(V + E) or nearly constant time per edge.
* **Space Complexity:** O(V) for the `parent` and `rank` arrays.
* **Tradeoffs:** Highly space-efficient because we don't need to build an adjacency list. It also naturally keeps a running count of the components as we process the data.

### 5. Select the solution

I will use **Union-Find**.

It perfectly matches the property of dynamic connectivity. By starting with `n` components and decrementing a counter every time an edge successfully bridges two disconnected sets, we bypass the need for an adjacency list entirely. It is cleaner to implement, less memory-intensive, and entirely avoids recursion depth issues. I will use standard arrays for `parent` and `rank` to achieve optimal path compression and union-by-rank.

### 6. Write the implementation outline

```java
int countComponents(int n, int[][] edges) {
    /*
     * Reframe:
     * Start with n isolated components and merge them as we process each edge.
     *
     * State:
     * A `parent` array to track the root of each node's set.
     * A `rank` array to keep the trees flat during merges.
     * Chosen because Union-Find perfectly models merging disjoint sets.
     *
     * Invariant:
     * The number of unique roots in the parent array always equals the 
     * current component count.
     *
     * Helpers:
     * int find(int node, int[] parent)
     * - Finds the root of the set containing the node, applying path compression.
     * boolean union(int node1, int node2, int[] parent, int[] rank)
     * - Merges two sets. Returns true if a merge occurred, false if they were 
     *   already connected.
     *
     * Core logic:
     * - initialize component count to n
     * - initialize the parent array so each node points to itself
     * - iterate through each edge
     * - attempt to union the two nodes
     * - if the union is successful, decrement the component count
     * - return the final component count
     *
     * Edge cases:
     * - 0 edges (returns n)
     * - redundant edges / cycles (union returns false, count doesn't change)
     * - disconnected graph components
     */
}

```

### 7. Implement iteratively

**Iteration 1: Method skeleton**
First, I'll set up the main state, the loop over the edges, and the stub for the helper methods.

```java
class Solution {
    public int countComponents(int n, int[][] edges) {
        int components = n;
        int[] parent = new int[n];
        int[] rank = new int[n];
        
        for (int i = 0; i < n; i++) {
            parent[i] = i;
        }

        // TODO: iterate over edges and merge
        // TODO: decrement components upon successful merge

        return components;
    }
    
    // TODO: implement find
    
    // TODO: implement union
}

```

**Iteration 2: Implement the core loop and `find` helper**
Next, I will add the path-compression logic to the `find` method, which is the engine that keeps our lookup fast.

```java
class Solution {
    public int countComponents(int n, int[][] edges) {
        int components = n;
        int[] parent = new int[n];
        int[] rank = new int[n];
        
        for (int i = 0; i < n; i++) {
            parent[i] = i;
        }

        // Added: loop through edges and invoke union
        for (int[] edge : edges) {
            if (union(edge[0], edge[1], parent, rank)) {
                components--;
            }
        }

        return components;
    }
    
    // Added: find with path compression
    private int find(int node, int[] parent) {
        if (parent[node] != node) {
            // Compress the path by pointing directly to the root
            parent[node] = find(parent[node], parent);
        }
        return parent[node];
    }
    
    // TODO: implement union
}

```

**Iteration 3: Complete the happy path**
Now, I will implement the `union` helper using union-by-rank to ensure the trees remain flat, completing the core logic.

```java
class Solution {
    public int countComponents(int n, int[][] edges) {
        int components = n;
        int[] parent = new int[n];
        int[] rank = new int[n];
        
        for (int i = 0; i < n; i++) {
            parent[i] = i;
        }

        for (int[] edge : edges) {
            if (union(edge[0], edge[1], parent, rank)) {
                components--;
            }
        }

        return components;
    }
    
    private int find(int node, int[] parent) {
        if (parent[node] != node) {
            parent[node] = find(parent[node], parent);
        }
        return parent[node];
    }
    
    // Added: union by rank returning boolean on success
    private boolean union(int node1, int node2, int[] parent, int[] rank) {
        int root1 = find(node1, parent);
        int root2 = find(node2, parent);
        
        if (root1 == root2) {
            return false; // Already in the same component
        }
        
        // Merge smaller tree under the larger tree
        if (rank[root1] > rank[root2]) {
            parent[root2] = root1;
        } else if (rank[root1] < rank[root2]) {
            parent[root1] = root2;
        } else {
            parent[root2] = root1;
            rank[root1]++;
        }
        
        return true;
    }
}

```

**Edge-case pass**

* **Empty input (`edges` is empty):** The loop over `edges` is skipped. The method correctly returns the initial value `components = n`.
* **Duplicate edges or self-loops:** If `[1, 2]` appears twice, the first call to `union` merges them and returns `true`. The second call finds they share a root (`root1 == root2`) and returns `false`, safely ignoring it.
* **Integer overflow:** Node labels are within `int` ranges, and array sizes max out at `n`. No sums or distances are calculated, so overflow is impossible here.

### 8. Analyze expensive sections and optimize

The current implementation is already heavily optimized.

* **Time Complexity:** O(V + E * α(V)). Initializing the arrays takes O(V). Iterating through the edges takes O(E). The `find` and `union` operations take amortized O(α(V)) time, which is effectively O(1). Overall time is O(V + E).
* **Space Complexity:** O(V). We create two arrays, `parent` and `rank`, each of size `n`.

No further optimization is necessary or practically beneficial.

### Final Code

```java
class Solution {
    public int countComponents(int n, int[][] edges) {
        int components = n;
        int[] parent = new int[n];
        int[] rank = new int[n];
        
        for (int i = 0; i < n; i++) {
            parent[i] = i;
        }

        for (int[] edge : edges) {
            if (union(edge[0], edge[1], parent, rank)) {
                components--;
            }
        }

        return components;
    }
    
    private int find(int node, int[] parent) {
        if (parent[node] != node) {
            parent[node] = find(parent[node], parent);
        }
        return parent[node];
    }
    
    private boolean union(int node1, int node2, int[] parent, int[] rank) {
        int root1 = find(node1, parent);
        int root2 = find(node2, parent);
        
        if (root1 == root2) {
            return false;
        }
        
        if (rank[root1] > rank[root2]) {
            parent[root2] = root1;
        } else if (rank[root1] < rank[root2]) {
            parent[root1] = root2;
        } else {
            parent[root2] = root1;
            rank[root1]++;
        }
        
        return true;
    }
}

```

### Brief Test Walkthrough

Let's test with `n = 4` and a cycle: `edges = [[0, 1], [1, 2], [2, 0]]`.

* Initialize `components = 4`.
* Edge `[0, 1]`: `union(0, 1)` -> different roots. Merge them. `components` becomes 3.
* Edge `[1, 2]`: `union(1, 2)` -> different roots. Merge them. `components` becomes 2.
* Edge `[2, 0]`: `union(2, 0)` -> `find(2)` and `find(0)` return the same root because they were connected previously. `union` returns `false`. `components` stays 2.
* Result: `2` (One component of size 3, plus node 3 which is isolated). This correctly identifies the disjoint structure despite the cycle.