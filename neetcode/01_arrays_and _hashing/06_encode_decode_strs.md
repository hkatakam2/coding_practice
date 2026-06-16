### question
Design an algorithm to encode a list of strings to a string. The encoded string is then sent over the network and is decoded back to the original list of strings.

### 1. Restating

Design two functions: `encode` takes list of strings, returns single string. `decode` takes single string, returns original list. Network safe. Must handle any character (spaces, symbols, emojis) without data loss.

### 2. Clarifying Questions

* Can list be empty? Yes.
* Can strings be empty? Yes.
* Character set? Any valid character.
* Inputs: `List[str]`
* Outputs: `str` (from encode), `List[str]` (from decode)

### 3. Example Input to Output by Hand

Input: `["we", "say", ":", "yes"]`
Idea: Prefix length to avoid delimiter collisions.
Format: `[length]#[string]`
Trace:
"we" -> length 2 -> `2#we`
"say" -> length 3 -> `3#say`
":" -> length 1 -> `1#:`
"yes" -> length 3 -> `3#yes`
Encoded: `2#we3#say1#:3#yes`
Decoding: Read integer till `#` (2). Read 2 chars (`we`). Next integer till `#` (3). Read 3 chars (`say`). And so on.

### 4. Brainstorming & Complexity

1. **Escape characters:** Join by delimiter `,`. If `,` is in string, escape it `\,`. Complex escaping logic if string contains `\`. O(N) time, O(N) space.
2. **Length Prefix (Chunking):** Encode string length before string itself, separated by a distinct character (e.g., `#`). Safe. No escaping needed because we strictly read `N` characters after the delimiter. O(N) time, O(N) space. This is our hand-traced solution.

### 5. Suggested Solutions

Prefer simple/clear. Length Prefix (Chunking) is best. Escaping gets messy and hard to read. We proceed with Length Prefix.

### 6. Outline

```python
class Codec:
    def encode(self, strs):  # -> str
        """
        Reframe: Map each string to a self-contained chunk with metadata to safely extract it later.
        State: Array of encoded chunks, chosen to easily build the final string.
        Invariant: Each encoded chunk starts with its exact char length followed by a '#' delimiter.

        chunkString(s) = prefix string with its length and a '#' delimiter.

        Core logic:
        - for each string in input, chunk it.
        - combine all chunks into one string.
        Edge cases:
        - empty list of strings.
        - strings containing '#' or numbers.
        - empty strings.
        """
        pass

    def decode(self, s):  # -> List[str]
        """
        Reframe: Traverse encoded string sequentially, using embedded lengths to jump exactly over string boundaries.
        State: Output list for decoded strings, pointer to current read position.
        Invariant: Pointer always rests at the start of a length-prefix or at end of string.

        findDelimiter(pos) = find the next '#' starting from pos.
        extractSubstring(start, length) = slice string to get original text.

        Core logic:
        - while pointer is not at end of string:
          - find delimiter to read the length.
          - extract the substring using the length.
          - advance pointer past the substring.
        - return output list.
        Edge cases:
        - empty input string.
        """
        pass

```

### 7. Iterative Implementation

**Iteration 1: Skeleton Code**

```python
class Codec:
    def encode(self, strs):
        # TODO: for each string, chunk it.
        # TODO: combine all chunks into one string.
        return ""
        
    def decode(self, s):
        res = []
        i = 0
        # TODO: while not end of string:
        # TODO: find delimiter, read length, extract substring, advance pointer
        return res

```

**Iteration 2: Encode Core Logic**

```python
class Codec:
    def encode(self, strs):
        # CHANGED: Implemented chunking loop.
        res = ""
        for string in strs:
            # chunkString logic
            chunk = str(len(string)) + "#" + string
            res += chunk
        return res
        
    def decode(self, s):
        res = []
        i = 0
        return res

```

**Iteration 3: Decode Core Logic**

```python
class Codec:
    def encode(self, strs):
        res = ""
        for string in strs:
            chunk = str(len(string)) + "#" + string
            res += chunk
        return res
        
    def decode(self, s):
        # CHANGED: Implemented parsing loop based on invariants.
        res = []
        i = 0
        while i < len(s):
            # findDelimiter
            j = i
            while s[j] != '#':
                j += 1
            
            # read length
            length = int(s[i:j])
            
            # extractSubstring
            start = j + 1
            end = start + length
            res.append(s[start:end])
            
            # advance pointer
            i = end
            
        return res

```

**Iteration 4: Walk Edge Cases**

* *Edge case:* Empty list of strings `[]`.
* `encode([])` returns `""`.
* `decode("")` skips while loop, returns `[]`. Works perfectly. No patch needed.


* *Edge case:* Strings with `#` or numbers (e.g. `["123#456"]`).
* `encode(["123#456"])` -> `"7#123#456"`.
* `decode("7#123#456")`: `i=0`, finds first `#` at `j=1`. length `7`. Extract `123#456`. Works perfectly. No patch needed.


* *Edge case:* Empty string `[""]`.
* `encode([""])` -> `"0#"`.
* `decode("0#")`: `length=0`. `start=2`, `end=2`. `s[2:2]` is `""`. Works perfectly. No patch needed.



Core logic organically handles all edge cases. No messy patches required.

### 8. Complexity & Optimizations

**Complexity:**

* Time Complexity: O(N) for both encode and decode, where N is total number of characters across all strings.
* Space Complexity: O(N) to hold the resulting structures in memory.

**Optimization:**
In Python, string concatenation `res += chunk` in a loop creates a new string every time, degrading to O(N^2) in worst case. Optimized `encode` uses an array and `"".join()`.

```python
class Codec:
    def encode(self, strs):
        # OPTIMIZATION: Use list append and join for O(N) string building.
        res = []
        for string in strs:
            res.append(str(len(string)) + "#" + string)
        return "".join(res)
        
    def decode(self, s):
        res = []
        i = 0
        while i < len(s):
            # find() is highly optimized in C under the hood
            j = s.find('#', i)
            length = int(s[i:j])
            
            start = j + 1
            end = start + length
            res.append(s[start:end])
            
            i = end
            
        return res

```