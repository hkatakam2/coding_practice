'''
you have a linked list and want to find the kth to last node.

breakdown;
it is tempting to iterate through the list until we reach the end and
then walk backwards k nodes. But it's a singly liked list

what if we had the length of the list?
we could iterate from head to tail and count the nodes

'''
def kth_to_last(k, head):
    # step 1: get the length of the list
    # start at 1, not 0
    # else we'd fail to count the head node
    list_length = 1
    current_node = head

    # traverese the whole list,
    # counting all the nodes
    while current_node.next:
        current_node = current_node.next
        list_length += 1
    

    # step 2: walk to the target node
    # calculate how far to go, from the head,
    # to get to the kth to the last node
    how_far_to_go = list_length - k
    current_node = head
    for i in range(how_far_to_go):
        current_node = current_node.next

    return current_node 
'''
O(n) time and O(1) space
can we do it one pass?
'''
def kth_to_last_node(k, head):
    left_node = head
    right_node = head

    # move right_node to the kth node
    for _ in range(k-1):
        right_node = right_node.next

    # starting with left_node on the head,
    # move left_node and right_node down the list,
    # maintaining the distance of k between them,
    # until right_node hits the end of the list
    while right_node:
        left_node = left_node.next
        right_node = right_node.next

    # since left_node is k nodes behind right_node,
    # left_node is now the kth to last_node
    return left_node

'''
edge case: check if k is grater than length of the list

Bonus: 
what if n is much greater than k? can we improve the second pass 
so that we need to walk only a little bit to get to the kth node 
from the last?
can we use some 'check points' while we are doing first pass

'''


def kth_to_last_node_with_checkpoints(k, head):
    if k < 1:
        raise ValueError("k must be positive")

    # Store checkpoints every k nodes
    checkpoints = []
    current = head
    count = 0

    # First pass: store checkpoints and get length
    while current:
        if count % k == 0:
            checkpoints.append(current)
        count += 1
        current = current.next

    if k > count:
        raise ValueError(f"k ({k}) is larger than list length ({count})")

    # Calculate which checkpoint to start from
    checkpoint_index = (count - k) // k
    if checkpoint_index >= len(checkpoints):
        checkpoint_index = len(checkpoints) - 1

    # Start from the nearest checkpoint
    current = checkpoints[checkpoint_index]
    steps_needed = count - k - (checkpoint_index * k)

    # Move to the target node
    for _ in range(steps_needed):
        current = current.next

    return current

'''
This optimized version:
- Handles edge cases (k < 1 or k > list length)
- Uses checkpoints for faster access when n >> k
- Time: O(n), but faster for subsequent calls
- Space: O(n/k) for storing checkpoints
'''