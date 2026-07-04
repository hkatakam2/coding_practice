### question
Given a binary tree, return true if it is height-balanced and false otherwise.

A height-balanced binary tree is defined as a binary tree in which the left and right subtrees of every node differ in height by no more than 1.


We need return whether **every node** in the binary tree is height-balanced.

A node is balanced when:

```text
abs(height(left subtree) - height(right subtree)) <= 1
```

And this must be true for **all nodes**, not just the root.

---

## 1. Restate the problem

Given `root` of a binary tree, return:

```python
True
```

if the tree is height-balanced.

Return:

```python
False
```

if at least one node has left/right subtree heights differing by more than `1`.

---

## 2. Clarifying questions

In interview, I would confirm:

1. Is an empty tree balanced?

   * Usually yes. Return `True`.

2. Height is measured in nodes or edges?

   * For balance, either works as long as consistent.
   * I will use height in **nodes**:

     * `None` has height `0`
     * leaf node has height `1`

3. Need optimize?

   * We should avoid recomputing heights repeatedly.
   * Best solution: one DFS pass.

---

## 3. Example by hand

Example:

```text
        1
       / \
      2   3
     /
    4
```

Heights:

```text
node 4:
left height = 0
right height = 0
balanced

node 2:
left height = 1
right height = 0
difference = 1
balanced

node 3:
left height = 0
right height = 0
balanced

node 1:
left height = 2
right height = 1
difference = 1
balanced
```

Return:

```python
True
```

Now example:

```text
        1
       /
      2
     /
    3
```

Heights:

```text
node 3 height = 1

node 2:
left height = 1
right height = 0
balanced

node 1:
left height = 2
right height = 0
difference = 2
not balanced
```

Return:

```python
False
```

---

## 4. Brainstorm solutions

### Solution 1: Naive height check

For every node:

1. Compute height of left subtree.
2. Compute height of right subtree.
3. Check balance.
4. Recurse into left and right children.

Problem: height gets recomputed many times.

Complexity:

```text
Time: O(n^2) in worst case
Space: O(h)
```

Bad for skewed trees.

---

### Solution 2: DFS returns height and balance together

For each node, ask:

```text
Is left subtree balanced?
Is right subtree balanced?
What are their heights?
```

Then current node is balanced if:

```text
left balanced
right balanced
abs(left height - right height) <= 1
```

This is clean and efficient.

Complexity:

```text
Time: O(n)
Space: O(h)
```

where `h` is recursion stack height.

This is the best interview solution.

---

## 5. Selected idea

Use postorder DFS.

Why postorder?

Because before deciding whether a node is balanced, we need the height of its left and right subtrees.

So we process:

```text
left subtree
right subtree
current node
```

---

## 6. Implementation outline

```python
def isBalanced(root):  # -> bool
    """
    Reframe: every node needs two facts from children: height and whether already balanced.

    State: recursive return pair:
        - subtree height
        - whether subtree is balanced

    Invariant:
        For every returned subtree, height is correct, and balanced tells whether all nodes
        inside that subtree satisfy the height-balance rule.

    check(node) = returns height and balance status of subtree rooted at node.

    Core logic:
    - If node is empty, its height is zero and it is balanced.
    - Recursively get left subtree height and balance.
    - Recursively get right subtree height and balance.
    - Current node is balanced only if:
        - left subtree is balanced
        - right subtree is balanced
        - left and right heights differ by at most one
    - Current height is one plus the taller child height.
    - Return current height and current balance.
    - Final answer is the balance value for root.

    Edge cases:
    - Empty tree: balanced.
    - Single node: balanced.
    - Completely skewed tree: may become unbalanced.
    - A tree where root looks balanced but deeper node is not balanced.
    - Duplicate values do not matter because structure only matters.
    """
```

---

## 7. Iterative implementation

### Step 1: skeleton

```python
def isBalanced(root):
    def check(node):
        # return height, is_balanced
        pass

    height, balanced = check(root)
    return balanced
```

---

### Step 2: handle empty subtree

```python
def isBalanced(root):
    def check(node):
        if node is None:
            return 0, True

        # return height, is_balanced
        pass

    height, balanced = check(root)
    return balanced
```

---

### Step 3: get left and right results

```python
def isBalanced(root):
    def check(node):
        if node is None:
            return 0, True

        left_height, left_balanced = check(node.left)
        right_height, right_balanced = check(node.right)

        # compute current result next
        pass

    height, balanced = check(root)
    return balanced
```

---

### Step 4: compute current node balance

```python
def isBalanced(root):
    def check(node):
        if node is None:
            return 0, True

        left_height, left_balanced = check(node.left)
        right_height, right_balanced = check(node.right)

        current_balanced = (
            left_balanced
            and right_balanced
            and abs(left_height - right_height) <= 1
        )

        # compute current height next
        pass

    height, balanced = check(root)
    return balanced
```

---

### Step 5: compute current height

```python
def isBalanced(root):
    def check(node):
        if node is None:
            return 0, True

        left_height, left_balanced = check(node.left)
        right_height, right_balanced = check(node.right)

        current_balanced = (
            left_balanced
            and right_balanced
            and abs(left_height - right_height) <= 1
        )

        current_height = 1 + max(left_height, right_height)

        return current_height, current_balanced

    height, balanced = check(root)
    return balanced
```

This is already correct.

---

## Final code

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def isBalanced(self, root):
        def check(node):
            if node is None:
                return 0, True

            left_height, left_balanced = check(node.left)
            right_height, right_balanced = check(node.right)

            current_balanced = (
                left_balanced
                and right_balanced
                and abs(left_height - right_height) <= 1
            )

            current_height = 1 + max(left_height, right_height)

            return current_height, current_balanced

        height, balanced = check(root)
        return balanced
```

---

## Slightly optimized version

We can return `-1` as a signal meaning:

```text
this subtree is already unbalanced
```

Then we do not need to keep returning `(height, balanced)`.

```python
class Solution:
    def isBalanced(self, root):
        def height(node):
            if node is None:
                return 0

            left_height = height(node.left)
            if left_height == -1:
                return -1

            right_height = height(node.right)
            if right_height == -1:
                return -1

            if abs(left_height - right_height) > 1:
                return -1

            return 1 + max(left_height, right_height)

        return height(root) != -1
```

This version is common in interviews.

But for explanation, the `(height, balanced)` version is clearer.

---

## Complexity

For the selected DFS solution:

```text
Time: O(n)
```

Each node is visited once.

```text
Space: O(h)
```

because of recursion stack.

Where:

```text
h = height of tree
```

Best case for balanced tree:

```text
Space: O(log n)
```

Worst case for skewed tree:

```text
Space: O(n)
```
