'''
input is message list of characters (not strings)
reverse order of the words in place;

message = ['c', 'a', 'k', 'e',' ',
            'p', 'o', 'u','n','d',' ',
            's','t','e','e','l']

reverse_words(message)

# prints: 'steel pound cake'
print(''.join(message))

assume: the message contains only letters and spaces, 
and all words are separated by one space
'''

'''
breakdown:
simpler problem: reverse all characters
def reverse_characters(message):
    pass

how can we use this to reveres words instead of characters?
notice:
1. how do we figure out where words begin and end?
2. once we know the start and end indices of two words, how do we swap those two words?

any problems with runtime? if we try to swap the words that aren't the same length?
it takes O(n) everytime we copy. total O(n^2) in the worst case

can we do better?
message: 'the eagle has landed'
revers_characters = 'dednal sah elgae eht'
reverse_words = 'landed has eagle the' # just use the reverse again on words
'''
def reverse_words(message):
    # first we reverese all the characters in the entire message
    reverese_characters(message, 0, len(message) - 1)

    # this gives us the right word order
    # but with each word backwards

    # now we'll make the words forward again
    # by reversing each word's characters

    # we hold the index of the start of the current word
    # as we look for the end of the current word
    current_word_start_index = 0

    for i in range(len(message) + 1):
        # found the end of the current word!
        if (i == len(message)) or (message[i] == ' '):
            reverese_characters(message, current_word_start_index, i-1)
            # if we haven't exhausted the message out
            # next word's start is one character ahead
            current_word_start_index = i + 1

def reverese_characters(message, left_index, right_index):
    # walk towards the middle, from both sides
    while left_index < right_index:
        # swap the left char and right char
        message[left_index], message[right_index] = \
            message[right_index], message[left_index]
        
        left_index += 1
        right_index -= 1

'''
O(n) time
O(1) space

Bonus: how would you handle punctuation?

what we learned?
the naive solution of replacing the words had a worst case O(n^2) runtime

solving a simpler version and see if it gets us closer to the solution
'''