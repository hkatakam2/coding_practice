### 1. Restate the problem

We need to find the maximum depth of a binary tree.
Given the root node of the tree, we must calculate the number of nodes along the longest possible downward path from the root to any leaf node.

* **Given:** The root of a binary tree.
* **Must return:** An integer representing the maximum depth.
* **Constraint/Relationship:** A tree's depth is 1 (for the current node) plus the maximum of the depths of its left and right subtrees.

### 2. Ask clarifying questions

Before writing code, I would confirm a few details about the environment and constraints:

* **Empty input:** Can the root be `null`? (Assumption: Yes, an empty tree should return a depth of `0`).
* **Single node:** If the tree has only a root, is the depth `1`? (Assumption: Yes, since the path contains exactly 1 node).
* **Tree size:** What is the maximum number of nodes in the tree? (Assumption: Up to 10,000 nodes. If the tree is entirely skewed—like a linked list—the recursion depth would reach 10,000, which might cause a `StackOverflowError` depending on JVM settings. I'll proceed with recursion as it's standard, but keep an iterative approach in mind if stack size is strictly limited).
* **Structure:** Standard `TreeNode` class with `val`, `left`, and `right` pointers? (Assumption: Yes).

### 3. Work through an example by hand

Let's trace an example with a slightly imbalanced tree:

```text
      3
     / \
    9  20
      /  \
     15   7
           \
            5

```

**Step-by-step evaluation (Bottom-Up):**

* Node `5` is a leaf. Its left and right are null (depth 0). Depth of `5` = 1 + max(0, 0) = 1.
* Node `7` has no left child (depth 0) and a right child `5` (depth 1). Depth of `7` = 1 + max(0, 1) = 2.
* Node `15` is a leaf. Depth of `15` = 1 + max(0, 0) = 1.
* Node `20` has left `15` (depth 1) and right `7` (depth 2). Depth of `20` = 1 + max(1, 2) = 3.
* Node `9` is a leaf. Depth of `9` = 1.
* Root Node `3` has left `9` (depth 1) and right `20` (depth 3). Depth of `3` = 1 + max(1, 3) = 4.

The final result is 4.

### 4. Brainstorm solutions aloud

* **Approach 1: Recursive Depth-First Search (DFS)**
The literal process I just used is a post-order traversal. We ask the left child for its depth, ask the right child for its depth, take the maximum of those two, and add 1 for the current node.
* *Time complexity:* O(N) because we visit each node exactly once.
* *Space complexity:* O(H) where H is the height of the tree. In the worst case (a skewed tree), this is O(N). In the best case (balanced tree), it is O(log N).


* **Approach 2: Iterative Breadth-First Search (BFS)**
We can use a `Queue` to traverse the tree level by level. We start with the root, and for each level, we dequeue all nodes currently in the queue, enqueue their non-null children, and increment a `depth` counter.
* *Time complexity:* O(N).
* *Space complexity:* O(W) where W is the maximum width of the tree. In a balanced tree, the bottom level has roughly N/2 nodes, making it O(N) space.
* *Tradeoff:* This avoids the method call stack overhead and prevents `StackOverflowError` on deeply skewed trees.


* **Approach 3: Iterative DFS**
We can mimic the call stack using an explicit `Deque` (stack) storing a pair or record of `(TreeNode, currentDepth)`.

### 5. Select the solution

I will select **Approach 1: Recursive DFS**.
For the problem of finding tree depth, recursion perfectly models the recursive, self-similar nature of a binary tree. It is extremely easy to explain, straightforward to implement without bugs, and runs in optimal O(N) time. Unless the interviewer specifically warns about `StackOverflowError` from deep, degenerate trees, the standard recursive approach is universally preferred here for its elegance.

### 6. Write the implementation outline

```java
int maxDepth(TreeNode root) {
    /*
     * Reframe:
     * The maximum depth is 1 (for the current node) plus the deepest path 
     * of either its left or right subtree.
     *
     * State:
     * No explicit data structures maintained; state is implicitly handled 
     * by the Java method call stack.
     * Chosen because tree depth is inherently a recursive property.
     *
     * Invariant:
     * For any given subtree, the method strictly returns the maximum 
     * number of nodes from that subtree's root to its farthest leaf.
     *
     * Core logic:
     * - Handle the base case: if the node is null, its depth is 0.
     * - Recursively calculate the depth of the left subtree.
     * - Recursively calculate the depth of the right subtree.
     * - Return 1 plus the larger of the two subtree depths.
     *
     * Edge cases:
     * - The root is null (empty tree).
     * - The tree is entirely skewed (handled naturally, assuming stack permits).
     */
}

```

