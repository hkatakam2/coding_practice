### 1. Restate the problem

We are asked to find the longest contiguous block of characters in a given string where no single character appears more than once. We just need to return the integer length of this substring, not the string itself.

* **Given:** A string `s`.
* **Return:** An integer representing the length of the longest substring containing all unique characters.
* **Constraint:** The characters must be contiguous (a substring, not a subsequence), and there can be no duplicates within that range.

### 2. Ask clarifying questions

Before writing code, I would clarify a few details:

* **Character set:** Does the string consist of strictly ASCII characters, or can it contain full Unicode? (Assumption: It could be extended ASCII or Unicode, so relying on standard Collections rather than fixed-size `int[128]` arrays is safer and more general).
* **Empty string:** Can the input be empty or null? (Assumption: It can be empty, but we will assume it is not null. If it's empty, the answer should be `0`).
* **Case sensitivity:** Is the string case-sensitive? (Assumption: Yes, 'a' and 'A' are distinct characters).

### 3. Work through an example by hand

Let's take the string `s = "pwwkew"`.
We want to read from left to right, keeping track of our current valid window of characters.

* Start: `p`. Window is `"p"`. Length = 1.
* Next: `w`. Window is `"pw"`. Length = 2.
* Next: `w`. This is a duplicate. We must shrink our window from the left until the first `w` is gone.
* Window becomes `"w"`. Max length seen so far is still 2.


* Next: `k`. Window is `"wk"`. Length is 2. Max length remains 2.
* Next: `e`. Window is `"wke"`. Length is 3. Max length updates to 3.
* Next: `w`. Another duplicate! The previous `w` is currently at the start of our window. We drop it.
* Window becomes `"kew"`. Length is 3. Max length remains 3.



The string ends. The maximum length we recorded was `3` (for both `"wke"` and `"kew"`).

### 4. Brainstorm solutions aloud

**Approach 1: Brute Force**
We could generate every possible substring, loop through them, and check if they contain all unique characters using a `HashSet`.

* *Time complexity:* $O(n^3)$ (or $O(n^2)$ with slight optimization).
* *Space complexity:* $O(\min(n, m))$ where $m$ is the character set size.
* *Verdict:* Too slow. We are doing redundant work by re-evaluating overlapping substrings.

**Approach 2: Sliding Window with a HashSet**
We use two pointers, `left` and `right`. The `right` pointer expands the window. If the character at `right` is already in our `HashSet`, we increment the `left` pointer, removing characters from the set until the duplicate is evicted.

* *Time complexity:* $O(n)$ because each character is visited at most twice (once by `right`, once by `left`).
* *Space complexity:* $O(\min(n, m))$.
* *Verdict:* Very good, but we can do slightly better by eliminating the inner `while` loop that increments `left` step-by-step.

**Approach 3: Sliding Window with a HashMap**
Instead of just remembering *that* we've seen a character, we can remember *where* we last saw it. We use a `HashMap<Character, Integer>` mapping a character to its most recent index. When we see a duplicate, we can instantly jump the `left` pointer to the right of the old duplicate's index, completely skipping the step-by-step inner loop.

* *Time complexity:* $O(n)$, visiting each character exactly once.
* *Space complexity:* $O(\min(n, m))$.
* *Verdict:* This is the optimal, standard solution.

### 5. Select the solution

I will use **Approach 3 (Sliding Window with a HashMap)**.
It operates in true $O(n)$ time by processing each character strictly once, avoiding nested loop traversals. The `HashMap` naturally handles any character set (ASCII or Unicode) safely without hardcoding array sizes.

### 6. Write the implementation outline

```java
int lengthOfLongestSubstring(String s) {
    /*
     * Reframe:
     * Find the maximum size of a sliding window that contains all unique characters.
     *
     * State:
     * Map from character to its most recent index.
     * Chosen because we need to know instantly where to jump our left pointer 
     * if a duplicate is found.
     *
     * Invariant:
     * The substring between windowStart and windowEnd (inclusive) always contains 
     * strictly unique characters.
     *
     * Core logic:
     * - set up variables for windowStart and maxLength
     * - iterate windowEnd through the string
     * - if the current character was seen before AND is inside the current window:
     *     - jump windowStart to right after the previous occurrence
     * - record/update the current character's index in the map
     * - calculate the current window length and update maxLength
     *
     * Edge cases:
     * - empty string (returns 0 naturally)
     * - jumping windowStart backward (must be prevented)
     */
}

```

### 7. Implement iteratively

**Iteration 1: Method skeleton**
First, I'll set up the data structures, the window boundaries, and the iteration over the string.

```java
public int lengthOfLongestSubstring(String s) {
    Map<Character, Integer> charIndexMap = new HashMap<>();
    
    int windowStart = 0;
    int maxLength = 0;
    
    for (int windowEnd = 0; windowEnd < s.length(); windowEnd++) {
        char currentChar = s.charAt(windowEnd);
        
        // TODO: shrink window if currentChar is a duplicate
        
        // TODO: add current character to map
        // TODO: update maxLength
    }
    
    return maxLength;
}

```

**Iteration 2: Adding characters and tracking length**
Now, I'll implement the happy path where we just add characters to the map and track the size of our window.

```java
public int lengthOfLongestSubstring(String s) {
    Map<Character, Integer> charIndexMap = new HashMap<>();
    
    int windowStart = 0;
    int maxLength = 0;
    
    for (int windowEnd = 0; windowEnd < s.length(); windowEnd++) {
        char currentChar = s.charAt(windowEnd);
        
        // TODO: shrink window if currentChar is a duplicate
        
        // Added: track the latest index of the character
        charIndexMap.put(currentChar, windowEnd);
        
        // Added: compute current window size and update max
        int currentLength = windowEnd - windowStart + 1;
        maxLength = Math.max(maxLength, currentLength);
    }
    
    return maxLength;
}

```

**Iteration 3: Handling duplicates**
Finally, I will add the logic to jump the `windowStart` pointer when we encounter a duplicate.

```java
public int lengthOfLongestSubstring(String s) {
    Map<Character, Integer> charIndexMap = new HashMap<>();
    
    int windowStart = 0;
    int maxLength = 0;
    
    for (int windowEnd = 0; windowEnd < s.length(); windowEnd++) {
        char currentChar = s.charAt(windowEnd);
        
        // Added: if we have seen this char, move the start pointer
        if (charIndexMap.containsKey(currentChar)) {
            int previousIndex = charIndexMap.get(currentChar);
            windowStart = previousIndex + 1; 
        }
        
        charIndexMap.put(currentChar, windowEnd);
        
        int currentLength = windowEnd - windowStart + 1;
        maxLength = Math.max(maxLength, currentLength);
    }
    
    return maxLength;
}

```

**Edge-case pass**
Wait, let's trace an edge case with the Iteration 3 code. What if the string is `"abba"`?

1. `windowEnd = 0`, char = `'a'`. `map={'a':0}`. `windowStart=0`. `maxLength=1`.
2. `windowEnd = 1`, char = `'b'`. `map={'a':0, 'b':1}`. `windowStart=0`. `maxLength=2`.
3. `windowEnd = 2`, char = `'b'`. Seen! `previousIndex = 1`. `windowStart=2`. `map={'a':0, 'b':2}`. `maxLength=2`.
4. `windowEnd = 3`, char = `'a'`. Seen! `previousIndex = 0`. **Bug!** `windowStart = 0 + 1 = 1`.
*Our window just expanded backward to index 1, which includes the duplicate 'b's!*

*Patch:* We should only jump `windowStart` forward. If a duplicate character is found, but its previous occurrence was *before* our current `windowStart`, it is outside our active window and we should ignore it.
We can fix this by doing: `windowStart = Math.max(windowStart, previousIndex + 1);`

### 8. Analyze expensive sections and optimize

The complexity is currently $O(n)$ because we iterate through the loop exactly $n$ times, and `HashMap` operations (`containsKey`, `get`, `put`) are expected $O(1)$.
Using `Math.max` avoids expensive inner loop iterations completely. Boxing chars into `Character` objects does introduce slight memory overhead and autoboxing costs, but unless we have a strict performance constraint guaranteeing ASCII, standardizing on `HashMap` is the cleanest, most resilient Java standard.

### Final code

```java
import java.util.HashMap;
import java.util.Map;

class Solution {
    public int lengthOfLongestSubstring(String s) {
        if (s == null || s.isEmpty()) {
            return 0;
        }

        Map<Character, Integer> charIndexMap = new HashMap<>();
        int windowStart = 0;
        int maxLength = 0;

        for (int windowEnd = 0; windowEnd < s.length(); windowEnd++) {
            char currentChar = s.charAt(windowEnd);

            // If we've seen the character before, we must jump the window forward.
            // Math.max ensures we never move windowStart backwards.
            if (charIndexMap.containsKey(currentChar)) {
                int previousIndex = charIndexMap.get(currentChar);
                windowStart = Math.max(windowStart, previousIndex + 1);
            }

            // Record the most recent occurrence of this character
            charIndexMap.put(currentChar, windowEnd);

            // Calculate the valid window size
            int currentLength = windowEnd - windowStart + 1;
            maxLength = Math.max(maxLength, currentLength);
        }

        return maxLength;
    }
}

```

### Complexity

* **Time Complexity:** $O(n)$ where $n$ is the length of the string. We pass through the string strictly once. Map insertions and lookups take $O(1)$ expected time.
* **Space Complexity:** $O(\min(n, m))$ where $m$ is the size of the character set (e.g., 26 for lowercase English, 128 for ASCII). This is the space used by the `HashMap` to store the character indices.

### Brief test walkthrough

Let's test it against a case that stresses our invariant: `s = "tmmzuxt"`.

1. `t` -> map={`t`:0}, start=0, max=1
2. `m` -> map={`t`:0, `m`:1}, start=0, max=2
3. `m` -> seen at 1. `windowStart` becomes `max(0, 1 + 1) = 2`. map updates `m`:2. max=2. (Window is `"m"`)
4. `z` -> map updates `z`:3. max=2. (Window is `"mz"`)
5. `u` -> map updates `u`:4. max=3. (Window is `"mzu"`)
6. `x` -> map updates `x`:5. max=4. (Window is `"mzux"`)
7. `t` -> seen at 0. `windowStart` becomes `max(2, 0 + 1) = 2`. It successfully ignores the out-of-window `t`. map updates `t`:6. max=5. (Window is `"mzuxt"`).

Result is 5, which is correct. The invariant successfully held.