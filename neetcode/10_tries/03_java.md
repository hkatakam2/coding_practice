### 1. Restate the problem

We are given a 2D grid of characters and a dictionary of words. We need to find every word from the dictionary that can be spelled by traversing the grid. We can move up, down, left, or right to adjacent cells. The single rule for a valid path is that we cannot use the same grid cell more than once for a single word. We need to return a list of all matching words.

### 2. Ask clarifying questions

Before jumping in, I'd want to confirm a few details about the inputs and constraints:

* **Characters:** Are the board characters and words guaranteed to be lowercase English letters? (Assuming yes, which simplifies Trie storage).
* **Duplicates:** Can the same word be formed in multiple ways on the board? If so, should it appear only once in the output? (Assuming yes, the result should contain unique words).
* **Modification:** Can I modify the `board` in place to keep track of visited cells, as long as I restore it? (Assuming yes, this saves memory).
* **Input size:** What are the typical bounds for the board dimensions and the dictionary size? (Assuming a moderately sized board like 12x12 and potentially thousands of words, making prefix filtering important).
* **Input/Output types:** I'll assume the signature takes `char[][] board` and `String[] words` (or `List<String>`), and returns `List<String>`.

### 3. Work through an example by hand

Let's take a small 3x3 board and a short dictionary.

**Board:**

```text
o a a
e t a
i h k

```

**Words:** `["oath", "pea", "eat", "rain"]`

1. **Word check:**
* We start at `(0,0)`: 'o'.
* Are there any words starting with 'o'? Yes, "oath".
* From 'o', we can move right to 'a' `(0,1)` or down to 'e' `(1,0)`. "oath" needs 'a', so we move right to `(0,1)`.
* From 'a', we need 't'. We move down to 't' `(1,1)`.
* From 't', we need 'h'. We move down to 'h' `(2,1)`. We found "oath"!


2. **Next search:**
* We scan the board for starting letters.
* `(1,0)` is 'e'. Do we have words starting with 'e'? Yes, "eat".
* From 'e', we need 'a'. We move up to `(0,0)` (which is 'o' - no), or right to `(1,1)` (which is 't' - no, we need 'a'). Wait, `(0,1)` is 'a'. From `(1,0)` 'e', right is 't'. 'a' is not adjacent to 'e'. So "eat" fails from here.
* We keep searching. No other words match.


3. **Result:** `["oath"]`.

### 4. Brainstorm solutions aloud

**Approach 1: Direct DFS for each word**
For every word in the dictionary, iterate through every cell in the grid. If the cell matches the first letter, perform a Depth-First Search (DFS) to see if the rest of the word exists.

* *Time Complexity:* $O(W \cdot M \cdot N \cdot 4^L)$, where $W$ is the number of words, $M$ and $N$ are grid dimensions, and $L$ is the max length of a word.
* *Critique:* If the dictionary is large, we do a massive amount of repeated scanning. Many words share prefixes, and we'd be retracing the same paths blindly.

**Approach 2: Trie + Board DFS**
Instead of searching for each word individually, we flip the problem. We put all the dictionary words into a Prefix Tree (Trie). Then, we iterate through the grid *once* (starting a DFS from each cell).
As we traverse the board, we step through the Trie simultaneously. If the current path on the board doesn't match any prefix in the Trie, we immediately stop and backtrack. If we reach a Trie node that marks the end of a word, we've found a match.

* *Time Complexity:* $O(M \cdot N \cdot 3^L)$. We start at $M \cdot N$ cells. For each, we explore up to length $L$. It's roughly $3^L$ instead of $4^L$ because we don't go backward to the cell we just came from.
* *Space Complexity:* $O(K)$ where $K$ is the total number of characters in the dictionary to store the Trie, plus $O(L)$ for the recursion stack.
* *Critique:* This is highly efficient. The Trie aggressively prunes dead-end paths on the board.

### 5. Select the solution

I will use the **Trie + Board DFS** approach. It is the standard, most optimal solution for this problem, exploiting the fact that multiple words share prefixes.

To keep it clean:

