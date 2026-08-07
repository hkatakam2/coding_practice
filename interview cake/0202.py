"""
given a list of integers find the highest product 
you can get from three of the integers

list_of_ints will always have at least 3 integers

Bruteforce:
we could iterate through the list_of_ints and multiply each integer by each other integer,
and then multipley that product by each other other integer
O(n^3) runtime

softing the list:
O(n log n) for sorting; can we do better?

greedy approach: O(n)
how can we keep track of the highest_product_of_3 so far 
as we do one walk through the list?
i.e. for each new current number during the iteration, how do we
know if it gives us a new highest_product_of_3 ?

initial guess:
1. our current highest_product_of_3
2. the three_numbers_which_give_highest_product
but this won't work for the negative numbers

2 guesses:
1. Keep track of the highest_2 and lowest_2 (most negative) numbers. 
If the current number times some combination of those is higher than 
the current highest_product_of_3, we have a new highest_product_of_3!
2. Keep track of the highest_product_of_2 and lowest_product_of_2 
(could be a low negative number). If the current number times one of 
those is higher than the current highest_product_of_3, we have a new highest_product_of_3!
"""
'''
let us do the method 2, to do that we need to keep track of something else

at each iteration we're keeping track of and updating:
highest_product_of_3
highest_product of_2
highest
lowest_product_of_2
lowest

while implementing keep in mind the order of storing these

at each iteration, the highest_product_of_3 is the highest of:
1. the current highest_product_of_3
2. current * highest_product_of_2
3. current * lowest_product_of_2 (if current and lowest_product_of_2 are both low negative numbers, this product is a high positive number).
'''
def highest_product_of_3(list_of_ints):
    if len(list_of_ints) < 3:
        raise ValueError('Less than 3 items in the input')
    
    # we're going to start at the 3rd item(at index 2)
    # so pre-populate highests and lowests based on the first 2 items
    highest = max(list_of_ints[0], list_of_ints[1])
    lowest = min(list_of_ints[0], list_of_ints[1])
    highest_product_of_2 = list_of_ints[0] * list_of_ints[1]
    lowest_product_of_2 = list_of_ints[0] * list_of_ints[1]

    # except this one -- we pre-populate it for the first 3 items
    # this means in our first pass it'll check against itself, which is fine
    highest_product_of_3 = list_of_ints[0] * list_of_ints[1] * list_of_ints[2]

    # walk through items, starting at index 2
    for i in range(2, len(list_of_ints)):
        current = list_of_ints[i]

        # do we have a new highest product of 3?
        highest_product_of_3 = max(highest_product_of_3,
                                    current * highest_product_of_2,
                                    current * lowest_product_of_2)
        # do we have a new highest product of 2?
        highest_product_of_2 = max(highest_product_of_2, 
                                   current * highest,
                                   current * lowest)
        # do we have a new lowest product of 2?
        lowest_product_of_2 = min(lowest_product_of_2,
                                  current * highest,
                                  current * lowest)
        # do we have a new highest?
        highest = max(highest, current)

        # do we have a new lowest?
        lowest = min(lowest, current)

    return highest_product_of_3
'''
O(n) time and O(1) additional space

Bonus:
1. What if we wanted the highest product of 4 items?
2. What if we wanted the highest product of k items?
3. If our highest product is really big, it could overflow. How should we protect against this?

learning:
greedy algorithm similar to apple stocks:
"Suppose we could come up with the answer in one pass through 
the input, by simply updating the 'best answer so far' as we went. 
What additional values would we need to keep updated as we looked at 
each item in our set, in order to be able to update the 'best answer 
so far' in constant time?"

For the Apple stocks question, the only "additional value" we needed 
was the min price so far.

For this one, we needed four things in order to calculate the new highest_product_of_3 at each step:
• highest_product_of_2
• highest
• lowest_product_of_2
• lowest
'''

'''
2. What if we wanted the highest product of k items?
we need to extend the same logic but maintain more state.

'''
def highest_product_of_k(list_of_ints, k):
    if len(list_of_ints) < k:
        raise ValueError(f'Less than {k} items in the input')
    
    # initialize arrays to track products and numbers
    highest_products = [float('-inf')] * (k + 1) # index i stores highest_product of i numbers
    lowest_products = [float('inf')] * (k + 1) # index i stores lowest_product of i numbers

    # initialize with first number
    highest_products[0] = 1 # Empty product is 1
    lowest_products[0] = 1
    highest_products[1] = list_of_ints[0]
    lowest_products[1] = list_of_ints[0]

    # process each number
    for i in range(1, len(list_of_ints)):
        current = list_of_ints[i]

        # update all possible products from k down to 2
        for j in range(min(i+1, k), 0, -1):
            highest_products[j] = max(
                highest_products[j],
                current * highest_products[j-1],
                current * lowest_products[j-1]
            )
            lowest_products[j] = min(
                lowest_products[j],
                current * highest_products[j-1],
                current * lowest_products[j-1]
            )
    return highest_products[k]

'''
The time complexity remains O(n) for the basic k-product solution and O(n*k) for the general k 
solution, but space complexity increases to O(k) to store the intermediate products.

Bonus 3: Handling Overflow
Here are several approaches to handle overflow:

Using Python's built-in arbitrary-precision integers: Python automatically handles large integers, but for other languages, you might need explicit handling.

Using logarithms:
'''
from math import log, exp

def highest_product_of_k_with_logs(list_of_ints, k):
    """
    Handle overflow by working with logs of numbers
    """
    if len(list_of_ints) < k:
        raise ValueError(f'Less than {k} items in the input')
    
    # Convert to logs
    log_numbers = [log(abs(num)) for num in list_of_ints]
    signs = [1 if num >= 0 else -1 for num in list_of_ints]
    
    # Track sum of logs instead of product of numbers
    current_sum = sum(log_numbers[:k])
    current_sign = 1
    for s in signs[:k]:
        current_sign *= s
        
    max_sum = current_sum
    max_sign = current_sign
    
    # Process remaining numbers
    for i in range(k, len(list_of_ints)):
        current_sum = current_sum - log_numbers[i-k] + log_numbers[i]
        current_sign = current_sign * signs[i] // signs[i-k]
        
        if current_sum > max_sum:
            max_sum = current_sum
            max_sign = current_sign
            
    return max_sign * int(exp(max_sum))
'''
Using a custom numeric type with overflow checking:
'''
class SafeInteger:
    MAX_VALUE = 2**53  # JavaScript-style safe integer limit
    
    def __init__(self, value):
        self.value = value
        self._check_overflow()
    
    def _check_overflow(self):
        if abs(self.value) > self.MAX_VALUE:
            raise OverflowError("Integer overflow detected")
    
    def __mul__(self, other):
        result = self.value * other.value
        return SafeInteger(result)
