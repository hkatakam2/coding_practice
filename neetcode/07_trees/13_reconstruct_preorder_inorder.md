### question
You are given two integer arrays preorder and inorder.

preorder is the preorder traversal of a binary tree
inorder is the inorder traversal of the same tree
Both arrays are of the same size and consist of unique values.
Rebuild the binary tree from the preorder and inorder traversals and return its root.

## 1. Restate the problem

We are given:

```python
preorder = root, left subtree, right subtree
inorder  = left subtree, root, right subtree
```

Both arrays describe the **same binary tree**, values are **unique**, and we need to rebuild the original tree and return its root.

---

## 2. Clarifying questions

In interview, I would ask:

1. Can the tree be empty?
   Assume yes, so `preorder = []`, `inorder = []` should return `None`.

2. Are all values unique?
   Yes. This is important because it lets us map each value to exactly one inorder position.

3. Are the inputs always valid traversals of the same tree?
   Usually yes in LeetCode-style problems. We do not need heavy validation.

4. What should we return?
   The root `TreeNode`.

---

## 3. Example by hand

Input:

```python
preorder = [3, 9, 20, 15, 7]
inorder  = [9, 3, 15, 20, 7]
```

Preorder says first value is root:

```text
root = 3
```

Find `3` in inorder:

```text
inorder = [9, 3, 15, 20, 7]
           L  R  R   R   R
```

Left of `3` is left subtree:

```text
[9]
```

Right of `3` is right subtree:

```text
[15, 20, 7]
```

Now preorder after root is:

```text
[9, 20, 15, 7]
```

Next value `9` becomes root of left subtree.

Then next value `20` becomes root of right subtree.

For right subtree:

```text
preorder part = [20, 15, 7]
inorder part  = [15, 20, 7]
```

Root is `20`.

In inorder, left of `20` is `[15]`, right of `20` is `[7]`.

Final tree:

```text
        3
       / \
      9   20
         /  \
        15   7
```

---

## 4. Brainstorm solutions

### Solution 1: Recursive slicing

At every root:

1. Take first preorder value as root.
2. Find root in inorder.
3. Slice inorder into left/right.
4. Slice preorder into left/right.
5. Recurse.

Easy to understand, but slicing costs extra time.

Complexity:

```text
Time: O(n^2) worst case
Space: O(n^2) because of repeated slicing
```

---

### Solution 2: Recursive with hashmap + preorder pointer

Use:

```python
value -> inorder index
```

Then recursively build using inorder boundaries.

We keep one pointer into preorder. Every time we create a node, we consume the next preorder value.

Complexity:

```text
Time: O(n)
Space: O(n)
```

This is the preferred interview solution.

---

## 5. Key insight

Preorder tells us **which node to create next**.

Inorder tells us **where that node's left and right subtrees are**.

So:

```text
preorder chooses root
inorder splits left and right subtree
```

---

## 6. Selected implementation outline

```python
def buildTree(preorder, inorder):  # -> Optional[TreeNode]
    """
    Reframe: preorder gives next root; inorder tells how much belongs left/right.

    State:
        - preorder_index: next root to consume from preorder.
        - inorder_position: maps value to its index in inorder.

        Hashmap is chosen because every root value must be found quickly in inorder.

    Invariant:
        buildSubtree(in_left, in_right) rebuilds exactly the subtree whose nodes
        appear inside that inorder window.

    buildSubtree(in_left, in_right) =
        rebuild the subtree contained between these inorder boundaries.

    Core logic:
    - If the inorder window is empty, return no node.
    - Take the next preorder value as the root value.
    - Create the root node.
    - Find root position in inorder.
    - Recursively build the left subtree from the inorder values before root.
    - Recursively build the right subtree from the inorder values after root.
    - Attach both subtrees and return root.

    Edge cases:
    - Empty input: return None.
    - Single node: create and return that node.
    - All-left-skewed tree: recursion keeps building left side.
    - All-right-skewed tree: recursion keeps building right side.
    - Invalid traversals: not expected by problem statement.
    """
```

---

## 7. Iterative implementation

### Iteration 1: skeleton with helper

```python
class Solution:
    def buildTree(self, preorder, inorder):
        inorder_position = {}

        preorder_index = 0

        def buildSubtree(in_left, in_right):
            # TODO: empty window means no node

            # TODO: take next preorder value as root

            # TODO: find root position in inorder

            # TODO: build left subtree

            # TODO: build right subtree

            # TODO: return root
            pass

        return buildSubtree(0, len(inorder) - 1)
```

