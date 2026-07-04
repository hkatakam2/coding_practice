### question
You are given the root of a binary tree root. Invert the binary tree and return its root.


**1. Restating the question**
Given a binary tree. Mirror it. Left children become right children, right children become left children. Return new root.

**2. Clarifying questions & inputs/outputs**

* Input: `root` of binary tree.
* Output: `root` of inverted tree.
* Modifying in-place? Yes, standard practice saves memory.
* Empty tree possible? Yes. Output should be `None`.

**3. Example input to output by hand**
Input:
4
/   

2     7
/ \   / 

1   3 6   9

Hand execution (Top-down):

* Look at 4. Swap children (2 and 7).
4
/   
7     2
/ \   / 
6   9 1   3  <-- notice children followed their parents
* Look at 7. Swap children (6 and 9).
* Look at 2. Swap children (1 and 3).

Output:
4
/   

7     2
/ \   / 

9   6 3   1

**4. Brainstorming & Complexity**

* **Recursive DFS (Pre-order):** Visit node, swap children, recurse left, recurse right. Time O(N) to visit all nodes. Space O(H) for call stack (H=height).
* **Iterative BFS:** Use queue. Pop node, swap children, push children. Time O(N). Space O(W) for queue width.
* **Iterative DFS:** Use stack. Pop node, swap children, push children. Time O(N). Space O(H).

**5. Suggesting solutions**

* Recursive DFS maps directly to our top-down hand execution.
* Iterative BFS avoids recursion limits.
* *Selection:* Recursive DFS. Simplest, cleanest, reads like plain English.

**6. Outline & Logic**

```python
def invertTree(root): 
    """
    Reframe: Tree inversion is just swapping left and right pointers at every single node.
    State: Call stack, chosen because trees are naturally recursive structures.
    Invariant: When a node is processed, its immediate left and right pointers are swapped.

    swap_children(node) = swaps the left and right pointers of the given node.
    invert_node(node) = applies invertTree to a node.

    Core logic:
    - Swap children of current root
    - Invert the left subtree
    - Invert the right subtree
    - Return root

    Edge cases:
    - Root is None (happens on empty tree or when reaching leaf's children)
    """

```

**7. Iterative Implementation**

*Iteration 1: Skeleton mapping to core logic*

```python
def invertTree(root):
    # Core Logic (Happy Path)
    swap_children(root)
    invert_node(root.left)
    invert_node(root.right)
    
    return root

```

*Iteration 2: Translating dummy helpers into real logic*

```python
def invertTree(root):
    # change: inline swap_children
    root.left, root.right = root.right, root.left
    
    # change: inline invert_node recursion
    invertTree(root.left)
    invertTree(root.right)
    
    return root

```

*Iteration 3: Walk edge cases and patch*
Code breaks if `root` is `None` (gives `AttributeError` on `root.left`). Add edge case check at the top.

```python
def invertTree(root):
    # change: patch edge case for empty node/tree
    if root is None:
        return None

    # Core Logic
    root.left, root.right = root.right, root.left
    
    invertTree(root.left)
    invertTree(root.right)
    
    return root

```

**8. Complexity & Optimizations**

* **Time:** O(N). Every node visited exactly once. Cannot optimize further; reading tree requires O(N).
* **Space:** O(H). Call stack goes as deep as tree height. O(log N) for balanced, O(N) for skewed.
* **Optimization note:** Python has a recursion limit (~1000). For extremely deep, unbalanced trees, this recursive approach crashes.
* **Fix for extreme scale (Iterative BFS):**

```python
def invertTree_iterative(root):
    if not root: return None
    queue = [root] # python list as queue for brevity
    while queue:
        curr = queue.pop(0) # O(N) pop, ideally use collections.deque
        curr.left, curr.right = curr.right, curr.left
        if curr.left: queue.append(curr.left)
        if curr.right: queue.append(curr.right)
    return root

```