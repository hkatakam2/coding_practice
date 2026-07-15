'''
Write code that takes a long string and builds its word cloud data 
in a dictionary, where the keys are words and the values are the 
number of times the words occurred.

Assume the input will only contain words and standard punctuation.
Eg: 'Add milk and eggs, then add flour and sugar.'

Breakdown:
This challenge has several parts. Let's break them down.
1. Splitting the words from the input string
2. Populating the dictionary with each word
3. Handling words that are both uppercase and lowercase in the input string

'''
def split_words(input_string):
    words = []
    current_word_start_index = 0
    current_word_length = 0

    for i, char in enumerate(input_string):
        if char.isalpha():
            if current_word_length == 0:
                current_word_start_index = i
            current_word_length += 1
        else:
            word = input_string[current_word_start_index : 
                                current_word_start_index + current_word_length]
            words.append(word)
            current_word_length = 0

    return words
'''
It is good but It doesn't work perfectly yet-you'll need to add code to handle the 
end of the input string, hyphenated words, punctuation, and edge cases.

The next part is populating our dictionary with unique words. 
What do we do with each word?

'''
words_to_counts = {}

def add_word_to_dictionary(word):
    if word in words_to_counts:
        words_to_counts[word] += 1
    else:
        words_to_counts[word] = 1
'''
Alright, last part! 
How should we handle words that are uppercase and lowercase?
'''
class WordCloudData:

    def __init__(self, input_string):
        self.words_to_counts = {}
        self.populate_words_to_counts(input_string)

    def populate_words_to_counts(self, input_string):
        # iterate over each character in the input string, splitting
        # words and passing them to add_word_to_dictionary()
        current_word_start_index = 0
        current_word_length = 0

        for i, character in enumerate(input_string):
            # if we reached the end of the string we check if the last
            # character is a letter and add the last word to our dictionary
            if i == len(input_string) - 1:
                if character.isalpha():
                    current_word_length += 1
                if current_word_length > 0:
                    current_word = input_string[current_word_start_index:
                                                current_word_start_index + current_word_length]
                    self.add_word_to_dictionary(current_word)

            # if we reach a space or emdash we know we're at the end of a word
            # so we add it to our dictionary and reset our current word
            elif character == '' or character == '\u2014':
                if current_word_length > 0:
                    current_word = input_string[current_word_start_index:
                                                current_word_start_index + current_word_length]
                    self.add_word_to_dictionary(current_word)
                    current_word_length = 0
            # if the character is a letter or an apostrophe, we add it to our current word
            elif character.isalpha() or character == '\'':
                if current_word_length == 0:
                    current_word_start_index = i
                current_word_length += 1
            # if the character is a hyphen, we want to check if it's surrounded by letters
            # if it is, we add it our current word
            elif character == '-':
                if i > 0 and input_string[i-1].isalpha() and \
                        input_string[i+1].isalpha():
                    current_word_length += 1
                else:
                    if current_word_length > 0:
                        current_word = input_string[current_word_start_index:
                                                    current_word_start_index + current_word_length]
                        self.add_word_to_dictionary(current_word)
                        current_word_length = 0

    def add_word_to_dictionary(self, word):
        # if the word is already in the dictionary we increment its count
        if word in self.words_to_counts:
            self.words_to_counts[word] += 1

        # If a lowercase version is in the dictionary, we know our input word must be uppercase
        # but we only include uppercase words if theyke always uppercase
        # so we just increment the lowercase version's count
        elif word.lower() in self.words_to_counts:
            self.words_to_counts[word.lower()] += 1

        # If an uppercase version is in the dictionary, we know our input word must be lowercase.
        # since we only include uppercase words if they're always uppercase, we add the
        # lowercase version and give it the uppercase version's count
        elif word. capitalize() in self.words_to_counts:
            self.words_to_counts[word] = 1
            self.words_to_counts[word] += self.words_to_counts[word.capitalize]
            del self.words_to_counts[word.capitalize()]
        # Otherwise, the word is not in the dictionary at all, lowercase or uppercase
        # so we add it to the dictionary
        else:
            self.words_to_counts[word] = 1

