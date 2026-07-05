### question
Given the roots of two binary trees p and q, return true if the trees are equivalent, otherwise return false.

Two binary trees are considered equivalent if they share the exact same structure and the nodes have the same values.

1. Restate
Check if two binary trees are identical in shape and node values.
2. Clarify & Confirm I/O
Inputs: `p` (root of tree 1), `q` (root of tree 2).
Outputs: Boolean.
Questions: Can trees be empty? Yes. Values fit in standard types? Yes.
3. By Hand Example
Input: `p` = [1, 2, 3], `q` = [1, 2, 3]
Compare root `p` (1) with root `q` (1) -> match.
Move left. Compare `p.left` (2) with `q.left` (2) -> match.
Move right. Compare `p.right` (3) with `q.right` (3) -> match.
All matched. Output: True.
4. Brainstorm Solutions

* Approach A: Depth First Search (DFS) recursion. Traverse both simultaneously. Check current, recurse left, recurse right. Time: O(N). Space: O(H) for call stack.
* Approach B: Breadth First Search (BFS) iterative. Queue holding node pairs. Pop, check, push children. Time: O(N). Space: O(N) for queue.
* Approach C: Serialize both to string (pre-order with null markers), compare strings. Time: O(N). Space: O(N).

5. Suggest Solutions
Prefer DFS recursion. Simple, maps directly to "by hand" traversal step. BFS is fine but more boilerplate. Serialize is memory heavy. Selecting DFS recursion.
6. Outline

```python
def isSameTree(p, q): 
    """
    Reframe: Trees match if current nodes match AND subtrees match.
    State: Call stack tracks current node pairs, chosen because recursion naturally handles tree traversal.
    Invariant: False if any visited pair mismatches.

    hasSameValue(nodeA, nodeB) = checks if both nodes hold same value.

    Core logic:
    - check if current nodes have same value
    - check if left subtrees are identical
    - check if right subtrees are identical
    - return true if all three checks pass

    Edge cases:
    - both nodes missing -> identical (base case)
    - one missing, one exists -> mismatch
    """

```

7. Iterative Implementation

Iteration 1: Skeleton of core logic (assuming nodes exist)

```python
def isSameTree(p, q):
    # check current
    val_match = hasSameValue(p, q)
    # check left
    left_match = isSameTree(left of p, left of q)
    # check right
    right_match = isSameTree(right of p, right of q)

    return val_match and left_match and right_match

```

Iteration 2: Replace plain English/stubs with Python syntax

```python
def isSameTree(p, q):
    # added real syntax for core logic
    val_match = (p.val == q.val)
    left_match = self.isSameTree(p.left, q.left)
    right_match = self.isSameTree(p.right, q.right)

    return val_match and left_match and right_match

```

Iteration 3: Patch first edge case (both missing)

```python
def isSameTree(p, q):
    # patch: handle both missing (reached leaf children or empty inputs)
    if not p and not q:
        return True

    val_match = (p.val == q.val)
    left_match = self.isSameTree(p.left, q.left)
    right_match = self.isSameTree(p.right, q.right)

    return val_match and left_match and right_match

```

Iteration 4: Patch second edge case (one missing)

```python
def isSameTree(p, q):
    if not p and not q:
        return True
    
    # patch: handle one missing, other exists (structural mismatch)
    if not p or not q:
        return False

    val_match = (p.val == q.val)
    left_match = self.isSameTree(p.left, q.left)
    right_match = self.isSameTree(p.right, q.right)

    return val_match and left_match and right_match

```

8. Complexity & Optimization
Time: O(N) where N is min nodes between `p` and `q`.
Space: O(H) where H is min height (call stack).
Code can be compressed to leverage Python's `and` short-circuiting. If `p.val != q.val`, it halts immediately without evaluating subtrees.

Final compressed code:

```python
def isSameTree(self, p, q):
    if not p and not q:
        return True
    if not p or not q:
        return False
    return p.val == q.val and self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)

```