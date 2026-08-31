'''
write a function to find the 2nd largest element in a binary search tree

simplify the question: find the largest 
'''
def find_largest(root_node):
    if root_node.right:
        return find_largest(root_node.right)
    return root_node.value
'''
use this to find the bigger problem
'''
def find_largest(root_node):
    if root_node is None:
        raise ValueError
    if root_node.right:
        return find_largest(root_node.right)
    return root_node.value

def find_second_largest(root_node):
    if (not root_node) or (not root_node.left and not root_node.right):
        raise ValueError
    
    # case: we're currently at largest, and largest has a left subtree
    # so 2nd largest is largest in said subtree
    if root_node.left and not root_node.right:
        return find_largest(root_node.left)

    # case: we're at parent of largest, and largest has no left subtree
    # so 2nd largest is the current node
    if (root_node.right and not root_node.right.left and not root_node.right.right):
        return root_node.value

    # otherwise: step right
    return find_second_largest(root_node.right)
'''
O(h) time and O(h) space call stack
how can we get this to constant space?
'''
def find_largest(root_node):
    current = root_node
    while current:
        if not current.right:
            return current.value
        current = current.right

def find_second_largest(root_node):
    if (root_node is None or (root_node.left is None and root_node.right is None)):
        raise ValueError
    
    current = root_node
    while current:
        # case: current is largest and has a left subtree
        if current.left and not current.right:
            return find_largest(current.left)
        
        # case: current is parent of largest and largest has no children
        if (current.right and not current.right.left and not current.right.right):
            return current.value
        
        # otherwise, step right
        current = current.right
'''
O(h) time and O(1) space

what we learned:
simplfy and adapt

breaking things down into cases
'''