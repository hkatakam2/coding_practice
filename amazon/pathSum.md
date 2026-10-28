# question
Binary Tree Maximum Path Sum (LeetCode 124) & Path Sum III: With negative node values; recent interviewers ask a follow-up to print the actual nodes in the maximum path rather than just returning the integer sum.

# clarify
1. what is a path?
2. can the values be negative? yes
3. what if every node is -ve? answer is not 0, it is the largest single node
4. if multiple path tie? anyone is ok
5. in what order should we print nodes? from one end to the other, the order we would walk


# ideas
1. brute force: try every pair of end points; exponential
2. every path has exactly one highest node, it's peak. 
   1. best_path is peak.val + best downward arm of left + best downward arm on right
   2. and an arm can be skipped if it is negative
3. define gain(node) as the best sum of a downward path starting at node
   1. gain(node) = ndoe.val + max(0, gain(node.left), gain(node.right))
   2. at every node we need two things;
      1. record a path at the node: val + L + R
      2. return only one arm: val + max(L, R). as a parent can't extend a forked path 

Follow-up (print the nodes).

Option A: return (sum, list) from every call. Copying lists costs O(n²) on a skewed tree.
Option B: remember the peak of the best path and each node’s gain. Afterward, rebuild the path by walking down from the peak, always stepping to the child with the larger positive gain. That’s O(n) with no copying.

# outline
solve(root):
    post-order: compute gain(node) for every node
        gain(node) = node.val + best_arm(left or right, whichever is larger)
        also: treat node as PEAK -> candidate = node.val + arm(left) + arm(right)
        remember the peak with the highest candidate
    path = reverse(arm_nodes(peak.left)) + [peak] + arm_nodes(peak.right)
    return best_sum, path

best_arm(child)   = max(0, gain(child))        # 0 means "don't extend"
arm_nodes(start)  = follow the better child while gain is positive

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right


def max_path_sum(root):
    best_sum, best_peak = float("-inf"), None
    gain = {}  # node -> best downward sum starting at that node

    # post-order: compute gain(node) for every node
    def compute_gain(node):
        nonlocal best_sum, best_peak
        if not node:
            return 0
        # best_arm(child) = max(0, gain(child))
        l = max(0, compute_gain(node.left))
        r = max(0, compute_gain(node.right))

        # treat node as PEAK -> candidate = node.val + arm(left) + arm(right)
        candidate = node.val + l + r
        # remember the peak with the highest candidate
        if candidate > best_sum:
            best_sum, best_peak = candidate, node

        # gain(node) = node.val + better single arm   (only ONE arm goes up)
        gain[node] = node.val + max(l, r)
        return gain[node]

    compute_gain(root)

    def g(n):
        return gain[n] if n else 0

    # arm_nodes(start) = follow the better child while gain is positive
    def arm_nodes(start):
        nodes, node = [], start
        while node and gain[node] > 0:
            nodes.append(node)
            node = node.left if g(node.left) >= g(node.right) else node.right
        return nodes

    # path = reverse(arm_nodes(peak.left)) + [peak] + arm_nodes(peak.right)
    path = arm_nodes(best_peak.left)[::-1] + [best_peak] + arm_nodes(best_peak.right)
    return best_sum, path
```



```python
3 ideas
1. down(node) -> best stright down path starting at the node
2. bend -> best path that turns at this node val + left + right
3. best -> biggest been seen 

def max_path_sum(root):
    best = float("-inf")
    def down(node): # best stright path goind down from node
        nonlocal best
        if not node: return 0
        l = max(0, down(node.left)) # negative arm, leave it 0
        r = max(0, down(node.right))
        best = max(best, node.val + l + r) # RECORD: bend here both arms
        return node.val + max(l, r) # RETURN: stright one arm only
    down(root)
    return best

printing needs 2 more things:
# where the best bend was, which way each node's stright down trail continues
def max_path_nodes(root):
    best, bend = float("-inf"), None
    nxt = {}
    def down(node):
        nonlocal best, bend
        if not node: return 0
        l = max(0, down(node.left))
        r = max(0, down(node.right))
        if node.val + l + r > best:
            best = node.val + l + r
            bend = node
            nxt[node] = node.left if l > r else node.right
        return node.val + max(l, r)
    down(root)

    def trail(node):
        pass

    return best, trail(bend.left)[::-1] + [bend] + trail(bend.right)

```

