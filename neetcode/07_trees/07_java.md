### 1. Restate the problem

We are given a Binary Search Tree (BST) and two specific nodes within that tree, `p` and `q`. We need to find their Lowest Common Ancestor (LCA).

The LCA is defined as the deepest node in the tree that has both `p` and `q` as descendants. A node can be considered a descendant of itself, meaning if `p` is the parent of `q`, `p` is the LCA.

Because this is a BST, we know that for any given node, all values in its left subtree are strictly less than the node's value, and all values in its right subtree are strictly greater.

### 2. Ask clarifying questions

Before implementing, I would normally clarify a few details with the interviewer:

* **Are `p` and `q` guaranteed to exist in the BST?**
* *Assumption for now:* Yes, they always exist in the tree.


* **Can `p` and `q` be the same node?**
* *Assumption for now:* They are distinct nodes, but if they were the same, the node itself would trivially be the LCA.


* **How large can the tree get, and is it balanced?**
* *Assumption for now:* The tree could be extremely unbalanced (essentially a linked list). This means recursion could theoretically hit an $O(N)$ depth and cause a `StackOverflowError`.


* **What is the class structure for the nodes?**
* *Assumption for now:* A standard `TreeNode` with `val`, `left`, and `right` fields.



### 3. Work through an example by hand

Let's trace an example with a BST.
Tree:

```text
        6
      /   \
     2     8
    / \   / \
   0   4 7   9
      / \
     3   5

```

**Scenario A: Find LCA of 2 and 8**

* Start at the root (6).
* Compare `p` (2) and `q` (8) to the current node (6).
* 2 is less than 6, meaning it's in the left subtree.
* 8 is greater than 6, meaning it's in the right subtree.
* Since `p` and `q` split directions at node 6, 6 must be the lowest common ancestor.

**Scenario B: Find LCA of 2 and 4**

* Start at root (6).
* Both 2 and 4 are less than 6. They must both be in the left subtree.
* Move down to the left child (2).
* Compare `p` (2) and `q` (4) to the current node (2).
* 2 is equal to the current node. 4 is greater than the current node.
* Since `p` is the current node, it's the ancestor of `q`. Node 2 is the LCA.

### 4. Brainstorm solutions aloud

**Approach 1: Generic Binary Tree LCA (Recursive)**
We could ignore the BST property and do a standard post-order traversal. If a node matches `p` or `q`, we return it. If a node's left and right subtrees both return a target, the current node is the LCA.

* *Time:* $O(N)$ because we might visit every node.
* *Space:* $O(N)$ in the worst case for the call stack if the tree is highly skewed.
* *Tradeoffs:* This works, but it completely ignores the BST property, making it unnecessarily slow.

**Approach 2: Use BST Property (Recursive)**
We can use the values of the nodes to navigate. If both `p` and `q` values are less than the current node's value, the LCA must be in the left subtree. If both are greater, it must be in the right subtree. Otherwise, we've found the split point.

* *Time:* $O(H)$ where $H$ is the height of the tree.
* *Space:* $O(H)$ for the recursive call stack.
* *Tradeoffs:* Much faster than Approach 1, but still uses auxiliary space for the call stack.

**Approach 3: Use BST Property (Iterative)**
We can take the exact logic from Approach 2 and apply it in a `while` loop. We just update a `currentNode` pointer to traverse left or right.

* *Time:* $O(H)$ to traverse down the tree.
* *Space:* $O(1)$ because we only use a single pointer to track our position.
* *Tradeoffs:* This is optimal in both time and space. It also avoids `StackOverflowError` on highly skewed trees.

### 5. Select the solution

I will select **Approach 3 (Iterative with BST Property)**. It leverages the inherent properties of the given data structure to provide an efficient $O(H)$ time complexity, and using a loop instead of recursion gives us an optimal $O(1)$ space complexity. It is also straightforward to explain and implement.

### 6. Write the implementation outline

