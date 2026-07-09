### question
Given the root of a binary tree, return true if it is a valid binary search tree, otherwise return false.

A valid binary search tree satisfies the following constraints:

The left subtree of every node contains only nodes with keys less than the node's key.
The right subtree of every node contains only nodes with keys greater than the node's key.
Both the left and right subtrees are also binary search trees.

**1. Restate**
Verify a binary tree is a valid BST. Every node's left descendants must be strictly smaller. Right descendants strictly larger. Rule applies recursively to all subtrees.

**2. Clarify & Confirm**

* Empty tree valid? Yes.
* Single node valid? Yes.
* Duplicates allowed? No, definition says "less than" and "greater than" (strict inequality).
* Input: `TreeNode` root.
* Output: `boolean`.

**3. Hand Trace**
Input: `[5, 4, 6, null, null, 3, 7]`

* Root: 5.
* Left child: 4. Is 4 < 5? Yes.
* Right child: 6. Is 6 > 5? Yes.
* Left subtree of 6: 3. Is 3 < 6? Yes. BUT is 3 > 5 (ancestor)? No.
* Fails. Output: False.

**4. Brainstorm & Complexity**

* *Approach A (Inorder Traversal)*: BST inorder traversal yields strictly increasing sequence. Traverse, store in array, check if sorted.
* Time: O(N). Space: O(N) array.


* *Approach B (Min/Max Bounds)*: Pass allowed value ranges down the tree. Root can be anything `(-inf, inf)`. Left child must be `(-inf, 5)`. Right child must be `(5, inf)`. Matches the hand trace exactly.
* Time: O(N). Space: O(H) call stack.



**5. Suggest Solutions**
Prefer Approach B. Clean, intuitive, matches human logic from step 3. Stops immediately upon finding violation. Approach A requires full traversal or global state tracking.

**6. Outline**

```python
def isValidBST(root): 
    """
    Reframe: Node valid if value falls within allowed (min, max) range dictated by ancestors.
    State: min_bound, max_bound passed down recursive stack. Chosen because BST rules transitively constrain all descendants.
    Invariant: At any node, all ancestors' rules satisfied if node.val is between bounds.

    validate_subtree(node, min_bound, max_bound) = checks if node respects bounds, then checks children with tightened bounds.

    Core logic:
    - if node is null, return true
    - check if node value violates min or max limits. If so, return false.
    - check left subtree, passing current node value as the new max limit.
    - check right subtree, passing current node value as the new min limit.
    - return true only if both left and right are valid.

    Edge cases:
    - Root is None (empty tree)
    - Node value equals bound (duplicate)
    - Node value is extreme integer (use infinity for initial bounds)
    """

```

**7. Iterative Implementation**

*Iteration 1: Skeleton*

```python
def isValidBST(root):
    # helper to check nodes recursively
    def validate_subtree(node, min_bound, max_bound):
        # TODO: base case
        # TODO: check current node against bounds
        # TODO: recurse left
        # TODO: recurse right
        pass
    
    # kick off with infinite bounds
    return validate_subtree(root, float('-inf'), float('inf'))

```

*Iteration 2: Core Logic*

```python
def isValidBST(root):
    def validate_subtree(node, min_bound, max_bound):
        # base case: reached bottom
        if not node:
            return True
            
        # check current node against bounds
        # logic: must be strictly greater than min, strictly less than max
        if node.val <= min_bound or node.val >= max_bound:
            return False
            
        # recurse left: max bound becomes current node val
        left_valid = validate_subtree(node.left, min_bound, node.val)
        
        # recurse right: min bound becomes current node val
        right_valid = validate_subtree(node.right, node.val, max_bound)
        
        return left_valid and right_valid

    return validate_subtree(root, float('-inf'), float('inf'))

```

*Iteration 3: Edge Cases Patching*
Core logic already naturally handles the edge cases mentioned:

* Empty tree (`root = None`) hits `if not node: return True` immediately.
* Duplicates handled correctly via `<=` and `>=` (fails them).
* Extreme integers handled by using Python's `float('-inf')` and `float('inf')`.
Code is fully robust as-is.

**8. Complexity & Optimizations**

* **Time Complexity:** O(N). Each node visited exactly once in worst case (valid BST).
* **Space Complexity:** O(H) where H is tree height. Best case O(log N) for balanced tree, worst case O(N) for skewed tree.
* **Optimization:** We compute both `left_valid` and `right_valid` completely before returning. Can short-circuit. If `left_valid` is False, no need to traverse right subtree.

*Final Optimized Logic:*

```python
def isValidBST(root):
    def validate_subtree(node, min_bound, max_bound):
        if not node:
            return True
            
        if node.val <= min_bound or node.val >= max_bound:
            return False
            
        # Short-circuit logic: immediately return if left fails
        return (validate_subtree(node.left, min_bound, node.val) and 
                validate_subtree(node.right, node.val, max_bound))

    return validate_subtree(root, float('-inf'), float('inf'))

```