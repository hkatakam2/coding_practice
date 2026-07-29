### 1. Restate the problem

Given two strings, find the length of the longest sequence of characters that appears in both strings in the same relative order.
Characters in a subsequence do not need to be contiguous. If no common characters exist, return 0.

### 2. Ask clarifying questions

* **Input size:** How long can the strings be? (Assumption: Up to a few thousand characters, meaning an $O(N \times M)$ time complexity is acceptable, but $O(2^N)$ is not).
* **Character set:** Are we strictly dealing with lowercase English letters, or all ASCII/Unicode characters? (Assumption: Standard ASCII, but the logic remains the same regardless).
* **Null or empty input:** Can the strings be empty or null? (Assumption: Strings are non-null but can be empty. If either is empty, the result is 0).

### 3. Work through an example by hand

Let `text1 = "abcde"` and `text2 = "ace"`.

We compare prefixes of the strings to build the solution.

1. Compare `'a'` with `'a'`. They match. Our LCS length is $1 + \text{LCS}(\text{"bcde"}, \text{"ce"})$.
2. Compare `'b'` with `'c'`. No match. Our LCS is the max of either:
* Ignoring `'b'` in `text1`: $\text{LCS}(\text{"cde"}, \text{"ce"})$
* Ignoring `'c'` in `text2`: $\text{LCS}(\text{"bcde"}, \text{"e"})$


3. Continuing this process:
* `'c'` matches `'c'` -> length becomes 2.
* `'d'` does not match `'e'`.
* `'e'` matches `'e'` -> length becomes 3.



Final result: 3 (the subsequence is "ace").

### 4. Brainstorm solutions aloud

* **Direct Simulation / Brute Force:** Generate every possible subsequence of `text1` ($2^N$ possibilities) and search for each in `text2` ($O(M)$ time). Time complexity is $O(M \cdot 2^N)$. This is too slow for strings longer than ~20 characters.
* **Top-Down Dynamic Programming (Memoization):** Use recursion to compare characters at `i` and `j`. If they match, add 1 and advance both pointers. If they don't, branch into two recursive calls (advance `i`, or advance `j`) and take the max. Cache the results in a 2D array. Time: $O(N \cdot M)$. Space: $O(N \cdot M)$ for the cache and the recursion call stack.
* **Bottom-Up Dynamic Programming:** Build the same 2D cache iteratively from the base cases (empty strings). `dp[i][j]` represents the LCS of the first `i` characters of `text1` and the first `j` characters of `text2`. Time: $O(N \cdot M)$. Space: $O(N \cdot M)$.

### 5. Select the solution

We will proceed with **Bottom-Up Dynamic Programming**.
It avoids the overhead and potential `StackOverflowError` of deep recursion. It is highly readable, easy to implement without bugs, and perfectly fits the constraints. Later, we can observe that computing the current row only requires the previous row, allowing us to optimize the space footprint.

### 6. Write the implementation outline

```java
int longestCommonSubsequence(String text1, String text2) {
    /*
     * Reframe:
     * Build the longest common subsequence by comparing characters step-by-step
     * and storing the optimal results of smaller prefixes.
     *
     * State:
     * A 2D integer grid where dp[i][j] holds the LCS length for text1 up to index i
     * and text2 up to index j. 
     * Chosen because each subproblem depends strictly on previously solved smaller subproblems.
     *
     * Invariant:
     * dp[i][j] always represents the optimal LCS for the string prefixes of lengths i and j.
     *
     * Core logic:
     * - create a 2D array of size (len1 + 1) by (len2 + 1)
     * - pad row 0 and col 0 with zeros to represent matching against an empty string
     * - loop through each character of text1
     * - loop through each character of text2
     * - if characters match, take the diagonal value (dp[i-1][j-1]) and add 1
     * - if they do not match, take the max of excluding the current text1 char (dp[i-1][j]) 
         or excluding the current text2 char (dp[i][j-1])
     * - return the bottom-right cell
     *
     * Edge cases:
     * - either string is empty
     * - entirely disjoint strings
     */
}

```

### 7. Implement iteratively

**Iteration 1: Method skeleton and broad control flow**
We set up the DP grid and the nested loops. We use 1-based indexing for the grid to easily handle the "empty prefix" base cases without out-of-bounds checks.

```java
public int longestCommonSubsequence(String text1, String text2) {
    int length1 = text1.length();
    int length2 = text2.length();
    
    // grid size is padded by 1 for empty string base cases
    int[][] dp = new int[length1 + 1][length2 + 1];

    for (int i = 1; i <= length1; i++) {
        for (int j = 1; j <= length2; j++) {
            // TODO: check for character match
            // TODO: update dp[i][j] based on match or mismatch
        }
    }

    return dp[length1][length2];
}

```