```java
TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {
    /*
     * Reframe:
     * Walk down the tree from the root. The first node we encounter where
     * p and q no longer lie in the same subtree is the lowest common ancestor.
     *
     * State:
     * A single pointer tracking the current node.
     * Chosen because we only need a top-down path without backtracking.
     *
     * Invariant:
     * Both p and q are guaranteed to be descendants of the current node
     * at the start of every loop iteration.
     *
     * Helpers:
     * None required.
     *
     * Core logic:
     * - set the current node to the root
     * - loop indefinitely (or while the current node is not null)
     * - if both p and q are smaller than the current node, move left
     * - if both p and q are larger than the current node, move right
     * - if they split, or one equals the current node, we found the LCA
     * - return the current node
     *
     * Edge cases:
     * - root is null (return null)
     */
}

```

### 7. Implement iteratively

**Iteration 1: Method skeleton**
I will define the standard `TreeNode` and establish the main traversal loop with TODOs.

```java
class TreeNode {
    int val;
    TreeNode left;
    TreeNode right;
    TreeNode(int x) { val = x; }
}

public TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {
    TreeNode current = root;

    while (current != null) {
        // TODO: check if both p and q are in the left subtree
        // TODO: check if both p and q are in the right subtree
        // TODO: otherwise, we found the split point, return current
    }

    return null;
}

```

**Iteration 2: Implement the easiest core section**
Now, I'll add the conditions to move left or right based on the BST property.

```java
public TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {
    TreeNode current = root;

    while (current != null) {
        // Added: Extract values for cleaner comparisons
        int pVal = p.val;
        int qVal = q.val;
        int currentVal = current.val;

        if (pVal < currentVal && qVal < currentVal) {
            // Both targets are strictly smaller, move to the left subtree
            current = current.left;
        } else if (pVal > currentVal && qVal > currentVal) {
            // Both targets are strictly greater, move to the right subtree
            current = current.right;
        } else {
            // TODO: handle the split point
        }
    }

    return null;
}

```

**Iteration 3: Complete the happy path**
If the targets are not both strictly less than or both strictly greater than the current node, it means they have diverged, or one of them *is* the current node. In either case, the current node is the LCA.

```java
public TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {
    TreeNode current = root;

    while (current != null) {
        int pVal = p.val;
        int qVal = q.val;
        int currentVal = current.val;

        if (pVal < currentVal && qVal < currentVal) {
            current = current.left;
        } else if (pVal > currentVal && qVal > currentVal) {
            current = current.right;
        } else {
            // Added: We found the split point. One node is on the left, 
            // the other is on the right, OR one node equals currentVal.
            return current;
        }
    }

    return null;
}

```

**Edge-case pass**

* *What if `root` is null?* The `current != null` loop condition handles this safely and returns `null` at the end.
* *What if `p` or `q` is the root?* `pVal < currentVal` evaluates to false, jumping directly to the `else` block and returning the root immediately. This is correct.
* *Are there integer overflow issues?* Comparing node values does not require arithmetic (like subtraction), so comparing `pVal < currentVal` is perfectly safe from overflow.

No code patches are required for edge cases.

### 8. Analyze expensive sections and optimize

Looking at the code, there are no expensive sections:

* No nested loops.
* No object instantiation or collection copying inside the loop.
* No recursive calls.

**Final Complexity:**

* **Time Complexity:** $O(H)$ where $H$ is the height of the tree. In the worst case (a completely unbalanced tree), this degrades to $O(N)$. In a balanced tree, it is $O(\log N)$.
* **Space Complexity:** $O(1)$. We only allocate a single reference variable (`current`) and a few primitive ints, regardless of the tree's size.

**Final Code**

```java
public class Solution {
    
    public TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {
        TreeNode current = root;

        while (current != null) {
            int pVal = p.val;
            int qVal = q.val;
            int currentVal = current.val;

            if (pVal < currentVal && qVal < currentVal) {
                current = current.left;
            } else if (pVal > currentVal && qVal > currentVal) {
                current = current.right;
            } else {
                return current;
            }
        }

        return null;
    }
}

```

### Brief test walkthrough

Let's test with the smallest valid tree that requires a split:
Tree: `[2, 1, 3]`, `p = 1`, `q = 3`

1. `current` = Node(2)
2. `pVal` = 1, `qVal` = 3, `currentVal` = 2
3. `pVal < currentVal && qVal < currentVal` -> `1 < 2 && 3 < 2` -> `false`
4. `pVal > currentVal && qVal > currentVal` -> `1 > 2 && 3 > 2` -> `false`
5. Falls into `else`, returns Node(2).
*Expected Result:* 2. *Actual Result:* 2. Works perfectly.