Question 2: Tree TransformationThe Setup: A tree problem where DFS/BFS works, but the interviewer pushes for an $O(1)$ space solution using "two pointers" and "transforming into a simpler structure" (Morris Traversal).

### question
Flattening the Hierarchy: You are given the root of a Binary Search Tree (BST) representing a company's hierarchical reporting structure. We are migrating to a new flat-management system. Convert this BST into a sorted doubly linked list in place, where the left pointer acts as "previous" and the right pointer acts as "next". (Expected approach: In-order DFS traversal, keeping track of the previously visited node. Uses $O(H)$ space for the call stack).

### 1. Restating the Question

Convert a Binary Search Tree (BST) into a sorted doubly linked list (DLL) in-place:

* `left` pointer becomes `previous` (`prev`).
* `right` pointer becomes `next`.
* Nodes must be ordered from smallest to largest value.
* Return the head of the newly formed doubly linked list.

---

### 2. Clarifying Questions

* **Linear vs Circular DLL?** Linear (first node's `left` and last node's `right` point to `None`).
* **Input empty/null?** Yes, if `root` is `None`, return `None`.
* **Single node tree?** Valid tree; `left` and `right` should both remain `None`.
* **Can we modify the original node structure?** Yes, reassigning `left` and `right` in-place.

---

### 3. Hand-Tracing an Example

**Input BST:**

```text
       4
     /   \
    2     5
   / \
  1   3

```

**In-Order Order:** `1 -> 2 -> 3 -> 4 -> 5`

**Process:**

1. Reach leftmost node: `1`. Set `head = 1`. `prev = 1`.
2. Visit `2`: `1.right = 2`, `2.left = 1`. Set `prev = 2`.
3. Visit `3`: `2.right = 3`, `3.left = 2`. Set `prev = 3`.
4. Visit `4`: `3.right = 4`, `4.left = 3`. Set `prev = 4`.
5. Visit `5`: `4.right = 5`, `5.left = 4`. Set `prev = 5`.

**Output DLL:** `1 <-> 2 <-> 3 <-> 4 <-> 5` (Return node `1`).

---

### 4. Brainstorming Solutions & Complexity

* **Approach A: Flatten to Array, then Relink**
* Store nodes in an array using in-order traversal, then iterate array to set `left`/`right`.
* *Time:* $O(N)$
* *Space:* $O(N)$ auxiliary space for array. Not strictly in-place.


* **Approach B: In-Order DFS Traversal with State Tracking (Chosen)**
* Maintain a `prev` pointer tracking the previously processed node during in-order traversal.
* Connect `prev.right = curr` and `curr.left = prev` on the fly.
* *Time:* $O(N)$
* *Space:* $O(H)$ call stack space ($H$ = tree height).



---

### 5. Suggested Solution

**In-Order DFS Traversal (Approach B)** is simple, clear, directly modifies pointers in sorted order, and requires only $O(H)$ stack memory.

---

### 6. Outline of Implementation

```python
def flattenToDoublyList(root):  # -> Node
    """
    Reframe: Standard BST in-order traversal visits nodes in strictly increasing order; re-link pointers continuously during traversal.
    State: `prev` (tracks last processed node), `head` (tracks first/smallest processed node).
    Invariant: Already visited nodes form a connected, sorted doubly linked list up to `prev`.

    link_nodes(curr) = links `prev.right = curr` and `curr.left = prev`, then updates `prev = curr`.

    Core logic:
    - recurse on left child
    - visit current node: link with previous node using dummy helper
    - recurse on right child
    - return head of list

    Edge cases:
    - tree is empty (root is None)
    - tree has single node (head and prev point to same node; subtrees empty)
    """

```

---

### 7. Iterative Implementation

#### Iteration 1: Code Skeleton (Plain English Core Logic Structure)

```python
class Node:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def flattenToDoublyList(root):
    # State tracking
    prev = None
    head = None
    
    def inorder(node):
        nonlocal prev, head
        # TODO: Return if node is empty
        
        # 1. Recurse left
        inorder(node.left)
        
        # 2. Visit current node (Core Happy Path)
        # TODO: Link prev and current node using helper logic
        
        # 3. Recurse right
        inorder(node.right)
        
    inorder(root)
    return head

```

#### Iteration 2: Realizing Core Logic (Happy Path)

```python
def flattenToDoublyList(root):
    prev = None
    head = None
    
    def inorder(node):
        nonlocal prev, head
        if not node:
            return
        
        # Recurse left
        inorder(node.left)
        
        # --- Core Logic Implementation ---
        # First node visited becomes the head
        if not head:
            head = node
            
        # Link previous node with current node if previous exists
        if prev:
            prev.right = node
            node.left = prev
            
        # Move state pointer forward
        prev = node
        # ---------------------------------
        
        # Recurse right
        inorder(node.right)
        
    inorder(root)
    return head

```

#### Iteration 3: Walking Edge Cases

1. **Edge Case 1: `root` is `None**`
* *Walkthrough:* `inorder(None)` exits immediately. `head` remains `None`. Returns `None`. Correct.


