### 1. Restate the problem

We are given a 2D grid of characters and a target string. We need to determine if the string can be spelled out by tracing a path through the grid.

A valid path:

* Starts at any cell.
* Moves only horizontally or vertically to an adjacent cell.
* Matches the characters of the target string in exact order.
* Never uses the same specific grid cell more than once per path.

We return `true` if such a path exists, and `false` otherwise.

### 2. Ask clarifying questions

* **Input size:** What are the maximum dimensions of the board and the maximum length of the word? (Assumption: The board is roughly up to 6x6 or 10x10, and the word is relatively short. For large boards, this problem scales exponentially.)
* **Character set:** Are we dealing strictly with ASCII characters (e.g., uppercase/lowercase English letters)? (Assumption: Standard English letters, case-sensitive.)
* **Empty inputs:** Can the board be empty, or the word be empty? (Assumption: The board has at least 1 cell, and the word has at least 1 character.)
* **Mutation:** Are we allowed to modify the `board` array in place to track visited cells, or must we treat it as read-only? (Assumption: Modifying the board in place during traversal is allowed as long as we restore it before returning.)

### 3. Work through an example by hand

Let's use a 3x3 board and the word `"BFC"`:

```
Row 0:  A  B  C
Row 1:  S  F  C
Row 2:  A  D  E

```

1. **Scan the board** for the first letter, `'B'`.
2. Found `'B'` at `(row 0, col 1)`.
3. **Start Path:** `[ (0,1)='B' ]`. Target next: `'F'`.
* Check neighbors of `(0,1)`:
* Left `(0,0)` is `'A'` (No match)
* Right `(0,2)` is `'C'` (No match)
* Down `(1,1)` is `'F'` (Match!)




4. **Extend Path:** `[ (0,1)='B', (1,1)='F' ]`. Target next: `'C'`.
* Check neighbors of `(1,1)`:
* Up `(0,1)` is already in our path! (Skip)
* Left `(1,0)` is `'S'` (No match)
* Down `(2,1)` is `'D'` (No match)
* Right `(1,2)` is `'C'` (Match!)




5. **Extend Path:** `[ (0,1)='B', (1,1)='F', (1,2)='C' ]`.
6. We have matched all characters in `"BFC"`. Return `true`.

### 4. Brainstorm solutions aloud

**Approach 1: Depth-First Search (DFS) with Backtracking**

* **Core idea:** Iterate through every cell in the grid. If the cell matches the first letter of our word, launch a recursive DFS. The DFS explores all 4 directions for the next character. To prevent reusing cells, we temporarily mark the current cell as "visited" (e.g., by changing its value to a special character like `'#'`) and restore it when backtracking.
* **Why it works:** DFS naturally models pathfinding. Backtracking ensures we can explore all possible branching paths without permanently destroying the board state for parallel branches.
* **Complexity:** Time complexity would be bounded by the number of starting cells $O(M \times N)$ multiplied by the maximum length of a DFS path. After the first character (4 choices), we have at most 3 valid directions, making it $O(M \times N \times 3^L)$ where $L$ is the length of the word. Space complexity is $O(L)$ for the recursion call stack.

**Approach 2: Pre-counting with DFS Pruning**

* **Core idea:** Do a quick $O(M \times N)$ scan of the board to count character frequencies. If the board doesn't contain enough of a specific character to form the word, return `false` immediately.
* **Why it works:** Often in worst-case scenarios, the board is filled with `"AAAAA"` and the word is `"AAAAAB"`. A pure DFS will explore millions of paths before failing. Pruning prevents this.
* **Tradeoffs:** Adds an initial $O(M \times N)$ time cost and $O(1)$ space (for a 256-char array). It's an excellent optimization but doesn't change the fundamental exponential nature of the search itself.

### 5. Select the solution

I will use **DFS with Backtracking** (Approach 1). It directly addresses the constraints, relies on standard graph traversal techniques, and is easy to implement cleanly without external data structures.

I'll use in-place board modification for the `visited` state, as it saves allocating an $O(M \times N)$ boolean array, remaining highly memory efficient.

### 6. Write the implementation outline

