### 1. Restatement

Given a target string `s` and a list of dictionary words `wordDict`, determine if `s` can be fully partitioned into one or more sequences of words found in the dictionary. Each word in the dictionary can be reused.

**Example:**

* Input: `s = "leetcode"`, `wordDict = ["leet", "code"]`
* Result: `true` (because "leet" + "code" = "leetcode")

### 2. Clarifying Questions and Assumptions

* **Input Size:** What is the maximum length of `s`? (Assume up to 300, which is standard for this problem; $O(n^2)$ is acceptable).
* **Dictionary size:** How many words? (Assume manageable, say up to 1000).
* **Null/Empty:** If `s` is empty, return `true`. If `wordDict` is empty but `s` is not, return `false`.
* **Output:** Return `boolean`.
* **Assumptions:** I will use a `Set` for `wordDict` for $O(1)$ lookups.

### 3. Manual Example

`s = "applepenapple"`, `wordDict = ["apple", "pen"]`

1. Start at index 0. Can we form a word from index 0? Yes, "apple" (length 5).
2. Now we need to check if "penapple" (index 5 to end) can be segmented.
3. From index 5, can we form a word? Yes, "pen" (length 3).
4. Now we need to check if "apple" (index 8 to end) can be segmented.
5. From index 8, can we form a word? Yes, "apple" (length 5).
6. Reached the end of the string. Return `true`.

### 4. Brainstorming Solutions

* **Brute Force (Recursion):** For every possible prefix, check if it's in the dictionary. If so, recurse on the remaining suffix. This is $O(2^n)$ due to overlapping subproblems.
* **Memoization:** Store the result of `canSegment(startIndex)`. If we've seen this index, return the stored result. This reduces complexity to $O(n \cdot m \cdot k)$ where $n$ is length of `s`, $m$ is number of words, and $k$ is average word length.
* **Dynamic Programming (Tabulation):** Create a boolean array `dp` where `dp[i]` indicates whether `s[0...i-1]` can be segmented. `dp[i]` is true if there exists some `j < i` such that `dp[j]` is true AND `s[j...i-1]` is in the dictionary. This is $O(n^2)$ and very clean.

### 5. Selected Solution

**Dynamic Programming.** It is iterative, avoids recursion depth limits, and is easy to implement using a boolean array.

### 6. Implementation Outline

```java
boolean wordBreak(String s, List<String> wordDict) {
    /*
     * Reframe:
     * Use a DP table where dp[i] represents if the prefix of length i can be segmented.
     *
     * State:
     * boolean[] dp = new boolean[s.length() + 1]
     * Chosen because:
     * We only care if a prefix can be broken down, and the result of larger
     * prefixes depends on smaller ones.
     *
     * Core logic:
     * - convert list to a HashSet for fast lookup
     * - mark dp[0] = true (empty string is always segmentable)
     * - iterate through all end positions i from 1 to n
     * - for each i, check all previous positions j
     * - if dp[j] is true AND substring s.substring(j, i) is in dict, set dp[i] = true
     *
     * Edge cases:
     * - empty string, string not segmentable, dictionary words longer than string.
     */
}

```

### 7. Iterative Implementation

**Iteration 1: Skeleton**

```java
public boolean wordBreak(String s, List<String> wordDict) {
    Set<String> dict = new HashSet<>(wordDict);
    boolean[] dp = new boolean[s.length() + 1];
    dp[0] = true;

    // TODO: Nested loop to fill DP table
    
    return dp[s.length()];
}

```

**Iteration 2: Happy Path**

```java
public boolean wordBreak(String s, List<String> wordDict) {
    Set<String> dict = new HashSet<>(wordDict);
    boolean[] dp = new boolean[s.length() + 1];
    dp[0] = true;

    for (int i = 1; i <= s.length(); i++) {
        for (int j = 0; j < i; j++) {
            // If prefix s[0...j] is valid and remaining s[j...i] is in dict
            if (dp[j] && dict.contains(s.substring(j, i))) {
                dp[i] = true;
                break; // Found a way to reach i
            }
        }
    }
    return dp[s.length()];
}

```

### 8. Edge Case Walkthrough

* **Empty string:** Not possible per constraints usually, but `dp[0]` is true, returns `true`.
* **No match:** `dp` remains all `false` except `dp[0]`, returns `false`.
* **Single word:** `s="a", dict=["a"]`. `i=1, j=0`. `dp[0]` is true, "a" in dict. `dp[1]=true`. Correct.

### 9. Final Code

```java
import java.util.*;

class Solution {
    public boolean wordBreak(String s, List<String> wordDict) {
        if (s == null || s.isEmpty()) return true;
        
        Set<String> dict = new HashSet<>(wordDict);
        boolean[] dp = new boolean[s.length() + 1];
        
        // Base case: empty prefix is segmentable
        dp[0] = true;
        
        for (int i = 1; i <= s.length(); i++) {
            for (int j = 0; j < i; j++) {
                // If prefix of length j is valid, check if substring (j, i) is a word
                if (dp[j] && dict.contains(s.substring(j, i))) {
                    dp[i] = true;
                    break;
                }
            }
        }
        
        return dp[s.length()];
    }
}

```

### 10. Complexity

* **Time:** $O(n^3)$ because of the nested loops ($O(n^2)$) and the `substring` operation ($O(n)$). This is perfectly acceptable for $n=300$.
* **Space:** $O(n + m)$ where $n$ is string length (DP array) and $m$ is the total characters in the dictionary (HashSet storage).