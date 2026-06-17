### question
Given a string `s`, return `true` if it is a palindrome, otherwise return `false`.
A palindrome is a string that reads the same forward and backward. It is also case-insensitive and ignores all non-alphanumeric characters.
Note: Alphanumeric characters consist of letters `(A-Z, a-z)` and numbers `(0-9)`.

### 1. Restate Question

Given string `s`. Return `true` if palindrome, `false` otherwise.
Conditions: Case-insensitive. Ignore non-alphanumeric chars.

### 2. Clarifying Questions

* Empty string? *Assume true (reads same forward/back).*
* String with only spaces/punctuation (e.g., `"  .,  "`)? *Assume true (becomes empty string after filtering).*
* Character set? *Assume standard ASCII (A-Z, a-z, 0-9).*

### 3. Example by Hand

Input: `s = "A man, a plan, a canal: Panama"`

* Filter & lowercase: `"amanaplanacanalpanama"`
* Reverse it: `"amanaplanacanalpanama"`
* Compare: `"amanaplanacanalpanama" == "amanaplanacanalpanama"` -> `true`.

Input: `s = "race a car"`

* Filter & lowercase: `"raceacar"`
* Reverse it: `"racaecar"`
* Compare: `"raceacar" == "racaecar"` -> `false`.

### 4. Brainstorming & Complexity

* **Idea 1: Clean, Reverse, Compare.** (Manual step above). Create new string/list with only valid chars, lowercase. Reverse it. Compare.
* Time: O(N) to traverse and filter, O(N) to reverse. Total O(N).
* Space: O(N) for the new filtered string.


* **Idea 2: Two Pointers.** Left pointer at start, right at end. Move inward. Skip non-alphanumeric chars. Compare at each step.
* Time: O(N) single pass.
* Space: O(1) no extra structures created.



### 5. Suggest Solutions

Prefer simple/straightforward.
Solution A: The manual trace (Idea 1). Filter string, build clean version, compare to reverse. Easy to explain, zero complex pointer logic.
Solution B: Two pointers (Idea 2). Optimal space, but slightly more complex loop logic.

Selecting **Solution A** for core implementation to maximize readability. Will address Solution B in optimization step.

### 6. Outline

```python
def isPalindrome(s: str) -> bool: 
    """
    Reframe: Strip noise, check if sequence perfectly reflects.
    State: Filtered array of characters, chosen because string immutability in Python makes direct string concatenation slow.
    Invariant: Filtered sequence strictly contains alphanumeric lowercase chars.

    is_valid(c) = checks if char is letter or number.
    lower(c) = converts char to lowercase.

    Core logic:
    - gather all valid characters from input sequence into a cleaned list
    - convert gathered characters to lowercase
    - reverse the cleaned list
    - check if original cleaned list equals the reversed list
    
    Edge cases:
    - empty string input
    - string containing no valid alphanumeric characters
    """

```

### 7. Iterative Implementation

**Iteration 1: Skeleton with stubs**

```python
def isPalindrome(s: str) -> bool:
    # 1. Gather valid, lowercased chars
    cleaned = get_clean_chars(s)
    
    # 2. Reverse
    reversed_cleaned = reverse_sequence(cleaned)
    
    # 3. Compare
    return cleaned == reversed_cleaned

def get_clean_chars(s: str) -> list:
    pass

def reverse_sequence(seq: list) -> list:
    pass

```

**Iteration 2: Implement cleaning logic**

```python
def isPalindrome(s: str) -> bool:
    cleaned = []
    for char in s:
        if char.isalnum():          # check if alphanumeric
            cleaned.append(char.lower()) # convert to lowercase and store
            
    # TODO: reverse and compare
    reversed_cleaned = reverse_sequence(cleaned)
    return cleaned == reversed_cleaned

```

**Iteration 3: Implement reverse and compare (Pythonic)**

```python
def isPalindrome(s: str) -> bool:
    # Build clean list
    cleaned = []
    for char in s:
        if char.isalnum():
            cleaned.append(char.lower())
            
    # Reverse and compare using slice
    return cleaned == cleaned[::-1] 

```

**Walk Edge Cases:**

* *Empty string*: `s = ""` -> `cleaned` is `[]`. `[] == []` is `True`. Works.
* *No alphanumeric*: `s = "  ., "` -> loop skips all chars -> `cleaned` is `[]`. `[] == []` is `True`. Works.

### 8. Complexity & Optimization

**Complexity of current solution:** - Time: O(N). Iterating through string once. String slicing `[::-1]` is also O(N).

* Space: O(N). Creating an array `cleaned` proportional to length of string.

**Optimization (O(1) Space using Two Pointers):**
Expensive section in current code is memory allocation for the `cleaned` list. We can avoid allocating memory by using two pointers reading from opposite ends of the original string.

```python
def isPalindrome(s: str) -> bool:
    left, right = 0, len(s) - 1
    
    while left < right:
        # Move left pointer to next alphanumeric char
        while left < right and not s[left].isalnum():
            left += 1
            
        # Move right pointer to previous alphanumeric char
        while left < right and not s[right].isalnum():
            right -= 1
            
        # Compare
        if s[left].lower() != s[right].lower():
            return False
            
        # Move both inwards
        left += 1
        right -= 1
        
    return True

```

*Comment:* Time remains O(N). Space drops to O(1). Complexity added: nested `while` loops to skip noise, must ensure `left < right` bounds are maintained inside inner loops to prevent index out of bounds.