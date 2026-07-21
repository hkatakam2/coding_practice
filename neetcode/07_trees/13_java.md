### 1. Restate the problem

We are given two arrays of integers, `preorder` and `inorder`, which represent two different depth-first traversals of the exact same binary tree.

* **Preorder** visits nodes in the order: Root -> Left Subtree -> Right Subtree.
* **Inorder** visits nodes in the order: Left Subtree -> Root -> Right Subtree.

Our task is to reconstruct the original binary tree using these two arrays and return the root node. All values in the tree are guaranteed to be unique.

### 2. Ask clarifying questions

Before writing any code, I would clarify a few details with the interviewer:

* **Input size:** How large can the tree be? (Assuming up to a few thousand nodes, meaning O(N²) might be too slow and recursion depth could be an issue if the tree is highly skewed).
* **Null or empty input:** Can the arrays be empty or null? (Assuming they can be empty; if so, we should return `null`).
* **Input consistency:** Are `preorder` and `inorder` always guaranteed to be the same length and valid representations of a single tree? (Assuming yes).
* **Values:** Can node values be negative? (Assuming yes, which is fine since we are just moving values into node objects).
* **Return type:** I assume we are using standard LeetCode-style `TreeNode` classes.

*Assumption for this interview:* The inputs are perfectly valid, sizes match, arrays can be empty, and we return standard `TreeNode` objects.

### 3. Work through an example by hand

Let's take a representative example:
`preorder = [3, 9, 20, 15, 7]`
`inorder  = [9, 3, 15, 20, 7]`

1. **Identify the root:** The first element in `preorder` is always the root of the current tree. Here, the root is `3`.
2. **Split the subtrees:** Find `3` in `inorder`. It's at index 1.
* Everything to the left of `3` in `inorder` (`[9]`) is the left subtree.
* Everything to the right of `3` in `inorder` (`[15, 20, 7]`) is the right subtree.


3. **Process left subtree:**
* The left subtree has 1 element.
* Next element in `preorder` is `9`.
* In `inorder`, the left side is `[9]`. Root is `9`. No elements left or right of it, so it's a leaf.


4. **Process right subtree:**
* The right subtree has 3 elements.
* The remaining `preorder` elements for this subtree are `[20, 15, 7]`. Root is `20`.
* In `inorder`, `[15, 20, 7]`. `20` is at the middle.
* Left of `20` in inorder is `[15]` (Left child).
* Right of `20` in inorder is `[7]` (Right child).


5. **Final tree structure:**
```text
    3
   / \
  9  20
    /  \
   15   7

```



### 4. Brainstorm solutions aloud

**Approach 1: Direct Simulation with Array Copying**

* **Core idea:** Exactly follow the manual process. Pick the first element of `preorder`, find it in `inorder` using a loop, slice both arrays using `Arrays.copyOfRange` to create left and right subarrays, and recurse.
* **Complexity:** Searching for the root takes O(N) time. Array copying takes O(N) time. Doing this recursively takes O(N²) time in the worst case (a skewed tree). Space complexity is also O(N²) due to creating many subarrays.
* **Critique:** This works but is very inefficient due to constant array creation and linear searching.

**Approach 2: Two Pointers with HashMap**

* **Core idea:** Instead of array slicing, pass the start and end boundary indices for both `preorder` and `inorder` arrays into our recursive function. To avoid the O(N) linear scan to find the root in `inorder`, we can precompute the value-to-index mappings of `inorder` using a `HashMap`.
* **Complexity:** Creating the HashMap takes O(N) time and O(N) space. Each recursive call does O(1) work (map lookup, index math). Total Time: O(N). Total Space: O(N) for the map and recursion stack.
* **Critique:** This is optimal. It maps perfectly to the problem constraints since we know tree values are unique.

### 5. Select the solution

I will use the **Two Pointers with HashMap** approach.

* **Correct:** It leverages the mathematical properties of tree traversals perfectly.
* **Efficient:** O(N) time and space are optimal because we must process every node.
* **Data Structure:** `HashMap` is chosen because fast O(1) lookups completely eliminate the O(N) linear search bottleneck.

### 6. Write the implementation outline

