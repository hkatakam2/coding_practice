### question
Given a string `s`, find the length of the longest substring without duplicate characters.
A substring is a contiguous sequence of characters within a string.

**1. Restating the Question**
Find longest continuous sequence of characters in string `s` that contains no repeating characters. Return its length.

**2. Clarifying Questions & Confirmations**

* **Input:** String `s`. Can contain any ASCII character (letters, numbers, symbols, spaces)? *Assume yes.*
* **Case sensitive?** 'a' and 'A' distinct? *Assume yes.*
* **Output:** Integer representing maximum length.
* **Empty string?** Return 0. *Confirmed.*

**3. Hand-Tracing an Example**
Input: `s = "abcabcbb"`

* `a`: valid, window="a", max=1
* `b`: valid, window="ab", max=2
* `c`: valid, window="abc", max=3
* `a`: duplicate! shrink left until 'a' removed. window="bca", max=3
* `b`: duplicate! shrink left until 'b' removed. window="cab", max=3
* `c`: duplicate! shrink left until 'c' removed. window="abc", max=3
* `b`: duplicate! shrink left. window="cb", max=3
* `b`: duplicate! shrink left. window="b", max=3
Result: 3.

**4. Brainstorming & Complexity**

* **Brute Force:** Generate all possible substrings. Check each for duplicates. Time: $O(N^3)$ or $O(N^2)$ depending on implementation. Space: $O(N)$. Too slow.
* **Sliding Window (Set):** Two pointers (left/right) form a window. Expand right. If duplicate, shrink left until duplicate gone. Track max. Time: $O(N)$. Space: $O(K)$ where $K$ is charset size.
* **Sliding Window (Dict):** Track exact indices of chars. On duplicate, jump left pointer directly to `index + 1`. Time: $O(N)$ (faster constant factor). Space: $O(K)$.

**5. Suggested Solutions**
Prefer simple, clear implementations.

1. Sliding Window with Set (matches our hand-trace in step 3). Easiest to conceptualize and explain (physically shrinking a window).
2. Sliding Window with Hash Map (Dict). Slightly more optimized but conceptually similar.
*Selection:* We will implement #1.

**6. Outline**

```python
def lengthOfLongestSubstring(s: str) -> int:
    """
    Reframe: Find longest valid window by dynamically adjusting left/right bounds.
    State: A 'seen' set, chosen because constant time O(1) lookups for duplicates. 
           Left and right pointers to define active window.
    Invariant: Substring between left and right pointer never contains duplicates.

    has_duplicate(char, seen_set) = checks if char is in our active window.
    remove_leftmost(left_ptr, seen_set) = removes character at left bound from set and advances left bound.
    add_rightmost(char, seen_set) = adds new char to set.
    update_max(current_len, max_len) = keeps track of biggest window seen.

    Core logic:
    - Traverse each character in string with a right pointer.
    - While the current character is a duplicate:
        - Shrink window from the left by removing the leftmost character.
    - Add the current character to our window.
    - Record the size of the window if it's the biggest we've seen.

    Edge cases:
    - Empty string.
    - String with all identical characters ("bbbbb").
    - String with all unique characters ("abcdef").
    """

```

**7. Iterative Implementation**

*Iteration 1: Skeleton*

```python
def lengthOfLongestSubstring(s: str) -> int:
    # initialize state (set, left pointer, max length)
    
    # loop right pointer through string
        
        # while current char is duplicate
            # remove leftmost char from set
            # move left pointer forward
            
        # add current char to set
        # calculate window size, update max
        
    # return max length

```

*Iteration 2: Translating skeleton to code chunks*

```python
def lengthOfLongestSubstring(s: str) -> int:
    seen = set()       # State: tracks unique chars in window
    left = 0           # State: left boundary of window
    max_len = 0        # State: longest found so far
    
    for right in range(len(s)):
        char = s[right]
        
        # while current char is duplicate
        while char in seen:
            seen.remove(s[left]) # remove leftmost char
            left += 1            # shrink window
            
        # add current char to set
        seen.add(char)
        
        # calculate window size, update max
        window_size = right - left + 1
        max_len = max(max_len, window_size)
        
    return max_len

```

*Iteration 3: Walking the Edge Cases*

* **Empty string (`""`):** `len(s)` is 0. Loop skipped. Returns `0`. Works perfectly.
* **All identical (`"bbbbb"`):** `seen` gets 'b'. Next 'b' triggers `while`. Removes old 'b', adds new 'b'. `window_size` stays 1. `max_len` remains 1. Works perfectly.
* **All unique (`"abc"`):** `while` never triggers. Adds chars to set. `max_len` increments up to 3. Works perfectly.
*No patching required. Core logic handles edge cases natively.*

**8. Complexity & Optimizations**

* **Time Complexity:** $O(N)$ where $N$ is length of `s`. Each character visited at most twice (once by `right` pointer, once by `left` pointer in the `while` loop).
* **Space Complexity:** $O(\min(N, M))$ where $M$ is size of character set (e.g., 128 for ASCII). This is the size of the `seen` set.
* **Optimization Commentary:** The `while` loop removes characters one by one. If input is `"abcdefggha"`, and we hit second `'a'`, `left` walks $O(N)$ steps to clear it. We can optimize to true $O(N)$ single-pass by storing the exact index of each character in a dictionary. When duplicate found, instantly jump `left` to `max(left, previously_seen_index + 1)`.

*Optimized Code (for reference):*

```python
def lengthOfLongestSubstring(s: str) -> int:
    seen_indices = {}
    left = 0
    max_len = 0
    
    for right in range(len(s)):
        char = s[right]
        
        if char in seen_indices:
            # Jump left pointer instantly, bypassing while-loop
            left = max(left, seen_indices[char] + 1)
            
        seen_indices[char] = right
        max_len = max(max_len, right - left + 1)
        
    return max_len

```