**Iteration 2: Complete the core logic**
We implement the state transitions. Note that DP index `i` corresponds to string index `i - 1`.

```java
public int longestCommonSubsequence(String text1, String text2) {
    int length1 = text1.length();
    int length2 = text2.length();
    
    int[][] dp = new int[length1 + 1][length2 + 1];

    for (int i = 1; i <= length1; i++) {
        for (int j = 1; j <= length2; j++) {
            // Added: Compare current characters
            if (text1.charAt(i - 1) == text2.charAt(j - 1)) {
                // Match: extend the LCS of the prefixes without these characters
                dp[i][j] = 1 + dp[i - 1][j - 1];
            } else {
                // Mismatch: take the max LCS by dropping one of the characters
                dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
            }
        }
    }

    return dp[length1][length2];
}

```

**Edge-case pass**

* *Empty strings:* If `text1` is `""`, `length1` is 0. The outer loop does not execute, and it correctly returns `dp[0][length2]`, which initializes to 0. No patch needed.
* *Disjoint strings ("abc", "def"):* The `else` branch entirely propagates 0s. Correct.

### 8. Analyze expensive sections and optimize

* **Time Complexity:** $O(N \cdot M)$ where $N$ and $M$ are the lengths of `text1` and `text2`. The nested loop processes every pair of prefixes once.
* **Space Complexity:** Currently $O(N \cdot M)$ because of the 2D `dp` array.

**Optimization:**
Notice inside the inner loop that `dp[i][j]` only ever references values from the current row `dp[i]` and the previous row `dp[i - 1]`. We don't need to keep the entire grid in memory. We can reduce the space complexity to $O(M)$ by maintaining just two 1D arrays: `previousRow` and `currentRow`.

To push memory optimization further, we can ensure we make the 1D arrays the size of the *shorter* string by swapping them if necessary, achieving $O(\min(N, M))$ space.

**Optimization Patch:**

```java
// Swapping to ensure text2 is the shorter string
if (text1.length() < text2.length()) {
    String temp = text1;
    text1 = text2;
    text2 = temp;
}

```

### Final Code

```java
public int longestCommonSubsequence(String text1, String text2) {
    // Ensure text2 is the shorter string to minimize memory usage
    if (text1.length() < text2.length()) {
        String temp = text1;
        text1 = text2;
        text2 = temp;
    }

    int length1 = text1.length();
    int length2 = text2.length();
    
    // We only need the previous row and the current row
    int[] previousRow = new int[length2 + 1];
    int[] currentRow = new int[length2 + 1];

    for (int i = 1; i <= length1; i++) {
        for (int j = 1; j <= length2; j++) {
            if (text1.charAt(i - 1) == text2.charAt(j - 1)) {
                currentRow[j] = 1 + previousRow[j - 1];
            } else {
                currentRow[j] = Math.max(previousRow[j], currentRow[j - 1]);
            }
        }
        
        // Move current row results to previous row for the next iteration
        // Using System.arraycopy is extremely fast for swapping array states
        System.arraycopy(currentRow, 0, previousRow, 0, length2 + 1);
    }

    return previousRow[length2];
}

```

### Complexity

* **Time:** $O(N \cdot M)$, where $N$ and $M$ are the lengths of the strings. Every character combination is evaluated exactly once.
* **Space:** $O(\min(N, M))$. By storing only two rows at a time and forcing `text2` to be the shorter string, we drastically reduce memory overhead.

### Brief test walkthrough

**Test: `text1 = "abc"`, `text2 = "def"**`

* Lengths are equal, no swap needed. `length2 = 3`.
* Both rows are initialized to `[0, 0, 0, 0]`.
* Comparing 'a' to 'd', 'e', 'f'. No matches. `currentRow` evaluates to max of 0 and 0. `previousRow` becomes `[0, 0, 0, 0]`.
* Comparing 'b' to 'd', 'e', 'f'. No matches. `previousRow` becomes `[0, 0, 0, 0]`.
* Comparing 'c' to 'd', 'e', 'f'. No matches. `previousRow` remains `[0, 0, 0, 0]`.
* Returns `previousRow[3]`, which is 0. Expected result.

**Test: `text1 = "ab"`, `text2 = "a"**`

* `text2` is shorter. `length1 = 2`, `length2 = 1`. Arrays sized 2.
* `i = 1` ('a'), `j = 1` ('a'). Match! `currentRow[1] = 1 + previousRow[0] = 1`. `previousRow` becomes `[0, 1]`.
* `i = 2` ('b'), `j = 1` ('a'). Mismatch. `currentRow[1] = Math.max(previousRow[1], currentRow[0]) = Math.max(1, 0) = 1`. `previousRow` becomes `[0, 1]`.
* Returns `previousRow[1]`, which is 1. Expected result.