### 1. Restate the problem

We need to implement a data structure called a Prefix Tree (or Trie). This structure must store a collection of strings and support three core operations:

* Adding a new word to the collection.
* Checking if a specific, exact word exists in the collection.
* Checking if there is any word in the collection that begins with a given prefix.

The goal is to design this so that all three operations are highly efficient.

### 2. Ask clarifying questions

In a real interview, I would confirm the following details before writing code:

* **Character set:** Are the inputs guaranteed to be lowercase English letters ('a' - 'z')? *(Assumption: Yes, this is standard for interview Trie problems).*
* **Null inputs:** Will we ever be passed `null` for a word or prefix? *(Assumption: No, we will assume valid string references).*
* **Empty strings:** Can we insert or search for an empty string? *(Assumption: Yes, inserting an empty string is valid and should be searchable).*
* **Deletions:** Do we need to support removing words from the tree? *(Assumption: No, only the requested operations).*

### 3. Work through an example by hand

Let's trace a sequence of operations: `insert("cat")`, `insert("cap")`, `search("cat")`, `search("ca")`, and `startsWith("ca")`.

1. **Start:** We have an empty root node.
2. **`insert("cat")`:**
* Read 'c': Root has no 'c' child. Create it. Move to 'c'.
* Read 'a': 'c' has no 'a' child. Create it. Move to 'a'.
* Read 't': 'a' has no 't' child. Create it. Move to 't'.
* End of word: Mark the 't' node as `isWord = true`.


3. **`insert("cap")`:**
* Read 'c': Root already has a 'c' child. Move to 'c'.
* Read 'a': 'c' already has an 'a' child. Move to 'a'.
* Read 'p': 'a' has no 'p' child. Create it. Move to 'p'.
* End of word: Mark the 'p' node as `isWord = true`.


4. **`search("cat")`:**
* Traverse 'c' -> 'a' -> 't'.
* The node exists, and its `isWord` flag is `true`. Return `true`.


5. **`search("ca")`:**
* Traverse 'c' -> 'a'.
* The node exists, but its `isWord` flag is `false`. Return `false`.


6. **`startsWith("ca")`:**
* Traverse 'c' -> 'a'.
* The node exists. Since we only care if the prefix is present, return `true`.



### 4. Brainstorm solutions aloud

* **Approach 1: HashSet of Words**
We could store all inserted words in a `HashSet<String>`. `insert` and `search` would be O(L) where L is the word length (due to computing the string hash). However, `startsWith` would require iterating through every word in the set to check its prefix, which takes O(N * L) time. This defeats the purpose of the data structure.
* **Approach 2: Prefix Hash Map**
We could maintain a `HashSet` of words and a separate `HashSet` of all possible prefixes. When inserting "cat", we add "c", "ca", and "cat" to the prefix set. This makes `startsWith` an O(L) operation, but space complexity explodes to O(L²) per inserted word.
* **Approach 3: Trie (Prefix Tree)**
We build a tree of characters. Every path down the tree represents a prefix. Because strings with common prefixes share the same ancestor nodes, we save space. Traversal for insertion, exact search, and prefix search is directly proportional to the length of the string, O(L). This gives us optimal time complexity without the massive space overhead of the prefix hash map.

### 5. Select the solution

I will use the **Trie (Prefix Tree)** approach.

For the internal representation of the tree nodes, I'll use a fixed-size array (`Node[26]`) for the children. Because the problem operates on lowercase English letters, a 26-element array provides O(1) deterministic child lookups without the boxing, hashing, and memory overhead of a `HashMap<Character, Node>`. Each node will also carry a boolean `isWord` flag to differentiate between intermediate prefix nodes and complete words.

### 6. Write the implementation outline

```java
class PrefixTree {
    /*
     * Reframe:
     * Build a character-by-character tree to share common prefixes and 
     * allow O(L) lookup times for both exact words and prefixes.
     *
     * State:
     * A custom TrieNode class holding an array of 26 child TrieNodes and a 
     * boolean flag indicating if the node represents the end of a valid word.
     * Chosen because array indexing is the fastest way to route a known alphabet.
     *
     * Invariant:
     * Any valid prefix traversed character-by-character from the root will 
     * successfully resolve to a non-null node.
     *
     * Helpers:
     * findNode(String prefix)
     * - Traverses the tree for a given string and returns the terminal node.
     * - Returns null if the path breaks.
     *
     * Core logic:
     * - insert: Start at root. For each char, if the child node doesn't exist, 
     *   create it. Move to the child. After the loop, mark the final node as a word.
     * - search: Use findNode to get the terminal node. Return true if the node 
     *   exists AND is marked as a word.
     * - startsWith: Use findNode to get the terminal node. Return true if the 
     *   node simply exists.
     *
     * Edge cases:
     * - Empty string inputs.
     * - Characters outside the 'a'-'z' range (prevented by problem constraints).
     */
}

```

### 7. Implement iteratively

**Iteration 1: Method skeleton and internal node structure**
First, I'll define the internal `TrieNode` structure and outline the methods.