### 7. Implement iteratively

**Iteration 1: Method skeleton and base case**
We begin by establishing the signature and the exit condition for our recursion.

```java
public int maxDepth(TreeNode root) {
    // Base case: reaching a null child means a depth of 0
    if (root == null) {
        return 0;
    }

    // TODO: compute left subtree depth
    // TODO: compute right subtree depth
    // TODO: return max + 1
    
    return 0;
}

```

*Why this step?* Handling the `null` check first prevents `NullPointerException` and serves as the stopping point for leaf node traversals.

**Iteration 2: Complete the core recursive logic**
Now we implement the post-order recursive calls and the arithmetic.

```java
public int maxDepth(TreeNode root) {
    if (root == null) {
        return 0;
    }

    // Added: recursively evaluate the subtrees
    int leftDepth = maxDepth(root.left);
    int rightDepth = maxDepth(root.right);

    // Added: return current node (1) plus the maximum of the child depths
    return 1 + Math.max(leftDepth, rightDepth);
}

```

*Why this step?* We calculate the left and right depths fully before processing the current node's height, completing the mathematical definition of tree depth.

**Edge-case pass**

* *Empty input:* `maxDepth(null)` immediately hits the first `if` and returns `0`. Correct.
* *Single node:* `maxDepth(new TreeNode(5))`. `leftDepth` and `rightDepth` will both evaluate to `0`. Returns `1 + Math.max(0, 0) = 1`. Correct.
* *Integer Overflow:* Could the depth exceed `Integer.MAX_VALUE`? No, because memory would run out (or the stack would overflow) long before a tree could hold 2 billion nodes. Primitive `int` is perfectly safe here.

### 8. Analyze expensive sections and optimize

Looking at the completed implementation:

* **Time Complexity:** O(N), where N is the total number of nodes in the tree. We must visit every single node once to ensure we haven't missed a deeper path. This cannot be optimized further.
* **Space Complexity:** O(H), where H is the height of the tree. This is the memory used by the recursion stack. In a perfectly balanced tree, H = log(N). In the absolute worst case (a completely unbalanced, linked-list-like tree), H = N, resulting in O(N) space.

There are no expensive repeated scans, loops, or object creations inside the core logic. The math is simple integer arithmetic. The solution is optimal.

### Final Code

Here is the clean, final version of the code, including the standard `TreeNode` definition for completeness:

```java
/**
 * Standard representation of a Binary Tree Node.
 */
class TreeNode {
    int val;
    TreeNode left;
    TreeNode right;

    TreeNode(int val) {
        this.val = val;
    }
}

class Solution {
    
    /**
     * Calculates the maximum depth of a binary tree.
     * 
     * @param root The root node of the tree.
     * @return The number of nodes along the longest path from root to leaf.
     */
    public int maxDepth(TreeNode root) {
        if (root == null) {
            return 0;
        }

        int leftDepth = maxDepth(root.left);
        int rightDepth = maxDepth(root.right);

        return 1 + Math.max(leftDepth, rightDepth);
    }
}

```

### Brief test walkthrough

Let's mentally test the smallest valid inputs:

1. **Test Case: Empty Tree**
* `root` = `null`
* Expected result: `0`
* Execution: The initial `root == null` check triggers immediately, returning `0`.


2. **Test Case: Left-skewed Tree (3 nodes)**
* `root` = `[2, 1, null]` (Node 2 has left child 1, no right child)
* Expected result: `2`
* Execution:
* `maxDepth(2)` calls `maxDepth(1)` and `maxDepth(null)`.
* `maxDepth(null)` returns `0` for the right side.
* `maxDepth(1)` evaluates its children (both null, so both return `0`), yielding `1 + Math.max(0,0) = 1`.
* Back at root `2`: yields `1 + Math.max(1, 0) = 2`. Result is correctly `2`.