2. **Edge Case 2: Single node tree (`root` with no children)**
* *Walkthrough:* Left recursive call returns. `head` set to `root`. `prev` set to `root`. Right call returns. Returns `head`. Correct.


3. **Edge Case 3: Skewed Tree (e.g., linked list shape)**
* *Walkthrough:* Left/right recursions hit base cases without breaking stack assumptions. Correct.



*Code is fully realized and robust against edge cases.*

---

### 8. Complexity & Optimizations

* **Time Complexity:** $O(N)$
* Every node visited exactly once during in-order traversal.


* **Space Complexity:** $O(H)$
* Where $H$ is tree height. Call stack depth equals maximum tree depth.
* Best/Average (balanced BST): $O(\log N)$ space.
* Worst (skewed tree): $O(N)$ space.



#### Optimization Note (Morris Traversal)

If $O(1)$ auxiliary space is strictly required (eliminating the recursion call stack), **Morris In-Order Traversal** can be used. However, it alters tree structure temporarily to navigate without recursion, increasing code complexity significantly. DFS with $O(H)$ stack space remains preferred for interview clarity.

## Follow up
Strict $O(1)$ Space: Our servers are highly memory-constrained, and the tree could be massively unbalanced (skewed like a linked list). Can you achieve this transformation using strictly $O(1)$ extra space, meaning no recursive call stack and no standard queue? (Expected approach: Morris Traversal, using a two-pointer approach to temporarily thread the rightmost child of the left subtree back to the current node)


### 1. Restating the Question

Convert a Binary Search Tree (BST) into a sorted doubly linked list (DLL) in-place:

* `left` acts as `previous` (`prev`).
* `right` acts as `next`.
* Resulting list must be sorted in ascending order.
* Must return head of newly created doubly linked list.
* **Strict Constraint:** $O(1)$ extra space. No recursion call stack, no auxiliary queue/stack.

---

### 2. Asking Clarifying Questions

* **Linear vs Circular DLL?** Linear (`head.left = None`, `tail.right = None`).
* **Empty Tree / Null Input?** If `root` is `None`, return `None`.
* **Single Node Tree?** Returns node itself with `left = None` and `right = None`.
* **Pointer Modification?** Direct modification of existing `left` and `right` pointers allowed.

---

### 3. Hand-Tracing Example

**Input BST:**

```text
       4
     /   \
    2     5
   / \
  1   3

```

**Target Sequence:** `1 <-> 2 <-> 3 <-> 4 <-> 5`

**Trace via Threading (Morris Logic):**

1. Start at `4`. Left child exists (`2`). Find in-order predecessor (`3`). Thread `3.right = 4`. Move `curr = 2`.
2. At `2`. Left child exists (`1`). Find in-order predecessor (`1`). Thread `1.right = 2`. Move `curr = 1`.
3. At `1`. Left child is `None`.
* First visited node $\rightarrow$ `head = 1`, `prev = 1`.
* Follow thread `1.right` $\rightarrow$ `curr = 2`.


4. At `2`. Predecessor `1` already points to `2` (thread exists).
* Link `prev (1)` and `curr (2)` doubly: `1.right = 2`, `2.left = 1`.
* `prev = 2`. Move `curr = 2.right` $\rightarrow$ `3`.


5. At `3`. Left child `None`.
* Link `prev (2)` and `curr (3)`: `2.right = 3`, `3.left = 2`.
* `prev = 3`. Follow thread `3.right` $\rightarrow$ `curr = 4`.


6. At `4`. Thread from `3` exists.
* Link `prev (3)` and `curr (4)`: `3.right = 4`, `4.left = 3`.
* `prev = 4`. Move `curr = 4.right` $\rightarrow$ `5`.


7. At `5`. Left child `None`.
* Link `prev (4)` and `curr (5)`: `4.right = 5`, `5.left = 4`.
* `prev = 5`. Move `curr = 5.right` $\rightarrow$ `None`.



**Result:** Returns `1`. `1.left = None`, `5.right = None`.

---

### 4. Brainstorming Solutions & Complexity

* **Option A: In-Order Traversal via Recursion / Stack**
* Standard DFS in-order traversal.
* Time: $O(N)$
* Space: $O(H)$ stack space ($H$ = tree height). Fails $O(1)$ space requirement for skewed tree ($O(N)$ stack depth).


* **Option B: Morris In-Order Traversal (Selected)**
* Temporarily thread predecessor's `right` pointer to `curr` node. Allows returning to parent without call stack.
* Time: $O(N)$ (each edge traversed at most twice).
* Space: $O(1)$ extra space strictly (only `curr`, `prev`, `head`, `pred` pointers).



---

### 5. Suggesting Solution

**Morris In-Order Traversal**: Standard iterative $O(1)$ extra space tree traversal technique. It builds thread links on the fly, visits nodes in sorted order, and re-wires `left` and `right` pointers into a doubly linked list.

---

