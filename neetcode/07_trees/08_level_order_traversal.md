### question
Given a binary tree root, return the level order traversal of it as a nested list, where each sublist contains the values of nodes at a particular level in the tree, from left to right.


**1. Restating the question**
Given binary tree root. Return list of lists. Each inner list contains node values for one level, ordered left to right. Top level first, bottom level last.

**2. Clarifying questions & I/O**

* Input: `root` (TreeNode)
* Output: `List[List[int]]`
* Empty tree allowed? Yes. Expect `[]`.
* Unbalanced tree allowed? Yes.
* Node values? Integers.

**3. Example by hand**
Tree: `[3, 9, 20, null, null, 15, 7]`

* Start at root. Level 0: `[3]`.
* Look at 3's children. Level 1: `[9, 20]`.
* Look at 9's children (none), 20's children (15, 7). Level 2: `[15, 7]`.
* Output: `[[3], [9, 20], [15, 7]]`
* Mechanism: Maintain a line (queue). Put 3 in line. Process line (3), add its kids to next line. Process next line (9, 20), add kids. Repeat until line empty.

**4. Brainstorming & Complexity**

* *Approach 1: Breadth-First Search (BFS).* Use queue. Process level by level. Push root. While queue not empty, get current size `L`. Pop `L` times, recording values. Push children. Time: O(N), Space: O(N) (max queue size is bottom level, ~N/2).
* *Approach 2: Depth-First Search (DFS).* Pass `level` int down recursive calls. Append `node.val` to `result[level]`. Time: O(N), Space: O(H) for call stack.

**5. Suggest solutions**
Always prefer simple. Approach 1 (BFS) maps perfectly to human intuition (Step 3). We process it exactly how we read it: level by level. DFS is clever but requires tracking depth and expanding the result list dynamically. Let's use BFS.

**6. Outline selected implementation**

```python
def levelOrder(root):
    """
    Reframe: Traverse level by level, grouping nodes horizontally.
    State: Queue maintained, chosen because FIFO nature preserves left-to-right, level-by-level ordering.
    Invariant: At start of each while loop iteration, queue contains ONLY nodes for the current level.

    get_children(node) = returns list of non-null left/right children.

    Core logic:
    - initialize result list 
    - initialize queue with root node
    - loop while queue has nodes:
        - create empty list for current level values
        - get number of nodes currently in queue (level size)
        - loop exactly that many times:
            - remove front node from queue
            - add its value to current level list
            - put its children into queue using get_children
        - add current level list to result
    - return result

    Edge cases:
    - root is null (empty tree): return empty list immediately.
    """

```

**7. Iterative implementation**

*Iteration 1: Skeleton Code (Core Logic)*

```python
def levelOrder(root):
    # init state
    result = []
    queue = [root]
    
    # loop levels
    while queue:
        current_level_vals = []
        level_size = len(queue)
        
        # process current level
        for _ in range(level_size):
            node = queue.pop(0) # TODO: optimize pop(0) later
            current_level_vals.append(node.val)
            
            # TODO: add children to queue
            
        result.append(current_level_vals)
        
    return result

```

*Iteration 2: Fleshing out children logic (Core Complete)*

```python
def levelOrder(root):
    result = []
    queue = [root]
    
    while queue:
        current_level_vals = []
        level_size = len(queue) 
        
        for _ in range(level_size):
            node = queue.pop(0) 
            current_level_vals.append(node.val)
            
            # ADDED: explicitly push left then right to maintain order
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
            
        result.append(current_level_vals)
        
    return result

```

*Iteration 3: Patching Edge Cases*

```python
def levelOrder(root):
    # ADDED: Edge case patch - empty tree breaks when queue=[None] and we check node.val
    if not root:
        return []

    result = []
    queue = [root]
    
    while queue:
        current_level_vals = []
        level_size = len(queue) 
        
        for _ in range(level_size):
            node = queue.pop(0) 
            current_level_vals.append(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
            
        result.append(current_level_vals)
        
    return result

```

**8. Complexity & Optimizations**

* **Current Issue:** `queue.pop(0)` on a standard Python list is O(N) time because it shifts all elements. Inside a loop running N times, this degrades time complexity to O(N^2).
* **Optimization:** Use `collections.deque`, which provides O(1) `popleft()`.

*Final Optimized Code:*

```python
from collections import deque

def levelOrder(root):
    if not root:
        return []

    result = []
    # OPTIMIZATION: deque for O(1) pops
    queue = deque([root])
    
    while queue:
        current_level_vals = []
        level_size = len(queue) 
        
        for _ in range(level_size):
            # OPTIMIZATION: popleft instead of pop(0)
            node = queue.popleft() 
            current_level_vals.append(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
            
        result.append(current_level_vals)
        
    return result

```

* **Final Time Complexity:** O(N) where N is number of nodes. Each node enqueued/dequeued exactly once.
* **Final Space Complexity:** O(N). Max queue size is max width of tree. In a perfect binary tree, bottom level holds N/2 nodes.