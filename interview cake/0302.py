'''
find duplicate in a list of integers 
1. integers are in the range 1..n
2. the list has a length of n+1

our list has at least one integer which appears at least twice. 
But it may have several duplicates, and each duplicate may appear 
more than twice.

optimize for space

Breakdown:
We just do one walk through the list, using a set to keep track 
of which items we've seen!
'''
def find_repeat(numbers):
    numbers_seen = set()

    for number in numbers:
        if number in numbers_seen:
            return number
        else:
            numbers_seen.add(number)
    # whoops -- no duplicate
    raise Exception('no duplicate!')
'''
O(n) time and O(n) space;
how to get O(1) space?

bruteforce: by taking each number in the range 1..n and, for each, 
walking through the list to see if it appears twice.
'''
def find_repeat_brute_force(numbers):
    for needle in range(1, len(numbers)):
        has_been_seen = False
        for number in numbers:
            if number == needle:
                if has_been_seen:
                    return number
                else:
                    has_been_seen = True
    # whoops -- no duplicate
    raise Exception('no duplicate!')
'''
O(1) space but O(n^2) time

we can do better by sorting O(n lg n)
1. Do an in-place sort of the list (for example an in-place merge sort).
2. Walk through the now-sorted list from left to right.
3. Return as soon as we find two adjacent numbers which are the same.

but modifying the input is kind of a drag -- it might cause problems elsewhere
can we maintain this time and space without modifying the input?

Solution:
Our approach is similar to a binary search, except we divide the range 
of possible answers in half at each step, rather than dividing the list
in half.
1. Find the number of integers in our input list which lie within the 
range 1..n/2•
2. Compare that to the number of possible unique integers in the same 
range.
3. If the number of actual integers is greater than the number of 
possible integers, we know there's a duplicate in the range 1..n/2, 
so we iteratively use the same approach on that range.
4. If the number of actual integers is not greater than the number of 
possible integers, we know there must be duplicate in the range (n+1)/2..n, 
so we iteratively use the same approach on that range.
5. At some point, our range will contain just 1 integer, which will 
be our answer.
'''
def find_repeat(numbers):
    floor = 1
    ceiling = len(numbers) - 1

    while floor < ceiling:
        # Divide our range 1..n into an upper range and lower range
        # (such that they don't overlap)
        # Lower range is floor..midpoint
        # Upper range is midpoint+1..ceiling
        midpoint = floor + ((ceiling - floor) // 2)
        lower_range_floor, lower_range_ceiling = floor, midpoint
        upper_range_floor, upper_range_ceiling = midpoint+1, ceiling
        
        # Count number of items in lower range
        items_in_lower_range = 0
        for item in numbers:
            # Is it in the lower range?
            if item >= lower_range_floor and item <= lower_range_ceiling:
                items_in_lower_range += 1
        distinct_possible_integers_in_lower_range = (lower_range_ceiling - lower_range_floor + 1)
        if items_in_lower_range > distinct_possible_integers_in_lower_range:
            # There must be a duplicate in the lower range
            # so use the same approach iteratively on that range
            floor, ceiling = lower_range_floor, lower_range_ceiling
        else:
            # There must be a duplicate in the upper range
            # so use the same approach iteratively on that range
            floor, ceiling = upper_range_floor, upper_range_ceiling
    # Floor and ceiling have converged
    # We found a number that repeats!
    return floor
'''
O(1) space and O(n lg n) time.

Bonus:
if there are several duplicates, write a function to return all duplicates
'''
def find_all_duplicates(numbers):
    seen = set()
    duplicates = set()
    for number in numbers:
        if number in seen:
            duplicates.add(number)
        else:
            seen.add(number)
    return duplicates

def find_all_duplicates_sorted(numbers):
    if not numbers:
        return []
        
    numbers.sort()  # in-place sort
    duplicates = []
    
    for i in range(1, len(numbers)):
        if numbers[i] == numbers[i-1] and (i == len(numbers)-1 or numbers[i] != numbers[i+1]):
            duplicates.append(numbers[i])
    
    return duplicates

