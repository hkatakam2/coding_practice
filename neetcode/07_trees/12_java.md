### 1. Restate the problem

We are given the root of a Binary Search Tree (BST) and an integer $k$.
We need to find the $k$-th smallest value in this tree.
The index $k$ is 1-based, meaning $k=1$ asks for the absolute smallest element.
Because it is a BST, the structural property is key: a node's left subtree contains strictly smaller values, and its right subtree contains larger values.

### 2. Ask clarifying questions

* **Input constraints:** Is $k$ guaranteed to be valid ($1 \le k \le$ number of nodes in the tree)? *Assumption: Yes, $k$ is always valid.*
* **Tree size:** Can the tree be empty? *Assumption: No, since $k \ge 1$ is valid, the tree has at least one node.*
* **Modifications:** Should the tree remain unmodified? *Assumption: Yes, read-only.*
* **Definition:** What does the Java node class look like? *Assumption: Standard `TreeNode` with `val`, `left`, and `right` fields.*

### 3. Work through an example by hand

Given this BST and $k = 3$:

```text
       5
      / \
     3   6
    / \
   2   4

```

* To find values in ascending order, we traverse the left-most path.
* Smallest (1st): go left as far as possible -> `2`.
* 2nd smallest: go up to parent -> `3`.
* 3rd smallest: go to right child of `3` -> `4`.
* Since we need $k=3$, the answer is `4`.

### 4. Brainstorm solutions aloud

* **Approach 1: Full In-Order Traversal**
* *Idea:* Traverse the entire tree in-order (left, root, right), append every value to a `List<Integer>`, then return `list.get(k - 1)`.
* *Complexity:* Time $O(n)$, Space $O(n)$ where $n$ is the total number of nodes.
* *Tradeoffs:* Very easy to write, but highly inefficient if the tree has 10,000 nodes and we only want the 1st smallest. It doesn't stop early.


* **Approach 2: Recursive In-Order with Counter**
* *Idea:* Do a recursive in-order traversal, but keep a counter. When the counter reaches $k$, record the result and halt further traversal.
* *Complexity:* Time $O(h + k)$, Space $O(h)$ for the call stack, where $h$ is the tree height.
* *Tradeoffs:* Better time complexity. However, in Java, primitives are passed by value, so maintaining a shared counter across recursive calls requires either an instance variable, a mutable wrapper class, or a 1-element array (`int[] count = {k}`). This can feel slightly clunky or violate pure functional design.


* **Approach 3: Iterative In-Order using a Stack**
* *Idea:* Simulate the recursive call stack manually using a `Deque`. We push all left children to the stack. When we pop, we process the node, decrement $k$, and if $k=0$, we found our answer. Otherwise, we move to the right child and repeat.
* *Complexity:* Time $O(h + k)$, Space $O(h)$.
* *Tradeoffs:* Achieves the optimal time and space without needing instance variables or wrapper arrays. Control flow is highly explicit.



### 5. Select the solution

I will use **Approach 3: Iterative In-Order using a Stack**.
It naturally models the "pause and resume" behavior needed to stop exactly at the $k$-th element. It strictly uses local variables, making it thread-safe and clean. An `ArrayDeque` will provide standard stack behavior.

### 6. Write the implementation outline

```java
int kthSmallest(TreeNode root, int k) {
    /*
     * Reframe:
     * Walk the BST in-order iteratively, counting down k until we hit 0.
     *
     * State:
     * Deque<TreeNode> stack: tracks the path back to the parent nodes.
     * Chosen because stack perfectly models the LIFO nature of tree backtracking.
     * TreeNode currentNode: tracks the node we are currently visiting.
     *
     * Invariant:
     * Nodes are popped from the stack in strictly ascending order.
     *
     * Core logic:
     * - initialize an empty stack and point currentNode to root
     * - loop while there are nodes to process (currentNode != null OR stack is not empty)
     *   - push the current node and dive left as far as possible
     *   - pop the top node from the stack (this is the next smallest element)
     *   - decrement k
     *   - if k is 0, return the popped node's value
     *   - shift currentNode to the right child to explore larger values
     *
     * Edge cases:
     * - Tree is purely right-skewed or left-skewed.
     */
}

```

### 7. Implement iteratively

**Iteration 1: method skeleton**
Setup the core variables and the main loop structure.

```java
public int kthSmallest(TreeNode root, int k) {
    Deque<TreeNode> stack = new ArrayDeque<>();
    TreeNode currentNode = root;

    // We continue as long as there are unexplored nodes in the tree
    while (currentNode != null || !stack.isEmpty()) {
        // TODO: travel all the way down the left spine
        
        // TODO: process the current smallest node
        
        // TODO: move to the right subtree
    }

    return -1; // Fallback if k is invalid
}

```

