'''
find the rotation point of a sorted list of words 

words = [
'ptolemaic',
'retrograde',
'supplant',
'undulate',
'xenoepist'
'asymptote'
"babka',
'banoffee',]

words = ['k','v','a','b','c','d",'e','g','i']


breakdown:
as the list is sorted; we can use binary search to be more efficient
'''
def find_rotation_point(words):
    first_word = words[0]
    floor_index = 0
    ceiling_index = len(words) - 1

    while floor_index < ceiling_index:
        # guess a point halfway between floor and ceiling
        guess_index = floor_index + ((ceiling_index - floor_index)//2)

        # if guess comes after first word or is the first word
        if words[guess_index] >= first_word:
            # go right
            floor_index = guess_index
        else:
            # go left
            ceiling_index = guess_index

        # if floor and ceiling have converged
        if floor_index + 1 == ceiling_index:
            # between floor and ceiling is where we flipped to the 
            # beginning so ceiling is alphabetically first
            return ceiling_index
        
'''
O(lg n) time; O(1) space

bonus: this list assumes the list is rotation;
if it isn't, what index does it return? how to make it return 0?
'''
def find_rotation_point(words):
    # Check if the list is unrotated
    if words[-1] >= words[0]:
        return 0

    first_word = words[0]
    floor_index = 0
    ceiling_index = len(words) - 1

    while floor_index < ceiling_index:
        # Guess a point halfway between floor and ceiling
        guess_index = floor_index + ((ceiling_index - floor_index) // 2)

        # If guess comes after first word or is the first word
        if words[guess_index] >= first_word:
            # Go right
            floor_index = guess_index
        else:
            # Go left
            ceiling_index = guess_index

        # If floor and ceiling have converged
        if floor_index + 1 == ceiling_index:
            # Between floor and ceiling is where we flipped to the beginning
            # so ceiling is alphabetically first
            return ceiling_index
'''
always think about cutting down the problem size, if sorted
this approach is also called divide and conquer

simpler version
'''
def find_rotation_point(words):
    # handling unrotated case
    if words[-1] >= words[0]:
        return 0
    
    left = 0
    right = len(words) - 1

    while left + 1 < right:
        mid = left + (right - left) // 2

        # if mid is in left sorted portion
        if words[mid] >= words[0]:
            left = mid
        else:
            right = mid
    
    return right
'''
words1 = ['k', 'v', 'a', 'b']

left = 0
right = 3

while 1 < 3:
mid = 1

left = 1
right 3

while 2 < 3:
mid = 2

right = 2
left = 1

return 2
'''