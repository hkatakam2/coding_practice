'''
previously we found duplicate using divide and conquer O(n log n) time and O(1) space

we can do this in O(n) time and O(1) space

strategy to find a duplicate integer! Working backward:
A. We know the position of a node with multiple incoming pointers is a duplicate in our list because the nodes that pointed to it must have the same value.
B. We find a node with multiple incoming pointers by finding the first node in a cycle.
C. We find the first node in a cycle by finding the length of the cycle and advancing two pointers: one starting at the head of the linked list, and the other starting ahead as many steps as there are steps in the cycle. The pointers will meet at the first node in the cycle.
D. We find the length of a cycle by remembering a position inside the cycle and counting the number of steps it takes to get back to that position.
E. We get inside a cycle by starting at the head and walking n steps. We know the head of the list is at position n + 1.

To get inside a cycle (step E above), we identify n, start at the head (the node in position n + 1), and walk n steps.
'''
def find_duplicate(int_list):
    n = len(int_list) - 1

    # step 1: get inside a cycle
    # start at position n+1 and walk n steps to
    # find a position guaranteed to be in a cycle
    position_in_cycle = n + 1
    for _ in range(n):
        position_in_cycle = int_list[position_in_cycle -1]
'''
Now we're guaranteed to be inside a cycle. To find the cycle's length (D), we remember the current position and step ahead until we come back to that same position, counting the number of steps.
'''

def find_duplicate(int_list):
    n = len(int_list) - 1
    
    # STEP 1: GET INSIDE A CYCLE
    # Start at position n+1 and walk n steps to
    # find a position guaranteed to be in a cycle
    position_in_cycle = n + 1
    for _ in range(n):
        position_in_cycle = int_list[position_in_cycle - 1]
    
    # STEP 2: FIND THE LENGTH OF THE CYCLE
    # Find the length of the cycle by remembering a position in the cycle
    # and counting the steps it takes to get back to that position
    remembered_position_in_cycle = position_in_cycle
    current_position_in_cycle = int_list[position_in_cycle - 1] # 1 step ahead
    cycle_step_count = 1
    
    while current_position_in_cycle != remembered_position_in_cycle:
        current_position_in_cycle = int_list[current_position_in_cycle - 1]
        cycle_step_count += 1

'''
Now we have the head and the length of the cycle. We need to find the first node in the cycle (C).
We set up 2 pointers: 1 at the head, and 1 ahead as many steps as there are nodes in the cycle.
These two pointers form our "stick."

'''
# STEP 3: FIND THE FIRST NODE OF THE CYCLE
# Start two pointers
# (1) at position n+1
# (2) ahead of position n+1 as many steps as the cycle's length
pointer_start = n + 1
pointer_ahead = n + 1
for _ in range(cycle_step_count):
    pointer_ahead = int_list[pointer_ahead - 1]
'''
Alright, we just need to find to the first node in the cycle (B), and return a duplicate value (A)!
'''
def find_duplicate(int_list):
    n = len(int_list) - 1
    # STEP 1: GET INSIDE A CYCLE
    # Start at position n+1 and walk n steps to
    # find a position guaranteed to be in a cycle
    position_in_cycle = n + 1
    for _ in range(n):
        position_in_cycle = int_list[position_in_cycle - 1]
        # we subtract 1 from the current position to step ahead:
        # the 2nd *position* in a list is *index* 1
    
    # STEP 2: FIND THE LENGTH OF THE CYCLE
    # Find the length of the cycle by remembering a position in the cycle
    # and counting the steps it takes to get back to that position
    remembered_position_in_cycle = position_in_cycle
    current_position_in_cycle = int_list[position_in_cycle - 1] # 1 step ahead
    cycle_step_count = 1
    
    while current_position_in_cycle != remembered_position_in_cycle:
        current_position_in_cycle = int_list[current_position_in_cycle - 1]
        cycle_step_count += 1
    
    # STEP 3: FIND THE FIRST NODE OF THE CYCLE
    # Start two pointers
    # (1) at position n+1
    # (2) ahead of position n+1 as many steps as the cycle's length
    pointer_start = n + 1
    pointer_ahead = n + 1
    for _ in range(cycle_step_count):
        pointer_ahead = int_list[pointer_ahead - 1]
    
    # Advance until the pointers are in the same position
    # which is the first node in the cycle
    while pointer_start != pointer_ahead:
        pointer_start = int_list[pointer_start - 1]
        pointer_ahead = int_list[pointer_ahead - 1]
    
    # Since there are multiple values pointing to the first node
    # in the cycle, its position is a duplicate in our list
    return pointer_start
'''
On) time and O(1) space.

Bonus:
There another approach using randomized algorithms that is O(n) time and O(1) space. Can you come up with that one? (Hint: You'll want to focus on the median.)

'''
'''
what we learned:

So if you get a hint in an interview, just relax and listen. The most impressive thing you can do is drop what you're doing, fully understand the hint, and then run with it.
'''