**Iteration 2: implementing the left spine dive**
We must push every node onto the stack as we go left, meaning we will process the deepest left node first.

```java
public int kthSmallest(TreeNode root, int k) {
    Deque<TreeNode> stack = new ArrayDeque<>();
    TreeNode currentNode = root;

    while (currentNode != null || !stack.isEmpty()) {
        // Added: push nodes onto stack while moving down the left spine
        while (currentNode != null) {
            stack.push(currentNode);
            currentNode = currentNode.left;
        }
        
        // TODO: process the node and move right
    }

    return -1;
}

```

**Iteration 3: complete the happy path**
We pop the node, which gives us the next value in sorted order, check our $k$ target, and redirect our pointer to the right child.

```java
public int kthSmallest(TreeNode root, int k) {
    Deque<TreeNode> stack = new ArrayDeque<>();
    TreeNode currentNode = root;

    while (currentNode != null || !stack.isEmpty()) {
        while (currentNode != null) {
            stack.push(currentNode);
            currentNode = currentNode.left;
        }
        
        // Added: pop the lowest unvisited node
        currentNode = stack.pop();
        k--; // We've found the next smallest element
        
        // Added: finish immediately when we hit the k-th element
        if (k == 0) {
            return currentNode.val;
        }
        
        // Added: move to the right child to continue the in-order traversal
        currentNode = currentNode.right;
    }

    return -1;
}

```

### 8. Edge-case pass

Let's trace potential edge cases:

* **$k=1$ (Absolute smallest):** We dive all the way left, pop once, $k$ becomes 0, we immediately return. Correct.
* **Tree is entirely left-skewed:** The inner `while` loop runs $N$ times. Then we pop, return. Correct.
* **Tree is entirely right-skewed:** The inner `while` loop runs once (for the root), pushing it. We pop it, if $k \neq 1$, we go right. Next outer loop iteration, we push the right child, pop it, etc. Correct.
* **$k$ is larger than tree size:** Our assumption is that $k$ is valid. If it wasn't, the loop would naturally exhaust, and the method would return `-1`. This behavior is acceptable given the constraints.

No code modifications are required for these edge cases.

### Final code

```java
/**
 * Definition for a binary tree node.
 * public class TreeNode {
 *     int val;
 *     TreeNode left;
 *     TreeNode right;
 *     TreeNode(int x) { val = x; }
 * }
 */
class Solution {
    public int kthSmallest(TreeNode root, int k) {
        Deque<TreeNode> stack = new ArrayDeque<>();
        TreeNode currentNode = root;

        while (currentNode != null || !stack.isEmpty()) {
            // Dive as far left as possible
            while (currentNode != null) {
                stack.push(currentNode);
                currentNode = currentNode.left;
            }
            
            // The top of the stack is the next smallest element
            currentNode = stack.pop();
            k--;
            
            // If we've popped k elements, we found our target
            if (k == 0) {
                return currentNode.val;
            }
            
            // Move to the right subtree
            currentNode = currentNode.right;
        }

        throw new IllegalArgumentException("k is larger than the number of nodes in the tree.");
    }
}

```

### Complexity

* **Time Complexity:** $O(h + k)$, where $h$ is the height of the tree. Reaching the leftmost leaf takes $O(h)$ steps. Afterward, we visit $k$ nodes. Pushing and popping each node takes $O(1)$ time. In the worst case (a right-skewed tree where we want the last element), it bounds to $O(n)$.
* **Space Complexity:** $O(h)$ to maintain the stack. In a balanced BST, this is $O(\log n)$. In a completely unbalanced (skewed) tree, it degrades to $O(n)$.

### Brief test walkthrough

Let's run the main example: Tree `[5, 3, 6, 2, 4, null, null]`, $k = 3$.

1. `stack` is empty. `currentNode = 5`.
2. Dive left: push `5`, push `3`, push `2`. `currentNode` is now `null`. Stack: `[2, 3, 5]`.
3. Pop `2`. `currentNode = 2`. $k$ becomes 2. $k \neq 0$.
4. `currentNode = 2.right`, which is `null`.
5. Dive left loop skipped.
6. Pop `3`. `currentNode = 3`. $k$ becomes 1. $k \neq 0$.
7. `currentNode = 3.right`, which is `4`.
8. Dive left: push `4`. `currentNode` becomes `null`. Stack: `[4, 5]`.
9. Pop `4`. `currentNode = 4`. $k$ becomes 0.
10. $k == 0$ is true. Return `4`.
Result is exactly as expected.