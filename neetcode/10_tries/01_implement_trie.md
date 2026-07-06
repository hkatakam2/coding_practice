### question
A prefix tree (also known as a trie) is a tree data structure used to efficiently store and retrieve keys in a set of strings. Some applications of this data structure include auto-complete and spell checker systems.

Implement the PrefixTree class:

PrefixTree() Initializes the prefix tree object.
void insert(String word) Inserts the string word into the prefix tree.
boolean search(String word) Returns true if the string word is in the prefix tree (i.e., was inserted before), and false otherwise.
boolean startsWith(String prefix) Returns true if there is a previously inserted string word that has the prefix prefix, and false otherwise.

We need implement a **Trie / PrefixTree** that supports:

`insert(word)` — store a word
`search(word)` — return true only if exact word was inserted
`startsWith(prefix)` — return true if any inserted word begins with prefix

Key distinction:

```text
insert("apple")

search("app")      -> False
startsWith("app")  -> True
search("apple")    -> True
```

---

## 1. Clarifying questions

In an interview I would confirm:

1. Are inputs lowercase English letters only?

   * Usually yes, but our implementation can support any character.
2. Can empty string be inserted?

   * Usually not in LeetCode-style Trie, but our code can handle it.
3. Should duplicate insertions matter?

   * No. Inserting same word twice still means word exists.

---

## 2. Example by hand

Operations:

```python
trie.insert("apple")
trie.search("apple")
trie.search("app")
trie.startsWith("app")
trie.insert("app")
trie.search("app")
```

Trie after inserting `"apple"`:

```text
root
 └── a
     └── p
         └── p
             └── l
                 └── e   word ends here
```

Now:

```python
search("apple") -> True
```

Because we can walk `a -> p -> p -> l -> e`, and final node is marked as end of word.

```python
search("app") -> False
```

Because we can walk `a -> p -> p`, but that node is not marked as word-ending yet.

```python
startsWith("app") -> True
```

Because the path `a -> p -> p` exists.

After:

```python
insert("app")
```

Now the second `p` node is also marked as word-ending.

```python
search("app") -> True
```

---

## 3. Brainstorm solutions

### Solution 1: Store all words in a set

```python
words = set()
```

`insert` is easy.

But `startsWith(prefix)` would require checking every word:

```python
for word in words:
    if word.startswith(prefix):
        return True
```

Complexity:

```text
insert: O(length of word)
search: O(length of word)
startsWith: O(number of words * prefix length)
```

Simple, but inefficient for prefix queries.

---

### Solution 2: Trie

Each node stores:

```python
children: character -> next TrieNode
is_word: whether a complete inserted word ends here
```

Complexity:

```text
insert: O(length of word)
search: O(length of word)
startsWith: O(length of prefix)
```

This is the intended solution.

---

## 4. Selected idea

Use a Trie node.

Each node represents a prefix.

For example, after inserting `"cat"`:

```text
root
 └── c
     └── a
         └── t  is_word=True
```

The path itself tells us the prefix exists.

The `is_word` flag tells us whether the path is a complete inserted word.

---

## 5. Implementation outline

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_word = False
```

Then:

```python
class PrefixTree:
    def __init__(self):
        self.root = TrieNode()
```

Shared helper:

```python
def _find_node(text):
    start at root
    for each character in text:
        if character is missing:
            return None
        move to child
    return final node
```

Then:

```python
insert(word):
    walk/create nodes for each character
    mark final node as word-ending

search(word):
    find node for word
    return node exists and node is word-ending

startsWith(prefix):
    find node for prefix
    return node exists
```

---

## 6. Plain-English core logic

```python
def PrefixTree(args):  # -> object
    """
    Reframe: every word is a path from root; exact word requires an end marker.

    State:
        root trie node.
        Each trie node has a map from character to child node.
        Each trie node has a boolean saying whether a complete word ends here.

    Invariant:
        After inserting a word, every prefix of that word has a valid path from root.
        Only the final node of the inserted word is marked as a complete word.

    findNode(text) = walk the trie using every character in text;
                     return the final node if the whole path exists,
                     otherwise return None.

    Core logic:
    - To insert a word:
        - Start at root.
        - For each character:
            - If the next node does not exist, create it.
            - Move into that next node.
        - Mark the final node as a complete word.

    - To search for a word:
        - Walk the trie using the word.
        - If the path does not exist, return False.
        - Otherwise return whether the final node is marked as a complete word.

    - To check startsWith:
        - Walk the trie using the prefix.
        - If the path exists, return True.
        - Otherwise return False.

    Edge cases:
    - Searching for a prefix that exists but was never inserted as a full word.
    - Searching for a word with a missing character path.
    - Checking startsWith on a missing prefix.
    - Inserting duplicate words.
    - Empty string, depending on problem constraints.
    """
