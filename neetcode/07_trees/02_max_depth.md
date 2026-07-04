### question
Given the root of a binary tree, return its depth.

The depth of a binary tree is defined as the number of nodes along the longest path from the root node down to the farthest leaf node.

**1. Restating the question**
Find longest path from root to farthest leaf. Count number of nodes on this path. Return count.

**2. Clarifying questions, confirming inputs and outputs**

* Input: `root` of binary tree.
* Output: `int` (depth).
* Empty tree? Return `0`.
* Single node tree? Return `1`.

**3. Turn an example input into output by hand**
Tree:
3
/ 

9  20
/  

15   7

* At node 3: need left depth and right depth.
* Left (9): no children. Depth = 1.
* Right (20): has children 15, 7.
* Left of 20 (15): no children. Depth = 1.
* Right of 20 (7): no children. Depth = 1.
* Back to 20: max(1, 1) + 1 = 2. Depth = 2.
* Back to 3: max(left:1, right:2) + 1 = 3.
* Total depth: 3.

**4. Brainstorming possible solutions and complexity**

* **Recursive DFS (Post-order):** Process left, right, then current node. Natural fit for trees. Time: O(N) visit all nodes. Space: O(H) where H is tree height (call stack).
* **Iterative BFS:** Level-order traversal using a queue. Count levels. Time: O(N). Space: O(N) for queue at bottom level.
* **Iterative DFS:** Stack storing `(node, current_depth)`. Track max depth seen. Time O(N), Space O(H).

**5. Suggest solutions**

1. **Recursive DFS:** Direct translation of manual process in step 3. Ask children for depths, take max, add 1. Simple, clear.
2. **Iterative BFS:** Good if recursion depth is a concern.
Prefer Recursive DFS. Simplest, highly readable.

**6. Outline of the selected implementation**

```python
def maxDepth(root): 
    """
    Reframe: Depth of tree is 1 plus max depth of its deepest subtree.
    State: Call stack handles traversal. No explicit data structure. chosen because tree inherently recursive.
    Invariant: Function always returns max depth of subtree rooted at given node.

    getMaxChildDepth(node) = returns the maximum depth between the left child and right child.

    Core logic:
    - Get max depth of children using getMaxChildDepth
    - Add 1 to account for current node
    - Return result

    Edge cases:
    - Root is null/empty
    """
    pass

```

**7. Iterative implementation**

*Iteration 1: Skeleton with helper stubs.*

```python
def maxDepth(root):
    # Core logic outline
    child_depth = getMaxChildDepth(root)
    return child_depth + 1

def getMaxChildDepth(node):
    # TODO: compute max of left and right subtrees
    pass

```

*Iteration 2: Expanding the helper logic into the main function (converting human logic to code).*

```python
def maxDepth(root):
    # CHANGED: Inlined getMaxChildDepth by recursively calling maxDepth on children
    left_depth = maxDepth(root.left)
    right_depth = maxDepth(root.right)
    
    child_depth = max(left_depth, right_depth)
    return child_depth + 1

```

*Iteration 3: Walking edge cases. Adding patch for empty tree.*

```python
def maxDepth(root):
    # EDGE CASE: root is empty. Breaks on root.left/root.right access.
    # PATCH: return 0 early.
    if not root:
        return 0
        
    left_depth = maxDepth(root.left)
    right_depth = maxDepth(root.right)
    
    child_depth = max(left_depth, right_depth)
    return child_depth + 1

```

**8. Complexity and Optimizations**

* **Time Complexity:** O(N). Every node visited exactly once. Cannot optimize further; must see every node to know max depth.
* **Space Complexity:** O(H) where H is tree height. Best case O(log N) balanced. Worst case O(N) skewed tree (linked list).
* **Optimization note:** Code is optimal for general binary trees. If Python's recursion limit is a concern for extremely skewed trees (e.g., >1000 nodes deep), switch to Iterative BFS to trade call stack space for heap space. Code is clean and idiomatic; no clever micro-optimizations needed here.