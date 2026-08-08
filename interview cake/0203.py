'''
product of all ints except the one at the index
input [1,7,3,4]
output [84,12,28,21]

constraint: can't use division

brute force:
A brute force approach would use two loops to multiply the integer at 
every index by the integer at every nested_index, unless index == nested_index.
This would give us a runtime of O(n^2). Can we do better?

'''
def get_product_of_all_except_at_index(int_list):
    result = [None] * len(int_list)
    for i in range(len(int_list)):
        product = 1
        for j in range(len(int_list)):
            if i == j:
                continue
            else:
                product *= int_list[j]
        result[i] = product
    
    return result

'''
we are redoing many multiplications; can we store them somehow to reuse

greedy: 
what do I need to know so that I can calculate the result at each index?

The product of all the integers except the integer at each index can be broken down into two pieces:
1. the product of all the integers before each index, and
2. the product of all the integers after each index.

'''
def get_products_of_all_ints_except_at_index(int_list):
    products_of_all_ints_before_index = [None] * len(int_list)

    # for each integer, find the product of all the integers 
    # before it, storing the total product so far each time
    product_so_far = 1
    for i in range(len(int_list)):
        products_of_all_ints_before_index[i] = product_so_far
        product_so_far *= int_list[i]

    products_of_all_ints_after_index = [None] * len(int_list)

    product_so_far = 1
    for i in range(len(int_list)-1, -1, -1):
        products_of_all_ints_after_index[i] = product_so_far
        product_so_far *= int_list[i]
'''
we can get the final list by multiplying these two lists.

can we save some space?
Yes, instead of building the second list products_of_all ints_after_index, 
we could take the product we would have stored and just multiply it by the 
matching integer in products_of_all_ints_before_index!

input [2,4,10]
product before index [1,2,8]
product after index [40,10,1]
output [40,20,8]

when we calculated our first (well, "Oth") "product after index" 
(which is 40), we'd just multiply that by our first "product before index" 
(1) instead of storing it in a new list. -- we just need 1 list

are there any edge cases? it works with zeroes 
'''

def get_products_of_all_ints_except_at_index(int_list):
    if len(int_list) < 2:
        raise IndexError('getting the product numbers at other'
                         'indices require at least 2 numbers')
    # we make a list with the length of the input list to hold the products
    products_of_all_ints_except_at_index = [None] * len(int_list)

    # for each integer, we find the product of all the integers before it,
    # storing the toal product so far each time
    product_so_far = 1
    for i in range(len(int_list)):
        products_of_all_ints_except_at_index[i] = product_so_far
        product_so_far *= int_list[i]

    # for each integer, we find the product of all the integers 
    # after it. since each index in products already has the product of 
    # all the integers before it, now we're storing the 
    # total product of all other integers
    product_so_far = 1
    for i in range(len(int_list)-1, -1, -1):
        products_of_all_ints_except_at_index[i] *= product_so_far
        product_so_far *= int_list[i]

    return products_of_all_ints_except_at_index
'''
O(n) time and O(n) additional space

learning: start with brute force solution, look for repeat work in that
solution, and modify it to only do that work once
'''


'''ß
observations:
writing the for loop for the previous index updation
naming the variables to express clearly; 
focus on how I would do on paper and translating it to code

ask: what do I need to remember to calculate the current value?ß

'''
    