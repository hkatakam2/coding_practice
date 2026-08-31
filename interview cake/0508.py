'''
write a function to check that a binary tree is a valid binary search tree

breakdown:
One way to break the problem down is to come up with a way to confirm 
that a single node is in a valid place relative to its ancestors. 
Then if every node passes this test, our whole tree is a valid BST.

What makes a given node "correct" relative to its ancestors in a BST? Two things:
• if a node is in the ancestor's left subtree, then it must be less than the ancestor, and
• if a node is in the ancestor's right subtree, then it must be greater than the ancestor.

we don't have to store all the ancestors we can think about bounds

'''
def is_binary_search_tree(root):
    # start at the root, with an arbitrary low lower bound
    # and an arbitrary high upper bound
    node_and_bounds_stack = [(root, -float('inf'), float('inf'))]

    # depth-first traversal
    while len(node_and_bounds_stack):
        node, lower_bound, upper_bound = node_and_bounds_stack.pop()

        # if this node is invalid, we return false right away
        if (node.value <= lower_bound) or (node.value >= upper_bound):
            return False
        
        if node.left:
            # this node must be less than the current node
            node_and_bounds_stack.append((node.left, lower_bound, node.value))
        if node.right:
            # this node must be greater than the current node
            node_and_bounds_stack.append((node.right, node.value, upper_bound))
    
    # if none of the nodes were invalid, return true
    return True
'''
instead of allocating stak ourselves, we could write a recursive function
that uses the call stack. it would work but vulnerable to stack overflow
'''
def is_binary_search_tree(root, lower_bound = -float('inf'), upper_bound = float('inf')):
    if not root:
        return True
    
    if not (lower_bound < root.value < upper_bound):
        return False
    
    return is_binary_search_tree(root.left, lower_bound, root.value) and is_binary_search_tree(root.right, root.value, upper_bound)
'''
checking if an in-order traversal of the tree is sorted is a great answer too,
especially if you are able to implement it without storing a full list of nodes
'''
def is_bst_in_order(root):
    def in_order_check(node):
        nonlocal last_seen_value

        if not node: return True    
        if not in_order_check(node.left): return False
                 
        # Check if this node is smaller than the last seen value
        if node.value < last_seen_value: return False
     
        last_seen_value = node.value
        
        return in_order_check(node.right)
    
    last_seen_value = -float('inf')
    return in_order_check(root)
'''
O(n) time and O(n) space

example: 
    5
   / \
  3   7
 / \
1   4
The in-order traversal would check nodes in this order: 
1 -> 3 -> 4 -> 5 -> 7 Each value must be greater than 
the previous one for the tree to be valid.


Bonus:
what if the input tree has duplicate values? 
our conditons needs to be modified to handle it (choose a rule: duplicates in left or right)


'''
# allow duplicates on the right
def is_binary_search_tree(root):
    node_and_bounds_stack = [(root, -float('inf'), float('inf'))]

    while len(node_and_bounds_stack):
        node, lower_bound, upper_bound = node_and_bounds_stack.pop()

        # Allow duplicates in right subtree
        if not (lower_bound < node.value <= upper_bound):
            return False
        
        if node.left:
            node_and_bounds_stack.append((node.left, lower_bound, node.value))
        if node.right:
            node_and_bounds_stack.append((node.right, node.value, upper_bound))
    
    return True

'''

Bonus:
What if -float ('inf') or float ('inf') appear in the input tree?

what we learned:
we could think of this as a greedy approach. 

we could also think this as a divide and conquer
'''