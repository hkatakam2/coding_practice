# question
Machine String Type Reduction: Given a string where a machine's "type" is defined by its first and last character (e.g., "abade" has type "ae"), find the maximum number of characters you can remove from either the prefix or suffix without changing the machine's type

Restated: given s with type (s[0], s[-1]), trim a prefix and/or suffix so the remaining string still has the same type, and maximize the number of characters trimmed.

# clarifications
1. removing prefix, suffix mean we have to trim; not delete random characters
2. can I trim both ends? yes seperately
3. must something remain? single character "a" -> "aa"? yes
4. empty string? return 0


# ideas:
reframe: any result is window s[i:j] . s[i] = a, s[j] = b; original s[0]= a, s[-1]=b
we need maximize the trimming means i and j must be closer; (j - i) must be minimized
1. brute force calculate all (i,j) pairs
2. precompute: collect all positions of a, b and then for each b we can find the nearest a to the left with binary search. O(n logn)
3. single pass: scan from left to right; remember the recent a. each time we hit b we get the (j-i) just return the minimum

# outline
max_removable(s):
    a, b = types_of(s)
    best_span = shortest_window_span(s,a,b) 
    return removed_count(n, best_span) # n - 1 - span
shortest_window_span(s, a, b):
    last_a = "none seen yet"
    best = full-string span
    for each char at idx:
        if char is b and an 'a' was seen:
            best = min(best, idx - last_a) # closest start for this end
        if char is a:
            last_a = idx
    return best

```python
def max_removable(s: string):

    a, b = s[0], s[-1]
    best_span = len(s) - 1
    
    last_a = None

    for idx, ch in enumerate(s):
        if ch == b and last_a is not None:
            best_span = min(best_span, idx - last_a)
        if ch == a:
            last_a = idx

    return len(s) - 1 - best_span

```
# edge cases
1. a == b; this is missing; 

```python
def max_removable(s: str) -> int:
    # Edge: empty string -> nothing to remove
    if not s:
        return 0

    # a, b = type_of(s)                    # first and last char
    a, b = s[0], s[-1]

    # best_span = full-string span (always a valid window -> covers "no removal possible")
    best_span = len(s) - 1
    # last_a = "none seen yet"
    last_a = None

    # for each char at idx:
    for idx, ch in enumerate(s):
        # Edge (a == b): update last_a FIRST so a single char can serve as
        # both start and end of the window (span 0).
        # if char is a:
        if ch == a:
            last_a = idx                       # last_a = idx

        # if char is b and an 'a' was seen:    (guards b-before-any-a)
        if ch == b and last_a is not None:
            # best = min(best, idx - last_a)   # closest start for this end
            best_span = min(best_span, idx - last_a)

    # return removed_count(n, best_span)       # n - 1 - span
    return len(s) - 1 - best_span


# Quick tests
assert max_removable("abade") == 2     # keep "ade"
assert max_removable("") == 0
assert max_removable("a") == 0
assert max_removable("aa") == 1        # same-char type: keep one 'a'
assert max_removable("abca") == 3
assert max_removable("abc") == 0       # only the full string works
assert max_removable("axbxaxb") == 4   # keep "axb"
assert max_removable("abxab") == 3     # keep "ab"
```
max_removable(s):
    a, b = type_of(s)
    last_a = 0                       # s[0] is always an 'a'
    best = full-string span
    for each char at idx:
        if char is a: last_a = idx
        if char is b: best = min(best, idx - last_a)
    return n - 1 - best

```python
def max_removable(s: str) -> int:
    # Edge: empty string -> nothing to remove
    if not s:
        return 0

    # a, b = type_of(s)
    a, b = s[0], s[-1]

    # last_a = 0   (s[0] is always an 'a', so a start always exists)
    last_a = 0
    # best = full-string span (always valid -> covers "no removal possible")
    best_span = len(s) - 1

    # for each char at idx:
    for idx, ch in enumerate(s):
        # if char is a: last_a = idx
        if ch == a:
            last_a = idx
        # if char is b: best = min(best, idx - last_a)
        if ch == b:
            best_span = min(best_span, idx - last_a)

    # return n - 1 - best
    return len(s) - 1 - best_span
```
