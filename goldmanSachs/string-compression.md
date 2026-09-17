### question
Given an array of characters chars, compress it using the following algorithm:

Begin with an empty string s. For each group of consecutive repeating characters in chars:

If the group's length is 1, append the character to s.
Otherwise, append the character followed by the group's length.
The compressed string s should not be returned separately, but instead, be stored in the input character array chars. Note that group lengths that are 10 or longer will be split into multiple characters in chars.

After you are done modifying the input array, return the new length of the array.

You must write an algorithm that uses only constant extra space.

Note: The characters in the array beyond the returned length do not matter and should be ignored.

 

Example 1:

Input: chars = ["a","a","b","b","c","c","c"]
Output: 6
Explanation: The groups are "aa", "bb", and "ccc". This compresses to "a2b2c3".
After modifying the input array in-place, the first 6 characters of chars should be ["a","2","b","2","c","3"].
Example 2:

Input: chars = ["a"]
Output: 1
Explanation: The only group is "a", which remains uncompressed since it is a single character.
After modifying the input array in-place, the first character of chars should be ["a"].
Example 3:

Input: chars = ["a","b","b","b","b","b","b","b","b","b","b","b","b"]
Output: 4
Explanation: The groups are "a" and "bbbbbbbbbbbb". This compresses to "ab12".
After modifying the input array in-place, the first 4 characters of chars should be ["a","b","1","2"].


**1. Restating the Question**
Compress an array of characters `chars` in-place using run-length encoding. For each consecutive run of identical characters:

* Length = 1: write the character once.
* Length > 1: write the character, followed by the string representation of the length (multi-digit lengths split into individual character elements).
Return the updated length. Extra space must be $O(1)$.

---

**2. Clarifying Questions & Input/Output Confirmation**

* **Input:** `chars: List[str]`, where each element is a single character.
* **Output:** Integer representing new valid length $k$; `chars[0...k-1]` must hold the compressed result.
* **Constraints:** $1 \le \text{len}(chars) \le 2000$; strictly $O(1)$ auxiliary space.
* **Can characters be non-alphabetic?** Yes, any ASCII character can repeat.

---

**3. Hand Simulation of Input to Output**
Input: `chars = ["a","b","b","b","b","b","b","b","b","b","b","b","b"]` (one 'a', twelve 'b's)

* Group 1: `'a'`, count = 1 $\to$ write `'a'` at index `0`. Write index becomes `1`.
* Group 2: `'b'`, count = 12 $\to$ write `'b'` at index `1`. Write `'1'` at index `2`. Write `'2'` at index `3`. Write index becomes `4`.
* Result prefix: `["a", "b", "1", "2"]`
* Return value: `4`.

---

**4. Brainstorming Solutions & Complexity**

* **Approach A: Separate Buffer**
* Scan input, construct new character list, copy back to `chars`.
* Time: $O(N)$, Space: $O(N)$.
* Rejected: Violates $O(1)$ space constraint.


* **Approach B: Two-Pointer In-Place Sweep (Read/Write)**
* Since compressed length $\le$ original run length for all groups ($1 \to 1$, $2 \to 2$, $k \ge 3 \to \le k$), write pointer never overtakes read pointer.
* Time: $O(N)$, Space: $O(1)$.
* Selected: Optimal, simple, zero allocation.



---

**5. Suggested Solution**
Two-Pointer In-Place Sweep using a `write` pointer for inserting compressed characters/digits and a `read` pointer to identify contiguous runs.

---

**6. Implementation Outline**