```java
TreeNode buildTree(int[] preorder, int[] inorder) {
    /*
     * Reframe:
     * We need to recursively partition the inorder array into left and right subtrees 
     * using the root node identified from the preorder array.
     *
     * State:
     * HashMap<Integer, Integer> inorderIndexMap: Maps node values to their index in the inorder array.
     * Chosen because: Fast lookups are needed to find the root's position and determine subtree sizes.
     *
     * Invariant:
     * The `preStart` points to the current root, and the `inStart` to `inEnd` bounds strictly 
     * confine the elements belonging to the current subtree.
     *
     * Helpers:
     * buildTreeHelper(preorder, preStart, inorder, inStart, inEnd, inorderIndexMap)
     * - Recursively builds the tree for a given boundary window.
     *
     * Core logic:
     * - build the inorder value-to-index map.
     * - call the recursive helper with full array bounds.
     * - inside helper: base case if left bound exceeds right bound.
     * - create the root node from preorder[preStart].
     * - find the root's index in inorder using the map.
     * - calculate the size of the left subtree.
     * - recursively build the left child using appropriately shifted bounds.
     * - recursively build the right child using appropriately shifted bounds.
     * - return the root node.
     *
     * Edge cases:
     * - empty input arrays
     * - single node tree
     */
}

```

### 7. Implement iteratively

**Iteration 1: Method skeleton and Map setup**
First, I will build the outer method, initialize the HashMap, and define the helper signature.

```java
public TreeNode buildTree(int[] preorder, int[] inorder) {
    // Edge case: null or empty arrays
    if (preorder == null || preorder.length == 0 || inorder == null || inorder.length == 0) {
        return null;
    }

    Map<Integer, Integer> inorderIndexMap = new HashMap<>();
    for (int i = 0; i < inorder.length; i++) {
        inorderIndexMap.put(inorder[i], i);
    }

    // TODO: delegate to recursive helper
    return null;
}

private TreeNode buildTreeHelper(
        int[] preorder, int preStart,
        int[] inorder, int inStart, int inEnd,
        Map<Integer, Integer> inorderIndexMap) {
    
    // TODO: handle base case
    // TODO: construct root node
    // TODO: recursive calls for left and right children
    
    return null;
}

```

**Iteration 2: The recursive helper (Base case and Root creation)**
Next, I'll add the base case that stops recursion and extract the root value to create the current node.

```java
private TreeNode buildTreeHelper(
        int[] preorder, int preStart,
        int[] inorder, int inStart, int inEnd,
        Map<Integer, Integer> inorderIndexMap) {
    
    // Base case: If there are no elements to construct the tree from
    if (inStart > inEnd) {
        return null;
    }

    // The first element in the current preorder window is the root
    int rootValue = preorder[preStart];
    TreeNode root = new TreeNode(rootValue);

    // TODO: recursively build left child
    // TODO: recursively build right child

    return root;
}

```

**Iteration 3: The recursive helper (Boundary calculation and Recursive steps)**
Now, I will implement the pointer math. The key insight is that the number of elements in the left subtree tells us exactly where the right subtree begins in the `preorder` array.

```java
private TreeNode buildTreeHelper(
        int[] preorder, int preStart,
        int[] inorder, int inStart, int inEnd,
        Map<Integer, Integer> inorderIndexMap) {
    
    if (inStart > inEnd) {
        return null;
    }

    int rootValue = preorder[preStart];
    TreeNode root = new TreeNode(rootValue);

    // Find the position of the root in the inorder array
    int rootIndexInorder = inorderIndexMap.get(rootValue);
    
    // Calculate how many nodes are in the left subtree
    int leftSubtreeSize = rootIndexInorder - inStart;

    // Recursively build the left subtree.
    // The left child's root is immediately after the current root in preorder (preStart + 1).
    // Its inorder bounds are everything left of rootIndexInorder.
    root.left = buildTreeHelper(
        preorder, preStart + 1,
        inorder, inStart, rootIndexInorder - 1,
        inorderIndexMap
    );

    // Recursively build the right subtree.
    // The right child's root is in preorder exactly after all nodes of the left subtree.
    // Its inorder bounds are everything right of rootIndexInorder.
    root.right = buildTreeHelper(
        preorder, preStart + leftSubtreeSize + 1,
        inorder, rootIndexInorder + 1, inEnd,
        inorderIndexMap
    );

    return root;
}

```

