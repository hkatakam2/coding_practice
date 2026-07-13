'''
write a function that takes a list of characters and revereses the letters in place

we are modyfing the input so we need a mutable type like a list.
inplace algorithm needs swap
'''
def reverse(list_of_chars):

    left_index = 0
    right_index = len(list_of_chars) - 1

    while left_index < right_index:
        # swap characters
        list_of_chars[left_index], list_of_chars[right_index] = \
            list_of_chars[right_index], list_of_chars[left_index]
        # move towards middle
        left_index += 1
        right_index -= 1

'''
O(n) time
O(1) space
'''


