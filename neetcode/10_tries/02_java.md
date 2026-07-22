### 1. Restate the problem

We need to design a custom data structure called `WordDictionary` that can store words and search for them.
The twist is that the search query can contain the `.` wildcard character, which matches exactly one of any letter.
We need to return `true` if there is a matching word previously added, and `false` otherwise.

### 2. Ask clarifying questions

Before writing code, I would verify a few assumptions:

* **Character set:** Are the words limited to lowercase English letters (`a-z`) and the `.` wildcard? *(Assumption: Yes.)*
* **Input validity:** Can words be null or empty? *(Assumption: Inputs are valid, non-null strings of length >= 1.)*
* **Search limits:** Can a search string consist entirely of dots (e.g., `...`)? *(Assumption: Yes, which should match any 3-letter word.)*
* **Workload:** Is the system read-heavy (more `search` calls) or write-heavy (more `addWord` calls)? *(Assumption: Mixed, but fast search is highly desirable.)*

### 3. Work through an example by hand

Let's add the words: `"bad"`, `"dad"`, and `"mad"`.
Then we search for `"pad"`, `"bad"`, and `".ad"`.

1. **Add "bad"**: Store 'b' -> 'a' -> 'd' (mark 'd' as end of word).
2. **Add "dad"**: Store 'd' -> 'a' -> 'd' (mark 'd' as end of word).
3. **Add "mad"**: Store 'm' -> 'a' -> 'd' (mark 'd' as end of word).

**Search "pad"**:

* Look for 'p'. It doesn't exist. Return `false`.

**Search "bad"**:

* Look for 'b' (found) -> 'a' (found) -> 'd' (found). It is marked as an end of a word. Return `true`.

**Search ".ad"**:

