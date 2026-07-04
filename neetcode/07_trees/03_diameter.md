### 1. Restate

Find longest path (measured in edges) between *any* two nodes in a binary tree. Path doesn't have to cross the root.

### 2. Clarifying Questions & I/O

* **Input:** `root` node of a binary tree.
* **Output:** Integer (max number of edges).
* **Questions:**
* Empty tree? (Assume 0).
* Single node tree? (Assume 0 edges).
* Node values matter? (No, only structure).



### 3. Example by Hand

Tree:

```text
      1
     / \
    2   3
   / \
  4   5

```

Paths to check:

* Through 1: left depth(2) + right depth(1) = 3 (Path: 4->2->1->3).
* Through 2: left depth(1) + right depth(1) = 2 (Path: 4->2->5).
Max edges = 3.

### 4. Brainstorming & Complexity

* **Approach A (Top-Down):** For every node, calculate `depth(left) + depth(right)`. Max of these is diameter.
* *Complexity:* `O(N^2)` worst case (skewed tree) because we recalculate depth repeatedly.


* **Approach B (Bottom-Up DFS):** Calculate depth from leaves up. At each node, compute its local diameter (`left_depth + right_depth`), update a global max, and return `max(left_depth, right_depth) + 1` to its parent.
* *Complexity:* `O(N)` time since we visit each node exactly once. `O(H)` space for call stack.



### 5. Suggested Solutions

Approach B is best. Simple, classic post-order traversal. It does the "by hand" logic (checking path lengths through each node) simultaneously with calculating depths.

### 6. Outline

```python
def diameterOfBinaryTree(root): # -> int
    """
    Reframe: Longest path through any node is the sum of its max left depth and max right depth.
    State: A single integer tracking maximum diameter seen so far, chosen because we only need the highest value across all nodes.
    Invariant: When processing a node, depths of its left and right subtrees are completely resolved.

    get_depth(node) = returns the max depth of the tree rooted at 'node', and updates the global diameter.

    Core logic:
    - initialize max diameter to zero
    - trigger depth calculation from root
        - compute left child depth
        - compute right child depth
        - path length through current node is left depth + right depth
        - update global max diameter if current path is longer
        - pass node's own max depth (1 + max of child depths) up to parent
    - return max diameter

    Edge cases:
    - node is null (return depth 0)
    """

```

### 7. Iterative Implementation

**Iteration 1: Skeleton & Stubs**

```python
def diameterOfBinaryTree(root):
    max_diameter = 0
    
    def get_depth(node):
        # TODO: base case
        # TODO: get left/right depths
        # TODO: update max_diameter
        # TODO: return depth
        pass
        
    get_depth(root)
    return max_diameter

```

**Iteration 2: Add recursive flow (Core Logic)**

```python
def diameterOfBinaryTree(root):
    max_diameter = [0] # List hack for nonlocal mutation
    
    def get_depth(node):
        # get left/right depths
        left_depth = get_depth(node.left)
        right_depth = get_depth(node.right)
        
        # update max_diameter
        # CHANGED: local diameter is sum of child depths
        current_diameter = left_depth + right_depth
        max_diameter[0] = max(max_diameter[0], current_diameter)
        
        # return depth
        # CHANGED: node's depth is 1 + longest branch
        return 1 + max(left_depth, right_depth)
        
    get_depth(root)
    return max_diameter[0]

```

**Iteration 3: Patching Edge Cases**

```python
def diameterOfBinaryTree(root):
    max_diameter = [0]
    
    def get_depth(node):
        # EDGES ADDED: if node is null, depth is 0. Prevents attribute errors on .left/.right
        if not node:
            return 0
            
        left_depth = get_depth(node.left)
        right_depth = get_depth(node.right)
        
        current_diameter = left_depth + right_depth
        max_diameter[0] = max(max_diameter[0], current_diameter)
        
        return 1 + max(left_depth, right_depth)
        
    get_depth(root)
    return max_diameter[0]

```

### 8. Complexity & Optimizations

* **Time Complexity:** `O(N)`. Every node is visited once during the DFS traversal. No redundant work.
* **Space Complexity:** `O(H)` where `H` is tree height. Best case `O(log N)` for balanced tree, worst case `O(N)` for linked-list-like skewed tree. Space used by recursion call stack.
* **Optimizations:** Code is already optimal for this problem. A minor Python-specific cleanup is using the `nonlocal` keyword instead of a list hack `[0]` to track state, making it slightly more readable:

```python
def diameterOfBinaryTree(root):
    max_diameter = 0
    
    def get_depth(node):
        nonlocal max_diameter
        if not node:
            return 0
        left = get_depth(node.left)
        right = get_depth(node.right)
        max_diameter = max(max_diameter, left + right)
        return 1 + max(left, right)
        
    get_depth(root)
    return max_diameter

```