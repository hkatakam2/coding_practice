### 1. Restate the problem

We need to traverse a binary tree and group the values of its nodes based on their depth.
Given the root of the tree, we must return a list of lists. The first inner list contains the root's value. The second inner list contains the values of the root's children from left to right. The third contains the values of their children from left to right, and so on, until we reach the bottom of the tree.

### 2. Ask clarifying questions

* **Can the input tree be empty (null root)?**
* *Assumption:* Yes. If the root is null, we should return an empty list of lists.


* **How large can the tree be?**
* *Assumption:* The tree might contain up to a few thousand nodes, so an $O(N)$ time complexity solution is ideal, and we should avoid blowing up the call stack if possible.


* **What is the required return type?**
* *Assumption:* We should return a `List<List<Integer>>`.


* **Do we need to modify the input tree?**
* *Assumption:* No, the tree is read-only.



### 3. Work through an example by hand

Let's take a representative binary tree:

```text
        3
       / \
      9  20
        /  \
       15   7

```

* **Step 1:** Start at the root level. Node is `3`.
* Result so far: `[[3]]`
* Next level nodes to visit: `9`, `20`


* **Step 2:** Process the next level. Nodes are `9` and `20`.
* Read their values: `9`, `20`
* Result so far: `[[3], [9, 20]]`
* Next level nodes to visit: `9` has no children. `20` has `15` and `7`.


* **Step 3:** Process the next level. Nodes are `15` and `7`.
* Read their values: `15`, `7`
* Result so far: `[[3], [9, 20], [15, 7]]`
* Next level nodes to visit: None, both are leaves.


* **Final Result:** `[[3], [9, 20], [15, 7]]`

### 4. Brainstorm solutions aloud

**Approach 1: Breadth-First Search (BFS) using a Queue**

* **Core idea:** We can use a standard BFS traversal. To group the nodes by level, we can check the size of the queue before we start popping nodes for that level. If the queue has 2 elements, we know exactly 2 elements belong to the current level. We pop those 2, record their values, and push their children back into the queue for the next level.
* **Data structures:** `ArrayDeque` for the queue (FIFO behavior), `ArrayList` for the results.
* **Time complexity:** $O(N)$ because we visit each node exactly once.
* **Space complexity:** $O(W)$ where $W$ is the maximum width of the tree. In a perfectly balanced binary tree, the leaf level contains $N/2$ nodes, so the space complexity is $O(N)$.

**Approach 2: Depth-First Search (DFS) with level tracking**

* **Core idea:** We traverse the tree using recursion (DFS). We pass the current depth as an argument to the recursive function. If our result list doesn't have a sublist for the current depth, we create one. Then we append the node's value to the sublist corresponding to its depth. We visit the left child, then the right child, ensuring the left-to-right order is preserved.
* **Data structures:** Call stack for recursion, `ArrayList` for the results.
* **Time complexity:** $O(N)$ because we visit each node exactly once.
* **Space complexity:** $O(H)$ where $H$ is the height of the tree (for the recursion stack). In the worst case (skewed tree), this is $O(N)$.

### 5. Select the solution

I will use **Approach 1 (BFS with a Queue)**.
While DFS is elegant, BFS is the most literal and natural fit for "level order" traversal. It explicitly processes the tree horizontally. Tracking the size of the queue at the start of each iteration is a standard, robust idiom for grouping BFS results by distance/level. `ArrayDeque` is the perfect data structure here because it provides efficient $O(1)$ operations at both ends.

### 6. Write the implementation outline

```java
List<List<Integer>> levelOrder(TreeNode root) {
    /*
     * Reframe:
     * Traverse the tree horizontally, grouping node values by their depth.
     *
     * State:
     * Queue containing nodes to visit.
     * List of Lists to store the final grouped values.
     * Chosen because: Queue enforces First-In-First-Out, meaning nodes at depth D 
     * are always processed before nodes at depth D+1.
     *
     * Invariant:
     * At the beginning of the outer loop, the queue contains exactly all the nodes 
     * for the current level, and nothing else.
     *
     * Core logic:
     * - handle empty tree immediately
     * - initialize result list and queue
     * - add root to the queue
     * - loop while the queue has nodes
     *   - record the current number of nodes in the queue (this is the level size)
     *   - create a new list for the current level's values
     *   - loop exactly 'level size' times:
     *     - remove a node from the front of the queue
     *     - add its value to the current level list
     *     - add its non-null left and right children to the back of the queue
     *   - add the current level list to the result
     * - return the result
     *
     * Edge cases:
     * - root is null
     */
}

```

### 7. Implement iteratively

#### Iteration 1: Method skeleton

First, let's define the method signature, the main data structures, and the early exit for the null root edge case.

```java
public List<List<Integer>> levelOrder(TreeNode root) {
    List<List<Integer>> result = new ArrayList<>();
    
    // Handle edge case: empty tree
    if (root == null) {
        return result;
    }
    
    Queue<TreeNode> queue = new ArrayDeque<>();
    queue.offer(root);
    
    // TODO: traverse the queue
    
    return result;
}

```