'''
Runtime and memory cost are both O(n).

Bonus:
1. We haven't explicitly talked about how to handle more complicated 
character sets. How would you make your solution work with more unicode 
characters? What changes need to be made to handle silly sentences like these:
2. We limited our input to letters, hyphenated words and punctuation. 
How would you expand your functionality to include numbers, email addresses, twitter handles, etc.?
3. How would you add functionality to identify phrases or words that 
belong together but aren't hyphenated? ("Fire truck" or "Interview Cake")
4. How could you improve your capitalization algorithm?
5. How would you avoid having duplicate words that are just plural or 
singular possessives?
'''


'''
Alternate approach:

This code will:

Remove all special characters and convert to lowercase
Split words based on spaces
Count word frequencies in a dictionary
'''
def create_word_cloud(input_string):
    # Step 1: Process the raw string
    # Remove special characters and convert to lowercase
    processed_string = ''
    for char in input_string:
        if char.isalpha() or char.isspace():
            processed_string += char.lower()
        
    # Step 2: Split the string into words
    words = processed_string.split()
    
    # Step 3: Count frequency using dictionary
    word_cloud = {}
    for word in words:
        if word in word_cloud:
            word_cloud[word] += 1
        else:
            word_cloud[word] = 1
            
    return word_cloud

# Test the function
test_string = 'Add milk and eggs, then add flour and sugar.'
result = create_word_cloud(test_string)
print(result)
'''
If you need to handle more complex cases like:

Hyphenated words
Apostrophes
Special Unicode characters
Proper nouns (capitalization)
'''
# First, let's handle hyphenated words and apostrophes:
def create_word_cloud(input_string):
    # Step 1: Process the raw string
    # Keep hyphens and apostrophes if they're between letters
    processed_string = ''
    for i, char in enumerate(input_string):
        # Keep letters and spaces
        if char.isalpha() or char.isspace():
            processed_string += char.lower()
        # Keep hyphens between letters
        elif char == '-' and i > 0 and i < len(input_string) - 1:
            if input_string[i-1].isalpha() and input_string[i+1].isalpha():
                processed_string += char
        # Keep apostrophes between letters
        elif char == "'" and i > 0 and i < len(input_string) - 1:
            if input_string[i-1].isalpha() and input_string[i+1].isalpha():
                processed_string += char
    
    # Step 2: Split the string into words
    words = processed_string.split()
    
    # Step 3: Count frequency using dictionary
    word_cloud = {}
    for word in words:
        if word in word_cloud:
            word_cloud[word] += 1
        else:
            word_cloud[word] = 1
            
    return word_cloud


# Now let's add proper noun handling:

def create_word_cloud(input_string):
    # Step 1: Process the raw string
    processed_string = ''
    for i, char in enumerate(input_string):
        if char.isalpha() or char.isspace():
            processed_string += char
        elif char == '-' and i > 0 and i < len(input_string) - 1:
            if input_string[i-1].isalpha() and input_string[i+1].isalpha():
                processed_string += char
        elif char == "'" and i > 0 and i < len(input_string) - 1:
            if input_string[i-1].isalpha() and input_string[i+1].isalpha():
                processed_string += char
    
    # Step 2: Split the string into words
    words = processed_string.split()
   
    # Step 3: Count frequency using dictionary with case handling
    word_cloud = {}
    for word in words:
        # Convert to lowercase unless it's a proper noun
        # (starts with capital and rest lowercase)
        if word.istitle() and len(word) > 1 and word[1:].islower():
            # Keep proper nouns as-is
            normalized_word = word
        else:
            normalized_word = word.lower()
            
        if normalized_word in word_cloud:
            word_cloud[normalized_word] += 1
        else:
            word_cloud[normalized_word] = 1
            
    return word_cloud

# Let's test the improved version:
# Test cases
test_cases = [
    "I love my mother-in-law's cooking",  # hyphenated words and apostrophe
    "New York is in America",  # proper nouns
    "I'm going to Sam's house",  # apostrophe
    "Python-based programming",  # hyphenated
]

for test in test_cases:
    print(f"\nInput: {test}")
    print(f"Word Cloud: {create_word_cloud(test)}")
'''
This improved version will:

Keep hyphenated words together (e.g., "mother-in-law")
Preserve apostrophes in contractions and possessives
Preserve proper nouns (like "New York", "America")
Still handle basic word counting
For Unicode characters, the code already works with them since Python 3 
'''