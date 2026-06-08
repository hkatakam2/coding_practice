# question
You have a graph of n nodes. You are given an integer n and an array edges where edges[i] = [aᵢ, bᵢ] indicates that there is an edge between aᵢ and bᵢ in the graph.
Return the number of connected components in the graph.

Here is the Union-Find approach, broken down using the same interview framework to show how you would build it iteratively.

### 6. Implementation Outline

```python
def countComponents(n, edges):
    """
    Reframe: Start with n isolated islands. Every time an edge connects two separate islands, the total island count drops by 1.
    State: `parent` array, chosen because we need to quickly check if two nodes belong to the same set and merge them if they don't.
    Invariant: Two nodes are in the same component if and only if they resolve to the same root in the `parent` array.

    find(node) = climbs the parent chain to find the absolute root of the set.
    union(node1, node2) = finds roots of both nodes. If different, makes one root point to the other and returns True (successful merge).

    Core logic:
    - initialize parent array where each node is its own parent
    - initialize component count to n
    - loop through each edge (u, v):
        - if union(u, v) is successful (they were in separate components):
            - decrement component count
    - return component count

    Edge cases:
    - edges array is empty (returns n, naturally handled)
    - multiple edges between same nodes or cycles (union returns False, count doesn't decrement, naturally handled)
    """

```

### 7. Iterative Implementation

**Iteration 1: Skeleton**
Translate the plain English core logic into a structure with stubs.

```python
def countComponents(n, edges):
    parents = [i for i in range(n)] 
    count = n
    
    # TODO: implement find helper
    def find(node):
        pass
        
    # TODO: implement union helper
    def union(n1, n2):
        pass
        
    for u, v in edges:
        if union(u, v):
            count -= 1
            
    return count

```

**Iteration 2: Implementing `find**`
Fleshing out the root-finding logic. We add "path compression" here so future lookups are $O(1)$.

```python
def countComponents(n, edges):
    parents = [i for i in range(n)]
    count = n
    
    # ADDED: find logic with path compression
    def find(node):
        if parents[node] == node:
            return node
        # Path compression: point directly to the root
        parents[node] = find(parents[node]) 
        return parents[node]
        
    def union(n1, n2):
        pass # TODO
        
    for u, v in edges:
        if union(u, v):
            count -= 1
            
    return count

```

**Iteration 3: Core Logic Complete**
Implementing `union` to merge sets and checking edge cases.

```python
def countComponents(n, edges):
    parents = [i for i in range(n)]
    count = n
    
    def find(node):
        if parents[node] == node:
            return node
        parents[node] = find(parents[node])
        return parents[node]
        
    # ADDED: union logic to merge distinct sets
    def union(n1, n2):
        root1 = find(n1)
        root2 = find(n2)
        
        if root1 != root2:
            parents[root2] = root1 # connect the roots
            return True
        return False # already in the same component
        
    for u, v in edges:
        if union(u, v):
            count -= 1
            
    return count

```

**Iteration 4: Edge Cases**

* **Cycles / Redundant Edges:** If an edge connects `1` and `2`, but they are already connected via other nodes, `find(1)` and `find(2)` will return the same root. `union` returns `False`, `count` is not decremented. Code handles this safely.
* **No edges:** Loop doesn't run, returns initial `count` ($n$). Safe.

### 8. Complexity Review

* **Time Complexity:** $O(V + E \cdot \alpha(V))$.
* Initializing the `parents` array takes $O(V)$ where $V$ is $n$.
* Iterating through $E$ edges takes $O(E)$. Inside the loop, `find` uses path compression, meaning the cost of operations grows extremely slowly, bounded by the Inverse Ackermann function $\alpha(V)$. For all practical purposes, this is nearly $O(1)$, making the total edge processing $O(E)$.


* **Space Complexity:** $O(V)$.
* The `parents` array requires space proportional to the number of nodes $n$. We completely avoided building an $O(V + E)$ adjacency list, strictly optimizing our memory footprint.