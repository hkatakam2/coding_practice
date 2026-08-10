'''
delete node in a linked list

class LinkedListNode(object):
    def _init__(self, value):
        self.value = value
        self.next = None

a = LinkedListNode('A')
b = LinkedListNode('B')
c = LinkedListNode('(')
a.next = b
b.next = c
delete_node(b)
'''

'''
breakdown:
it is tempting to traverse the list but we don't have reference 
to the first node 

we need a way to skip over the current node and go straight to the 
next node. But we don't even have access to the previous node!

Other than rerouting the previous node's pointer, is there another way 
to skip from the previous pointer's value to the next pointer's value?

what if we modify the current node instead of deleting it?
'''
def delete_node(node_to_delete):
    # get the input node's next node, the one we want to skip tp
    next_node = node_to_delete.next

    if next_node:
        # replace the input node's value and pointer with the next
        # node's value and pointer. The previous node now effectively
        # skips over the input node
        node_to_delete.value = next_node.value
        node_to_delete.next = next_node.next
    else:
        # Eep, we're trying to delete the last node!
        raise Exception('Cant delete the last node with this technique')
    
'''
O(1) time and O(1) space

what we learned:
it modifies the list "in place" it can cause other parts of the surrounding 
system to break. This is called a "side effect."

in-place operations can save time and/or space, but they're risky. 
If you ever make in-place modifications in an interview, make sure you tell 
your interviewer that in a real system you'd carefully check for 
side effects in the rest of the code base.
'''