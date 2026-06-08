# question
You are given two words, beginWord and endWord, and also a list of words wordList. All of the given words are of the same length, consisting of lowercase English letters, and are all distinct.
Your goal is to transform beginWord into endWord by following the rules:

You may transform beginWord to any word within wordList, provided that at exactly one position the words have a different character, and the rest of the positions have the same characters.
You may repeat the previous step with the new word that you obtain, and you may do this as many times as needed.
Return the minimum number of words within the transformation sequence needed to obtain the endWord, or 0 if no such sequence exists.

### 1. Restating the Question

Find the shortest transformation sequence from a starting word to a target word. Each step must change exactly one character. Every intermediate word must exist in a given dictionary. Return the total number of words in the shortest path, or 0 if impossible.

### 2. Clarifying Questions & Confirmations

* **Inputs:** `beginWord` (string), `endWord` (string), `wordList` (list of strings).
* **Outputs:** Integer (length of sequence).
* Are all words the same length? *Yes.*
* Only lowercase English letters? *Yes.*
* Does `beginWord` need to be in `wordList`? *No.*
* Does `endWord` need to be in `wordList`? *Yes. If not, impossible.*
* Is the sequence length counting the words or the edges? *Words. `hit` -> `hot` returns 2.*

### 3. Hand Trace Example

`beginWord` = "hit", `endWord` = "cog"
`wordList` = ["hot", "dot", "dog", "lot", "log", "cog"]

* **Step 1:** "hit"
* Valid 1-char changes in dict: "hot"


* **Step 2:** "hot"
* Valid 1-char changes in dict: "dot", "lot"


* **Step 3:** "dot", "lot"
* From "dot": "dog"
* From "lot": "log"


* **Step 4:** "dog", "log"
* From "dog": "cog" (Found target!)


* **Result:** hit -> hot -> dot -> dog -> cog. Length = 5.

### 4. Brainstorming & Complexity

* **Unweighted shortest path:** Breadth-First Search (BFS) is the standard. DFS might find a path, but rarely the shortest, and risks infinite loops without strict visited sets.
* **Graph modeling:** Words are nodes. Edges exist if words differ by exactly 1 char.
* **Finding neighbors (Edges):**
* *Approach A:* Compare current word against all dict words. Time: $O(N \times M)$ per word ($N$ words, length $M$). Total graph: $O(N^2 \times M)$. Bad if dictionary is huge.
* *Approach B:* Take current word, swap each char with 'a'-'z', check if in dict. Time: $O(M^2 \times 26)$ per word. Much faster if word length $M$ is small and $N$ is large.


* **Cycles:** Track visited words. Better yet, just delete seen words from the dictionary set.

### 5. Suggested Solutions

1. **Standard BFS with a-z character substitution (Approach B).** This mimics our hand-trace. Simple, clear, avoids $O(N^2)$ comparisons.
2. **Bi-directional BFS.** Search from `beginWord` forward and `endWord` backward simultaneously. Meets in the middle. Halves the search space size, but logic is much denser and harder to explain quickly.

**Selection:** Standard BFS (Approach B). Always prefer simple and clear.

### 6. Outline

```python
def ladderLength(beginWord: str, endWord: str, wordList: list[str]) -> int:
    """
    Reframe: Shortest path in an unweighted graph where edges are 1-letter mutations.
    State: A queue for BFS tracking word and distance, a set of wordList for O(1) lookups.
    Invariant: Queue processes words in monotonically increasing distance from beginWord.

    getValidMutations(word, word_set) = yields all 1-letter variations of the word present in word_set.

    Core logic:
    - put start word into queue with distance 1
    - while queue has items:
        - grab next word and its current distance
        - if word matches target, return distance
        - for every valid mutation of word:
            - remove mutation from word set to prevent revisits
            - put mutation into queue with distance + 1
    - if queue empties, return 0

    Edge cases:
    - target word is not in the word set initially
    - start word is the same as target word
    """
    pass

```

### 7. Iterative Implementation

**Iteration 1: Skeleton Code**
Setting up the structure based on plain English outline.

