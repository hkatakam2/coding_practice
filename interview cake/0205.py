'''
write a function for doing an in-place shuffle of a list

shuffle must be uniform; each item in the original list must have the 
same probability of ending up in each spot in the final list

assume you have a function get_random(floor, ceiling)

breakdown:
ignore the inplace requirement. 

how do we do this by hand?
choose a random item to be the first item in the resulting list,
then choose another random item(from the items remaining) and so on

w/o inplace, we can remove the selected item and use the remaining for 
next step

with inplace requirement?
'''
import random

def get_random(floor, ceiling):
    return random.randrange(floor, ceiling + 1)

def shuffle(the_list):
    # if it's 1 or 0 items, just return
    if len(the_list) < 2:
        return the_list
    
    last_index_in_the_list = len(the_list) - 1

    # walk through from beginning to end
    for index_we_are_choosing_for in range(0, len(the_list) - 1):

        # choose a random not_yet_placed item to place there
        # (could also be the item currently in that spot)
        # must be an item AFTER the current item, because the stuff
        # before has all already been placed 
        random_choice_index = get_random(index_we_are_choosing_for,
                                         last_index_in_the_list)
        
        # place our random choice in the spot for swapping
        if random_choice_index != index_we_are_choosing_for:
            the_list[index_we_are_choosing_for], the_list[random_choice_index] = \
                the_list[random_choice_index], the_list[index_we_are_choosing_for]
'''
this is also called Fisher_Yates shuffle or Knuth shuffle
O(n) time, O(1) space

learning:
why naive methods won't give uniform shuffle?
'''
# sort by random numbers
def naive_shuffle_1(the_list):
    # create pairs of (random_number, item)
    pairs = [(random.random(), x) for x in the_list]
    # sort by random numbers
    pairs.sort()
    # extract items back
    return [x for (r,x) in pairs]
'''
For Sort by Random Method:

Not all permutations have equal probability
The number of possible random float values is much larger than the number of possible permutations
Some orderings become more likely than others due to how floating-point numbers are distributed
'''
# Random swap
def naive_shuffle_2(the_list):
    n = len(the_list)
    for i in range(n):
        # randomly swap each position with any other position
        j = random.randint(0, n-1)
        the_list[i], the_list[j] = the_list[j], the_list[i]
    return the_list
'''
For Random Swap Method:

Some permutations are more likely than others
Example with 3 items [A, B, C]:
The same position might be swapped multiple times
Some elements might never move
'''
# fisher yeates(the correct way)
def fisher_yates_shuffle(the_list):
    n = len(the_list)
    for i in range(n-1):
        # choose from remaining elements
        j = random.randint(i, n-1)
        the_list[i], the_list[j] = the_list[j], the_list[i]
    return the_list
'''
The Fisher-Yates shuffle:

Guarantees uniform distribution
Each permutation has exactly 1/n! probability
Works in-place
Has O(n) time complexity
Has O(1) space complexity
The key difference is that Fisher-Yates:

Processes the list from left to right
Only swaps with remaining positions
Never re-shuffles already placed elements
'''