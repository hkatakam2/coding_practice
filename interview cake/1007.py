'''
stolen breakfast drone
Given the list of IDs, which contains many duplicate integers and one unique integer, 
find the unique integer.

The IDs are not guaranteed to be sorted or sequential. Orders aren't always fulfilled 
in the order they were received, and some deliveries get cancelled before takeoff.

bruteforce: nested loop
O(n^2) time and O(1) space


well, we know every integer appears twice except one, can we just
keep track how many times each integer appers?
'''
def find_unique_delivery_id(delivery_ids):
    ids_to_occurances = {}

    for delivery_id in delivery_ids:
        if delivery_id in ids_to_occurances:
            ids_to_occurances[delivery_id] += 1
        else:
            ids_to_occurances[delivery_id] = 1

    for delivery_id, occurances in list(ids_to_occurances.items()):
        if occurances == 1:
            return delivery_id
'''
O(n) time; O(n) space
can we brind space down?

how is the unique_id stored in the computer?
bitwise operations
'''
def find_unique_delivery_id(delivery_ids):
    unique_delivery_id = 0

    for delivery_id in delivery_ids:
        unique_delivery_id ^= delivery_id

    return unique_delivery_id

'''
O(n) time
O(1) space

learning:
knowledge of what's happening at bit level is helpful

how to know when bit manipulation might be the key?
1. you want to multiply or divide by 2 (use a left shift to multiply, 
right shift to divide by 2)
2. you want to "cancel out" matching numbers (use XOR)
'''