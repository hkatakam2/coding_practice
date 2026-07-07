'''
UTF-8 is a character encoding that maps each symbol to one, two, three, or four bytes.

For example, the Euro sign, €, corresponds to the three bytes 11100010 10000010 10101100. The rules for mapping characters are as follows:

For a single-byte character, the first bit must be zero.
For an n-byte character, the first byte starts with n ones and a zero. The other n - 1 bytes all start with 10.

Bytes   |           Byte format
-----------------------------------------------
   1     | 0xxxxxxx
   2     | 110xxxxx 10xxxxxx
   3     | 1110xxxx 10xxxxxx 10xxxxxx
   4     | 11110xxx 10xxxxxx 10xxxxxx 10xxxxxx


Write a program that takes in an array of integers representing byte values, and returns whether it is a valid UTF-8 encoding.

breakdown:

'''

def validate_utf8(data):
    def get_number_of_bytes(byte):
        # Check number of leading 1s
        if (byte & 0b10000000) == 0:  # starts with 0
            return 1
        elif (byte & 0b11100000) == 0b11000000:  # starts with 110
            return 2
        elif (byte & 0b11110000) == 0b11100000:  # starts with 1110
            return 3
        elif (byte & 0b11111000) == 0b11110000:  # starts with 11110
            return 4
        return 0  # Invalid starting byte

    def is_valid_following_byte(byte):
        # Check if byte starts with 10
        return (byte & 0b11000000) == 0b10000000

    index = 0
    while index < len(data):
        # Get first byte
        first_byte = data[index]
        num_bytes = get_number_of_bytes(first_byte)
        
        # Validate number of bytes
        if num_bytes == 0 or num_bytes > 4:
            return False
            
        # Check if we have enough bytes
        if index + num_bytes > len(data):
            return False
            
        # Validate following bytes
        for i in range(1, num_bytes):
            if not is_valid_following_byte(data[index + i]):
                return False
                
        index += num_bytes
        
    return True

# Test cases
test_cases = [
    ([197, 130, 1], True),  # valid 2-byte char followed by 1-byte char
    ([235, 140, 4], False),  # invalid because 4 is not a valid following byte
    ([240, 162, 138, 147], True),  # valid 4-byte char
    ([145], False),  # invalid start byte
]

for data, expected in test_cases:
    result = validate_utf8(data)
    print(f"Input: {data}, Expected: {expected}, Got: {result}")

'''
4. Complexity Analysis
Time Complexity: O(n) where n is the length of the input array
We scan through each byte exactly once
Bit operations are O(1)
Space Complexity: O(1)
We only use a constant amount of extra space

5. Key Insights

Bit Manipulation:

Use bit masks to check byte patterns:
& operator for checking specific bit patterns
Numbers in binary format (0b11000000) for clarity

Sequential Processing:

Process bytes sequentially
Need to keep track of current position
Skip appropriate number of bytes based on first byte

Error Conditions:

Invalid starting byte
Not enough following bytes
Invalid following bytes
Total sequence must be complete
'''