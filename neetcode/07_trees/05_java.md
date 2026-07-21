### 1. Restate the problem

We are given the root nodes of two binary trees, `p` and `q`. We need to determine if these two trees are completely identical.

"Identical" or "equivalent" means two things must be true:

1. **Structural equality**: The trees have the exact same shape (if a node has a left child in tree `p`, the corresponding node in tree `q` must also have a left child, and so on).
2. **Value equality**: Every corresponding pair of nodes in the two trees contains the exact same integer value.

If both conditions are met everywhere, we return `true`. Otherwise, we return `false`.

### 2. Ask clarifying questions

Before writing code, I would normally clarify a few constraints with the interviewer:

* **Can the trees be empty (null)?**
* *Assumption:* Yes. If both are null, they are equivalent. If one is null and the other is not, they are not equivalent.


* **What is the maximum number of nodes in these trees?**
* *Assumption:* Standard constraints (e.g., up to 10^4 nodes). This helps decide if recursion depth will cause a `StackOverflowError`.


* **Can tree values be negative or zero?**
* *Assumption:* Yes. We will use standard `==` integer comparison which handles this naturally.


* **Are we allowed to modify the trees?**
* *Assumption:* No, this should be a read-only operation.


* **What is the tree node structure?**
* *Assumption:* A standard `TreeNode` class with `int val`, `TreeNode left`, and `TreeNode right`.



### 3. Work through an example by hand

Let's take a representative example where the structure matches initially, but a value differs deeper in the tree, and one node has a different structure.

**Tree P:**

```text
      1
     / \
    2   3
   /
  4

```

**Tree Q:**

```text
      1
     / \
    2   3
     \
      4

```

**Step-by-step comparison:**

1. **Compare roots:** `p` is 1, `q` is 1. They match. We must now check their left and right subtrees.
2. **Compare left subtrees (p=2, q=2):** Both exist, values match (2 == 2). We must check their subtrees.
* **Check p's left (4) vs q's left (null):** One exists, the other does not. The structures differ.


3. **Result:** We immediately know the trees are not equivalent. We can return `false` without needing to check the right subtree of the root (node 3).

### 4. Brainstorm solutions aloud

**Approach 1: Recursive Depth-First Search (DFS)**

* **Core idea:** Two trees are identical if their roots are identical, their left subtrees are identical, and their right subtrees are identical. This naturally lends itself to recursion.
* **Data structures:** The call stack (implicit).
* **Time complexity:** O(n), where n is the minimum number of nodes between the two trees, because we visit each node at most once and stop early if a mismatch is found.
* **Space complexity:** O(h), where h is the height of the tree, representing the maximum depth of the call stack. In the worst case (a completely skewed tree), this is O(n). In a balanced tree, it's O(log n).

**Approach 2: Iterative Breadth-First Search (BFS)**

* **Core idea:** Traverse both trees level by level simultaneously. Use a queue to hold pairs of nodes to compare.
* **Data structures:** A `Queue<TreeNode>` or two separate queues.
* **Time complexity:** O(n), comparing each pair.
* **Space complexity:** O(w), where w is the maximum width of the tree. In a perfectly balanced tree, the bottom level has n/2 nodes, so space is O(n).
* **Tradeoffs:** This avoids the risk of a `StackOverflowError` for extremely deep, unbalanced trees (e.g., 100,000 nodes in a straight line).

### 5. Select the solution

I will choose **Approach 1 (Recursive DFS)**.

*Why?* Binary trees are inherently recursive data structures. The DFS approach perfectly mirrors the definition of tree equivalence. It is extremely easy to explain, implement without bugs, and read. While BFS is safer for artificially deep trees, standard interview constraints (and most real-world binary trees) rarely hit Java's default recursion limit (usually around 10,000 frames). I'll proceed with recursion but acknowledge the BFS alternative.

### 6. Write the implementation outline

```java
boolean isSameTree(TreeNode p, TreeNode q) {
    /*
     * Reframe:
     * Check if the current nodes match in existence and value, then recursively 
     * enforce the same rule on their children.
     *
     * State:
     * The call stack tracks our current position in both trees simultaneously.
     * Chosen because tree equivalence is a naturally recursive property.
     *
     * Invariant:
     * If the function hasn't returned false, all ancestor nodes of the current
     * nodes were perfectly identical.
     *
     * Core logic:
     * - if both nodes are null, this branch matches (return true)
     * - if only one node is null, structure is different (return false)
     * - if values differ, content is different (return false)
     * - recursively check if left children match AND right children match
     *
     * Edge cases:
     * - Both trees are entirely empty (handled by base case).
     * - Trees are different sizes (handled by the one-null check).
     */
}

```

