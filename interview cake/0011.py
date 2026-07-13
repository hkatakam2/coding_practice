'''
cafe order checker

write a function to check my service is first-come first-served

take_out_orders = [1,3,5]
dine_in_orders = [2,4,6]
served_orders = [1,2,4,6,5,3] 
output: false; as 3 was requested before 5

take_out_orders = [17,8,24]
dine_in_orders = [12,19,2]
served_orders = [17,8,12,19,24,2]
output: true

logic: false; all the items before that item in it's category must have been served

breakdown: how to re-phrase this problem in terms of smaller subproblems?

first order in served orders must be either first order in take_out or dine_in

once we accounted for that throw this order from both served and it's own orderlist

now we are left with smaller problem.

'''
def is_first_come_first_served(take_out_orders, dine_in_orders, served_orders):
    # base case
    if len(served_orders) == 0:
        return True

    # if the first order in served_orders is the same as the 
    # first order in take_out_orders
    # (making sure first that we have an order in take_out_orders
    if len(take_out_orders) and take_out_orders[0] == served_orders[0]:
        # take the first order off take_out_orders and served_orders and recurse
        return is_first_come_first_served(take_out_orders[1:], dine_in_orders, served_orders[1:])

    # if the first order in served_orders is the same as the 
    # first order in dine_in_orders
    elif len(dine_in_orders) and dine_in_orders[0] == served_orders[0]:
        return is_first_come_first_served(take_out_orders, dine_in_orders[1:], served_orders[1:])

    # first order in served_orders doesn't match the first in 
    # take_out_orders or dine_in_orders, so we know it's not first come fits served
    else:
        return False
    
'''
this solution works; how can we make it better?
O(n^2) time
O(n^2) extra space

take_out_orders[1:] cost O(m), where m is the size of the resulting list

avoid slicing and keep track of the indices in the list
'''
def is_first_come_first_served(take_out_orders, dine_in_orders, served_orders,
                               take_out_orders_index = 0, dine_in_orders_index = 0,
                               served_orders_index= 0):
    # base case we've hit the end of served_orders
    if served_orders_index == len(served_orders):
        return True

    # if we still have orders in take_out_orders
    # and the current order in take_out_orders is the same
    # as the current order in served_orders
    if((take_out_orders_index < len(take_out_orders)) and
       take_out_orders[take_out_orders_index] == served_orders[served_orders_index]):
        take_out_orders_index += 1

    # if we still have orders in dine_in_orders
    # and the current order in dine_in_orders is the same
    # as the current order in served orders
    elif((dine_in_orders_index < len(dine_in_orders)) and 
       dine_in_orders[dine_in_orders_index] == served_orders[served_orders_index]):
        served_orders_index += 1
    
    # if the current order in served_orders doesn't match
    # the current order in take_out_orders or dine_in_orders, then we're not
    # serving first_come, first_served order
    else:
        return False
    
    # the current order in served_orders has now been "accounted for"
    # so move on to the next one
    served_orders_index += 1
    return is_first_come_first_served(take_out_orders, dine_in_orders, served_orders,
                                      take_out_orders_index, dine_in_orders_index,
                                      served_orders_index)

'''
O(n) time 
O(n) space in the call stack;

rewrite this as an iterative function to get that memory cost down to O(1)
what's happening in each iteration of our recursive function?
sometimes we are taking out take_out_orders and some times dine_in_orders,
but we are always taking a customer order out of served_orders.

so what if instead of taking customer orders out of served_orders 1 by 1, 
we iterated over them?

that can work, are we missing any edge cases?

'''
def is_first_come_first_served(take_out_orders, dine_in_orders, served_orders):
    take_out_orders_index = 0
    dine_in_orders_index = 0
    take_out_orders_max_index = len(take_out_orders) -1
    dine_in_orders_max_index = len(dine_in_orders) -1

    for order in served_orders:
        # if we still have orders in take_out_orders
        # and the current order in take_out_orders is the same
        # as the current order in served_orders
        if take_out_orders_index < take_out_orders_max_index and \
            order == take_out_orders[take_out_orders_index]:
            take_out_orders_index += 1

        # if we still have orders in dine_in_orders
        # and the current order in dine_in_orders is the same 
        # as the current order in server_orders
        elif dine_in_orders_index < dine_in_orders_max_index and \
            order == dine_in_orders[dine_in_orders_index]:
            dine_in_orders_index += 1
        
        # if the current order in served_orders doesn't match the current
        # order in take_out_orders or dine_in_orders, then we're not FCFS
        else:
            return False
        
    # check for any extra orders at the end of take_out orders or dine_in_orders
    if dine_in_orders_index != len(dine_in_orders) or \
        take_out_orders_index != len(take_out_orders):
        return False
    
    # all orders in served_orders have been accounted for
    # so we're serving first come. first-served
    return True

'''
O(n) time
O(1) additional space

bonus:
1. this assumes each customer order in served_orders is unique. 
How can we adapt this to handle lists of customer orders with potential repeats
2. our implementation returns True when all the items in dine_in_orders and take_out_orders
are FCFS in served_orders and False otherwise.
That said it'd we reasonable to raise an exception if some orders that went into kitch
were never served, or orders were served but not paid for at either register.
how could we check for those cases?
3. Our solution iterated through the customer orders from front to back. 
Would our algorithm work if we iterated from the back towards the front?
which approach is cleaner?

what we learned?
our recusrion function cost us extra space

if you have a solution that's recursive, see if you can save space by using an 
iterative algorithm instead.
'''

'''
practice:

how will you write the recursive solution
how will you remove call stack by doing the iterations yourself?

complexity analysis

'''