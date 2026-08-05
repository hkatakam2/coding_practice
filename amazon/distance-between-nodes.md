### question
Find distance between any two nodes in a tree. Parent pointers not given. Only have root, source, and target in input.

### Step 1: Restate Question

Given root of binary tree, find number of edges in shortest path between two target nodes `p` and `q`. Parent pointers not available.

---

### Step 2: Clarify & Confirm Inputs/Outputs

* **Tree Type:** General Binary Tree (not BST, unsorted).
* **Inputs:** `root: TreeNode`, `p: TreeNode`, `q: TreeNode`.
* **Output:** `int` (distance/edge count).
* **Assumptions:** `p` and `q` exist in tree; node references unique; `p == q` returns `0`.

---

### Step 3: Manual Example

```text
       3
      / \
     5   1
    / \ / \
   6  2 0  8
     / \
    7   4

```

* **Example 1:** `p = 5`, `q = 1`
* Path: `5 -> 3 -> 1`
* Distance = 2.


* **Example 2:** `p = 5`, `q = 4`
* Path: `5 -> 2 -> 4`
* Distance = 2 (LCA is `5`).



---

### Step 4: Brainstorm Solutions & Complexity

1. **Root-to-Node Paths:** Find path array from `root` to `p` and `root` to `q`. Find mismatch index.
* *Time:* $O(N)$, *Space:* $O(H)$ for paths.


2. **LCA + Subtree Depth:** Find Lowest Common Ancestor (LCA) of `p` and `q`. Distance = `depth(LCA, p) + depth(LCA, q)`.
* *Time:* $O(N)$, *Space:* $O(H)$ recursion stack.



---

### Step 5: Suggested Solution

Choose **Approach 2 (LCA + Depth)**. Modular, highly readable, mirrors manual visual traversal.

---

### Step 6: Implementation Outline

```python
def find_distance(root: TreeNode, p: TreeNode, q: TreeNode) -> int:
    """
    Reframe: Distance between p and q equals distance(LCA, p) + distance(LCA, q).
    State: Call stack frame state during tree traversal.
    Invariant: find_lca returns LCA of p and q in subtree; get_depth returns edge distance from root of subtree to target node.

    find_lca(node, p, q) = returns node if node is LCA or matches p/q in subtree, else None.
    get_depth(node, target) = returns edge count from node to target, or -1 if target not in subtree.

    Core logic:
    - find lowest common ancestor of p and q in tree
    - compute depth from lowest common ancestor to p
    - compute depth from lowest common ancestor to q
    - return sum of depth to p and depth to q

    Edge cases:
    - p == q (same node)
    - p is ancestor of q (or vice versa)
    - p or q is root
    """

```

---

### Step 7: Iterative Implementation

#### Iteration 1: Skeleton with stubs

```python
def find_distance(root: TreeNode, p: TreeNode, q: TreeNode) -> int:
    # Core logic outline using helpers
    lca = find_lca(root, p, q)
    dist_p = get_depth(lca, p)
    dist_q = get_depth(lca, q)
    return dist_p + dist_q

def find_lca(node: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    # TODO: implement LCA logic
    pass

def get_depth(node: TreeNode, target: TreeNode) -> int:
    # TODO: implement depth lookup
    pass

```

#### Iteration 2: Fill in `get_depth` helper

```python
def find_distance(root: TreeNode, p: TreeNode, q: TreeNode) -> int:
    lca = find_lca(root, p, q)
    dist_p = get_depth(lca, p, 0) # UPDATED: add distance accumulator
    dist_q = get_depth(lca, q, 0)
    return dist_p + dist_q

def find_lca(node: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    pass

def get_depth(node: TreeNode, target: TreeNode, current_dist: int) -> int:
    # ADDED: base case and recursive tree traversal for depth
    if not node:
        return -1
    if node == target:
        return current_dist
    
    left = get_depth(node.left, target, current_dist + 1)
    if left != -1:
        return left
        
    return get_depth(node.right, target, current_dist + 1)

```

#### Iteration 3: Fill in `find_lca` helper (Core Logic Complete)

```python
def find_distance(root: TreeNode, p: TreeNode, q: TreeNode) -> int:
    lca = find_lca(root, p, q)
    dist_p = get_depth(lca, p, 0)
    dist_q = get_depth(lca, q, 0)
    return dist_p + dist_q

def find_lca(node: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    # ADDED: standard post-order LCA lookup
    if not node or node == p or node == q:
        return node
    
    left = find_lca(node.left, p, q)
    right = find_lca(node.right, p, q)
    
    if left and right:
        return node
    return left if left else right

def get_depth(node: TreeNode, target: TreeNode, current_dist: int) -> int:
    if not node:
        return -1
    if node == target:
        return current_dist
    
    left = get_depth(node.left, target, current_dist + 1)
    if left != -1:
        return left
        
    return get_depth(node.right, target, current_dist + 1)

```

#### Iteration 4: Checking Edge Cases

1. **Edge Case: `p == q**`
* `find_lca` returns `p`.
* `get_depth(p, p, 0)` returns `0`. `get_depth(p, p, 0)` returns `0`.
* Result = `0`. **(Passes without code changes)**


2. **Edge Case: `p` is ancestor of `q**`
* `find_lca` hits `node == p` early and returns `p`.
* `get_depth(p, p, 0)` returns `0`.
* `get_depth(p, q, 0)` returns exact distance from `p` to `q`.
* Result = `dist(p, q)`. **(Passes without code changes)**


3. **Edge Case: `p` or `q` is `root**`
* `find_lca` returns `root`.
* Depth logic evaluates from root correctly. **(Passes without code changes)**



---

### Step 8: Complexity & Optimizations

* **Time Complexity:**
* `find_lca`: $O(N)$ (visits all nodes worst case).
* `get_depth`: $O(N)$ twice.
* Total Time: $O(N)$.


* **Space Complexity:**
* $O(H)$ recursion stack depth ($H$ = tree height; $O(N)$ worst-case skew, $O(\log N)$ balanced).



#### Single-Pass Optimization Trade-off:

Can compute distance in a single DFS pass by returning distance when finding target nodes. However, 2-pass (LCA + Depth) keeps functions decoupled, reduces bug surface in live interviews, and maintains identical $O(N)$ asymptotic time complexity.