### 7. Implement iteratively

**Iteration 1: Method skeleton**
I'll define the standard `TreeNode` class first, then set up the skeleton of our recursive method.

```java
class TreeNode {
    int val;
    TreeNode left;
    TreeNode right;
    TreeNode(int val) { this.val = val; }
}

class Solution {
    public boolean isSameTree(TreeNode p, TreeNode q) {
        // TODO: Handle base cases (null checks)
        
        // TODO: Compare current node values
        
        // TODO: Recursively check left and right subtrees
        return false; 
    }
}

```

**Iteration 2: Adding base cases**
The most critical part of tree recursion is handling null references safely before attempting to read node values.

```java
class Solution {
    public boolean isSameTree(TreeNode p, TreeNode q) {
        // Added: If both nodes are null, we've reached the end of identical branches.
        if (p == null && q == null) {
            return true;
        }
        
        // Added: If exactly one is null, the structures don't match.
        if (p == null || q == null) {
            return false;
        }
        
        // TODO: Compare current node values
        
        // TODO: Recursively check left and right subtrees
        return false; 
    }
}

```

*Note: The `p == null || q == null` check is only reached if they aren't BOTH null (thanks to the first `if`). This elegantly ensures we only return false when one is null and the other is not.*

**Iteration 3: Complete the happy path**
Now that we know both `p` and `q` are non-null, we can safely compare their values and recurse.

```java
class Solution {
    public boolean isSameTree(TreeNode p, TreeNode q) {
        if (p == null && q == null) {
            return true;
        }
        if (p == null || q == null) {
            return false;
        }
        
        // Added: Verify the values match.
        if (p.val != q.val) {
            return false;
        }
        
        // Added: Both children must be identical for the trees to be identical.
        return isSameTree(p.left, q.left) && isSameTree(p.right, q.right);
    }
}

```

**Edge-case pass**
Let's review the edge cases:

* *Empty trees (`p = null, q = null`)*: The first `if` catches this and returns `true`. Correct.
* *Differing sizes*: If `p` has a left child but `q` doesn't, `isSameTree(p.left, q.left)` is called. Inside that call, `p` is not null, but `q` is null. The second `if` catches this and returns `false`. Correct.
* *Negative values*: Standard `!=` operator handles negative numbers perfectly. Correct.

No code patches are needed. The logic naturally covers all edge cases.

### 8. Analyze expensive sections and optimize

**Final Code**

```java
/**
 * Definition for a binary tree node.
 */
class TreeNode {
    int val;
    TreeNode left;
    TreeNode right;
    
    TreeNode() {}
    TreeNode(int val) { this.val = val; }
    TreeNode(int val, TreeNode left, TreeNode right) {
        this.val = val;
        this.left = left;
        this.right = right;
    }
}

class Solution {
    public boolean isSameTree(TreeNode p, TreeNode q) {
        // Base case: both nodes are null, meaning structurally identical up to leaf
        if (p == null && q == null) {
            return true;
        }
        
        // Base case: one node is null and the other isn't, so structures differ
        if (p == null || q == null) {
            return false;
        }
        
        // Base case: values don't match
        if (p.val != q.val) {
            return false;
        }
        
        // Recursive step: left subtrees must match AND right subtrees must match
        return isSameTree(p.left, q.left) && isSameTree(p.right, q.right);
    }
}

```

**Complexity**

* **Time Complexity**: O(n), where n is the minimum number of nodes in the two trees. We do exactly O(1) work per node pair visited. We stop early if a mismatch is found, meaning we at most visit the nodes present in the smaller tree (or all nodes if they are identical).
* **Space Complexity**: O(h), where h is the height of the tree, representing the memory used by the recursion stack.
* Best case (balanced tree): O(log n).
* Worst case (skewed tree, like a linked list): O(n).



**Test Walkthrough**
Let's run a quick mental test on our initial example:

* **P:** 1 -> left: 2 -> left: 4
* **Q:** 1 -> left: 2 -> right: 4

1. `isSameTree(1, 1)`: Both non-null. `1 == 1`. Calls `isSameTree(p.left, q.left)` and `isSameTree(p.right, q.right)`.
2. *Left branch evaluate*: `isSameTree(2, 2)`. Both non-null. `2 == 2`. Calls left and right.
3. *Left-left branch evaluate*: `isSameTree(4, null)`. First check fails (`4!=null`). Second check triggers (`q==null`). Returns `false`.
4. The `&&` in `isSameTree(2, 2)` short-circuits. Returns `false`.
5. The `&&` in `isSameTree(1, 1)` short-circuits. Returns `false`.

The test returns the expected result, efficiently stopping execution the moment a structural mismatch is detected.