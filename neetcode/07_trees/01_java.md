### 1. Restate the problem

We need to "invert" a binary tree. This means we are flipping the tree horizontally, treating the vertical axis through the root as a mirror.

For every single node in the tree, its left child should become its right child, and its right child should become its left child. We are given the root node, and we must return the root node of the fully inverted tree.

### 2. Ask clarifying questions

Before writing code, I would confirm a few details with the interviewer:

* **Can the input tree be empty?** Yes, the root can be `null`. We should return `null` in that case.
* **Are we allowed to modify the tree in place?** Yes, mutating the existing `TreeNode` objects is standard for this problem rather than allocating a completely new tree.
* **How large can the tree be?** If the tree is massive and completely unbalanced (a straight line of nodes), we might exceed the maximum call stack size with a recursive solution. Assuming a standard constraint (e.g., up to 10,000 nodes), standard recursion will be perfectly fine.

*(Assumption: The tree is of a reasonable size where recursion depth is not an issue, and we are mutating the given tree in place.)*

### 3. Work through an example by hand

Let's take a small tree:

```text
      4
    /   \
   2     7
  / \   / \
 1   3 6   9

```

1. Start at the root `4`.
2. Swap its children `2` and `7`.
```text
      4
    /   \
   7     2
  / \   / \
 6   9 1   3   <-- Notice the children of 7 and 2 moved with them

```


3. Move down to the new left child, `7`. Swap its children `6` and `9`.
```text
      4
    /   \
   7     2
  / \   / \
 9   6 1   3

```


4. Move to the new right child, `2`. Swap its children `1` and `3`.
```text
      4
    /   \
   7     2
  / \   / \
 9   6 3   1

```


5. Move to the leaf nodes (`9`, `6`, `3`, `1`). Swapping their `null` children changes nothing.
6. The tree is now fully inverted.

### 4. Brainstorm solutions aloud

**Approach 1: Recursive Depth-First Search (DFS)**
Because a tree is a recursive data structure, this problem naturally suggests a recursive approach. We can visit a node, swap its left and right child pointers, and then recursively call the same function on those children.

* **Time Complexity:** O(N), where N is the number of nodes, because we visit every node exactly once.
* **Space Complexity:** O(H), where H is the height of the tree, representing the call stack frames. In the worst case (a skewed tree), this is O(N). In the best case (a balanced tree), it's O(log N).

**Approach 2: Iterative Breadth-First Search (BFS)**
If we are strictly worried about StackOverflow errors on massive, skewed trees, we could use an iterative approach. We initialize a `Queue`, add the root, and while the queue isn't empty, we pop a node, swap its children, and push its non-null children into the queue.

* **Time Complexity:** O(N), as we still visit every node.
* **Space Complexity:** O(W), where W is the maximum width of the tree. In the worst case (the bottom level of a perfect binary tree), this is O(N/2) = O(N).

### 5. Select the solution

I will use the **Recursive DFS** approach.

It perfectly matches the recursive definition of a binary tree. It is significantly shorter, requires fewer explicit data structures, and is less error-prone to write. The space complexity is practically identical to BFS, except it uses the implicit call stack instead of an explicit queue heap allocation.

### 6. Write the implementation outline

```java
TreeNode invertTree(TreeNode root) {
    /*
     * Reframe:
     * Visit each node, swap its left and right pointers, and tell its 
     * children to do the same.
     *
     * State:
     * No extra data structures needed; we use the implicit call stack.
     *
     * Invariant:
     * When returning from a recursive call, the subtree rooted at that 
     * node has been completely inverted.
     *
     * Core logic:
     * - if the current node is null, return null (base case)
     * - save a reference to the left child
     * - set the left child to be the inverted right subtree
     * - set the right child to be the inverted left subtree
     * - return the current node
     *
     * Edge cases:
     * - Empty tree (handled by base case)
     * - Tree with only one child (handled gracefully since null subtrees 
     *   return null and overwrite the pointers correctly)
     */
}

```

### 7. Implement iteratively

**Iteration 1: Method skeleton and base case**
We set up the standard definition for the method and handle the case where the tree might be empty or we've reached past a leaf node.

```java
public TreeNode invertTree(TreeNode root) {
    if (root == null) {
        return null;
    }

    // TODO: Invert the subtrees
    // TODO: Swap the subtrees

    return root;
}

```

**Iteration 2: Completing the recursive swap**
We grab the left child, and replace it with the completely inverted right child. Then we replace the right child with the completely inverted left child (using our saved reference).

```java
public TreeNode invertTree(TreeNode root) {
    if (root == null) {
        return null;
    }

    // Added: Save the left subtree before we overwrite the pointer
    TreeNode tempLeft = root.left;

    // Added: Recursively invert the right subtree and attach it to the left
    root.left = invertTree(root.right);

    // Added: Recursively invert the original left subtree and attach to the right
    root.right = invertTree(tempLeft);

    return root;
}

```

### Edge-case pass

Let's review the potential edge cases:

* **Empty input (`root == null`):** The first `if` statement catches this and returns `null`. Safe.
* **Single node:** Fails the `if`, sets `tempLeft` to `null`. `root.left` becomes `invertTree(null)` which is `null`. `root.right` becomes `invertTree(null)` which is `null`. Returns `root`. Safe.
* **Left-skewed tree (`[2, 1, null]`):** `tempLeft` is `1`. `root.left` becomes `invertTree(null)` which is `null`. `root.right` becomes `invertTree(1)`. The tree becomes `[2, null, 1]`. Safe.

No patches are necessary. The logic is robust.

### Final code

For completeness in a standard Java environment, I will include the `TreeNode` definition.

```java
class TreeNode {
    int val;
    TreeNode left;
    TreeNode right;
    
    TreeNode() {}
    
    TreeNode(int val) { 
        this.val = val; 
    }
    
    TreeNode(int val, TreeNode left, TreeNode right) {
        this.val = val;
        this.left = left;
        this.right = right;
    }
}

class Solution {
    public TreeNode invertTree(TreeNode root) {
        if (root == null) {
            return null;
        }

        TreeNode tempLeft = root.left;
        root.left = invertTree(root.right);
        root.right = invertTree(tempLeft);

        return root;
    }
}

```

### Complexity

* **Time Complexity:** O(N), where N is the number of nodes in the tree. We visit every single node exactly once to swap its children.
* **Space Complexity:** O(H), where H is the height of the tree. This is the memory used by the recursion call stack. For a perfectly balanced tree, the height is log(N), so space is O(log N). For a completely unbalanced tree (e.g., all left children), the height is N, so worst-case space is O(N).

### Brief test walkthrough

Let's trace a small tree: `root = [2, 1, 3]` (node 2 has left child 1, right child 3).

1. `invertTree(2)` is called. `root` is not `null`.
2. `tempLeft` = node 1.
3. We execute `root.left = invertTree(node 3)`.
* *Inner call*: `invertTree(3)`. `tempLeft` = `null`. `left` = `invertTree(null)`, `right` = `invertTree(null)`. Returns node 3.


4. Back in `invertTree(2)`, `root.left` is now node 3.
5. We execute `root.right = invertTree(tempLeft)` which is `invertTree(node 1)`.
* *Inner call*: `invertTree(1)`. Evaluates to node 1 just like node 3 did.


6. Back in `invertTree(2)`, `root.right` is now node 1.
7. Return `root` (node 2).
Expected result: `[2, 3, 1]`. Actual result: `[2, 3, 1]`. The structure is successfully inverted.