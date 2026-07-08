### question
Given the root of a non-empty binary tree, return the maximum path sum of any non-empty path.

A path in a binary tree is a sequence of nodes where each pair of adjacent nodes has an edge connecting them. A node can not appear in the sequence more than once. The path does not necessarily need to include the root.

The path sum of a path is the sum of the node's values in the path.

### 1. Restate

Find sequence of connected nodes with highest total sum. Path can start and end anywhere in the tree. Sequence cannot branch (no repeats). Does not have to pass through root.

### 2. Clarify

* **Input:** Root of binary tree.
* **Output:** Integer (max path sum).
* **Nodes negative?** Yes. Crucial because adding a negative branch reduces sum.
* **Single node path valid?** Yes.
* **Empty tree?** Prompt says non-empty.

### 3. Hand Trace

Input Tree:

```text
      -10
      /  \
     9   20
        /  \
       15   7

```

Bottom-up process:

* Leaf `15`: Path through it is `15`. Returns `15` to parent.
* Leaf `7`: Path through it is `7`. Returns `7` to parent.
* Node `20`: Path peaking here = `15 + 20 + 7 = 42`. Best branch upward = `20 + max(15, 7) = 35`.
* Leaf `9`: Path through it is `9`. Returns `9` to parent.
* Node `-10`: Path peaking here = `9 + (-10) + 35 = 34`.
* Max seen across all steps = `42`.

### 4. Brainstorm

* **Approach A (Top-down / Brute Force):** Treat every node as the "peak" of a path. Write a helper to find max depth sum left and right.
* *Complexity:* O(N^2) time, O(N) space. Re-calculating branches redundantly.


* **Approach B (Bottom-up DFS):** Exactly like hand trace. Do post-order traversal. At each node, compute the max path *peaking* there (to update a global max) AND return the max single *branch* extending downward (to feed to its parent).
* *Complexity:* O(N) time, O(H) space.



### 5. Suggest

Go with **Approach B**. It directly maps to how a human traces the problem from the bottom up. One pass, clean, and avoids redundant calculations.

### 6. Outline

```python
def maxPathSum(root): 
    """
    Reframe: Every path has exactly one "highest" node (peak); max sum is peak + max left branch + max right branch.
    State: global_max tracking highest peak sum seen so far, chosen because the optimal path can peak anywhere in the tree.
    Invariant: Post-order traversal ensures left and right branches are fully solved before evaluating the parent peak.

    get_max_branch(node) = returns max sum of a downward path starting from node.

    Core logic:
    - traverse to bottom of left subtree to get left branch sum
    - traverse to bottom of right subtree to get right branch sum
    - calculate path sum peaking at current node (left + right + node)
    - update global_max if this local peak is higher
    - return max single branch (node + max(left, right)) upward to parent
    
    Edge cases:
    - null nodes
    - negative branch sums hurting the total
    - tree with only negative numbers
    """
    pass

```

### 7. Iterative Implementation

**Iteration 1: Skeleton and State**
Setup outer structure and dummy helper to hold the state.

```python
class Solution:
    def maxPathSum(self, root: TreeNode) -> int:
        self.global_max = float('-inf') # State
        
        def get_max_branch(node):
            # TODO: core logic
            pass
            
        get_max_branch(root)
        return self.global_max

```

**Iteration 2: Fleshing out Core Logic (Happy Path)**
Assuming all positive numbers and valid nodes. Read directly from the English outline.

```python
class Solution:
    def maxPathSum(self, root: TreeNode) -> int:
        self.global_max = float('-inf')
        
        def get_max_branch(node):
            # left branch sum
            left_sum = get_max_branch(node.left)
            # right branch sum
            right_sum = get_max_branch(node.right)
            
            # calculate path sum peaking at current node
            local_peak_sum = left_sum + right_sum + node.val
            # update global max
            self.global_max = max(self.global_max, local_peak_sum)
            
            # return max single branch upward to parent
            return node.val + max(left_sum, right_sum)
            
        get_max_branch(root)
        return self.global_max

```

**Iteration 3: Patching Edge Cases**
*Edge Case 1: Null nodes.* Code breaks if `node.left` is null.
*Fix:* Add base case for null nodes returning 0.
*Edge Case 2 & 3: Negative branch sums / All negative trees.* If a branch sum is negative, it hurts the path. We should ignore it (treat it as 0).
*Fix:* Cap `left_sum` and `right_sum` at `0`.

```python
class Solution:
    def maxPathSum(self, root: TreeNode) -> int:
        self.global_max = float('-inf')
        
        def get_max_branch(node):
            if not node: # Patch: Null nodes return 0
                return 0
            
            # Patch: Ignore negative branches by taking max(0, sum)
            left_sum = max(0, get_max_branch(node.left))
            right_sum = max(0, get_max_branch(node.right))
            
            local_peak_sum = left_sum + right_sum + node.val
            self.global_max = max(self.global_max, local_peak_sum)
            
            return node.val + max(left_sum, right_sum)
            
        get_max_branch(root)
        return int(self.global_max)

```

*(If the tree is all negatives, capping branches at 0 works perfectly: `left_sum` and `right_sum` become 0, `local_peak_sum` becomes just `node.val`. `global_max` accurately records the least negative node.)*

### 8. Complexity & Optimization

* **Time Complexity:** O(N). We visit each node exactly once during the DFS traversal. No redundant work.
* **Space Complexity:** O(H) where H is tree height. Space is consumed by the recursion stack. In worst case (skewed tree), O(N). In balanced tree, O(log N).
* **Optimization:** This is already optimal. Doing it in a single pass with constant extra operations per node is as fast as it gets for tree traversal. Keeping state in a class variable (`self.global_max`) or a mutable array `[float('-inf')]` avoids passing state down the call stack, keeping code clean.