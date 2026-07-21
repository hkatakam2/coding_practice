### 1. Restate the problem

We are given two binary trees: a main tree (`root`) and a smaller tree (`subRoot`). We need to determine if `subRoot` appears exactly as-is somewhere inside `root`.

To count as a valid subtree, the matching portion must start at some node in the main tree and include *all* of that node's descendants. It must be identical in both structure and node values. The main tree is also considered a valid subtree of itself. We must return `true` if a match is found, and `false` otherwise.

### 2. Ask clarifying questions

Before implementing, I would want to confirm a few details:

* **Can `root` or `subRoot` be `null`?**
* *Assumption:* Standard constraints usually dictate at least one node in both trees (e.g., 1 to $10^4$ nodes). However, I will assume `subRoot` might theoretically be null (an empty tree is a subtree of any tree) and handle it defensively.


* **Are node values unique?**
* *Assumption:* No. Duplicate values are allowed, which means we might find multiple nodes in `root` that match the root value of `subRoot`.


* **Is the input allowed to be modified?**
* *Assumption:* No, we should treat the trees as read-only.


* **How large can the trees get?**
* *Assumption:* A depth of up to a few thousand nodes, meaning standard recursion might push stack limits, but we will assume standard JVM stack sizes can handle typical $O(H)$ recursive depth.



### 3. Work through an example by hand

Let's use a representative example:
**`root` tree:**

```text
      3
     / \
    4   5
   / \
  1   2

```

**`subRoot` tree:**

```text
    4
   / \
  1   2

```

**Step-by-step Execution:**

1. **Current state:** Look at `root` node `3`.
* *Decision:* Compare tree starting at `3` with `subRoot` starting at `4`. Values `3` and `4` do not match.


2. **Current state:** Move to left child `4`.
* *Decision:* Compare tree starting at `4` with `subRoot` starting at `4`. Values match.
* Check left children: `1` matches `1`.
* Check right children: `2` matches `2`.
* Check children of `1` and `2`: Both are null in `root` and `subRoot`. Match is complete.


3. **Result:** Since a full match was found, we immediately return `true`.

### 4. Brainstorm solutions aloud

**Approach 1: Direct Simulation (DFS + DFS)**

* **Core idea:** Traverse every node in `root`. Treat every single node as a potential starting point. For each node, run a helper function `isSameTree` that checks if the tree originating there perfectly matches `subRoot`.
* **Data structures:** None explicitly, just the implicit call stack for Depth-First Search (DFS).
* **Time complexity:** $O(M \times N)$ where $M$ is the number of nodes in `root` and $N$ is the number of nodes in `subRoot`. In the worst case (e.g., all nodes have the value `1`), we do a full $O(N)$ comparison at every single node.
* **Space complexity:** $O(H)$ where $H$ is the height of `root`, due to the recursion stack.
* **Tradeoffs:** Very simple to implement and understand. Worst-case time complexity is quadratic, but practical performance is usually much faster because mismatches are found instantly.

**Approach 2: Tree Serialization and Substring Search**

* **Core idea:** Traverse both trees (e.g., using preorder traversal) and convert them into strings. We must include markers for nulls (like `#`) and boundaries (like `^` and `$`) so that a node value of `12` isn't accidentally matched by a subRoot of `2`. Then, use a substring search to see if the `subRoot` string exists inside the `root` string.
* **Data structures:** `StringBuilder` for string construction.
* **Time complexity:** $O(M + N)$ to serialize, plus $O(M + N)$ for KMP substring search (or built-in `String.contains`).
* **Space complexity:** $O(M + N)$ to store the serialized strings.
* **Tradeoffs:** Better worst-case time complexity, but building large strings requires substantial memory and heap allocations. Boundary markers make the code slightly messy and prone to edge-case bugs.

### 5. Select the solution

I will choose **Approach 1: Direct Simulation (DFS + DFS)**.

* **Justification:** The constraints for this problem generally allow an $O(M \times N)$ worst-case. The DFS approach requires $O(1)$ auxiliary space beyond the stack, avoids expensive string allocations, and demonstrates core tree traversal logic cleanly. It is the most robust, easiest to test, and most readable approach. We prefer standard recursion and clear tree helpers over dense string hacking.

### 6. Write the implementation outline

```java
boolean isSubtree(TreeNode root, TreeNode subRoot) {
    /*
     * Reframe:
     * Walk through every node in the main tree. At each node, ask: "Do the 
     * trees match perfectly starting here?" If yes, we found our answer.
     *
     * State:
     * Recursion stack to track our position in both trees. No extra collections.
     * Chosen because tree structures naturally align with recursive decomposition.
     *
     * Invariant:
     * For any given subtree in 'root', either it matches 'subRoot' exactly, 
     * or the valid match must exist somewhere in its left or right children.
     *
     * Helpers:
     * isSameTree(tree1, tree2)
     * - Returns true only if both trees have identical structure and values.
     *
     * Core logic:
     * - If subRoot is null, it's always a subtree (true).
     * - If root is null but subRoot is not, it can't contain the subtree (false).
     * - Check if the trees match perfectly right now using isSameTree.
     * - If they do, return true.
     * - Otherwise, recursively search the left child OR the right child.
     *
     * Edge cases:
     * - Reaching leaf nodes without a match.
     * - Mismatched structures (one side is null, the other has a node).
     */
}

```

### 7. Implement iteratively

#### Iteration 1: Method skeleton

I'll set up the main traversal method and stub out the equality helper.

```java
public boolean isSubtree(TreeNode root, TreeNode subRoot) {
    // TODO: Handle null edge cases for root and subRoot
    
    // TODO: Check if the current tree matches subRoot
    
    // TODO: Recursively check the left and right subtrees
    
    return false;
}

private boolean isSameTree(TreeNode tree1, TreeNode tree2) {
    // TODO: Compare structure and values of both trees
    return false;
}

```