#### Iteration 2: Core queue traversal

Next, I'll add the basic BFS loop. This iteration just pulls nodes from the queue and pushes their children, but doesn't yet group them by level.

```java
public List<List<Integer>> levelOrder(TreeNode root) {
    List<List<Integer>> result = new ArrayList<>();
    
    if (root == null) {
        return result;
    }
    
    Queue<TreeNode> queue = new ArrayDeque<>();
    queue.offer(root);
    
    // Added: Standard BFS loop
    while (!queue.isEmpty()) {
        TreeNode currentNode = queue.poll();
        
        // TODO: group values into a list for the current level
        
        if (currentNode.left != null) {
            queue.offer(currentNode.left);
        }
        if (currentNode.right != null) {
            queue.offer(currentNode.right);
        }
    }
    
    return result;
}

```

#### Iteration 3: Complete the happy path (Level grouping)

Now I will use the "queue size" trick. By capturing the queue's size at the start of the `while` loop iteration, I know exactly how many nodes belong to the current level. I'll add an inner loop to process only those nodes.

```java
public List<List<Integer>> levelOrder(TreeNode root) {
    List<List<Integer>> result = new ArrayList<>();
    
    if (root == null) {
        return result;
    }
    
    Queue<TreeNode> queue = new ArrayDeque<>();
    queue.offer(root);
    
    while (!queue.isEmpty()) {
        // Added: Capture the number of nodes at the current level
        int levelSize = queue.size();
        List<Integer> currentLevelValues = new ArrayList<>();
        
        // Added: Process exactly the nodes that exist at this depth
        for (int i = 0; i < levelSize; i++) {
            TreeNode currentNode = queue.poll();
            currentLevelValues.add(currentNode.val);
            
            if (currentNode.left != null) {
                queue.offer(currentNode.left);
            }
            if (currentNode.right != null) {
                queue.offer(currentNode.right);
            }
        }
        
        // Added: Store the completed level
        result.add(currentLevelValues);
    }
    
    return result;
}

```

#### Edge-case pass

* **Empty input (`root == null`):** Handled at the very beginning. Returns an empty `ArrayList`, which is correct.
* **Tree with only one node:** The queue starts with 1 node. `levelSize` is 1. Inner loop runs once, adds the value to the sublist, pushes no children (both null). Outer loop finishes. Returns `[[val]]`. Correct.
* **Skewed tree (e.g., all left children):** Handled correctly. `levelSize` will just be `1` for every level, returning `[[1], [2], [3]]` etc.
* **Mutation:** The tree nodes are strictly read, not mutated.

### 8. Analyze expensive sections and optimize

**Time Complexity:** $O(N)$
We process each node in the tree exactly once when we poll it from the queue. Adding to an `ArrayList` and polling/offering to an `ArrayDeque` are $O(1)$ operations. The total time is strictly proportional to the number of nodes.

**Space Complexity:** $O(N)$
In the worst-case scenario (a perfect binary tree), the queue will hold all the nodes of the lowest level at once. The lowest level of a perfect binary tree contains $N/2$ nodes. Thus, the maximum size of the queue scales linearly with $N$, giving an $O(N)$ space complexity.

No further optimizations are needed as this approaches the theoretical lower bounds for traversing all nodes (Time $O(N)$) and keeping a BFS frontier (Space $O(N)$).

### Final Code

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
    public List<List<Integer>> levelOrder(TreeNode root) {
        List<List<Integer>> result = new ArrayList<>();
        
        if (root == null) {
            return result;
        }
        
        Deque<TreeNode> queue = new ArrayDeque<>();
        queue.offer(root);
        
        while (!queue.isEmpty()) {
            int levelSize = queue.size();
            List<Integer> currentLevelValues = new ArrayList<>(levelSize);
            
            for (int i = 0; i < levelSize; i++) {
                TreeNode currentNode = queue.poll();
                currentLevelValues.add(currentNode.val);
                
                if (currentNode.left != null) {
                    queue.offer(currentNode.left);
                }
                if (currentNode.right != null) {
                    queue.offer(currentNode.right);
                }
            }
            
            result.add(currentLevelValues);
        }
        
        return result;
    }
}

```

*(Note: I added an initial capacity `new ArrayList<>(levelSize)` to the inner list in the final clean code to prevent unnecessary resizing of the underlying array during the inner loop, acting as a minor memory optimization).*

### Brief test walkthrough

Let's test with the smallest valid input: a tree with just a `root` of value `1`.

1. `root == null` is false.
2. `queue.offer(root)` puts `1` in the queue.
3. Outer loop starts. `queue.isEmpty()` is false.
4. `levelSize = 1`.
5. Inner loop runs from `i = 0` to `0`.
6. `currentNode` becomes node `1`. `currentLevelValues` gets `1`.
7. Node `1` has no children, so nothing is added to the queue.
8. `currentLevelValues` `[1]` is added to `result`.
9. Queue is now empty. Outer loop terminates.
10. Returns `[[1]]`. Expected result achieved.