```java
boolean exist(char[][] board, String word) {
    /*
     * Reframe:
     * Find a continuous, non-overlapping path in the grid that spells the word.
     *
     * State:
     * The grid itself serves as our state. We mutate the current cell to '#' 
     * to mark it as visited, and backtrack by restoring its original character.
     * Chosen because:
     * It avoids allocating a separate O(M x N) boolean visited matrix.
     *
     * Invariant:
     * Entering the DFS for a given index means all previous characters in the 
     * word have been successfully matched to a valid path of adjacent cells.
     *
     * Helpers:
     * dfs(board, row, col, word, wordIndex)
     * - recursively checks the 4 neighbors for the next character in the word.
     *
     * Core logic:
     * - iterate over every row and column
     * - if the current cell matches the first character of the word, start dfs
     * - if dfs returns true, we immediately return true
     * - if the loops finish without finding a path, return false
     *
     * Edge cases:
     * - the word is longer than the total number of cells
     * - single-character words
     */
}

```

### 7. Implement iteratively

#### Iteration 1: Method skeleton

First, I'll set up the main loops that will scan the board for potential starting points.

```java
public boolean exist(char[][] board, String word) {
    int rows = board.length;
    int cols = board[0].length;
    
    // Scan every cell in the grid
    for (int row = 0; row < rows; row++) {
        for (int col = 0; col < cols; col++) {
            // TODO: If the cell matches the start of the word, trigger DFS
        }
    }
    
    return false;
}

// TODO: define dfs helper

```

*Note: This loops through the grid but doesn't do anything yet. It clearly establishes our entry points.*

#### Iteration 2: Core trigger and DFS skeleton

Now, I will add the condition to start the DFS and sketch out the DFS boundaries.

```java
public boolean exist(char[][] board, String word) {
    int rows = board.length;
    int cols = board[0].length;
    
    for (int row = 0; row < rows; row++) {
        for (int col = 0; col < cols; col++) {
            // Added: trigger DFS if the first character matches
            if (board[row][col] == word.charAt(0)) {
                if (dfs(board, row, col, word, 0)) {
                    return true;
                }
            }
        }
    }
    
    return false;
}

private boolean dfs(char[][] board, int row, int col, String word, int wordIndex) {
    // Added: base case for successful find
    if (wordIndex == word.length()) {
        return true;
    }
    
    // Added: boundary checks and character match check
    if (row < 0 || row >= board.length || col < 0 || col >= board[0].length 
            || board[row][col] != word.charAt(wordIndex)) {
        return false;
    }
    
    // TODO: mark visited, explore neighbors, backtrack
    return false;
}

```

*Note: We have successfully linked the main scanner to our recursive helper and established the base conditions for terminating the recursion.*

#### Iteration 3: Complete the happy path with backtracking

Finally, I'll implement the actual pathfinding logic, mutating the board to prevent self-intersections.

```java
public boolean exist(char[][] board, String word) {
    int rows = board.length;
    int cols = board[0].length;
    
    for (int row = 0; row < rows; row++) {
        for (int col = 0; col < cols; col++) {
            if (board[row][col] == word.charAt(0)) {
                if (dfs(board, row, col, word, 0)) {
                    return true;
                }
            }
        }
    }
    
    return false;
}

private boolean dfs(char[][] board, int row, int col, String word, int wordIndex) {
    if (wordIndex == word.length()) {
        return true;
    }
    
    if (row < 0 || row >= board.length || col < 0 || col >= board[0].length 
            || board[row][col] != word.charAt(wordIndex)) {
        return false;
    }
    
    // Added: Store current character and mark as visited
    char temp = board[row][col];
    board[row][col] = '#';
    
    // Added: Explore all 4 adjacent directions
    boolean found = dfs(board, row + 1, col, word, wordIndex + 1) ||
                    dfs(board, row - 1, col, word, wordIndex + 1) ||
                    dfs(board, row, col + 1, word, wordIndex + 1) ||
                    dfs(board, row, col - 1, word, wordIndex + 1);
                    
    // Added: Backtrack by restoring the cell
    board[row][col] = temp;
    
    return found;
}

```

*Note: The core logic is complete. `||` operators intentionally short-circuit, so if the first direction finds the word, we don't bother exploring the others.*

#### Edge-case pass

Let's review the potential edge cases:

* **The word length exceeds total grid cells**: Our DFS will naturally fail, but it could waste time verifying impossible lengths. *Patch*: Check `word.length() > rows * cols` at the very beginning and return `false` instantly.
* **Empty board**: Constraints usually prevent this, but `board.length == 0` would throw an exception on `board[0].length`. *Patch*: Not explicitly necessary if standard LeetCode constraints guarantee $M, N \ge 1$, but good practice to guard against.