```

---

## 7. Iterative implementation

### Iteration 1: skeleton

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_word = False


class PrefixTree:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        pass

    def search(self, word: str) -> bool:
        pass

    def startsWith(self, prefix: str) -> bool:
        pass
```

---

### Iteration 2: implement insert

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_word = False


class PrefixTree:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root

        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()

            node = node.children[char]

        node.is_word = True

    def search(self, word: str) -> bool:
        pass

    def startsWith(self, prefix: str) -> bool:
        pass
```

After this, `insert("apple")` creates the path:

```text
a -> p -> p -> l -> e
```

and marks `e.is_word = True`.

---

### Iteration 3: add shared helper

Both `search` and `startsWith` need to walk a string through the trie.

So add `_find_node`.

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_word = False


class PrefixTree:
    def __init__(self):
        self.root = TrieNode()

    def _find_node(self, text: str):
        node = self.root

        for char in text:
            if char not in node.children:
                return None

            node = node.children[char]

        return node

    def insert(self, word: str) -> None:
        node = self.root

        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()

            node = node.children[char]

        node.is_word = True

    def search(self, word: str) -> bool:
        pass

    def startsWith(self, prefix: str) -> bool:
        pass
```

---

### Iteration 4: complete search and startsWith

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_word = False


class PrefixTree:
    def __init__(self):
        self.root = TrieNode()

    def _find_node(self, text: str):
        node = self.root

        for char in text:
            if char not in node.children:
                return None

            node = node.children[char]

        return node

    def insert(self, word: str) -> None:
        node = self.root

        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()

            node = node.children[char]

        node.is_word = True

    def search(self, word: str) -> bool:
        node = self._find_node(word)

        return node is not None and node.is_word

    def startsWith(self, prefix: str) -> bool:
        node = self._find_node(prefix)

        return node is not None
```

This is already correct.

---

## 8. Final code

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_word = False


class PrefixTree:
    def __init__(self):
        self.root = TrieNode()

    def _find_node(self, text: str):
        node = self.root

        for char in text:
            if char not in node.children:
                return None

            node = node.children[char]

        return node

    def insert(self, word: str) -> None:
        node = self.root

        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()

            node = node.children[char]

        node.is_word = True

    def search(self, word: str) -> bool:
        node = self._find_node(word)

        return node is not None and node.is_word

    def startsWith(self, prefix: str) -> bool:
        node = self._find_node(prefix)

        return node is not None
```

---

## 9. Edge case walkthrough

### Case 1: prefix exists but word was not inserted

```python
trie.insert("apple")
trie.search("app")
```

Path exists, but `app` node has `is_word = False`.

Returns:

```python
False
```

Correct.

---

### Case 2: prefix exists

```python
trie.insert("apple")
trie.startsWith("app")
```

Path exists.

Returns:

```python
True
```

Correct.

---

### Case 3: word missing midway

```python
trie.insert("apple")
trie.search("apx")
```

Path breaks at `"x"`.

`_find_node` returns `None`.

Returns:

```python
False
```

Correct.

---

### Case 4: duplicate insert

```python
trie.insert("cat")
trie.insert("cat")
trie.search("cat")
```

The second insert walks the same path and sets `is_word = True` again.

Still correct.

---

### Case 5: empty string

This implementation supports it:

```python
trie.insert("")
trie.search("")
```

`insert("")` marks root as `is_word = True`.

So `search("")` returns `True`.

Usually interview platforms do not test empty strings unless explicitly mentioned.

---

## 10. Complexity

Let `L` be the length of the input word or prefix.

### Insert

```text
Time: O(L)
Space: O(L) worst case
```

Worst case, every character needs a new node.

### Search

```text
Time: O(L)
Space: O(1)
```

No new nodes created.

### startsWith

```text
Time: O(L)
Space: O(1)
```

Same traversal logic as search, but does not require `is_word = True`.

Final key insight:

```text
search checks path + word-ending marker.
startsWith checks only path.
```
