'''
super balanced binary tree: the difference between the depths of 
any two leaf nodes is no greater than one
'''
class BinaryTree:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def insert_left(self, value):
        self.left = BinaryTree(value)
        return self.left
    
    def insert_right(self, value):
        self.right = BinaryTree(value)
        return self.right
'''
Breakdown: comparing depths of all possible pairs of leaf nodes is expensive
if there are n nodes in the tree, there are n^2 possible pairs of nodes

simplification: 
1. the difference between the min leaf depth and the max leaf depth is 1 or 0
2. there are at most two distinct leaf depths, and they are at most 1 apart
'''

def is_balanced(tree_root):
    # a tree with no nodes is superbalanced, since there are no leaves
    if tree_root is None:
        return True
    
    # we short-circuit as soon as we find more than 2
    depths = []

    # we'll treat this list as a stack that will store tuples of (node, depth)
    nodes = []
    nodes.append((tree_root, 0))
    
    while len(nodes):
        # pop a node and its depth from the top of our stack
        node, depth = nodes.pop()

        # case: we found a leaf
        if (not node.left) and (not node.right):
            # we only care if it's a new depth
            if depth not in depths:
                depths.append(depth)

            # two ways we might now have an unbalanced tree:
            # 1) more than 2 different leaf depths
            # 2) 2 leaf depths that are more than 1 apart    
            if len(depths) > 2 or (len(depths) == 2 and abs(depths[0] - depths[1]) > 1):
                return False
        else:
            # case: this isn't a leaf - keep stepping down
            if node.left:
                nodes.append((node.left, depth + 1))
            if node.right:
                nodes.append((node.right, depth + 1))
    return True
'''
O(n) time and O(n) space

bfs uses queue
dfs uses stack

'''