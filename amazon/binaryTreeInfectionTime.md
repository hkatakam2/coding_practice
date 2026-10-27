# question
Amount of Time for Binary Tree to Be Infected (LeetCode 2385): Frequently asked with a twist: extend it to an N-ary Tree or also return the exact infection path

# clarifications
1. does infection spread in both direction? yes
2. start node always exists, tree could be empty?
3. start is infected at minute 0
4. infection path? from start to the last node infected or the full order of infection [waves per minute and start to last node]
5. for N-ary how are children stored?  a list

# ideas
1. convert tree to an undirected graph, the BFS. O(n) time O(n) space
2. parent map plus BFS. same idea without building the whole adjacency map. A node's neghbors are its children and parent

# outline
infect(root, start):
    index_tree(root) # parent map, plus find start node
    neighbors(node) # kids(node) + parent(node)
    waves, infected_by = spread(start_node, neighbors) # BFS, one wave per minte
    minutes = waves - 1
    path = trace_back(infected_by, from=any node in last wave)
    return minutes, path, waves

kids(node): children of a node. It is the only line that changes for N-ary.
index_tree: one traversal that records each node’s parent and finds the start node.
spread: BFS where each wave is one minute, and infected_by[x] doubles as the visited set.
trace_back: follow infected_by from a last-infected node to the start, then reverse.

```python
from typing import Optional, List, Tuple


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right


# kids(node): children of a node.
# N-ary twist: replace the body with `return node.children`. Nothing else changes.
def kids(node) -> list:
    return [c for c in (node.left, node.right) if c]


def infect(root: Optional[TreeNode], start: int) -> Tuple[int, List[int], List[List[int]]]:
    """Returns (minutes, path from start to a last-infected node, values infected per minute)."""

    # EDGE: empty tree, so there is nothing to infect.
    if root is None:
        raise ValueError("empty tree")

    # index_tree(root) -> parent map, plus the start node
    parent = {root: None}
    start_node = None
    stack = [root]                       # EDGE: iterative, so a 10^5-deep skewed tree
    while stack:                         #       can't hit the recursion limit
        node = stack.pop()
        if node.val == start:
            start_node = node
        for child in kids(node):
            parent[child] = node
            stack.append(child)

    # EDGE: start value not present in the tree
    if start_node is None:
        raise ValueError(f"start value {start} not in tree")

    # neighbors(node) = kids(node) + [parent(node)]
    def neighbors(node):
        result = list(kids(node))        # EDGE: copy, so for N-ary we never append
        if parent[node] is not None:     #       onto the node's real children list
            result.append(parent[node])  # EDGE: the root has no parent
        return result

    # waves, infected_by = spread(start_node, neighbors)   (BFS, one wave per minute)
    infected_by = {start_node: None}     # doubles as the visited set, so no node is
    wave = [start_node]                  # re-infected (the parent link would loop back)
    waves = [wave]
    while True:
        next_wave = []
        for node in wave:
            for nxt in neighbors(node):
                if nxt not in infected_by:
                    infected_by[nxt] = node
                    next_wave.append(nxt)
        if not next_wave:                # EDGE: single-node tree, or the last wave
            break                        #       reached, so stop (answer stays 0 for one node)
        waves.append(next_wave)
        wave = next_wave

    # minutes = number_of_waves - 1
    minutes = len(waves) - 1             # minute 0 is just the start node

    # path = trace_back(infected_by, from=any node in last wave)
    path, cur = [], waves[-1][0]         # EDGE: ties for farthest node, any one is valid
    while cur is not None:
        path.append(cur.val)
        cur = infected_by[cur]
    path.reverse()                       # now it reads start -> last infected

    # return minutes, path, waves
    return minutes, path, [[n.val for n in w] for w in waves]


# The original LeetCode signature is just a thin wrapper.
def amountOfTime(root: Optional[TreeNode], start: int) -> int:
    return infect(root, start)[0]
```
