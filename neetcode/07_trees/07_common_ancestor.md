### question
Given a binary search tree (BST) where all node values are unique, and two nodes from the tree p and q, return the lowest common ancestor (LCA) of the two nodes.

The lowest common ancestor between two nodes p and q is the lowest node in a tree T such that both p and q as descendants. The ancestor is allowed to be a descendant of itself.

### 1. Restating the Question

Given a Binary Search Tree (BST) with unique values, find the Lowest Common Ancestor (LCA) of two given nodes, `p` and `q`. LCA is the deepest node that has both `p` and `q` as descendants (a node can be a descendant of itself).

### 2. Clarifying Questions

* **Inputs:** `root` node of BST, `p` node, `q` node.
* **Outputs:** `Node` that is the LCA.
* **Assumptions to confirm:**
* Are `p` and `q` guaranteed to exist in the tree? *Assume yes.*
* Can `p` or `q` be the `root`? *Assume yes.*
* Do nodes have parent pointers? *Assume no.*
* Are `p` and `q` guaranteed to be distinct? *Assume yes.*



### 3. Hand-Trace Example

Input: BST `[6, 2, 8, 0, 4, 7, 9]`, `p = 2`, `q = 8`

* Start at root `6`.
* Compare `p` (2) and `q` (8) with root `6`.
* `2 < 6` (left side) and `8 > 6` (right side).
* `p` and `q` diverge at `6`.
* Output: `6`.

Input 2: `p = 2`, `q = 4` (same tree)

* Start at root `6`.
* `2 < 6` and `4 < 6`. Both are on the left.
* Move to left child: `2`.
* Compare `p` (2) and `q` (4) with current node `2`.
* `2 == 2`, `4 > 2`. One matches, one goes right. Divergence!
* Output: `2`.

### 4. Brainstorming & Complexity

* **Approach A:** Standard Binary Tree LCA. Traverse whole tree, bubble up found nodes. Ignores BST properties. Complexity: Time O(N), Space O(H) for call stack.
* **Approach B:** Recursive BST property. If both `< root`, recurse left. If both `> root`, recurse right. Else return root. Complexity: Time O(H), Space O(H) call stack.
* **Approach C:** Iterative BST property (simulating the hand-trace). Maintain current node. Traverse down based on value comparisons. Stop when nodes split. Complexity: Time O(H), Space O(1).

### 5. Suggest Solutions

Prefer Approach C (Iterative BST traversal). It translates the exact hand-trace logic from step 3 directly into a space-efficient, easy-to-explain loop. No call stack overhead. Clear "split point" logic.

### 6. Outline Selected Implementation

```python
def lowestCommonAncestor(root, p, q): # -> TreeNode
    """
    Reframe: LCA is the exact point where the paths to p and q diverge.
    State: current_node, chosen because tracking the traversal path downwards suffices for BST.
    Invariant: The true LCA is always within the subtree of current_node.

    both_smaller(node, p, q) = checks if values of p and q are both less than node value
    both_larger(node, p, q) = checks if values of p and q are both greater than node value

    Core logic:
    - start at tree root
    - loop continuously
    - if both_smaller(current_node, p, q), move current_node to left child
    - if both_larger(current_node, p, q), move current_node to right child
    - otherwise, paths diverge here (or one node equals current_node). Return current_node.

    Edge cases:
    - empty tree (root is None)
    """

```

### 7. Iterative Implementation

**Iteration 1: Skeleton with helper stubs**

```python
def lowestCommonAncestor(root, p, q):
    # Setup state
    curr = root
    
    # Core logic loop
    while curr:
        if both_smaller(curr, p, q):
            curr = curr.left
        elif both_larger(curr, p, q):
            curr = curr.right
        else:
            # Divergence found
            return curr

# To-do: implement both_smaller, both_larger

```

**Iteration 2: Inline helpers to finish core logic**

```python
def lowestCommonAncestor(root, p, q):
    curr = root
    
    while curr:
        # Changed: inlined both_smaller using node values
        if p.val < curr.val and q.val < curr.val:
            curr = curr.left
        # Changed: inlined both_larger using node values
        elif p.val > curr.val and q.val > curr.val:
            curr = curr.right
        else:
            return curr

```

**Iteration 3: Patching edge cases**
*Edge case: Empty tree (root is None).*
Look at Iteration 2: If `root` is `None`, `curr` is `None`. The `while curr:` loop skips, implicitly returning `None` at the end of the function. No explicit patch needed, but let's make it explicit for clarity.

```python
def lowestCommonAncestor(root, p, q):
    # Added: explicit edge case check
    if not root:
        return None
        
    curr = root
    while curr:
        if p.val < curr.val and q.val < curr.val:
            curr = curr.left
        elif p.val > curr.val and q.val > curr.val:
            curr = curr.right
        else:
            return curr

```

### 8. Complexity & Optimizations

* **Time Complexity:** O(H), where H is height of BST. In worst case (skewed tree), O(N). In balanced tree, O(log N). Only traversing one path down.
* **Space Complexity:** O(1). Only maintaining `curr` pointer. No auxiliary memory allocated.
* **Optimization:** Logic is optimal. Space cannot be improved. Time cannot be improved without self-balancing guarantees (which would make worst-case O(log N), but logic remains identical). Code is minimal and highly readable.