### question
Design a data structure that supports adding new words and searching for existing words.

Implement the WordDictionary class:

void addWord(word) Adds word to the data structure.
bool search(word) Returns true if there is any string in the data structure that matches word or false otherwise. word may contain dots '.' where dots can be matched with any letter.

**1. Restating the question**
Build data structure. Two operations:

* `addWord(word)`: inserts string.
* `search(word)`: returns true if word exists. Supports `.` as wildcard for any single character.

**2. Clarifying questions, inputs, outputs**

* Char set? Lowercase a-z and `.`.
* Max word length? Usually ~500.
* Search empty string? Assume no, but good to handle.
* Output: `addWord` -> void. `search` -> boolean.

**3. Turn example input into output by hand**
`addWord("bad")` -> store 'b' -> 'a' -> 'd' (end)
`search(".ad")` ->

* Char 1: `.` -> can be anything. We have 'b'. Follow 'b'.
* Char 2: `a` -> must be 'a'. 'b' has 'a'. Follow 'a'.
* Char 3: `d` -> must be 'd'. 'a' has 'd'. Follow 'd'.
* End of word. Is 'd' an end node? Yes. Return True.

**4. Brainstorming solutions & complexity**

* *List/Array*: Store all words. `search` loops all words, compares chars. Add: O(1). Search: O(N * L).
* *HashMap grouped by length*: `dict[len] = [words]`. Filter by length, then compare. Add: O(1). Search: O(M * L), M = words of same length.
* *Trie (Prefix Tree)*: Node per char. Shared prefixes. `.` branches to all children. Add: O(L). Search: O(26^L) worst case for all dots, O(L) for exact word.

**5. Suggest solutions**

* HashMap by length. Simple, intuitive. (By-hand comparison approach).
* Trie. Standard for prefix/wildcard search. More efficient space for overlapping words.
* *Selected*: Trie. Clean recursive matching.

**6. Outline of selected implementation**

```python
class TrieNode:
    # basic node with children map and is_end flag
    pass

class WordDictionary:
    def search(self, word: str) -> bool:
        """
        Reframe: Tree traversal where '.' acts as a multi-way branch.
        State: Trie nodes, chosen because prefix-sharing minimizes redundant character checks.
        Invariant: Current node represents the valid matched prefix so far.

        match_path(node, remaining_word) = true if remaining_word perfectly maps to a path from node to an end-node.

        Core logic:
        - if word is fully consumed, check if current node is an end-of-word.
        - extract next character.
        - if character is a dot:
            - try match_path on all existing children of current node.
            - if any child returns true, return true.
        - if character is normal letter:
            - check if child exists for this letter.
            - if yes, go to child and return match_path.
        - if no valid paths, return false.

        Edge cases:
        - empty word string.
        - word perfectly matches a prefix, but prefix is not a complete word.
        - dot matches children, but none of those paths reach a valid end.
        """

```

**7. Iterative implementation**

*Iteration 1: Skeleton with stubs*

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class WordDictionary:
    def __init__(self):
        self.root = TrieNode()

    def addWord(self, word: str) -> None:
        # standard trie insert
        curr = self.root
        for char in word:
            if char not in curr.children:
                curr.children[char] = TrieNode()
            curr = curr.children[char]
        curr.is_end = True

    def search(self, word: str) -> bool:
        # TODO: call match_path helper
        pass

    def _match_path(self, node, word_slice) -> bool:
        # TODO: implement core traversal
        pass

```

*Iteration 2: Core logic (Happy path)*

```python
    # ... previous code ...
    def search(self, word: str) -> bool:
        return self._match_path(self.root, word) # start at root

    def _match_path(self, node, word_slice) -> bool:
        # base case: consumed whole string
        if not word_slice:
            return node.is_end

        char = word_slice[0]
        rest = word_slice[1:]

        if char == '.':
            # check all children
            for child in node.children.values():
                if self._match_path(child, rest):
                    return True
            return False
        else:
            # normal char
            if char in node.children:
                return self._match_path(node.children[char], rest)
            return False

```

*Iteration 3: Addressing Edge Cases & Refactoring*

* *Edge case 1: empty string.* Handled by `if not word_slice: return node.is_end`. If root, returns false (unless empty string added).
* *Edge case 2: prefix but not word.* Handled by `node.is_end` check at base case.
* *Inefficiency patch*: String slicing `word_slice[1:]` creates new strings, O(N) per step. Change to index pointer `i` to avoid string copying.

*Final Core Logic Patch (using index)*

```python
    def search(self, word: str) -> bool:
        return self._match_path(self.root, word, 0) # added index 0

    def _match_path(self, node, word, i) -> bool: # changed word_slice to word + index
        if i == len(word): # no more chars
            return node.is_end

        char = word[i]
        
        if char == '.':
            for child in node.children.values():
                if self._match_path(child, word, i + 1): # pass i+1 instead of slice
                    return True
            return False
        else:
            if char in node.children:
                return self._match_path(node.children[char], word, i + 1)
            return False

```

**8. Complexity & optimizations**

* *Space*: O(N * L) for Trie, where N = words, L = max length.
* *Time - addWord*: O(L).
* *Time - search*:
* Without dots: O(L). Very fast.
* With dots: O(26^L) worst case (e.g., search `..........` explores entire tree).


* *Optimization note*: If search with many dots is heavily called and tree is dense, the HashMap grouped by length actually outperforms Trie. For interview, Trie is expected. Slicing removal (`i` index instead of `word[1:]`) was the major practical optimization here, reducing space/time overhead of substring generation.