```python
from collections import deque

def ladderLength(beginWord: str, endWord: str, wordList: list[str]) -> int:
    word_set = set(wordList)
    
    # TODO: Edge cases later
    
    # Core BFS setup
    queue = deque()
    # TODO: queue start word with distance 1
    
    # TODO: loop while queue has items
        # TODO: pop word and distance
        # TODO: check if target found
        # TODO: get valid mutations and enqueue
        
    return 0 

def getValidMutations(word, word_set):
    # TODO: yield 1-letter changes found in word_set
    pass

```

**Iteration 2: Core Logic Chunking**
Filling in the BFS loop logic. Assuming `getValidMutations` works magically.

```python
from collections import deque

def ladderLength(beginWord: str, endWord: str, wordList: list[str]) -> int:
    word_set = set(wordList)
    
    # Added: queue initialization
    queue = deque([(beginWord, 1)])
    
    # Added: BFS loop
    while queue:
        current_word, dist = queue.popleft()
        
        if current_word == endWord:
            return dist
            
        for next_word in getValidMutations(current_word, word_set):
            word_set.remove(next_word) # mark visited
            queue.append((next_word, dist + 1))
            
    return 0 

def getValidMutations(word, word_set):
    # TODO: yield 1-letter changes found in word_set
    pass

```

**Iteration 3: Implementing Helper**
Turning the `getValidMutations` stub into real code.

```python
from collections import deque

def getValidMutations(word: str, word_set: set):
    # Added: logic to generate a-z replacements
    for i in range(len(word)):
        for c in 'abcdefghijklmnopqrstuvwxyz':
            if c == word[i]:
                continue
            # string slicing takes O(M) time
            new_word = word[:i] + c + word[i+1:]
            if new_word in word_set:
                yield new_word

def ladderLength(beginWord: str, endWord: str, wordList: list[str]) -> int:
    word_set = set(wordList)
    
    queue = deque([(beginWord, 1)])
    
    while queue:
        current_word, dist = queue.popleft()
        
        if current_word == endWord:
            return dist
            
        for next_word in getValidMutations(current_word, word_set):
            word_set.remove(next_word) 
            queue.append((next_word, dist + 1))
            
    return 0 

```

**Iteration 4: Edge Cases**
Addressing the edge cases mentioned in the outline.

```python
from collections import deque

def getValidMutations(word: str, word_set: set):
    for i in range(len(word)):
        for c in 'abcdefghijklmnopqrstuvwxyz':
            if c == word[i]: continue
            new_word = word[:i] + c + word[i+1:]
            if new_word in word_set:
                yield new_word

def ladderLength(beginWord: str, endWord: str, wordList: list[str]) -> int:
    word_set = set(wordList)
    
    # Edge case 1: target not in list
    if endWord not in word_set:
        return 0
        
    # Edge case 2: start == target (not strictly needed by constraints, but safe)
    if beginWord == endWord:
        return 1
    
    queue = deque([(beginWord, 1)])
    
    while queue:
        current_word, dist = queue.popleft()
        
        if current_word == endWord:
            return dist
            
        for next_word in getValidMutations(current_word, word_set):
            word_set.remove(next_word) 
            queue.append((next_word, dist + 1))
            
    return 0 

```

### 8. Complexity & Optimization

**Time Complexity:** $O(M^2 \times N)$

* $N$ is the number of words in `wordList`.
* $M$ is the length of each word.
* For each of the $N$ words, we do $M$ iterations. In each iteration, we create 26 new strings. String creation via slicing takes $O(M)$ time. Therefore, generating mutations takes $O(M^2 \times 26) \to O(M^2)$.

**Space Complexity:** $O(M \times N)$

* Queue can hold up to $N$ words in the worst case, each taking $M$ space.
* The Set takes $O(M \times N)$ space.

**Optimizations (To Discuss, Not Code):**
The most expensive part is the branching factor (level size grows exponentially).
To optimize, use **Bi-directional BFS**. Instead of one queue, maintain two sets (one expanding from `beginWord`, one from `endWord`). At each step, always expand the smaller set to minimize the branching factor. If the two sets ever intersect, a path is found. This drastically reduces the search space size while keeping the same theoretical time complexity bounds.