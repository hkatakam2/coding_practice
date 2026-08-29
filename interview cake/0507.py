'''
write a function to see if a tree is super balanced ( difference between
the depths of any two leaf nodes is no greater than one)

class BinaryTreeNode(object):
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
    def insert_left(self, value):
        self.left = BinaryTreeNode(value)
        return self.left
    def insert_right(self, value):
        self.right = BinaryTreeNode(value)
        return self.right


Breakdown:
simplify the problem: 
"the difference between the depths of any two leaf nodes is no greater 
than 1" implies that we'll have to compare the depths of all possible 
pairs of leaves. That'd be expensive-if there are n leaves, there are 
O(n) possible pairs of leaves.

we can simplify to reduce work:
For example, we could equivalently say:
• "The difference between the min leaf depth and the max leaf depth is 1 or less"
• "There are at most two distinct leaf depths, and they are at most 1 apart"

write iterative approach if you can't think recursive
'''
def is_balanced(tree_root):
    # a tree with no nodes is superbalanced
    if tree_root is None:
        return True
    
    # we short circuit as soon as we find more than 2
    depths = []

    # we'll treat this list as stack that will store tuples of (node, depth)
    nodes  = []
    nodes.append((tree_root, 0))

    while len(nodes):
        # pop a node and its depth from the top of the stack
        node, depth = nodes.pop()

        # case: we found a leaf
        if (not node.left) and (not node.right):
            # we only care if it's a new depth
            if depth not in depths:
                depths.append(depth)

                # two ways we might now have an unbalanced tree
                # 1) more than 2 different leaf depths
                # 2) 2 leaf depths that are more than 1 apart
                if (len(depth) > 2) or (len(depths) == 2 and abs (depths[0]- depths[1]) > 1):
                    return False
        else:
            # case: this isn't a leaf - keep stepping down
            if node.left:
                nodes.append((node.left, depth + 1))
            if node.right:
                nodes.append((node.right, depth + 1))
    return True
'''
O(n) time O(n) space

what we learned?
tip: bfs uses a queue and dfs uses stack (could be a call stack!)
'''