### 6. Outline of Implementation

```python
def bst_to_doubly_linked_list(root): # -> Node
    """
    Reframe: Use temporary threading to traverse BST in-order without a stack, continuously re-wiring nodes into a doubly linked list.
    State: `curr` (traversal pointer), `prev` (last processed DLL node), `head` (smallest element / list head).
    Invariant: Nodes processed prior to `curr` form a valid doubly linked list from `head` up to `prev`.

    get_predecessor(curr) = finds the rightmost node of curr's left subtree.
    link_nodes(prev, curr) = sets `prev.right = curr` and `curr.left = prev`.

    Core logic:
    - while traversal node exists:
        - if left child is missing:
            - set head if not yet assigned
            - doubly-link current node with previous node
            - advance current node to right child
        - else (left child exists):
            - locate in-order predecessor in left subtree
            - if predecessor has no right link:
                - thread predecessor right link to current node
                - move current node to left child
            - else (thread already exists):
                - doubly-link current node with previous node
                - advance current node to right child
    Edge cases:
    - root is None (empty input)
    - root has no children (single node tree)
    - right-skewed or left-skewed tree
    """

```

---

### 7. Iterative Implementation

#### Iteration 1: Skeleton with helper stubs & placeholders

```python
class Node:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def bst_to_doubly_linked_list(root):
    if not root:
        return None
    
    curr = root
    prev = None
    head = None
    
    # Placeholder helper for predecessor retrieval
    def get_predecessor(node):
        # TODO: Implement rightmost search on node.left
        pass

    while curr:
        if not curr.left:
            # TODO: Visit curr (link with prev, update head, move right)
            pass
        else:
            pred = get_predecessor(curr)
            # TODO: Handle threading setup vs threaded return
            pass
            
    return head

```

#### Iteration 2: Realizing Core Morris Traversal Logic

```python
def bst_to_doubly_linked_list(root):
    if not root:
        return None
    
    curr = root
    prev = None
    head = None

    while curr:
        if not curr.left:
            # --- Visit Current Node ---
            if not head:
                head = curr
            if prev:
                prev.right = curr
                curr.left = prev
            prev = curr
            curr = curr.right
            # --------------------------
        else:
            # Find in-order predecessor
            pred = curr.left
            while pred.right and pred.right != curr:
                pred = pred.right
                
            if not pred.right:
                # Create temporary thread
                pred.right = curr
                curr = curr.left
            else:
                # --- Thread visited: Process Current Node ---
                if prev:
                    prev.right = curr
                    curr.left = prev
                prev = curr
                curr = curr.right
                # ---------------------------------------------

    return head

```

#### Iteration 3: Walk Edge Cases & Refine Code

Let's walk through edge cases to check for pointer breaks or loops:

1. **Edge Case 1: `root` is `None**`
* Guard clause `if not root: return None` handles immediately.


2. **Edge Case 2: Single Node (`root` with no children)**
* `curr = root`. `curr.left` is `None`.
* Sets `head = root`. `prev = root`. Moves `curr = curr.right` (`None`).
* Loop ends. Returns `head` (`root`). `root.left` and `root.right` stay `None`. Correct.


3. **Edge Case 3: Left-skewed tree ($3 \leftarrow 2 \leftarrow 1$)**
* Threads created down left spine. Processed bottom-up correctly as `curr.left` becomes `None` at deepest node (`1`).


4. **Edge Case 4: Right-skewed tree ($1 \rightarrow 2 \rightarrow 3$)**
* `curr.left` is always `None`. Straight linear processing, setting `head = 1`, linking $1 \leftrightarrow 2 \leftrightarrow 3$.



---

### Final Fully Realized Code

```python
class Node:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def bst_to_doubly_linked_list(root: Node) -> Node:
    if not root:
        return None
    
    curr = root
    prev = None
    head = None

    while curr:
        if not curr.left:
            # No left subtree: process current node
            if not head:
                head = curr
            if prev:
                prev.right = curr
                curr.left = prev
            prev = curr
            curr = curr.right
        else:
            # Find in-order predecessor in left subtree
            pred = curr.left
            while pred.right and pred.right != curr:
                pred = pred.right
                
            if not pred.right:
                # Thread predecessor to current node and step left
                pred.right = curr
                curr = curr.left
            else:
                # Returning from left subtree via thread: process current node
                if prev:
                    prev.right = curr
                    curr.left = prev
                prev = curr
                curr = curr.right

    # Clean bounds for head and tail
    if head:
        head.left = None
    if prev:
        prev.right = None

    return head

```

---

### 8. Complexity & Optimizations

* **Time Complexity:** $O(N)$
* Although finding predecessor uses an inner `while` loop, every edge in the tree is traversed at most 3 times (once to find predecessor, once to establish thread, once during actual traversal). Overall time remains linear $O(N)$.


* **Space Complexity:** $O(1)$ Auxiliary Space
* Uses strictly constant pointers (`curr`, `prev`, `head`, `pred`). No call stack or external data structures used. Fits server constraints.