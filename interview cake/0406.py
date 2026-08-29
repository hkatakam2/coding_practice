'''
find 2nd largest element in a bst

simplify:
find the largest element in a bst
1. find the right most leaf 

'''
def find_largest(root_node):
    if not root_node:
        return ValueError('Tree must have atleast 1 node')
    if root_node.right:
        return find_largest(root_node.right)

    return root_node.value

'''
what is 2nd largest?
1. if the largest has no children, then its parent
2. if the largest has a left subtree, then largest element in the left subtree

'''
def find_second_largest(root_node):
    # tree must have atleast 2 nodes
    if (not root_node or
            (not root_node.left) and (not root_node.right)):
        return ValueError('Tree must have atleast 2 nodes')

    # case: largest node has a left subtree
    # so 2nd largest is largest in the left subtree
    if root_node.left and not root_node.right:
        return find_largest(root_node.left)
    
    # case: we are at parent of largest, and largest has no children
    # so 2nd largest must be the current node
    if (root_node.right and 
            not root_node.right.left and 
            not root_node.right.right):
        return root_node.value

    # otherwise: step right
    return find_second_largest(root_node.right)
'''
O(h) time; h is the height of the tree
O(h) space; h space is the call stack; avoidable
can you get constant space
'''

def find_largest(root_node):
    current = root_node
    while current:
        if not current.right:
            return current.value
        current = current.right

def find_second_largest(root_node):
    # atleast 2 nodes need to be there

    current = root_node
    while current:
        # case: current is largest and has a left subtree
        if current.left and not current.right:
            return find_largest(current.left)

        # case: current is parent of largest and largest has no children
        if (current.right and 
                not current.right.left and 
                not current.right.right):
            return current.value
        
        # otherwise: step right
        current = current.right

'''
O(h) time
O(1) space

what we learned?
simplify, solve and adapt
'''
        
    