* I'll use a `TrieNode` class. Instead of storing a boolean `isWord`, I'll store `String word` at the terminal nodes. When we find a word, we can grab it directly without passing a `StringBuilder` through the recursion.
* To handle duplicates (finding the same word via two different paths), once a word is found, I will set `node.word = null`. This naturally prevents adding it to our result list twice, avoiding the need for a `HashSet` to filter the final output.
* I'll mutate the board using a placeholder character (`'#'`) to mark cells as visited, restoring them as the recursion unspools.

### 6. Write the implementation outline

```java
List<String> findWords(char[][] board, String[] words) {
    /*
     * Reframe:
     * Find all paths in the grid that match complete words in a dictionary.
     *
     * State:
     * A Trie containing all target words.
     * Chosen because it allows simultaneous prefix-matching for all words, 
     * immediately pruning grid paths that can't possibly form a valid word.
     *
     * Invariant:
     * During DFS, the current Trie node corresponds exactly to the sequence 
     * of characters visited on the board path so far.
     *
     * Helpers:
     * buildTrie(words)
     * - creates the prefix tree from the input dictionary
     * backtrack(board, row, col, node, result)
     * - explores valid neighbors recursively
     *
     * Core logic:
     * - build the Trie from the words
     * - initialize an empty result list
     * - loop through every cell (row, col) in the board
     * - initiate backtracking from each cell using the Trie root
     * - return the result list
     *
     * Edge cases:
     * - empty board or empty words list
     * - out of bounds during DFS
     * - navigating back to a visited cell (cycle prevention)
     */
}

```

### 7. Implement iteratively

#### Iteration 1: Method skeleton and Trie structure

Let's define the core structure, the `TrieNode`, and the main loop.

```java
class Solution {
    class TrieNode {
        TrieNode[] children = new TrieNode[26];
        String word; // Stores the word ending at this node, null otherwise
    }

    public List<String> findWords(char[][] board, String[] words) {
        List<String> result = new ArrayList<>();
        TrieNode root = buildTrie(words);
        
        // TODO: Start DFS from every cell
        
        return result;
    }

    private TrieNode buildTrie(String[] words) {
        // TODO: Insert words into Trie
        return new TrieNode();
    }
    
    // TODO: implement backtrack()
}

```

#### Iteration 2: Implement Trie building

Next, I'll flesh out `buildTrie`. This is standard Trie insertion.

```java
    private TrieNode buildTrie(String[] words) {
        TrieNode root = new TrieNode();
        for (String word : words) {
            TrieNode current = root;
            for (char c : word.toCharArray()) {
                int index = c - 'a';
                if (current.children[index] == null) {
                    current.children[index] = new TrieNode();
                }
                current = current.children[index];
            }
            // Store the whole string at the leaf for easy retrieval
            current.word = word; 
        }
        return root;
    }

```

#### Iteration 3: Complete the backtracking (DFS) logic

Now, let's connect the board iteration to the DFS, handling boundaries, visited states, and Trie progression.

```java
    public List<String> findWords(char[][] board, String[] words) {
        List<String> result = new ArrayList<>();
        TrieNode root = buildTrie(words);
        
        // Start a DFS from every cell on the board
        for (int row = 0; row < board.length; row++) {
            for (int col = 0; col < board[0].length; col++) {
                backtrack(board, row, col, root, result);
            }
        }
        
        return result;
    }

    private void backtrack(char[][] board, int row, int col, TrieNode node, List<String> result) {
        // Added: Extract character and check Trie
        char c = board[row][col];
        
        // Base case / Pruning: 
        // If the cell is visited ('#') or there is no matching prefix, stop.
        if (c == '#' || node.children[c - 'a'] == null) {
            return;
        }
        
        // Move to the next Trie node
        node = node.children[c - 'a'];
        
        // Check if we found a completed word
        if (node.word != null) {
            result.add(node.word);
            node.word = null; // Prevent duplicate additions
        }
        
        // Mark the current cell as visited
        board[row][col] = '#';
        
        // Explore all 4 adjacent directions
        // TODO: add boundary checks for the 4 directional calls
        
        // Backtrack: Restore the cell's original character
        board[row][col] = c;
    }

```

### 8. Edge-case pass and Optimization

Looking at the DFS:

