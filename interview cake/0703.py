'''
reverse a linked list

given head of the list, return the new head of the list
'''
def reverse(head_of_list):
    current_node = head_of_list
    previous_node = None
    next_node = None

    # until we have 'fallen off' the end of the list
    while current_node:
        # copy a pointer to the next element
        # before we overwrite current_node.next
        next_node = current_node.next

        # reverse the 'next' pointer
        current_node.next = previous_node

        # step forward in the list
        previous_node = current_node
        current_node = next_node

    return previous_node
'''
O(n) time and O(1) space

Bonus: this in-place reversal destroys the input linked list. what if 
we wanted to keep a copy of the original list? 
'''
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
def referse_out_of_place(head_of_list):
    if not head_of_list:
        return None
    
    # initialize the new head of the reveresed list
    new_head = None
    current_node = head_of_list

    while current_node:
        # create a new node for the current value
        new_node = Node(current_node.value)

        # insert the new node at the beginning of the new list
        new_node.next = new_head
        new_head = new_node

        # move to the next node in the original list
        current_node = current_node.next
    return new_head
'''
learning: Write out a sample linked list and walk through your code 
by hand, step by step, running each operation on your sample input 
to see if the final output is what you expect. This is a great 
strategy for any coding interview question.

bonus: create and print a linkedlist
'''
def create_linked_list(values):
    if not values:
        return None
    head = Node(values[0])
    current = head
    for value in values[1:]:
        current.next = Node(value)
        current = current.next
    return head

def print_linked_list(head):
    values = []
    current = head
    while current:
        values.append(current.value)
        current = current.next
    print(" -> ".join(map(str, values)))