### 1. Restate the problem

We are given the root of a binary tree. We need to find the maximum possible sum of any valid path in this tree.

A path is a continuous sequence of connected nodes.

* It does not need to start or end at the root.
* It does not need to be a straight line (it can go up to a parent and down to another child).
* A node can only appear once in the path.
* The path must contain at least one node.
We must return the maximum sum of the values of the nodes along such a path.

### 2. Ask clarifying questions

* **Can node values be negative?** Yes, this is crucial because if values can be negative, we might prefer to completely ignore certain subtrees if they decrease our sum.
* **What is the size of the tree?** (Assuming 1 to $10^4$ nodes, so an $O(N)$ solution is required).
* **What if all nodes are negative?** Since the path must be non-empty, if all nodes are negative, the maximum path sum will be the single node with the highest (closest to zero) negative value.
* **Are we allowed to modify the tree?** We shouldn't need to, but it's good to confirm. (Assuming no).
* **Return type:** The problem implies returning an integer.

*Assumption:* We will use a standard `TreeNode` class with `val`, `left`, and `right` fields.

### 3. Work through an example by hand

Let's use a tree with a mix of positive and negative values:

```text
       -10
       /  \
      9   20
         /  \
       15    7

```

If we consider each node as the "highest" node (the peak) of a path:

* **Node 9:** The only path is `[9]`. Sum = 9.
* **Node 15:** The only path is `[15]`. Sum = 15.
* **Node 7:** The only path is `[7]`. Sum = 7.
* **Node 20:** A path can go up from 15, through 20, and down to 7. Sum = `15 + 20 + 7 = 42`.
* **Node -10:** A path could go from 9, up to -10, and down to 20. But wait, 20 has branches. A path cannot split, so it can only take *one* branch from 20. The best single branch from 20 is towards 15 (summing to `20 + 15 = 35`). So the path through -10 would be `9 + (-10) + 35 = 34`.

The maximum of all these possibilities is **42** (the path `15 -> 20 -> 7`).

### 4. Brainstorm solutions aloud

**Approach 1: Brute Force (Top-Down)**
For every node in the tree, treat it as the peak of the path. We calculate the maximum single straight path down its left child, and the maximum single straight path down its right child. We sum them with the node's value.

* *Time Complexity:* $O(N^2)$ because for each of the $N$ nodes, we traverse its subtrees to find the max single paths.
* *Space Complexity:* $O(H)$ for the call stack.

**Approach 2: Bottom-Up Post-order Traversal (DFS)**
We can optimize this by calculating things from the bottom up.
When we visit a node, we ask its children: "What is the maximum single-leg path you can provide?"
If a child returns a negative number, we should just ignore that child completely (treat it as 0) because adding a negative branch would only hurt our path sum.
At the current node, we can calculate two things:

1. **The max path if this node is the peak:** `node.val + max(0, left_leg) + max(0, right_leg)`. We update a global maximum with this value.
2. **What this node returns to its parent:** It can only return a single leg to its parent, so it returns `node.val + max(left_leg, right_leg)`.

* *Time Complexity:* $O(N)$ because we visit each node exactly once.
* *Space Complexity:* $O(H)$ for the recursion stack.

### 5. Select the solution

I will select **Approach 2 (Bottom-Up DFS)**. It is optimal $O(N)$, relies on a standard post-order traversal, and perfectly exploits the tree structure by solving subproblems recursively. It is the standard, most elegant way to solve tree path problems.

### 6. Write the implementation outline