1. **Boundaries:** I need to ensure the DFS doesn't go out of bounds. I can do this by passing valid coordinates to `backtrack` or checking them inside `backtrack`. Checking inside is usually cleaner.
2. **Trie Pruning (Optimization):** When a leaf node's word is found, we set `node.word = null`. However, that leaf node now sits uselessly in the Trie. If we are searching a massive board, we might repeatedly traverse down to that dead leaf. While not strictly required, a common optimization is to remove nodes from the Trie once they no longer lead to any un-found words. I'll omit this to keep the code highly readable, as the `node.word = null` trick already yields excellent performance and guarantees correctness.

Let's refine the boundary checks and finalize the code.

### 9. Final Code

```java
import java.util.ArrayList;
import java.util.List;

class Solution {
    
    private static class TrieNode {
        TrieNode[] children = new TrieNode[26];
        String word; // Holds the completed word if this node is a terminal character
    }

    public List<String> findWords(char[][] board, String[] words) {
        List<String> result = new ArrayList<>();
        if (board == null || board.length == 0 || words == null || words.length == 0) {
            return result;
        }

        TrieNode root = buildTrie(words);

        for (int row = 0; row < board.length; row++) {
            for (int col = 0; col < board[0].length; col++) {
                backtrack(board, row, col, root, result);
            }
        }

        return result;
    }

    private void backtrack(char[][] board, int row, int col, TrieNode node, List<String> result) {
        // Boundary checks and visited check
        if (row < 0 || row >= board.length || col < 0 || col >= board[0].length) {
            return;
        }
        
        char c = board[row][col];
        if (c == '#' || node.children[c - 'a'] == null) {
            return;
        }

        // Advance the Trie pointer
        TrieNode nextNode = node.children[c - 'a'];

        // If a word ends at this node, we've found a match
        if (nextNode.word != null) {
            result.add(nextNode.word);
            // Nullify the word to prevent adding duplicates if found via another path
            nextNode.word = null; 
        }

        // Mark current cell as visited
        board[row][col] = '#';

        // Explore neighbors
        backtrack(board, row - 1, col, nextNode, result); // Up
        backtrack(board, row + 1, col, nextNode, result); // Down
        backtrack(board, row, col - 1, nextNode, result); // Left
        backtrack(board, row, col + 1, nextNode, result); // Right

        // Backtrack: restore the cell's original character
        board[row][col] = c;
    }

    private TrieNode buildTrie(String[] words) {
        TrieNode root = new TrieNode();
        for (String word : words) {
            TrieNode current = root;
            for (char c : word.toCharArray()) {
                int index = c - 'a';
                if (current.children[index] == null) {
                    current.children[index] = new TrieNode();
                }
                current = current.children[index];
            }
            current.word = word;
        }
        return root;
    }
}

```

### 10. Complexity

* **Time Complexity:** $O(M \cdot N \cdot 3^L)$, where $M$ is the number of rows, $N$ is the number of columns, and $L$ is the maximum length of a word in the dictionary. The worst-case is starting a path from every cell and exploring up to length $L$. It's roughly $3^L$ instead of $4^L$ at each step because we mark the current cell as visited, eliminating the path directly behind us. Building the Trie takes $O(K)$, where $K$ is the total number of characters across all words, which is dominated by the grid search.
* **Space Complexity:** $O(K)$ for storing the Trie. The recursive call stack for DFS requires $O(L)$ space.

### 11. Brief test walkthrough

If we pass the board `[['a', 'a']]` and words `["aaa", "aa"]`:

1. Trie is built with "aa" and "aaa".
2. DFS starts at `(0,0)` 'a'. Moves into Trie. Marks `(0,0)` as `#`.
3. DFS explores right to `(0,1)` 'a'. Moves into Trie. Trie `nextNode.word` is `"aa"`. `"aa"` is added to `result` and set to null. Marks `(0,1)` as `#`.
4. DFS tries to explore from `(0,1)`. All neighbors are out of bounds or `#`. Backtracks to `(0,0)`.
5. DFS starts at `(0,1)` 'a'. Explores left to `(0,0)` 'a'. Hits node for `"aa"`, but `word` is already null, so it skips adding the duplicate.
6. Result is successfully `["aa"]`. Correctly ignores the impossible "aaa".