'''
check if the cafe is first come first served?

take_out_orders, dine_in_orders, served_orders

given all three lists, write a function to check that my service is 
FCFS.

breakdown:
how can we re-phrase this problem in terms of smaller subproblems?
take served_orders[0],
if we are FCFS then it must be same as either take_out_orders[0] or
dine_in_orders[0]; else we are not FCFS

once we check that we can "throw out" the first order from both lists
and continue this way until there is nothing in served_orders

how do we implement it? recursion
what is the base case? served_orders is empty

'''
def is_first_come_first_served(take_out_orders, dine_in_orders, served_orders):
    # base case
    if len(served_orders) == 0:
        return True
    
    # (making sure first that we have an order in take_out_orders)
    if len(take_out_orders) and take_out_orders[0] == served_orders[0]:
        return is_first_come_first_served(take_out_orders[1:], dine_in_orders, served_orders[1:])
    
    elif len(dine_in_orders) and dine_in_orders[0] == served_orders[0]:
        return is_first_come_first_served(take_out_orders, dine_in_orders[1:], served_orders[1:])
    
    else:
        return False
'''
this works but can we do better?
O(n^2) time and O(n^2) additional space
slicing cost O(m) time and space (n-1)+(n-2)+...+1 = O(n^2)

keep track of indices
'''
def is_first_come_first_served(take_out_orders, dine_in_orders, served_orders,
                               take_out_orders_index = 0,
                               dine_in_orders_index = 0,
                               served_orders_index = 0):
    # base case
    if served_orders_index == len(served_orders):
        return True
    
    if ((take_out_orders_index < len(take_out_orders)) and take_out_orders[take_out_orders_index] == served_orders[served_orders_index]):
        take_out_orders_index += 1
    elif ((dine_in_orders_index < len(dine_in_orders)) and dine_in_orders[dine_in_orders_index] == served_orders[served_orders_index]):
        dine_in_orders += 1
    else:
        return False
    
    served_orders_index += 1
    return is_first_come_first_served(take_out_orders, dine_in_orders, served_orders,
                                      take_out_orders_index, 
                                      dine_in_orders_index,
                                      served_orders_index)
    

def is_fcfs(take_out_orders, dine_in_orders, served_orders,
            take_out_orders_index=0, dine_in_orders_index=0, served_orders_index=0):
    # Check if we've reached the end of served_orders
    if len(served_orders) == served_orders_index:
        # Make sure we've used all orders from both queues
        return (take_out_orders_index == len(take_out_orders) and 
                dine_in_orders_index == len(dine_in_orders))
    
    # Check take-out orders
    if (take_out_orders_index < len(take_out_orders) and 
            served_orders[served_orders_index] == take_out_orders[take_out_orders_index]):
        return is_fcfs(take_out_orders, dine_in_orders, served_orders,
                      take_out_orders_index + 1, dine_in_orders_index, served_orders_index + 1)
    
    # Check dine-in orders
    elif (dine_in_orders_index < len(dine_in_orders) and 
            dine_in_orders[dine_in_orders_index] == served_orders[served_orders_index]):
        return is_fcfs(take_out_orders, dine_in_orders, served_orders,
                      take_out_orders_index, dine_in_orders_index + 1, served_orders_index + 1)
    
    # If neither matches, orders weren't served in FCFS order
    return False

'''
now O(n) time 
O(n) additional space in call stack!

we can rewrite this as an iterative function to get the memory cost down to O(1)
what is happening in each iteration?
we are taking out served_order in each step, what if we iterate over it

'''
def is_first_come_first_served(take_out_orders, dine_in_orders, served_orders):
    take_out_orders_index = 0
    dine_in_orders_index = 0
    take_out_orders_max_index = len(take_out_orders) - 1
    dine_in_orders_max_index = len(dine_in_orders) - 1

    for order in served_orders:
        if (take_out_orders_index < take_out_orders_max_index) and order == take_out_orders[take_out_orders_index]:
            take_out_orders_index += 1
        elif (dine_in_orders_index < dine_in_orders_max_index) and order == dine_in_orders[dine_in_orders_index]:
            dine_in_orders_index += 1
        else:
            return False
    if dine_in_orders_index != len(dine_in_orders) or take_out_orders_index != len(take_out_orders):
        return False

    return True
'''
O(n) time and O(1) space

learning:
additional time and space needed for slicing

additional call stack space and how we can use iteration to cut down that
'''