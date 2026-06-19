### question
You are given a string `s` consisting of only uppercase english characters and an integer `k`. You can choose up to `k` characters of the string and replace them with any other uppercase English character.
After performing at most `k` replacements, return the length of the longest substring which contains only one distinct character.

### 1. Restating the Question

Given string `s` of uppercase letters and integer `k`. Find longest contiguous substring of identical characters achievable by changing at most `k` characters. Return its length.

### 2. Clarifying Questions & I/O

* **Input:** `s` (uppercase A-Z), `k` (integer >= 0).
* **Output:** Integer (max length).
* **Questions:**
* Can `k` exceed `s` length? Yes, max length is then `len(s)`.
* Empty string? Assume length >= 1 based on standard constraints.



### 3. Hand Trace Example

Input: `s = "AABABBA"`, `k = 1`.

* Look at "AAB". 1 'B'. Change to 'A'. Result "AAA". Valid, length 3.
* Look at "AABA". 1 'B'. Change to 'A'. Result "AAAA". Valid, length 4.
* Look at "AABAB". 2 'B's. Need 2 changes. Invalid since `k=1`.
* Look at "BABB". 1 'A'. Change to 'B'. Result "BBBB". Valid, length 4.
* Max valid length found: 4.

### 4. Brainstorming & Complexity

* **Idea 1: Brute Force.** Generate all substrings. For each, find most frequent character count (`maxf`). If `length - maxf <= k`, it's valid. Update max length.
* *Complexity:* Time O(N^2) or O(N^3). Space O(1) (26 letters). Too slow.


* **Idea 2: Sliding Window.** (Matches hand trace). Expand window right. Track character frequencies in window. If replacements needed (`window length - max frequent char > k`) exceed `k`, shrink window from left.
* *Complexity:* Time O(N). Space O(1).



### 5. Suggest Solutions

Prefer Sliding Window. Directly models how human intuitively scans the string left-to-right, remembering character counts and pulling the left boundary forward when rule breaks (too many oddball characters to swap).

### 6. Outline of Implementation

```python
def characterReplacement(s: str, k: int) -> int:
    """
    Reframe: Find longest window where (window_length - most_frequent_char_count) <= k.
    State: frequency map, chosen because we need to know the dominant character count to calculate required replacements.
    Invariant: Window is strictly valid, or maintains maximum size seen so far while searching for a better valid window.

    getMostFrequentCount() = scans frequency map and returns highest value.
    needsTooManyReplacements() = checks if current window size minus most frequent count strictly exceeds k.

    Core logic:
    - expand right side of window, record new character in frequency map
    - while window needs too many replacements to be uniform:
        - remove left character from frequency map
        - shrink window from left
    - record maximum window size seen
    
    Edge cases:
    - k >= length of string
    - string length is 1
    """

```

### 7. Iterative Implementation

**Iteration 1: Skeleton with Stubs**

```python
def characterReplacement(s: str, k: int) -> int:
    # TODO: init state
    
    # Core logic outline
    # for each character sliding right:
        # update state
        # while needsTooManyReplacements():
            # shrink left
        # update max
        
    return 0

```

**Iteration 2: Adding sliding window mechanics (using dummy helpers)**

```python
def characterReplacement(s: str, k: int) -> int:
    counts = {} # frequency map
    left = 0
    max_len = 0
    
    for right in range(len(s)):
        char = s[right]
        counts[char] = counts.get(char, 0) + 1 # record right char
        
        # While loop to shrink if invalid
        while needsTooManyReplacements(left, right, counts, k):
            left_char = s[left]
            counts[left_char] -= 1 # remove left char
            left += 1
            
        max_len = max(max_len, right - left + 1)
        
    return max_len

```

**Iteration 3: Implementing helpers into core logic**
*Change: Replace `needsTooManyReplacements` with actual math. `window_len = right - left + 1`. `maxf = max(counts.values())`.*

```python
def characterReplacement(s: str, k: int) -> int:
    counts = {}
    left = 0
    max_len = 0
    
    for right in range(len(s)):
        counts[s[right]] = counts.get(s[right], 0) + 1
        
        # calculate max frequency in current window
        maxf = max(counts.values()) 
        window_len = right - left + 1
        
        # check if replacements needed > k
        while window_len - maxf > k:
            counts[s[left]] -= 1
            left += 1
            # recalculate window_len after shrink
            window_len = right - left + 1 
            # Note: technically maxf needs recalc here in strict while loop
            maxf = max(counts.values())
            
        max_len = max(max_len, right - left + 1)
        
    return max_len

```

**Iteration 4: Edge Cases & Final Core**
*Check edge cases:* `k >= len(s)` works (while loop never triggers). `len(s) == 1` works. Code is robust.

### 8. Complexity & Optimization

* **Current Complexity:** Time O(N * 26) because `max(counts.values())` scans 26 keys inside the loop. Space O(1) (26 characters max).
* **Optimization:** We don't need to strictly shrink the window in a `while` loop, nor do we need to recalculate `maxf` when shrinking. We only care about finding a *larger* window. If window is invalid, just shift the *entire* window right by incrementing `left` by 1 (turning `while` into `if`). The historic `maxf` acts as a watermark.

**Optimized Code (The "Clever" Trick for Performance):**

```python
def characterReplacement(s: str, k: int) -> int:
    counts = {}
    left = 0
    max_len = 0
    max_f = 0 # Historical max frequency
    
    for right in range(len(s)):
        counts[s[right]] = counts.get(s[right], 0) + 1
        max_f = max(max_f, counts[s[right]]) # Only check newly added char
        
        # If invalid, shift window (don't shrink, just maintain size)
        # Because we only care about beating the historical max_f + k size
        if (right - left + 1) - max_f > k:
            counts[s[left]] -= 1
            left += 1
            
        max_len = max(max_len, right - left + 1)
        
    return max_len

```

*Optimized Complexity:* Time strictly O(N). Space strictly O(1).