'''
merge sorted lists?

my_list = [3,4,6,10,11,15]
alices_list = [1,5,8,12,14,19]

break down:
we could simply concatenate the two lists and then sort the result
'''
def merge_lists(arr1, arr2):
    return sorted(arr1 + arr2)
'''
O(n log n) time for sorting;

our input lists are already sorted we can use that to reduce the time
tip:
write an algorithm to do it by hand; think about the 0th element of merged_list
'''
def merge_lists(my_list, alices_list):
    # make a list big enough to fit the elements from both lists
    merged_list_size = len(my_list) + len(alices_list)
    merged_list  = [None] * merged_list_size

    head_of_my_list = my_list[0]
    head_of_alices_list = alices_list[0]

    if head_of_my_list < head_of_alices_list:
        merged_list[0] = head_of_my_list
    else:
        merged_list[0] = head_of_alices_list
    
    # eventually we'll want to return the merged list
    return merged_list
'''
this works for 0th element, how will we find the next element?
'''
def merge_lists(my_list, alices_list):
    merged_list_size = len(my_list) + len(alices_list)
    merged_list = [None] * merged_list_size

    current_index_mine = 0
    current_index_alices = 0
    current_index_merged = 0
    while current_index_merged < merged_list_size:
        first_unmerged_alices = alices_list[current_index_alices]
        first_unmerged_mine = my_list[current_index_mine]

        if first_unmerged_mine < first_unmerged_alices:
            merged_list[current_index_merged] = first_unmerged_mine
            current_index_mine += 1
        else:
            merged_list[current_index_merged] = first_unmerged_alices
            current_index_alices += 1
        
        current_index_merged += 1

    return merged_list
'''
this works, what about edge cases? does our function handle them corrently?
1. One or both of our input lists is 0 elements or 1 element
2. One of our input lists is longer than the other.
3. One of our lists runs out of elements before we're done merging.
'''
def merge_lists(my_list, alices_list):
    merged_list_size = len(my_list) + len(alices_list)
    merged_list = [None] * merged_list_size

    current_index_alices = 0
    current_index_mine = 0
    current_index_merged = 0
    while current_index_merged < merged_list_size:
        if current_index_mine >= len(my_list):
            # Case: my list is exhausted
            merged_list[current_index_merged] = alices_list[current_index_alices]
            current_index_alices += 1
        elif current_index_alices >= len(alices_list):
            # Case: Alice's list is exhausted
            merged_list[current_index_merged] = my_list[current_index_mine]
            current_index_mine += 1
        elif my_list[current_index_mine] < alices_list[current_index_alices]:
            # Case: my item is next
            merged_list[current_index_merged] = my_list[current_index_mine]
            current_index_mine += 1
        else:
            # Case: Alice's item is next
            merged_list[current_index_merged] = alices_list[current_index_alices]
            current_index_alices += 1
        
        current_index_merged += 1
    
    return merged_list
'''
this works but it is repetitive

if (is_alices_list_exhausted or my_list[current_index_mine] < alices_list[current_index_alices]):
    merged_list[current_index_merged] = my_list[current_index_mine]
    current_index_mine += 1
'''
def merge_lists(my_list, alices_list):
    # Set up our merged_list
    merged_list_size = len(my_list) + len(alices_list)
    merged_list = [None] * merged_list_size

    current_index_alices = 0
    current_index_mine = 0
    current_index_merged = 0
    while current_index_merged < merged_list_size:
        is_my_list_exhausted = current_index_mine >= len(my_list)
        is_alices_list_exhausted = current_index_alices >= len(alices_list)
        if (not is_my_list_exhausted and (is_alices_list_exhausted or my_list[current_index_mine] < alices_list[current_index_alices])):
            # Case: next comes from my list
            # My list must not be exhausted, and EITHER:
            # 1) Alice's list IS exhausted, or
            # 2) the current element in my list is less
            # than the current element in Alice's list
            merged_list[current_index_merged] = my_list[current_index_mine]
            current_index_mine += 1
        else:
            # Case: next comes from Alice's list
            merged_list[current_index_merged] = alices_list[current_index_alices]
            current_index_alices += 1

        current_index_merged += 1
    
    return merged_list
'''
O(n) time and O(n) additional space

if our inputs were linked lists, we could avoid allocating a new 
structure and do the merge by simply adjusting the next pointers 
in the list nodes!

In our implementation above, we could avoid tracking current_index_merged 
and just compute it on the fly by adding current_index_mine and 
current_index_alices. This would only save us one integer of space 
though, which is hardly anything. It's probably not worth the added 
code complexity.
'''

'''
Bonus:
What if we wanted to merge several sorted lists? Write a function that 
takes as an input a list of sorted lists and outputs a single sorted 
list with all the items from each list.
'''
import heapq

def merge_sorted_lists(sorted_lists):
    # create a min heap to store (value, list_index, element_index)
    min_heap = []

    # add the first element of each list to the heap
    for list_index, lst in enumerate(sorted_lists):
        if lst: # only add non empty lists
            heapq.heappush(min_heap, (lst[0], list_index, 0))
    
    merged_list = []

    # while the heap is not empty, extract the smallest element
    while min_heap:
        value, list_index, element_index = heapq.heappop(min_heap)
        merged_list.append(value)

        # if there is a next element in the same list, add it to the heap
        if element_index + 1 < len(sorted_lists[list_index]):
            next_value = sorted_lists[list_index][element_index + 1]
            heapq.heappush(min_heap, (next_value, list_index, element_index + 1))

    return merged_list  
'''
Runtime Complexity
	•	Building the heap initially: O(k), where k is the number of sorted lists.
	•	Merging the elements: O(n log k), where n is the total number of elements across all lists.

Do we absolutely have to allocate a new list to use for the merged 
output? Where else could we store our merged list? How would our 
function need to change?
'''  
def merge_lists_in_place(target_list, source_list):
    # Expand target_list to fit all elements
    target_list.extend([None] * len(source_list))

    # Indices for merging
    i = len(target_list) - len(source_list) - 1  # Last valid element in the original target_list
    j = len(source_list) - 1  # Last element in source_list
    k = len(target_list) - 1  # Last position in the expanded target_list

    # Merge from the back
    while i >= 0 and j >= 0:
        if target_list[i] > source_list[j]:
            target_list[k] = target_list[i]
            i -= 1
        else:
            target_list[k] = source_list[j]
            j -= 1
        k -= 1

    # Copy remaining elements from source_list (if any)
    while j >= 0:
        target_list[k] = source_list[j]
        j -= 1
        k -= 1

    return target_list    

'''
Pros:
	•	Space-efficient: Does not require a new list.
	•	Cache-friendly: Works directly on input data.
Cons:
	•	Destructive: Modifies one of the input lists.
	•	Complexity: Logic for merging in place is harder to implement and debug.


learnings:
Sometimes it's easy to lose steam at the end of a coding interview 
when you're debugging. But keep sprinting through to the finish! 
Think about edge cases. Look for off-by-one errors.
'''