### question
Given an array of strings `strs`, group all anagrams together into sublists. You may return the output in any order.
An anagram is a string that contains the exact same characters as another string, but the order of the characters can be different.

### 1. Restating

Given list of words. Group them. Words in same group must be anagrams (same characters, different order). Output list of grouped lists. Order irrelevant.

### 2. Clarifying Questions

* **Characters?** Assume lowercase English alphabet only.
* **Empty strings?** Yes, possible. Should group together.
* **Constraints?** Max length of array? Max length of string? Assume fits in memory.

### 3. By-Hand Example

Input: `strs = ["eat", "tea", "tan", "ate", "nat", "bat"]`

* Look at "eat". Normalize it (sort characters) -> "aet". Put in bucket "aet". Bucket "aet": `["eat"]`
* Look at "tea". Normalize -> "aet". Put in bucket "aet". Bucket "aet": `["eat", "tea"]`
* Look at "tan". Normalize -> "ant". Bucket "ant": `["tan"]`
* Look at "ate". Normalize -> "aet". Bucket "aet": `["eat", "tea", "ate"]`
* Look at "nat". Normalize -> "ant". Bucket "ant": `["tan", "nat"]`
* Look at "bat". Normalize -> "abt". Bucket "abt": `["bat"]`

Output: `[["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]`

### 4. Brainstorming & Complexity

* **Approach 1: Brute Force.** Compare every string to every other string. $O(N^2 \cdot K \log K)$ where $N$ is array length, $K$ is max string length. Too slow.
* **Approach 2: Sort String as Key.** (Matches manual example). Sort each string to create a uniform key. Use Hash Map. $O(N \cdot K \log K)$ time. Space $O(N \cdot K)$.
* **Approach 3: Char Count as Key.** Count frequencies of 26 letters. Use tuple of counts as Hash Map key. $O(N \cdot K)$ time. Space $O(N \cdot K)$.

### 5. Suggesting Solutions

Prefer **Approach 2 (Sort String as Key)**. Extremely readable, trivial to explain. Happy path directly matches manual trace. We can optimize to Approach 3 later if $K$ (string length) is huge.

### 6. Outline & Logic

```python
def groupAnagrams(strs):
    """
    Reframe: Anagrams share identical normalized forms.
    State: Hash map (dict), chosen because it groups O(1) lookups by a shared key.
    Invariant: Words sharing characters resolve to the exact same hash map key.

    get_normalized(word) = sorts the word's characters alphabetically.

    Core logic:
    - initialize empty map for groups
    - for each word in input:
        - get normalized version of word using helper
        - append original word to the list in map under normalized key
    - return all lists from the map

    Edge cases:
    - empty input array (return [])
    - empty strings (normalize to "")
    - single char strings (normalize to themselves)
    """

```

### 7. Iterative Implementation

**Iteration 1: Skeleton**

```python
import collections

def groupAnagrams(strs):
    # TODO: initialize map
    
    # TODO: iterate words
        # TODO: normalize
        # TODO: group
        
    # TODO: return values
    pass

def get_normalized(word):
    # TODO: return sorted string
    pass

```

**Iteration 2: Core Loop**

```python
import collections

def groupAnagrams(strs):
    # initialize map (using defaultdict for automatic list creation)
    groups = collections.defaultdict(list) 
    
    # iterate words
    for word in strs:
        # normalize
        key = get_normalized(word) 
        # group
        groups[key].append(word) 
        
    # return values
    return list(groups.values())

def get_normalized(word):
    # TODO: return sorted string
    pass

```

**Iteration 3: Helper Completion**

```python
import collections

def groupAnagrams(strs):
    groups = collections.defaultdict(list)
    for word in strs:
        key = get_normalized(word)
        groups[key].append(word)
    return list(groups.values())

def get_normalized(word):
    # sort returns list of chars, join back to string for dict key
    return "".join(sorted(word)) 

```

**Iteration 4: Edge Cases check**

* *Empty array?* `strs = []`. Loop skips. Returns `[]`. Works perfectly. No patch needed.
* *Empty string?* `strs = [""]`. `get_normalized("")` returns `""`. Map stores `{"": [""]}`. Returns `[[""]]`. Works perfectly. No patch needed.
* *Single chars?* Works perfectly.

Core logic inherently handles the listed edge cases.

### 8. Complexity & Optimizations

**Current Time Complexity:** $O(N \cdot K \log K)$. Sorting string takes $K \log K$. Repeated $N$ times.
**Bottleneck:** `get_normalized` helper relying on `sorted()`.

**Optimization:** Since vocabulary is limited to 26 lowercase English letters, we can skip sorting. We count characters instead. Create an array of size 26. Convert to tuple (tuples are hashable in Python, lists are not).

```python
# OPTIMIZED HELPER
def get_normalized(word):
    # Array of 26 zeros
    count = [0] * 26 
    
    for char in word:
        # map 'a' to index 0, 'b' to 1, etc.
        index = ord(char) - ord('a') 
        count[index] += 1
        
    # convert to tuple so it can be a dict key
    return tuple(count) 

```

**New Time Complexity:** $O(N \cdot K)$. We just iterate over the string once per word. Hash lookup is $O(1)$ on the tuple.