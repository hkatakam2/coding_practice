### question
You are given a string `s` consisting of the following characters: `'('`, `')'`, `'{'`, `'}'`, `'['` and `']'`.
The input string `s` is valid if and only if:

1. Every open bracket is closed by the same type of close bracket.
2. Open brackets are closed in the correct order.
3. Every close bracket has a corresponding open bracket of the same type.
Return `true` if `s` is a valid string, and `false` otherwise.

## 1. Restate

We need determine whether brackets are balanced.

A string is valid when:

- each closing bracket matches the most recent unmatched opening bracket
- bracket types match
- no opening or closing bracket remains unmatched

## 2. Clarifying questions

- Can `s` be empty? Assume yes; empty string is valid.
- Does `s` contain only the six listed characters? Yes.
- Return boolean, not text? Yes.
- Any size constraints? Not given; target linear time.

## 3. Example by hand

Input:

```text
s = "({[]})"
```

Process left to right:

```text
character   unmatched openings
(           (
{           ( {
[           ( { [
]           ( {       matches [
}           (         matches {
)           empty     matches (
```

Nothing remains unmatched, so return `True`.

Invalid example:

```text
s = "([)]"
```

When `)` arrives, the most recent opening bracket is `[`. Types differ, so return `False`.

## 4. Brainstorm solutions

### Repeated removal

Repeatedly remove:

```text
()
{}
[]
```

If the string becomes empty, valid.

- Simple idea
- Matches the manual cancellation process
- Worst case: `O(n²)` because each replacement may scan/rebuild the string
- Extra space: potentially `O(n)`

### Stack

Keep unmatched opening brackets in a stack.

- Opening bracket: push
- Closing bracket: compare against most recent opening
- Wrong type or empty stack: invalid
- End with nonempty stack: invalid

Complexity:

- Time: `O(n)`
- Space: `O(n)`

Selected: stack. Clear, direct, standard interview solution.

## 5. Solution insight

Correct closing order means every closing bracket must match the most recently seen unmatched opening bracket. That is exactly stack behavior: last in, first out.

## 6. Plain-English implementation outline

```python
def is_valid(s: str) -> bool:
    """
    Reframe: Every closing bracket must match the most recent unmatched
    opening bracket.

    State: A stack of unmatched opening brackets, chosen because bracket
    closing order is last-opened, first-closed.

    Invariant: After processing each character, the stack contains exactly
    the opening brackets not yet matched, in opening order.

    matchingOpening(closeBracket) = the opening bracket required by this
    closing bracket.

    Core logic:
    - start with no unmatched opening brackets
    - read each bracket from left to right
    - if it opens a pair, remember it
    - otherwise, inspect the most recent unmatched opening bracket
    - if none exists or its type differs, return false
    - remove the matched opening bracket
    - after reading everything, return whether nothing remains unmatched

    Edge cases:
    - empty string
    - string begins with a closing bracket
    - closing bracket has the wrong type
    - extra closing bracket after valid pairs
    - unmatched opening brackets remain at the end
    - one-character input
    """
```

## 7. Iterative implementation

### Iteration 1: skeleton

```python
def is_valid(s: str) -> bool:
    unmatched_openings = []

    for bracket in s:
        if is_opening(bracket):
            remember_opening(bracket, unmatched_openings)
        else:
            if not closes_latest_opening(bracket, unmatched_openings):
                return False

            remove_latest_opening(unmatched_openings)

    return no_unmatched_openings(unmatched_openings)
```

The control flow now reads close to English. Helpers remain unfinished.

### Iteration 2: implement opening-bracket handling

```python
def is_valid(s: str) -> bool:
    unmatched_openings = []

    for bracket in s:
        if bracket in "([{":
            unmatched_openings.append(bracket)  # implemented remembering
        else:
            if not closes_latest_opening(bracket, unmatched_openings):
                return False

            unmatched_openings.pop()  # implemented removing latest opening

    return no_unmatched_openings(unmatched_openings)
```

### Iteration 3: implement bracket matching

Use a mapping from closing bracket to required opening bracket.

```python
def is_valid(s: str) -> bool:
    required_opening = {
        ")": "(",
        "]": "[",
        "}": "{",
    }

    unmatched_openings = []

    for bracket in s:
        if bracket in "([{":
            unmatched_openings.append(bracket)
        else:
            # Implement closes_latest_opening.
            if not unmatched_openings:
                return False

            if unmatched_openings[-1] != required_opening[bracket]:
                return False

            unmatched_openings.pop()

    return no_unmatched_openings(unmatched_openings)
```

### Iteration 4: implement final check

```python
def is_valid(s: str) -> bool:
    required_opening = {
        ")": "(",
        "]": "[",
        "}": "{",
    }

    unmatched_openings = []

    for bracket in s:
        if bracket in "([{":
            unmatched_openings.append(bracket)
        else:
            if not unmatched_openings:
                return False

            if unmatched_openings[-1] != required_opening[bracket]:
                return False

            unmatched_openings.pop()

    # Valid only when every opening bracket was matched.
    return not unmatched_openings
```

## Edge-case walkthrough

### Empty string

Loop does nothing. Stack is empty. Returns `True`. No patch.

### Begins with closing bracket

```text
")"
```

Stack is empty when closing bracket arrives. Returns `False`. No patch.

### Wrong bracket type

```text
"(]"
```

Latest opening is `(`, but `]` requires `[`. Returns `False`. No patch.

### Extra closing bracket

```text
"())"
```

First pair empties stack. Final `)` finds empty stack. Returns `False`. No patch.

### Unmatched opening brackets

```text
"(()"
```

One opening remains after traversal. Returns `False`. No patch.

### One opening bracket

```text
"["
```

Remains in stack. Returns `False`. No patch.

No edge-case patches needed; core conditions already cover them.

## 8. Final solution and complexity

```python
def is_valid(s: str) -> bool:
    required_opening = {
        ")": "(",
        "]": "[",
        "}": "{",
    }

    unmatched_openings = []

    for bracket in s:
        if bracket in "([{":
            unmatched_openings.append(bracket)
            continue

        if not unmatched_openings:
            return False

        if unmatched_openings[-1] != required_opening[bracket]:
            return False

        unmatched_openings.pop()

    return not unmatched_openings
```

- Time: `O(n)` — each bracket is processed once.
- Space: `O(n)` — worst case, every character is an opening bracket.
- No useful optimization beyond this; `O(n)` time is optimal because every character may need inspection.