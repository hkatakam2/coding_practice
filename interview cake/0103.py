'''
Write an efficient function that checks whether any permutation of 
an input string is a palindrome. 

bruteforce: check every permutation of the input string.
time?
1. We'd have to generate every permutation of the input string. 
If the string has n characters, then there are n choices for the 
first character, n - 1 choices for the second character, and so on. 
In total, that's n! permutations.
2. We'd have to check each permutation to see if it's a palindrome. 
That takes O(n) time per permutation, since each permutation is n letters.
Together, that's O(n! * n) time. Yikes! We can do better.
'''

'''
Let's try rephrasing the problem. How can we tell if any permutation 
of a string is a palindrome?
We can simply check that each character appears an even number of times
(unless there is a middle character, which can appear once or some other
 odd number of times).

So we'll go through all the characters and track how many times each 
character appears in the input string. Then we just have to make sure 
no more than one of the characters appears an odd numbers of times.

O(n) time; but can we still clean out solution up a little?
We don't really care how many times a character appears in the string, 
we just need to know whether the character appears an even or odd number of times.

What if we just track whether or not each character appears an odd number of times?
Then we can map characters to booleans. 
This will be more explicit (we don't have to check each number's parity, we already have booleans)

Can we take this a step further and clean it up even more?
Even more specifically than whether characters appear an even or 
odd number of times, we really just need to know there isn't more than 
one character that appears an odd number of times.

What if we only track the characters that appear an odd number of times? 
Is there a data structure even simpler than a dictionary we could use?

We could use a set, adding and removing characters as we look through the input string, 
so the set always only holds the characters that appear an odd number of times.
'''

def has_palindrome_permutation(the_string):
    # track characters we've seen an odd number of times
    unpaired_characters = set()

    for char in the_string:
        if char in unpaired_characters:
            unpaired_characters.remove(char)
        else:
            unpaired_characters.add(char)
    # the string has a palindrome permutation if it 
    # has one or zero characters without a pair
    return len(unpaired_characters) <= 1

'''
O(n) time
O(n) space

we can do this in less elegant way using character counting
'''
def has_palindrome_permutation(the_string):
    # count frequency of each character
    char_counts = {}

    # build a frequency map
    for char in the_string:
        char_counts[char] = char_counts.get(char, 0) + 1

    # count characters with odd frequencies
    odd_count = 0
    for count in char_counts.values():
        if count % 2 != 0:
            odd_count += 1
            # early exit
            if odd_count > 1:
                return False
    return True

