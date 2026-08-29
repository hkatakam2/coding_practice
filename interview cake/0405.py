'''
check if a binary tree is a valid binary search tree

what is a binary search tree?
child in left subtree is smaller than parent; any child in right subtree is larger than parent
we have to check this for each node 

breakdown: insted of storing all the ancestor nodes, we could 
store the lower, upper bounds within which the current node should be

'''

def is_binary_search_tree(root):
    # start at the root with arbitrary upper and lower bounds
    node_and_bounds_stack = [(root, -float('inf'), float('inf'))]

    # depth first traversal
    while len(node_and_bounds_stack):
        node, lower_bound, upper_bound = node_and_bounds_stack.pop()

        # if this node is outof bounds, return false
        if not (lower_bound < node.value < upper_bound):
            return False
        
        if node.left:
            # upper bound for this node changes
            node_and_bounds_stack.append((node.left, lower_bound, node.value))

        if node.right:
            # lower bound for this node changes
            node_and_bounds_stack.append((node.right, node.value, upper_bound))
    # if none of the nodes are outof bounds then return true
    return True

'''
to make the code look cleaner we could use a recursive function 
instead of allocating the stack overselves
this implementation is vulnerable to stack overflow
'''

def is_binary_search_tree_recursive(root, lower_bound = -float('inf'), upper_bound = float('inf')):
    if not root:
        return True
    
    if not (lower_bound < root.value < upper_bound):
        return False
    
    return (is_binary_search_tree_recursive(root.left, lower_bound, root.value) 
            and is_binary_search_tree_recursive(root.right, root.value, upper_bound))

'''
complexity:
O(n) time
the stack stores at most d nodes; d is the depth of the tree;
the worst case O(n) space; in a balanced tree d = log n
'''

'''
what we learned?
greedy approach! we were trying to solve the problem in one walk through the tree
so we asked what values do i need to track to do that; lower and upper bounds

divide and conquer!! this tree is valid bst if the left subtree is valid bst
and right subtree is valid bst; this is apparent in recursive formulation


'''

