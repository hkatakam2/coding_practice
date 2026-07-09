### question
You are given the root of a binary tree. Return only the values of the nodes that are visible from the right side of the tree, ordered from top to bottom.


**1. Restate**
Find the rightmost node at each depth of a binary tree. Return their values from top to bottom. Essentially, the last node of each level.

**2. Clarify**

* Q: Empty tree? A: Return empty list.
* Q: Tree leans heavily left? (Right children missing). A: Return leftmost visible node at that depth.
* Input: `TreeNode` root. Output: `List[int]`.

**3. Manual Example**
Input:

```text
    1
   / \
  2   3
   \   \
    5   4

```

* Level 0: nodes [1]. Last is 1.
* Level 1: nodes [2, 3]. Last is 3.
* Level 2: nodes [5, 4]. Last is 4.
Output: `[1, 3, 4]`.

**4. Brainstorm & Complexity**

* *Approach A (BFS Level-Order)*: Traverse level by level using a queue. Take the last node of each level.
* Time: O(N) visit every node.
* Space: O(W) where W is max tree width (at most N/2).


* *Approach B (DFS Right-First)*: Traverse root -> right -> left. Track depth. First time hitting a depth, add to result.
* Time: O(N).
* Space: O(H) where H is tree height.



**5. Suggest Solutions**
Prefer BFS (Approach A). It directly models the manual example (reading level by level and picking the last). Easy to explain, no recursive call-stack mental overhead.

**6. Outline**

```python
def right_side_view(root):  # -> List[int]
    """
    Reframe: Collect the final node processed at each depth level.
    State: Queue of nodes, chosen because BFS naturally isolates levels one by one.
    Invariant: At the start of the outer loop, the queue contains exactly the nodes for one complete level.

    get_level_size(q) = counts nodes currently in queue.
    add_children(node, q) = pushes left and right children to queue.

    Core logic:
    - push root to queue
    - while queue not empty:
        - note the size of the current level
        - iterate through exactly that many nodes
        - keep track of the current node
        - queue its children for the next level
        - after level finishes, the last seen node is the rightmost
        - add its value to results

    Edge cases:
    - Root is null
    """

```

**7. Iterative Implementation**

*Iteration 1: Skeleton with stubs*

```python
def right_side_view(root):
    result = []
    queue = Queue()
    queue.push(root)
    
    while queue.has_nodes():
        level_size = queue.get_level_size()
        last_node = None
        
        # process current level
        for _ in range(level_size):
            node = queue.pop()
            last_node = node
            queue.add_children(node)
            
        result.append(last_node.val)
        
    return result

```

*Iteration 2: Replace Queue stubs with standard `collections.deque*`

```python
from collections import deque

def right_side_view(root):
    result = []
    # changed: use standard deque for O(1) popleft
    queue = deque()
    queue.append(root)
    
    while queue:
        # changed: len(queue) correctly snapshots level size
        level_size = len(queue)
        last_node = None
        
        for _ in range(level_size):
            # changed: popleft for queue behavior
            node = queue.popleft()
            last_node = node
            
            # stub: add children
            if node.left: queue.append(node.left)
            if node.right: queue.append(node.right)
            
        result.append(last_node.val)
        
    return result

```

*Iteration 3: Patch Edge Cases*
Edge case identified in outline: Root is null.
Current code throws error on `queue.append(root)` followed by `node.left` if `root` is `None`.

```python
from collections import deque

def right_side_view(root):
    # PATCH: handle empty tree immediately
    if not root:
        return []

    result = []
    queue = deque([root])
    
    while queue:
        level_size = len(queue)
        
        for i in range(level_size):
            node = queue.popleft()
            
            # PATCH: instead of saving last_node every loop, 
            # just check if it's the last iteration of this level
            if i == level_size - 1:
                result.append(node.val)
            
            if node.left: 
                queue.append(node.left)
            if node.right: 
                queue.append(node.right)
                
    return result

```

**8. Complexity & Optimizations**

* **Time**: O(N). Each node appended/popped exactly once. `popleft()` is O(1).
* **Space**: O(W). Max queue size is max leaf nodes at bottom level. W <= N/2 for full tree. O(N) worst case.
* **Optimization**: Memory is bounded by deque overhead. No algorithmic optimization needed. DFS right-first could optimize space to O(H) (height of tree), better for wide trees, but BFS is optimal for readability and prevents max-recursion depth errors in extremely unbalanced trees. Logic is tight.