```java
int maxPathSum(TreeNode root) {
    /*
     * Reframe:
     * Find the max path sum by visiting each node, treating it as the highest
     * point of a potential path, while passing a "single leg" sum up to its parent.
     *
     * State:
     * A global integer tracking the maximum path sum found so far.
     * Chosen because the maximum path could be entirely contained in a subtree
     * and never reach the root.
     *
     * Invariant:
     * The recursive helper always returns the maximum sum of a path extending 
     * strictly downwards from the current node. It never returns a path that 
     * branches both left and right.
     *
     * Helpers:
     * int findMaxLeg(TreeNode node)
     * - computes the maximum straight-line path extending from node down to a leaf
     *
     * Core logic:
     * - initialize global max to the smallest possible integer
     * - call findMaxLeg on the root
     * - inside findMaxLeg:
     *     - if node is null, return 0
     *     - recursively find the max leg of the left child (cap at 0 if negative)
     *     - recursively find the max leg of the right child (cap at 0 if negative)
     *     - compute the local path sum (left + right + current value)
     *     - update the global max if this local path sum is larger
     *     - return current value + the larger of the two legs
     *
     * Edge cases:
     * - tree has all negative numbers
     * - single node tree
     */
}

```

### 7. Implement iteratively

**Iteration 1: Method skeleton and global state**
First, I will set up the main method, the global state, and the stub for the recursive helper. I need an array of size 1 (or a class-level variable) to hold the global max because Java passes primitives by value. I'll use a class-level variable for simplicity.

```java
class Solution {
    private int globalMax;

    public int maxPathSum(TreeNode root) {
        // Initialize to minimum possible value in case all nodes are negative
        globalMax = Integer.MIN_VALUE;
        
        // TODO: Call recursive helper to traverse the tree
        
        return globalMax;
    }

    private int findMaxLeg(TreeNode node) {
        // TODO: Implement bottom-up traversal
        return 0;
    }
}

```

**Iteration 2: Recursive traversal and return value**
Next, I'll flesh out the recursive helper. I'll calculate the maximum legs from the left and right children.

```java
class Solution {
    private int globalMax;

    public int maxPathSum(TreeNode root) {
        globalMax = Integer.MIN_VALUE;
        findMaxLeg(root);
        return globalMax;
    }

    private int findMaxLeg(TreeNode node) {
        if (node == null) {
            return 0;
        }

        // Added: Post-order traversal to get max paths from children.
        // We use Math.max(0, ...) because a negative path sum is worse than no path at all.
        int leftLeg = Math.max(0, findMaxLeg(node.left));
        int rightLeg = Math.max(0, findMaxLeg(node.right));

        // TODO: Update global maximum with the path that peaks at this node

        // Added: Return the maximum single leg extending down from this node
        return node.val + Math.max(leftLeg, rightLeg);
    }
}

```

**Iteration 3: Complete the happy path**
Now I will add the logic to calculate the path that peaks at the current node and update the global maximum.

```java
class Solution {
    private int globalMax;

    public int maxPathSum(TreeNode root) {
        globalMax = Integer.MIN_VALUE;
        findMaxLeg(root);
        return globalMax;
    }

    private int findMaxLeg(TreeNode node) {
        if (node == null) {
            return 0;
        }

        int leftLeg = Math.max(0, findMaxLeg(node.left));
        int rightLeg = Math.max(0, findMaxLeg(node.right));

        // Added: The path sum if the current node is the highest point (the peak).
        // It connects the best left leg, the node itself, and the best right leg.
        int localPeakSum = node.val + leftLeg + rightLeg;
        globalMax = Math.max(globalMax, localPeakSum);

        return node.val + Math.max(leftLeg, rightLeg);
    }
}

```

### 8. Edge-case pass

Let's review the edge cases identified earlier.

**Edge case 1: Tree with only negative values**
Suppose the tree is just:

```text
    -3
   /  \
 -5   -2

```