```java
class PrefixTree {
    
    private static class TrieNode {
        // 26 slots for lowercase English letters
        final TrieNode[] children = new TrieNode[26];
        boolean isWord = false;
    }

    private final TrieNode root;

    public PrefixTree() {
        root = new TrieNode();
    }

    public void insert(String word) {
        // TODO: traverse and create nodes
    }

    public boolean search(String word) {
        // TODO: find node and check isWord
        return false;
    }

    public boolean startsWith(String prefix) {
        // TODO: find node
        return false;
    }
}

```

**Iteration 2: Implement `insert**`
Now I will implement the character-by-character insertion logic. I'll use simple math (`c - 'a'`) to map characters 'a'-'z' to indices 0-25.

```java
class PrefixTree {
    
    private static class TrieNode {
        final TrieNode[] children = new TrieNode[26];
        boolean isWord = false;
    }

    private final TrieNode root;

    public PrefixTree() {
        root = new TrieNode();
    }

    public void insert(String word) {
        TrieNode current = root;
        
        for (int i = 0; i < word.length(); i++) {
            int index = word.charAt(i) - 'a';
            
            // Added: Create the path if it doesn't exist
            if (current.children[index] == null) {
                current.children[index] = new TrieNode();
            }
            current = current.children[index];
        }
        
        // Added: Mark the end of the traversal as a valid dictionary word
        current.isWord = true;
    }

    // ... search and startsWith remaining
}

```

**Iteration 3: Implement `search` and `startsWith**`
Both search operations require traversing the tree to see if the path exists. I'll extract this shared logic into a `findNode` helper.

```java
    // Added helper to centralize tree traversal logic
    private TrieNode findNode(String str) {
        TrieNode current = root;
        
        for (int i = 0; i < str.length(); i++) {
            int index = str.charAt(i) - 'a';
            if (current.children[index] == null) {
                return null; // Path breaks
            }
            current = current.children[index];
        }
        
        return current;
    }

    public boolean search(String word) {
        TrieNode node = findNode(word);
        // Word exists only if path exists AND it was explicitly inserted
        return node != null && node.isWord;
    }

    public boolean startsWith(String prefix) {
        TrieNode node = findNode(prefix);
        // Prefix exists if the path simply exists
        return node != null;
    }

```

**Edge-case pass**

* **Empty strings:** If we pass `""` into `insert`, the loop does not execute, and the root node's `isWord` becomes `true`. Calling `search("")` will return `root.isWord` (`true`), which is logically correct.
* **Out of bounds characters:** If an uppercase letter or symbol is passed, `charAt(i) - 'a'` will produce an invalid index and throw an `ArrayIndexOutOfBoundsException`. Based on standard interview constraints (lowercase English letters only), this is acceptable. If the scope were broader, we would swap the `TrieNode[]` array for a `Map<Character, TrieNode>`.

### 8. Analyze expensive sections and optimize

* **Time Complexity:**
* `insert`: O(L), where L is the length of the word. We do exactly L array lookups.
* `search`: O(L).
* `startsWith`: O(L).


* **Space Complexity:** O(N * L) in the worst case, where N is the number of words inserted and L is the average word length. Space is significantly reduced when words share common prefixes.
* **Optimizations:** The choice of `TrieNode[]` instead of a `HashMap` is already an optimization for speed and avoiding object-creation overhead during traversal, at the cost of a slightly larger memory footprint for sparse nodes. No further optimization is required for standard constraints.

### Final code

```java
public class PrefixTree {

    private static class TrieNode {
        final TrieNode[] children = new TrieNode[26];
        boolean isWord = false;
    }

    private final TrieNode root;

    public PrefixTree() {
        this.root = new TrieNode();
    }

    public void insert(String word) {
        TrieNode current = root;
        
        for (int i = 0; i < word.length(); i++) {
            int index = word.charAt(i) - 'a';
            
            if (current.children[index] == null) {
                current.children[index] = new TrieNode();
            }
            current = current.children[index];
        }
        
        current.isWord = true;
    }

    public boolean search(String word) {
        TrieNode node = findNode(word);
        return node != null && node.isWord;
    }

    public boolean startsWith(String prefix) {
        return findNode(prefix) != null;
    }

    private TrieNode findNode(String str) {
        TrieNode current = root;
        
        for (int i = 0; i < str.length(); i++) {
            int index = str.charAt(i) - 'a';
            if (current.children[index] == null) {
                return null;
            }
            current = current.children[index];
        }
        
        return current;
    }
}

```

### Brief test walkthrough

* **Smallest valid input:** `PrefixTree tree = new PrefixTree(); tree.insert("a");`
* Root creates a child at index 0. `current` moves to child. `isWord` becomes `true`.
* `search("a")` -> `findNode` returns the child at index 0. `isWord` is `true`. Output: `true`.


* **Stressing the invariant:** `tree.startsWith("ab")`
* `findNode` looks for 'a', finds it. Looks for 'b', index 1 is `null`. Returns `null`. `startsWith` correctly returns `false`.


* **Prefix vs Word distinction:** `tree.insert("app"); tree.search("ap");`
* `findNode` correctly finds the 'p' node. However, `isWord` was only set on the second 'p', not the first. Returns `false`. Expected result.