### 8. Analyze expensive sections and optimize

The algorithm runs $O(M \times N)$ starting points. For each, it can travel up to $L$ steps (where $L$ is `word.length()`). At each step, it explores up to 3 directions (excluding where it came from). Total time complexity is strictly $O(M \times N \times 3^L)$. Space complexity is $O(L)$ entirely due to the recursion stack.

To protect against worst-case "flood" inputs (e.g., a board of all `'A'`s and a target word `"AAAAAAAAAAB"`), we can add a frequency check optimization. It takes just $O(M \times N)$ time upfront to ensure the board actually contains all the necessary letters for the word.

#### Final Code

```java
class Solution {
    public boolean exist(char[][] board, String word) {
        int rows = board.length;
        int cols = board[0].length;
        
        // Edge case: word is physically too long for the board
        if (word.length() > rows * cols) {
            return false;
        }
        
        // Optional Optimization: verify character frequencies before searching.
        // Prevents exponential time waste on impossible boards.
        int[] boardFreq = new int[128];
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                boardFreq[board[r][c]]++;
            }
        }
        for (char c : word.toCharArray()) {
            boardFreq[c]--;
            if (boardFreq[c] < 0) {
                return false; // Board lacks necessary characters
            }
        }
        
        // Core Logic: search for valid paths
        for (int row = 0; row < rows; row++) {
            for (int col = 0; col < cols; col++) {
                // Trigger DFS only when we find a matching start character
                if (board[row][col] == word.charAt(0)) {
                    if (dfs(board, row, col, word, 0)) {
                        return true;
                    }
                }
            }
        }
        
        return false;
    }

    private boolean dfs(char[][] board, int row, int col, String word, int wordIndex) {
        // Base case: we successfully matched the entire word
        if (wordIndex == word.length()) {
            return true;
        }
        
        // Base case: out of bounds or character doesn't match
        if (row < 0 || row >= board.length || col < 0 || col >= board[0].length 
                || board[row][col] != word.charAt(wordIndex)) {
            return false;
        }
        
        // State: mark cell visited with '#'
        char temp = board[row][col];
        board[row][col] = '#';
        
        // Explore all 4 adjacent directions. 
        // Short-circuit evaluation (||) stops exploration as soon as one path succeeds.
        boolean found = dfs(board, row + 1, col, word, wordIndex + 1) ||
                        dfs(board, row - 1, col, word, wordIndex + 1) ||
                        dfs(board, row, col + 1, word, wordIndex + 1) ||
                        dfs(board, row, col - 1, word, wordIndex + 1);
                        
        // Backtrack: restore the original character so other paths can use it
        board[row][col] = temp;
        
        return found;
    }
}

```

#### Complexity

* **Time Complexity**: $\mathcal{O}(M \times N \times 3^L)$ in the worst case, where $M$ is rows, $N$ is columns, and $L$ is the length of `word`. From the starting cell (4 directions), each subsequent cell has at most 3 unseen neighbors. The frequency map optimization handles total failure cases in $\mathcal{O}(M \times N + L)$ time.
* **Space Complexity**: $\mathcal{O}(L)$. Modifying the board saves us an $\mathcal{O}(M \times N)$ visited array. The only extra memory is the $\mathcal{O}(L)$ depth of the call stack during recursion, plus $\mathcal{O}(1)$ for the 128-element frequency map.

#### Brief test walkthrough

* **Input**: `board = [['A','B'],['S','F']]`, `word = "ABFS"`
* **Flow**:
* Word fits in board ($4 \le 4$).
* Frequencies check out.
* Loop starts at `(0,0)`, matches `'A'`.
* `dfs` triggered at `index 0`. Matches `'A'`, marks `board[0][0] = '#'`.
* `dfs` at `row 0, col 1` (`index 1`). Matches `'B'`, marks `board[0][1] = '#'`.
* `dfs` at `row 1, col 1` (`index 2`). Matches `'F'`, marks `board[1][1] = '#'`.
* `dfs` at `row 1, col 0` (`index 3`). Matches `'S'`, marks `board[1][0] = '#'`.
* Next recursive calls check `index 4 == word.length()`, return `true`.
* `true` propagates back up the stack.
* Result: `true` (Correct).