#### Iteration 2: Implement the `isSameTree` helper

Now, I will implement the helper function. This requires checking both nodes simultaneously.

```java
public boolean isSubtree(TreeNode root, TreeNode subRoot) {
    // TODO: Check if the current tree matches subRoot
    // TODO: Recursively check the left and right subtrees
    return false;
}

private boolean isSameTree(TreeNode tree1, TreeNode tree2) {
    // Added: Both nodes reached null simultaneously -> identical paths
    if (tree1 == null && tree2 == null) {
        return true;
    }
    
    // Added: Only one node is null -> structural mismatch
    if (tree1 == null || tree2 == null) {
        return false;
    }
    
    // Added: Values must match, AND both left and right subtrees must match perfectly
    return (tree1.val == tree2.val) 
        && isSameTree(tree1.left, tree2.left) 
        && isSameTree(tree1.right, tree2.right);
}

```

*Note: The helper is completely self-contained. It strictly verifies identicalness.*

#### Iteration 3: Complete the main traversal logic

Now I will wire the main `isSubtree` method to utilize the helper at every node.

```java
public boolean isSubtree(TreeNode root, TreeNode subRoot) {
    // Added: Base case - an empty subRoot is technically a subtree of anything
    if (subRoot == null) {
        return true;
    }
    // Added: Base case - if we've exhausted the main tree without finding subRoot
    if (root == null) {
        return false;
    }
    
    // Added: Check if the identical tree starts exactly at this root node
    if (isSameTree(root, subRoot)) {
        return true;
    }
    
    // Added: Otherwise, search downwards into the left and right branches
    return isSubtree(root.left, subRoot) || isSubtree(root.right, subRoot);
}

private boolean isSameTree(TreeNode tree1, TreeNode tree2) {
    if (tree1 == null && tree2 == null) {
        return true;
    }
    if (tree1 == null || tree2 == null) {
        return false;
    }
    return (tree1.val == tree2.val) 
        && isSameTree(tree1.left, tree2.left) 
        && isSameTree(tree1.right, tree2.right);
}

```

#### Edge-case pass

Let's review the edge cases identified:

1. **Empty `subRoot`:** Handled by `if (subRoot == null) return true;`.
2. **Empty `root`:** Handled by `if (root == null) return false;`. Order matters here! We must check `subRoot == null` before `root == null` to satisfy the case where both are null.
3. **Trees are identical:** `isSameTree` triggers on the very first node. Returns `true`.
4. **Values match but structure diverges deeper down:** `isSameTree` will correctly return `false`, and `isSubtree` will seamlessly fall back to searching `root.left` and `root.right`.

The logic holds up. No code patches are necessary.

### 8. Final code

Assuming the standard `TreeNode` definition exists, here is the complete, readable implementation:

```java
/**
 * Definition for a binary tree node.
 * public class TreeNode {
 *     int val;
 *     TreeNode left;
 *     TreeNode right;
 *     TreeNode() {}
 *     TreeNode(int val) { this.val = val; }
 *     TreeNode(int val, TreeNode left, TreeNode right) {
 *         this.val = val;
 *         this.left = left;
 *         this.right = right;
 *     }
 * }
 */
class Solution {
    public boolean isSubtree(TreeNode root, TreeNode subRoot) {
        // An empty subtree is present in every tree.
        if (subRoot == null) {
            return true;
        }
        // If the main tree is exhausted but subRoot is not, it's not a match.
        if (root == null) {
            return false;
        }
        
        // If the tree rooted at the current node matches subRoot exactly, we are done.
        if (isSameTree(root, subRoot)) {
            return true;
        }
        
        // Otherwise, continue searching down both branches.
        return isSubtree(root.left, subRoot) || isSubtree(root.right, subRoot);
    }

    private boolean isSameTree(TreeNode tree1, TreeNode tree2) {
        // Both nodes are null: we've reached the bottom of a matching path.
        if (tree1 == null && tree2 == null) {
            return true;
        }
        
        // One node is null while the other isn't: structural mismatch.
        if (tree1 == null || tree2 == null) {
            return false;
        }
        
        // Ensure values match, and recursively verify the entire structure beneath them.
        return (tree1.val == tree2.val) 
            && isSameTree(tree1.left, tree2.left) 
            && isSameTree(tree1.right, tree2.right);
    }
}

```

### Complexity

* **Time Complexity:** $O(M \times N)$ in the worst case, where $M$ is the number of nodes in `root` and $N$ is the number of nodes in `subRoot`. This occurs if we have to do a deep traversal of `subRoot` at every single node of `root` (for instance, if `root` is a long single line of `1`s, and `subRoot` is also a slightly shorter line of `1`s).
* **Space Complexity:** $O(H)$ worst-case auxiliary space for the recursion call stack, where $H$ is the depth of `root`. In a balanced tree, this is $O(\log M)$. In a completely skewed tree, it is $O(M)$. No input mutation or data copying is performed.

### Brief test walkthrough

Let's test with the smallest edge case: Both `root` and `subRoot` are a single node with the value `5`.

* `isSubtree` starts. Neither is null.
* `isSameTree(5, 5)` is called.
* Neither is null.
* Values `5 == 5`.
* Recurses to `isSameTree(null, null)` for the left child. Returns `true`.
* Recurses to `isSameTree(null, null)` for the right child. Returns `true`.
* `isSameTree` returns `true`.


* `isSubtree` immediately returns `true`.
* *Result:* Expected behavior confirmed. Identical single-node trees correctly register as subtrees.