1. `findMaxLeg(-5)` returns `Math.max(0, 0) + (-5) = -5`.
Inside, `localPeakSum` is `-5 + 0 + 0 = -5`. `globalMax` becomes `-5`.
2. `findMaxLeg(-2)` returns `-2`.
Inside, `localPeakSum` is `-2`. `globalMax` becomes `-2`.
3. `findMaxLeg(-3)` calls left and right.
`leftLeg` = `Math.max(0, -5)` = `0`.
`rightLeg` = `Math.max(0, -2)` = `0`.
`localPeakSum` = `-3 + 0 + 0` = `-3`.
`globalMax` = `Math.max(-2, -3)` = `-2`.
The code correctly identifies `-2` as the maximum path. The `Math.max(0, ...)` logic handles negative branches perfectly, while `globalMax = Integer.MIN_VALUE` ensures we don't accidentally return `0` when the best valid path is negative. No patch is needed.

**Edge case 2: Single node tree**
If the tree is just `[5]`.
`findMaxLeg(5)` calculates `leftLeg = 0`, `rightLeg = 0`.
`localPeakSum = 5`. `globalMax` becomes 5.
Returns 5. Correct.

### 9. Analyze expensive sections and optimize

The algorithm visits each node exactly once using a standard DFS recursion.
There are no expensive operations inside the loop (only constant time additions and `Math.max` checks). No intermediate objects or strings are created.

* **Time Complexity:** $O(N)$, where $N$ is the number of nodes in the binary tree, since we visit every node exactly once.
* **Space Complexity:** $O(H)$, where $H$ is the height of the tree. This accounts for the maximum size of the recursion stack. In the worst case (a perfectly unbalanced, list-like tree), this is $O(N)$. In the best case (a perfectly balanced tree), this is $O(\log N)$.

This is optimal for the problem since we must inspect at least every node to know the maximum path sum.

### Final code

```java
/**
 * Definition for a binary tree node.
 */
class TreeNode {
    int val;
    TreeNode left;
    TreeNode right;
    TreeNode(int x) { val = x; }
}

class Solution {
    private int globalMax;

    public int maxPathSum(TreeNode root) {
        globalMax = Integer.MIN_VALUE;
        findMaxLeg(root);
        return globalMax;
    }

    private int findMaxLeg(TreeNode node) {
        if (node == null) {
            return 0;
        }

        // Ignore negative paths by capping the minimum contribution at 0.
        int leftLeg = Math.max(0, findMaxLeg(node.left));
        int rightLeg = Math.max(0, findMaxLeg(node.right));

        // Calculate the maximum path sum assuming the current node is the highest point.
        int localPeakSum = node.val + leftLeg + rightLeg;
        
        // Update the global maximum if this path is the best we've seen.
        globalMax = Math.max(globalMax, localPeakSum);

        // Return the maximum single leg extending downwards from this node
        // so the parent can potentially append it to its own path.
        return node.val + Math.max(leftLeg, rightLeg);
    }
}

```

### 10. Brief test walkthrough

Let's briefly trace our initial manual example:

```text
       -10
       /  \
      9   20
         /  \
       15    7

```

1. DFS reaches leaf `9`. `leftLeg = 0`, `rightLeg = 0`. `localPeak = 9`. `globalMax = 9`. Returns `9`.
2. DFS reaches leaf `15`. `leftLeg = 0`, `rightLeg = 0`. `localPeak = 15`. `globalMax = 15`. Returns `15`.
3. DFS reaches leaf `7`. `leftLeg = 0`, `rightLeg = 0`. `localPeak = 7`. `globalMax = 15`. Returns `7`.
4. DFS reaches `20`. `leftLeg = Math.max(0, 15) = 15`. `rightLeg = Math.max(0, 7) = 7`. `localPeak = 20 + 15 + 7 = 42`. `globalMax` updates to `42`. Returns `20 + max(15, 7) = 35`.
5. DFS reaches `-10`. `leftLeg = Math.max(0, 9) = 9`. `rightLeg = Math.max(0, 35) = 35`. `localPeak = -10 + 9 + 35 = 34`. `globalMax` remains `42`. Returns `-10 + 35 = 25`.

The traversal concludes. The method returns `globalMax`, which correctly holds `42`.