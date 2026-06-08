# question:
You are given a connected undirected graph with `n` nodes labeled from `1` to `n`. Initially, it contained no cycles and consisted of `n-1` edges.
We have now added one additional edge to the graph. The edge has two different vertices chosen from `1` to `n`, and was not an edge that previously existed in the graph.
The graph is represented as an array `edges` of length `n` where `edges[i] = [ai, bi]` represents an edge between nodes `ai` and `bi` in the graph.
Return an edge that can be removed so that the graph is still a connected non-cyclical graph. If there are multiple answers, return the edge that appears last in the input `edges`.

# 1. Restate

Tree (n nodes, n-1 edges, acyclic, connected) + 1 extra edge = n edges, exactly one cycle. Find & return the edge to delete so it's a tree again. If multiple valid, return the one latest in `edges`.

# 2. Clarifying Qs

- Edges undirected? **Yes.**
- Guaranteed exactly one extra edge (one cycle)? **Yes.**
- Nodes 1..n; `edges.length == n`? **Yes.**
- "Last in input" → scan order matters; the redundant edge is the one that closes a cycle when added in order. Return it.
- Self-loops? No (two different vertices). Duplicate of existing edge? No.

# 3. Example by hand

`edges = [[1,2],[1,3],[2,3]]`
- add [1,2]: 1,2 now connected.
- add [1,3]: 1,3 connected → component {1,2,3}.
- add [2,3]: 2 & 3 *already* in same component → this edge closes the cycle → **answer [2,3]**.

# 4. Brainstorm

- **Cycle detection via DFS**: build graph, find cycle, pick last edge on it. Fiddly to recover "last in input."
- **Union-Find (DSU)**: process edges in order; for each, if endpoints already connected → that's the redundant one (the cycle-closer). Because we scan in input order, the *first* edge we hit that connects two already-joined nodes is automatically the last-occurring redundant edge given the single-cycle guarantee. O(n·α(n)). Clean, directly answers the question.

Both work. DSU maps the "in-order, detect when an edge is superfluous" idea straight onto the by-hand process from step 3.

# 5. Pick

Two candidates:
- **DSU** (the formalization of the hand-trace in step 3)
- **DFS cycle-find**

# 6. Outline

```python
def findRedundantConnection(edges):  # -> List[int]
    """
    Reframe: scanning edges in order, the redundant one is the first edge
        whose two endpoints are ALREADY connected — adding it would close the cycle.
    State: DSU (disjoint-set / union-find) over nodes 1..n, chosen because it
        answers "are these two already in the same component?" in ~O(1),
        which is exactly the cycle-closing test.
    Invariant: after processing each kept edge, every set = one tree component
        (still acyclic). An edge that joins two nodes of the SAME set is the
        cycle-closer.

    find(x)        = representative (root) of x's component.
    connected(a,b) = find(a) == find(b).
    union(a,b)     = merge the two components.

    Core logic:
    - for each edge (a,b) in input order:
        - if a and b already connected -> this edge is redundant, return it
        - else union them
    Edge cases:
    - guaranteed one answer exists, so loop always returns (no fallthrough)
    - DSU init must cover labels 1..n (1-indexed)
    """
```

# 7. Iterative implementation

**Skeleton**

```python
def findRedundantConnection(edges):
    parent = init_dsu(n)
    for a, b in edges:
        if connected(a, b):
            return [a, b]
        union(a, b)
```

**Iter 1 — DSU init + find (path compression deferred)**

```python
def findRedundantConnection(edges):
    n = len(edges)
    parent = list(range(n + 1))          # 1-indexed; index 0 unused

    def find(x):
        while parent[x] != x:            # walk to root
            x = parent[x]
        return x

    for a, b in edges:
        if find(a) == find(b):           # connected -> redundant
            return [a, b]
        parent[find(a)] = find(b)        # union (naive)
```

**Iter 2 — add path compression (cheap optimization, keeps it readable)**

```python
def findRedundantConnection(edges):
    n = len(edges)
    parent = list(range(n + 1))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]  # compress: point to grandparent
            x = parent[x]
        return x

    for a, b in edges:
        ra, rb = find(a), find(b)
        if ra == rb:                       # same component -> cycle-closer
            return [a, b]
        parent[ra] = rb                    # union
```

Core logic complete.

**Edge cases walk**
- *Answer guaranteed* → loop always returns; no need for a fallthrough `return []`. Leave as-is.
- *1-indexed labels* → handled by sizing `parent` to `n+1`. ✓
- No self-loops / dup edges to special-case (problem guarantees). ✓

# 8. Complexity

- Each `find` ≈ O(α(n)) amortized with path compression (α = inverse Ackermann, effectively constant).
- Loop over n edges → **O(n·α(n)) ≈ O(n)** time, **O(n)** space for `parent`.
- Could add union-by-rank for the theoretical guarantee, but path compression alone is fast enough and adding rank hurts readability — skip unless asked.
