'''
write a function that takes an integer n and returns the nth fibo number

fib(0) = 0
fib(1) = 1
fib(2) = 1

fib(n) = fib(n-1) + fib(n-2)

can we write a recursive solution?

'''
def fib(n):
    if n in [0,1]:
        return n
    return fib(n-1) + fib(n-2)
'''
each fib() calls 2 more function calls.

try to draw the binary tree of calls for fib(5); it has height n
O(2^n) is the runtime; this worse than O(n^2)

how to remove some of the repeat work?
memoize;
let's wrap fib() in a class with an instance variable where 
we store the answer for any n that we compute 
'''
class Fibber(object):
    def __init__(self):
        self.memo = {}
    
    def fib(self, n):
        if n < 0:
            raise ValueError('Index was negative')

        # base case
        elif n in [0,1]:
            return n

        #see if we've already calculated this
        if n in self.memo:
            return self.memo[n]
        
        result = self.fib(n-1) + self.fib(n-2)

        # memoize
        self.memo[n] = result

        return result
'''
runtime? O(n)
O(n) additional space and we are building up a call stack that occupy n space

can we avoid both these?

we can start with fib(0) and work our way up
'''
def fib(n):
    # edge cases:
    if n < 0:
        raise ValueError
    elif n in [0,1]:
        return n
    
    # we'll be building the fibo series from the bottom up
    # so we'll need to track the previous 2 numbers at each step
    
    prev_prev = 0 # 0th fib
    prev = 1 # 1st fib

    for _ in range(n-1):
        # iteration 1: current = 2nd fibo
        # iteration 2: current = 3rd fibo
        # iteration n-1: current = nth fibo
        current = prev + prev_prev
        prev_prev = prev
        prev = current
    return current
'''
O(n) time
O(1) space

what we learned?
recursive solution is cute but could cost us O(2^n)
also think about call stack in an iterative solution, iterative solution might be efficient
'''