---

### Iteration 2: add hashmap

```python
class Solution:
    def buildTree(self, preorder, inorder):
        # changed: store value -> index for fast root lookup
        inorder_position = {value: index for index, value in enumerate(inorder)}

        preorder_index = 0

        def buildSubtree(in_left, in_right):
            pass

        return buildSubtree(0, len(inorder) - 1)
```

---

### Iteration 3: create root from preorder

```python
class Solution:
    def buildTree(self, preorder, inorder):
        inorder_position = {value: index for index, value in enumerate(inorder)}

        preorder_index = 0

        def buildSubtree(in_left, in_right):
            nonlocal preorder_index

            # changed: empty inorder window means no subtree
            if in_left > in_right:
                return None

            # changed: preorder gives next root
            root_value = preorder[preorder_index]
            preorder_index += 1

            root = TreeNode(root_value)

            return root

        return buildSubtree(0, len(inorder) - 1)
```

At this point, this only builds root nodes, but not children yet.

---

### Iteration 4: split inorder and recurse

```python
class Solution:
    def buildTree(self, preorder, inorder):
        inorder_position = {value: index for index, value in enumerate(inorder)}

        preorder_index = 0

        def buildSubtree(in_left, in_right):
            nonlocal preorder_index

            if in_left > in_right:
                return None

            root_value = preorder[preorder_index]
            preorder_index += 1

            root = TreeNode(root_value)

            # changed: find where root splits inorder
            root_inorder_index = inorder_position[root_value]

            # changed: build left first because preorder is root-left-right
            root.left = buildSubtree(in_left, root_inorder_index - 1)

            # changed: then build right
            root.right = buildSubtree(root_inorder_index + 1, in_right)

            return root

        return buildSubtree(0, len(inorder) - 1)
```

Core logic is complete.

---

## 8. Edge case walk-through

### Edge case 1: empty input

```python
preorder = []
inorder = []
```

Call:

```python
buildSubtree(0, -1)
```

Since `0 > -1`, return `None`.

Works.

---

### Edge case 2: single node

```python
preorder = [1]
inorder = [1]
```

Root is `1`.

Left window is empty.

Right window is empty.

Return node `1`.

Works.

---

### Edge case 3: all-left-skewed tree

```text
    3
   /
  2
 /
1
```

```python
preorder = [3, 2, 1]
inorder  = [1, 2, 3]
```

Each root is found at the far right of current inorder window.

So right subtree is always empty, left subtree keeps building.

Works.

---

### Edge case 4: all-right-skewed tree

```text
1
 \
  2
   \
    3
```

```python
preorder = [1, 2, 3]
inorder  = [1, 2, 3]
```

Each root is found at the far left of current inorder window.

So left subtree is always empty, right subtree keeps building.

Works.

---

## Final code

```python
# Usually provided by LeetCode / NeetCode
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def buildTree(self, preorder, inorder):
        """
        Reframe: preorder gives next root; inorder tells left/right boundaries.

        State:
            preorder_index: next root to consume.
            inorder_position: value -> inorder index.

        Invariant:
            buildSubtree(in_left, in_right) builds the subtree represented
            by that inorder window.
        """
        inorder_position = {value: index for index, value in enumerate(inorder)}
        preorder_index = 0

        def buildSubtree(in_left, in_right):
            nonlocal preorder_index

            if in_left > in_right:
                return None

            root_value = preorder[preorder_index]
            preorder_index += 1

            root = TreeNode(root_value)
            root_inorder_index = inorder_position[root_value]

            root.left = buildSubtree(in_left, root_inorder_index - 1)
            root.right = buildSubtree(root_inorder_index + 1, in_right)

            return root

        return buildSubtree(0, len(inorder) - 1)
```

---

## Complexity

Let `n` be number of nodes.

Building the hashmap:

```text
O(n)
```

Each node is created once:

```text
O(n)
```

Each root lookup is `O(1)`:

```text
O(1) per node
```

Total:

```text
Time: O(n)
Space: O(n)
```

Space comes from:

```text
hashmap: O(n)
recursion stack: O(h)
```

where `h` is tree height.

Worst case skewed tree:

```text
O(n) recursion stack
```

Balanced tree:

```text
O(log n) recursion stack
```
