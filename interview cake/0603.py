'''
implement a queue with 2 stacks

assume you have a stck implementation and it gives O(1) time to push and pop

breakdown:
basically storing everything in stack1, using stack2 only for 
temporarily "flipping" all of our items during a dequeue to get the 
bottom (oldest) element.
This is a complete solution. but O(m^2)

What if we didn't move things back to stack1 after 
putting them on stack2?
'''
class QueueTwoStacks(object):
    def __init__(self):
        self.in_stack = []
        self.out_stack = []

    def enqueue(self, item):
        self.in_stack.append(item)

    def dequeue(self, item):
        if len(self.out_stack) == 0:
            # move items from in_stack to out_stack, reversing order
            while len(self.in_stack) > 0:
                newest_in_stack_item = self.in_stack.pop()
                self.out_stack.append(newest_in_stack_item)

            # if out_stack is still empty, raise an error
            if len(self.out_stack) == 0:
                raise IndexError("can't deque from empty queue!")
            
        return self.out_stack.pop()
    
'''
each enque is O(1)
average deque is O(1)

Our m enqueue and dequeue operations put m or fewer items into 
the system, giving a total runtime of O(m).

learning:
we are looking at runtime of m operations instead of 
runtime of 1 call (enque/ deque) in this case
'''