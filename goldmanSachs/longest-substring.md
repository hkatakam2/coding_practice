## 1. Restate

We need the length of the longest **contiguous substring** where every character is unique.

Example:

```text
s = "abcabcbb"

"abc" -> all unique -> length 3
"abca" -> duplicate 'a' -> invalid

answer = 3
```

Key word: **substring**, so characters must stay contiguous.

---

## 2. Clarifying questions

In interview:

* Can `s` be empty? → yes, return `0`.
* Are spaces/symbols valid characters? → yes.
* Do we return the substring or only its length? → only length.
* Case-sensitive? → normally yes: `'A' != 'a'`.

---

## 3. Work an example by hand

Take:

```text
s = "pwwkew"
```

Maintain a current window containing no duplicates.

```text
char    window       action                best
-------------------------------------------------
p       "p"          add p                   1
w       "pw"         add w                   2
w       "w"          duplicate w:
                     remove from left        2
k       "wk"         add k                   2
e       "wke"        add e                   3
w       "kew"        duplicate w:
                     move left past old w    3
```

Answer:

```text
3
```

---

# 4. Brainstorm solutions

### Solution 1: brute force

Generate every possible substring and check whether it contains duplicate characters.

```text
start every possible position
    end every possible position
        check whether substring has duplicates
```

There are `O(n²)` substrings.

Checking each substring can cost `O(n)`.

```text
Time: O(n³)
Space: O(n)
```

We can improve checking incrementally using a set:

```text
for each starting position:
    create empty set

    extend substring one character at a time

    once duplicate appears:
        stop
```

This becomes:

```text
Time: O(n²)
Space: O(n)
```

---

## Solution 2: sliding window

Instead of restarting from scratch, maintain one valid substring.

```text
[left ........ right]
```

Invariant:

> everything currently inside the window is unique.

When the next character is new:

```text
expand right
```

When the next character is already present:

```text
shrink from left until duplicate disappears
```

Each character enters the window at most once and leaves at most once.

```text
Time: O(n)
Space: O(n)
```

This is the cleanest interview solution.

---

# 5. Selected solution

Use:

```text
sliding window + HashSet
```

Example:

```text
abcabcbb
^^^
abc

next = a
duplicate

remove characters from left until old a disappears

 bc
  ^ next a

window becomes:
bca
```

We never need to reconsider characters that are already permanently left of the window.

---

# 6. Implementation outline

```python
def lengthOfLongestSubstring(s: str) -> int:
    """
    Reframe:
    Keep the largest contiguous window whose characters are all unique.

    State:
    - window_chars: set of characters currently in the window
    - left: beginning of current valid window
    - best: largest valid window length seen

    Set chosen because:
    - we need fast detection of whether the next character
      already exists in the current substring.

    Invariant:
    The substring between left and the current right position
    contains no duplicate characters.

    Core logic:
    - move the right side through the string
    - if the new character already exists in the window:
        shrink the left side until that character disappears
    - add the new character
    - update the largest valid window length

    Edge cases:
    - empty string
    - one character
    - every character identical
    - every character unique
    - duplicate appears immediately
    - duplicate appears far inside the current window
    - spaces/symbols
    """
```

---

# 7. Iterative implementation

## Iteration 1: skeleton

```python
def lengthOfLongestSubstring(s: str) -> int:
    left = 0
    window_chars = set()
    best = 0

    for right in range(len(s)):
        # remove duplicates if necessary

        # add current character

        # update best

    return best
```

---

## Iteration 2: happy path

Suppose there are no duplicates.

```python
def lengthOfLongestSubstring(s: str) -> int:
    left = 0
    window_chars = set()
    best = 0

    for right in range(len(s)):
        window_chars.add(s[right])

        current_length = right - left + 1
        best = max(best, current_length)

    return best
```

For:

```text
"abcde"
```

this correctly returns:

```text
5
```

But it breaks for:

```text
"abcabc"
```

because duplicates remain in our set/window.

---

## Iteration 3: handle duplicates

Before adding the current character:

```python
while s[right] in window_chars:
```

remove characters from the left.

```python
def lengthOfLongestSubstring(s: str) -> int:
    left = 0
    window_chars = set()
    best = 0

    for right in range(len(s)):

        # NEW: restore the unique-window invariant
        while s[right] in window_chars:
            window_chars.remove(s[left])
            left += 1

        window_chars.add(s[right])

        current_length = right - left + 1
        best = max(best, current_length)

    return best
```

Core solution is now complete.

---

# 8. Walk through edge cases

### Empty string

```python
s = ""
```

Loop never executes.

```text
best = 0
```

Correct.

---

### Single character

```text
"a"
```

```text
window = "a"
best = 1
```

Correct.

---

### All duplicates

```text
"bbbbb"
```

Each new `b` causes the previous `b` to leave.

```text
window always = "b"
best = 1
```

Correct.

---

### All unique

```text
"abcdef"
```

No shrinking.

```text
best = 6
```

Correct.

---

### Important duplicate case

```text
"abba"
```

Let's trace carefully:

```text
right = a
window = a
best = 1

right = b
window = ab
best = 2

right = b
duplicate

remove a
window = b

still duplicate

remove b
window = empty

add b
window = b

right = a
window = ba

best = 2
```

Correct.

The `while`, rather than `if`, is important.

---

# Final implementation

```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        left = 0
        window_chars = set()
        best = 0

        for right in range(len(s)):
            # Shrink until current character can safely enter.
            while s[right] in window_chars:
                window_chars.remove(s[left])
                left += 1

            window_chars.add(s[right])

            current_length = right - left + 1
            best = max(best, current_length)

        return best
```

## Complexity

The interesting part is:

```python
while s[right] in window_chars:
    window_chars.remove(s[left])
    left += 1
```

It looks nested, but it is **not `O(n²)`**.

`right` moves forward at most `n` times.

`left` also moves forward at most `n` times.

No pointer ever moves backward.

Therefore:

```text
Time:  O(n)
Space: O(min(n, character-set-size))
```

### Interview one-line explanation

> I maintain a sliding window containing only unique characters. I expand the right boundary normally, and whenever a duplicate enters, I shrink from the left until the duplicate is removed. Since each character enters and leaves the window at most once, the solution is O(n).
