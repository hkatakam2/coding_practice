### question
Given the root of a binary search tree, and an integer k, return the kth smallest value (1-indexed) in the tree.

A binary search tree satisfies the following constraints:

The left subtree of every node contains only nodes with keys less than the node's key.
The right subtree of every node contains only nodes with keys greater than the node's key.
Both the left and right subtrees are also binary search trees.

We need return the **kth smallest node value** in a BST.

Key BST property:

For any node:

```text
all left values < node.val < all right values
```

So if we do **inorder traversal**:

```text
left subtree -> node -> right subtree
```

we visit values in **sorted ascending order**.

So the kth visited node in inorder is the answer.

---

## 1. Clarify inputs / outputs

Assumptions:

```python
def kthSmallest(root: Optional[TreeNode], k: int) -> int:
```

Input:

```text
root = root of BST
k = 1-indexed position
```

Output:

```text
integer value of kth smallest node
```

Clarifying questions I would ask in interview:

1. Is `k` always valid? Meaning `1 <= k <= number of nodes`?
2. Are all node values unique? BST definition says strict less/greater, so yes.
3. Should we return the value, not the node? Problem says value.

I will assume `k` is valid.

---

## 2. Example by hand

Example BST:

```text
        5
       / \
      3   7
     / \   \
    2   4   8
```

Inorder traversal:

```text
2, 3, 4, 5, 7, 8
```

If:

```text
k = 3
```

3rd smallest is:

```text
4
```

So answer is:

```text
4
```

---

## 3. Brainstorm solutions

### Solution 1: Full inorder traversal

Traverse whole tree, store values in list.

```python
values = [2, 3, 4, 5, 7, 8]
return values[k - 1]
```

Complexity:

```text
Time: O(n)
Space: O(n)
```

Simple, but stores all values even though we only need kth.

---

### Solution 2: Recursive inorder with counter

Do inorder DFS. Count visited nodes. Stop when count becomes k.

Complexity:

```text
Time: O(h + k) average, O(n) worst
Space: O(h) recursion stack
```

Good, but recursive early stopping can be slightly awkward in Python because we need nonlocal state.

---

### Solution 3: Iterative inorder with stack

Use stack to simulate recursion.

Keep going left until we cannot.

Then pop one node: that is the next smallest.

Decrement `k`.

When `k == 0`, return that node value.

Complexity:

```text
Time: O(h + k)
Space: O(h)
```

This is clean, interview-friendly, and avoids recursion issues.

I would choose this.

---

## 4. Selected implementation outline

```python
def kthSmallest(root, k):  # -> int
    """
    Reframe: kth smallest in BST = kth node visited by inorder traversal.

    State: stack of ancestors, chosen because inorder needs us to pause nodes
        while we fully explore their left subtree first.

    Invariant: every time we pop from stack, that node is the next smallest
        unvisited value in the BST.

    pushLeftPath(node) = push node and all of its left descendants onto stack.

    Core logic:
    - start from root
    - keep pushing left descendants until reaching null
    - pop one node from stack
    - that popped node is the next smallest value
    - decrement k
    - if k becomes zero, return this value
    - then move to the popped node's right child
    - repeat

    Edge cases:
    - root is null
    - k is 1, return smallest value
    - k equals number of nodes, return largest value
    - tree is completely left-skewed
    - tree is completely right-skewed
    - k is invalid, though problem usually guarantees valid k
    """
```

---

## 5. Iteration 1: skeleton

```python
def kthSmallest(root, k):
    stack = []
    curr = root

    while curr or stack:
        # go as far left as possible

        # visit next smallest node

        # move to right subtree

    # only reached if k was invalid
```

This matches inorder:

```text
left -> node -> right
```

---

## 6. Iteration 2: add left-walk

```python
def kthSmallest(root, k):
    stack = []
    curr = root

    while curr or stack:
        # push all left nodes
        while curr:
            stack.append(curr)
            curr = curr.left

        # visit next smallest node

        # move to right subtree
```

Now stack contains a path of nodes waiting to be visited after their left side is done.

---

## 7. Iteration 3: visit next smallest

```python
def kthSmallest(root, k):
    stack = []
    curr = root

    while curr or stack:
        while curr:
            stack.append(curr)
            curr = curr.left

        # smallest unvisited node
        curr = stack.pop()
        k -= 1

        if k == 0:
            return curr.val

        # explore right subtree next
        curr = curr.right
```

This is the core logic complete.

---

## 8. Final code

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        """
        Reframe: kth smallest in BST = kth node visited by inorder traversal.

        State: stack of ancestors, chosen because inorder traversal needs to
            pause nodes while fully exploring their left subtree first.

        Invariant: every time we pop from the stack, that node is the next
            smallest unvisited value.

        Core logic:
        - push current node and all left descendants
        - pop one node; this is the next smallest value
        - count it
        - if it is the kth visited node, return its value
        - then explore its right subtree

        Edge cases:
        - k == 1
        - k == number of nodes
        - left-skewed tree
        - right-skewed tree
        - empty root or invalid k, if not guaranteed by problem
        """

        stack = []
        curr = root

        while curr or stack:
            # Go to the smallest unvisited node in this subtree.
            while curr:
                stack.append(curr)
                curr = curr.left

            # Visit next smallest node.
            curr = stack.pop()
            k -= 1

            if k == 0:
                return curr.val

            # Now visit values larger than curr, starting from right subtree.
            curr = curr.right

        # Problem usually guarantees valid k.
        return -1
```

---

## 9. Edge cases walkthrough

### Case 1: `k = 1`

We keep going left until smallest node.

First pop is smallest.

Return immediately.

```text
Works.
```

---

### Case 2: `k = number of nodes`

Traversal visits every node in sorted order.

The final visited node is largest.

```text
Works.
```

---

### Case 3: left-skewed tree

```text
    5
   /
  4
 /
3
/
2
```

Stack gets all nodes.

Pop order:

```text
2, 3, 4, 5
```

```text
Works.
```

---

### Case 4: right-skewed tree

```text
2
 \
  3
   \
    4
     \
      5
```

Each node has no left child.

Pop order:

```text
2, 3, 4, 5
```

```text
Works.
```

---

## 10. Complexity

Let:

```text
h = height of tree
k = kth position
n = number of nodes
```

We do not necessarily visit all nodes. We stop after visiting `k` nodes.

Time:

```text
O(h + k)
```

Why?

We may first walk down height `h`, then pop/visit `k` nodes.

Worst case:

```text
O(n)
```

Space:

```text
O(h)
```

Because stack stores at most one root-to-leaf path.

Worst case skewed tree:

```text
O(n)
```

Balanced tree:

```text
O(log n)
```