**Edge-case pass**

* *Empty arrays:* Handled correctly in the main method with the `preorder == null || preorder.length == 0` check.
* *Single element:* `preStart` is 0, `inStart` is 0, `inEnd` is 0. `leftSubtreeSize` becomes 0. `root.left` gets `inStart > inEnd` (0 > -1) and returns null. `root.right` gets `inStart > inEnd` (1 > 0) and returns null. It correctly returns the single node.
* *Skewed tree:* The index boundaries tighten exactly by 1 each time, causing normal recursion ending accurately without out-of-bounds errors. Memory stack will hit O(N) depth, which is expected and unavoidable for standard recursion.

### Final Code

Here is the clean, final version of the solution.

```java
import java.util.HashMap;
import java.util.Map;

// Standard definition for a binary tree node.
class TreeNode {
    int val;
    TreeNode left;
    TreeNode right;
    TreeNode(int val) { this.val = val; }
}

public class Solution {

    public TreeNode buildTree(int[] preorder, int[] inorder) {
        if (preorder == null || inorder == null || preorder.length == 0) {
            return null;
        }

        // Cache the indices of the inorder array elements for O(1) lookups
        Map<Integer, Integer> inorderIndexMap = new HashMap<>();
        for (int i = 0; i < inorder.length; i++) {
            inorderIndexMap.put(inorder[i], i);
        }

        return buildTreeHelper(
            preorder, 0, 
            inorder, 0, inorder.length - 1, 
            inorderIndexMap
        );
    }

    private TreeNode buildTreeHelper(
            int[] preorder, int preStart,
            int[] inorder, int inStart, int inEnd,
            Map<Integer, Integer> inorderIndexMap) {
        
        // Base case: window is empty
        if (inStart > inEnd) {
            return null;
        }

        // The current root is always at preStart
        int rootValue = preorder[preStart];
        TreeNode root = new TreeNode(rootValue);

        // Find the root in inorder to split left and right subtrees
        int rootIndexInorder = inorderIndexMap.get(rootValue);
        
        // Determine the number of elements in the left subtree
        int leftSubtreeSize = rootIndexInorder - inStart;

        // Build left and right branches using mathematically shifted pointers
        root.left = buildTreeHelper(
            preorder, preStart + 1,
            inorder, inStart, rootIndexInorder - 1,
            inorderIndexMap
        );
        
        root.right = buildTreeHelper(
            preorder, preStart + leftSubtreeSize + 1,
            inorder, rootIndexInorder + 1, inEnd,
            inorderIndexMap
        );

        return root;
    }
}

```

### Complexity

* **Time Complexity:** O(N), where N is the number of nodes in the tree. We iterate through the `inorder` array once to populate the HashMap, which takes O(N) time. The `buildTreeHelper` function is called exactly once per node, and each call performs O(1) work (map lookups and basic arithmetic).
* **Space Complexity:** O(N). The `HashMap` stores exactly N key-value pairs. The recursion stack uses O(H) space, where H is the height of the tree. In the worst case (a heavily skewed tree), H = N. Therefore, total space complexity is bounded by O(N).

### Brief test walkthrough

Let's trace the smallest valid input: `preorder = [1]`, `inorder = [1]`.

* `HashMap` maps `{1: 0}`.
* Call helper with `preStart = 0`, `inStart = 0`, `inEnd = 0`.
* `inStart <= inEnd` is true. `rootValue` is 1. We create `TreeNode(1)`.
* `rootIndexInorder` = 0.
* `leftSubtreeSize` = 0 - 0 = 0.
* `root.left` is called with `inStart = 0`, `inEnd = -1`. Returns `null`.
* `root.right` is called with `preStart = 1`, `inStart = 1`, `inEnd = 0`. Returns `null`.
* Returns `TreeNode(1)`.

This exactly creates and returns a single node with no children, confirming correct pointer boundaries.