* First character is `.`. We must check all existing first letters: 'b', 'd', 'm'.
* Path 1 ('b'): Next is 'a' (found) -> 'd' (found) -> end of word. Return `true`.
* (We don't need to check 'd' or 'm' because we already found a match).

### 4. Brainstorm solutions aloud

* **Approach 1: A simple List or HashSet of strings.**
* *Idea:* Just add words to a list or set.
* *Search:* If the search string has no dots, a HashSet does this in O(1). But if it has dots, we must iterate through the entire dataset and perform a regular expression match.
* *Complexity:* `addWord` is O(1). `search` is O(N * L) where N is the number of words and L is the length. This is too slow if we have thousands of words.


* **Approach 2: Grouped Hash Map (`Map<Integer, List<String>>`).**
* *Idea:* Store words in a map where the key is the word length.
* *Search:* We only check words of the exact same length.
* *Complexity:* Better than Approach 1, but still scales poorly (O(N * L)) if there are many words of the same length and lots of wildcards.


* **Approach 3: Prefix Tree (Trie).**
* *Idea:* Words that share prefixes share nodes.
* *Search:* For a standard character, we just move to that child node. For a `.`, we recursively check all non-null child nodes.
* *Complexity:* `addWord` is O(L). `search` without dots is O(L). `search` with dots worst-case explores the tree up to O(26^dots * L), but it naturally prunes paths that don't exist in the dictionary.
* *Tradeoffs:* Higher memory overhead due to object creation for nodes, but much faster for prefix matching.



### 5. Select the solution

I will use the **Trie (Prefix Tree)** approach. It is the standard, most optimal data structure for dictionary wildcard searches because it aggressively prunes invalid search paths.

I will use standard arrays `TrieNode[] children = new TrieNode[26]` for the nodes, as array lookups are extremely fast and lowercase English letters map cleanly to indices `0-25`.

### 6. Write the implementation outline

```java
class WordDictionary {
    /*
     * Reframe:
     * We need a Trie to store characters. Searches with standard letters follow 
     * a single path. Searches with a dot wildcard branch out to all existing paths.
     *
     * State:
     * A TrieNode root containing child nodes and an isWord boolean.
     * Chosen because Tries naturally group words by prefix, reducing search space.
     *
     * Invariant:
     * The boolean isWord is only true on nodes that represent the final character 
     * of an inserted word.
     *
     * Helpers:
     * match(word, index, currentNode)
     * - A recursive method that handles the wildcard branching logic.
     *
     * Core logic:
     * - addWord: traverse the string character by character, creating new TrieNodes 
     *   when they don't exist. Mark the final node.
     * - search: delegate to the match helper starting from the root at index 0.
     * - match:
     *     - if we reach the end of the word, return whether the current node is a word.
     *     - if the current character is a dot, iterate through all 26 children. If any 
     *       child recursively matches the rest of the string, return true.
     *     - if the current character is a letter, move to that specific child. If null, 
     *       return false; otherwise, recursively match the rest.
     */
}

```

### 7. Implement iteratively

#### Iteration 1: Method skeleton and data structure definition

First, I will define the `TrieNode` class and the basic structure of the `WordDictionary`.

```java
class WordDictionary {
    
    // Internal TrieNode structure
    private static class TrieNode {
        TrieNode[] children = new TrieNode[26];
        boolean isWord = false;
    }
    
    private final TrieNode root;

    public WordDictionary() {
        root = new TrieNode();
    }
    
    public void addWord(String word) {
        // TODO: iterate through chars and build the Trie
    }
    
    public boolean search(String word) {
        // TODO: call a recursive helper for dot matching
        return false;
    }
}

```

#### Iteration 2: Implement the `addWord` method

Now I'll implement the insertion logic. We iterate through the string, creating nodes as needed.

```java
class WordDictionary {
    
    private static class TrieNode {
        TrieNode[] children = new TrieNode[26];
        boolean isWord = false;
    }
    
    private final TrieNode root;

    public WordDictionary() {
        root = new TrieNode();
    }
    
    public void addWord(String word) {
        TrieNode current = root;
        for (int i = 0; i < word.length(); i++) {
            int charIndex = word.charAt(i) - 'a';
            // Added: Create node if path doesn't exist
            if (current.children[charIndex] == null) {
                current.children[charIndex] = new TrieNode();
            }
            current = current.children[charIndex];
        }
        // Added: mark the end of the word
        current.isWord = true;
    }
    
    public boolean search(String word) {
        // TODO: call a recursive helper for dot matching
        return false;
    }
}

```

#### Iteration 3: Implement the `search` happy path and wildcard logic

We need a recursive helper to handle the branching nature of the `.` wildcard.

```java
class WordDictionary {
    
    private static class TrieNode {
        TrieNode[] children = new TrieNode[26];
        boolean isWord = false;
    }
    
    private final TrieNode root;

    public WordDictionary() {
        root = new TrieNode();
    }
    
    public void addWord(String word) {
        TrieNode current = root;
        for (int i = 0; i < word.length(); i++) {
            int charIndex = word.charAt(i) - 'a';
            if (current.children[charIndex] == null) {
                current.children[charIndex] = new TrieNode();
            }
            current = current.children[charIndex];
        }
        current.isWord = true;
    }
    
    public boolean search(String word) {
        // Added: start the recursive search from the root at index 0
        return match(word, 0, root);
    }
    
    // Added: recursive helper to handle wildcards
    private boolean match(String word, int index, TrieNode node) {
        // Base case: we've processed all characters
        if (index == word.length()) {
            return node.isWord;
        }
        
        char c = word.charAt(index);
        
        if (c == '.') {
            // Check all possible paths
            for (TrieNode child : node.children) {
                if (child != null && match(word, index + 1, child)) {
                    return true;
                }
            }
            return false;
        } else {
            // Standard letter path
            int charIndex = c - 'a';
            TrieNode child = node.children[charIndex];
            return child != null && match(word, index + 1, child);
        }
    }
}

```

#### Edge-case pass

* *What if `word` is empty?* The prompt usually implies lengths >= 1, but our code handles it safely. `addWord("")` marks the root as `isWord = true`. `search("")` immediately hits the base case and returns `root.isWord`.
* *What if the search string has characters outside `a-z` other than `.`?* Assuming strictly valid inputs per standard constraints. If invalid chars were possible, we'd add boundary checks before doing `c - 'a'`.
* *Recursion depth:* The max depth is the length of the longest word (e.g., 500 chars). The JVM stack can easily handle this (default max depth is typically ~10,000+), so StackOverflow is not a concern here.

### 8. Analyze expensive sections and optimize

* **Time Complexity:**
* `addWord`: $O(L)$, where $L$ is the length of the word.
* `search`: $O(M)$ for words without dots, where $M$ is the length of the query. For queries with dots, worst-case is $O(26^M)$ if the Trie is completely dense, but on average it is much faster because it only traverses existing branches.


* **Space Complexity:** $O(\Sigma L)$ for the Trie, where $\Sigma L$ is the sum of lengths of all inserted words. The recursive search takes $O(M)$ stack space.
* *Optimization check:* No Stream pipelines were used; a primitive `char` loop is the fastest way to process string indices. Creating the node array is somewhat memory heavy, but using a `HashMap<Character, TrieNode>` instead of an array would add constant-time boxing/unboxing overhead. The `TrieNode[]` array is optimal for read speed here.

### Final Code

Here is the clean, compilable solution.

```java
class WordDictionary {

    private static class TrieNode {
        TrieNode[] children = new TrieNode[26];
        boolean isWord = false;
    }

    private final TrieNode root;

    public WordDictionary() {
        root = new TrieNode();
    }

    public void addWord(String word) {
        TrieNode current = root;
        for (int i = 0; i < word.length(); i++) {
            int charIndex = word.charAt(i) - 'a';
            
            if (current.children[charIndex] == null) {
                current.children[charIndex] = new TrieNode();
            }
            current = current.children[charIndex];
        }
        current.isWord = true;
    }

    public boolean search(String word) {
        return match(word, 0, root);
    }

    private boolean match(String word, int index, TrieNode node) {
        if (index == word.length()) {
            return node.isWord;
        }

        char c = word.charAt(index);

        if (c == '.') {
            for (TrieNode child : node.children) {
                if (child != null && match(word, index + 1, child)) {
                    return true;
                }
            }
            return false;
        } else {
            int charIndex = c - 'a';
            TrieNode child = node.children[charIndex];
            return child != null && match(word, index + 1, child);
        }
    }
}

```

### Brief test walkthrough

Let's run a quick dry run on a critical path.

* `WordDictionary dict = new WordDictionary();`
* `dict.addWord("bad");` -> Creates 'b', 'a', 'd'. 'd' is marked `isWord = true`.
* `dict.search("b..");` ->
* Index 0: `c == 'b'`. Child exists. Recurse with index 1, child 'b'.
* Index 1: `c == '.'`. Iterates through all 26 children. Finds 'a'. Recurse with index 2, child 'a'.
* Index 2: `c == '.'`. Iterates through all 26 children. Finds 'd'. Recurse with index 3, child 'd'.
* Index 3: `index == 3 (word.length())`. Returns `node.isWord`, which is `true` for 'd'.
* Result cascades up and returns `true`. Expected behavior confirmed.