```python
def compress(chars: list[str]) -> int:
    """
    Reframe: In-place array overwrite via two pointers since compressed length <= uncompressed length.
    State: `read` (scanner), `write` (insertion position), chosen because read/write separation prevents overwriting unprocessed characters.
    Invariant: chars[0...write-1] contains the fully compressed sequence for all characters scanned up to read.

    find_run_end(chars, start) = returns index where the run of chars[start] terminates.
    write_run(chars, write_idx, char, count) = writes character and multi-digit count starting at write_idx; returns updated write_idx.

    Core logic:
    - Initialize read and write pointers at index 0.
    - While read pointer has not reached the end:
      - Determine the character and measure length of current consecutive run.
      - Write character to write pointer and advance write pointer.
      - If run length > 1, write each digit of the count to write pointer and advance write pointer for each digit.
      - Advance read pointer to start of next run.
    - Return write pointer value.

    Edge cases:
    - Single character array (count 1 -> no digits written, returns 1).
    - All distinct characters (no counts written, chars remains unchanged, returns len(chars)).
    - Run length >= 10 (count requires multiple writes for each decimal digit).
    """

```

---

**7. Iterative Implementation**

**Iteration 1: Skeleton with stubs and plain-English mappings**

```python
def compress(chars: list[str]) -> int:
    write = 0
    read = 0
    n = len(chars)

    while read < n:
        # TODO: find the end of the current run of identical characters
        # TODO: write the character at `write` pointer
        # TODO: if run length > 1, write each digit of length to `write` pointer
        # TODO: advance `read` to start of next run
        pass

    return write

```

**Iteration 2: Implementing run detection and character writing**

```python
def compress(chars: list[str]) -> int:
    write = 0
    read = 0
    n = len(chars)

    while read < n:
        char = chars[read]
        # CHANGED: find run end using a nested pointer
        run_end = read
        while run_end < n and chars[run_end] == char:
            run_end += 1

        count = run_end - read

        # CHANGED: write the character itself
        chars[write] = char
        write += 1

        # TODO: write count digits if count > 1

        # CHANGED: advance read pointer past the processed run
        read = run_end

    return write

```

**Iteration 3: Implementing count digit writing (completing core logic)**

```python
def compress(chars: list[str]) -> int:
    write = 0
    read = 0
    n = len(chars)

    while read < n:
        char = chars[read]
        run_end = read
        while run_end < n and chars[run_end] == char:
            run_end += 1

        count = run_end - read

        chars[write] = char
        write += 1

        # CHANGED: convert count to digits and write each digit
        if count > 1:
            for digit in str(count):
                chars[write] = digit
                write += 1

        read = run_end

    return write

```

**Walking Edge Cases:**

* **Edge 1: Single-element array (`["a"]`)**
* `read=0`, `run_end=1`, `count=1`.
* `chars[0] = 'a'`, `write=1`. `count > 1` is False.
* Loop exits. Returns `1`. **Passes without modification.**


* **Edge 2: All unique elements (`["a","b","c"]`)**
* Each step has `count=1`. Characters overwritten in same positions.
* Returns `3`. **Passes without modification.**


* **Edge 3: Run length $\ge 10$ (`["a"] * 12`)**
* `char='a'`, `count=12`. `chars[0]='a'`.
* `str(12) -> ['1', '2']`. `chars[1]='1'`, `chars[2]='2'`, `write=3`.
* Returns `3`. **Passes without modification.**



---

**8. Complexity & Optimizations**

```python
def compress(chars: list[str]) -> int:
    write = 0
    read = 0
    n = len(chars)

    while read < n:
        char = chars[read]
        run_end = read
        # Cost: Linear scan. Each index visited at most once by run_end.
        while run_end < n and chars[run_end] == char:
            run_end += 1

        count = run_end - read
        chars[write] = char
        write += 1

        # Cost: str(count) creates <= 4 chars for N <= 2000 -> O(1) time & space.
        if count > 1:
            for digit in str(count):
                chars[write] = digit
                write += 1

        read = run_end

    return write

```

* **Time Complexity:** $O(N)$ — `read` and `run_end` traverse the array once; `write` advances at most $N$ times.
* **Space Complexity:** $O(1)$ — all mutations occur in-place with fixed integer variables.