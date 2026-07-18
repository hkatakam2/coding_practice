### 1. Restate the problem

We are given a string `s` made entirely of uppercase English letters, and an integer `k`. We are allowed to change at most `k` characters in the string to any other uppercase English letter.

Our goal is to find the length of the longest possible contiguous substring that contains only one distinct character after making those changes.

**In simpler terms:** What is the longest contiguous block of identical letters we can create, assuming we have `k` "wildcards" to overwrite other letters that disrupt the block?

### 2. Ask clarifying questions

Before writing code, I would clarify a few constraints:

* **What are the bounds on the string length and `k`?** (Assume `s.length` is up to 100,000, and `k` is non-negative).
* **What if `k` is greater than or equal to the length of the string?** (Then we can just replace everything and the answer is the length of the string).
* **Can the string be empty?** (Assume it can be; the answer would be 0).
* **Signature:** The standard signature would be `int characterReplacement(String s, int k)`.

### 3. Work through an example by hand

Let's trace an example: `s = "AABABBA"`, `k = 1`.

We want to find a window where the number of "other" characters (characters that aren't the most frequent one in the window) is at most `k`.
Formula to evaluate validity: `(Window Length) - (Frequency of most common char) <= k`.

Let's maintain a window from `left` to `right`.

* `R=0, L=0`: Window `"A"`. Length=1. Most frequent='A' (1). Changes needed = 1 - 1 = 0 <= 1. Valid. Max Length = 1.
* `R=1, L=0`: Window `"AA"`. Length=2. Most frequent='A' (2). Changes needed = 2 - 2 = 0 <= 1. Valid. Max Length = 2.
* `R=2, L=0`: Window `"AAB"`. Length=3. Most frequent='A' (2). Changes needed = 3 - 2 = 1 <= 1. Valid. Max Length = 3.
* `R=3, L=0`: Window `"AABA"`. Length=4. Most frequent='A' (3). Changes needed = 4 - 3 = 1 <= 1. Valid. Max Length = 4.
* `R=4, L=0`: Window `"AABAB"`. Length=5. Most frequent='A' (3). Changes needed = 5 - 3 = 2 > 1. **Invalid.**
* *Decision:* Shrink the window from the left. `L` becomes 1. Window is `"ABAB"`.


* `R=5, L=1`: Window `"ABABB"`. Length=5. Most frequent='B' (3). Changes needed = 5 - 3 = 2 > 1. **Invalid.**
* *Decision:* Shrink from left. `L` becomes 2. Window is `"BABB"`.


* `R=6, L=2`: Window `"BABBA"`. Length=5. Most frequent='B' (3). Changes needed = 5 - 3 = 2 > 1. **Invalid.**
* *Decision:* Shrink from left. `L` becomes 3. Window is `"ABBA"`.



The max length recorded during this process is 4.

### 4. Brainstorm solutions aloud

**Approach 1: Brute Force**
We could look at every possible substring. For each substring, count the character frequencies, find the maximum frequency, and check if `Length - MaxFreq <= k`.

* *Time Complexity:* Generating O(N²) substrings, and checking each takes O(N), resulting in O(N³). This is too slow.

**Approach 2: Sliding Window (Two Pointers)**
Instead of recalculating from scratch, we can expand a window `[left, right]` by moving `right` one character at a time. We maintain a frequency map (or an array of size 26) for the characters in the current window.
At each step, we update the frequency of `s.charAt(right)`. If the window becomes invalid (i.e., `(right - left + 1) - maxFrequency > k`), we shrink the window by moving `left` forward and decreasing the frequency of `s.charAt(left)`.

* *Time Complexity:* `right` moves N times. `left` moves at most N times. Inside the loop, finding the max frequency could take O(26). Total time: O(26 * N) = O(N).
* *Space Complexity:* O(26) = O(1) for the frequency array.

**A Crucial Optimization for Sliding Window:**
Do we actually need to search for the *new* `maxFrequency` when we move `left` and remove a character?
No! We are only interested in finding a *longer* valid window. A longer window can only be formed if we find a character count that *exceeds* our historical maximum frequency. Therefore, we can just keep a running tally of the highest frequency we've ever seen. If a window becomes invalid, we don't shrink it; we just *shift* it (increment both `left` and `right`) so its size stays exactly the same, waiting for a new character that boosts the maximum frequency.

### 5. Select the solution

I will use the optimized **Sliding Window** approach. It is O(N) time and O(1) space. It uses a simple integer array of size 26 for frequencies, which is a standard and efficient way to map uppercase ASCII characters.

### 6. Write the implementation outline

```java
int characterReplacement(String s, int k) {
    /*
     * Reframe:
     * Find the maximum size of a sliding window where the total characters
     * minus the most frequent character is at most k.
     *
     * State:
     * int[] counts: Tracks the frequencies of letters in the current window.
     * Chosen because the alphabet is strictly 26 uppercase English letters.
     * int maxFrequency: The highest frequency of a single character we have EVER seen in any window.
     *
     * Invariant:
     * The window size will only grow when we find a character whose frequency
     * pushes maxFrequency higher. Otherwise, the window size remains static
     * (by moving both left and right pointers) or is perfectly valid.
     *
     * Core logic:
     * - initialize counts array, left pointer, maxFrequency, and maxLength
     * - iterate right pointer through the string
     * - increment the count of the character at the right pointer
     * - update maxFrequency if the new character's count is higher
     * - check if the current window is invalid (window length - maxFrequency > k)
     * - if invalid, decrement the count of the left pointer's character and move left forward
     * - update maxLength with the current window size
     *
     * Edge cases:
     * - null or empty string
     */
}

```

### 7. Implement iteratively

#### Iteration 1: Method skeleton and state setup

We start by declaring our state variables and the main loop.

```java
int characterReplacement(String s, int k) {
    if (s == null || s.isEmpty()) {
        return 0;
    }

    int[] counts = new int[26];
    int left = 0;
    int maxFrequency = 0;
    int maxLength = 0;

    for (int right = 0; right < s.length(); right++) {
        // TODO: expand window
        
        // TODO: shrink/shift window if invalid
        
        // TODO: update maxLength
    }

    return maxLength;
}

```

*I chose an array of size 26 because mapping `A-Z` to indices `0-25` is highly efficient for lookup and update.*

#### Iteration 2: Expanding the window

Now we add the logic to pull characters into the window and update our maximum frequency tracking.

```java
int characterReplacement(String s, int k) {
    if (s == null || s.isEmpty()) {
        return 0;
    }

    int[] counts = new int[26];
    int left = 0;
    int maxFrequency = 0;
    int maxLength = 0;

    for (int right = 0; right < s.length(); right++) {
        // Added: Map character to 0-25 and update its frequency
        int rightCharIndex = s.charAt(right) - 'A';
        counts[rightCharIndex]++;
        
        // Added: Keep track of the highest frequency we've seen
        maxFrequency = Math.max(maxFrequency, counts[rightCharIndex]);
        
        // TODO: shrink/shift window if invalid
        
        // TODO: update maxLength
    }

    return maxLength;
}

```

#### Iteration 3: Complete the happy path

Finally, we add the logic to validate the window. If the number of characters we have to change exceeds `k`, we must move the `left` pointer to maintain the maximum valid window size we've achieved so far.

```java
int characterReplacement(String s, int k) {
    if (s == null || s.isEmpty()) {
        return 0;
    }

    int[] counts = new int[26];
    int left = 0;
    int maxFrequency = 0;
    int maxLength = 0;

    for (int right = 0; right < s.length(); right++) {
        int rightCharIndex = s.charAt(right) - 'A';
        counts[rightCharIndex]++;
        
        maxFrequency = Math.max(maxFrequency, counts[rightCharIndex]);
        
        // Added: Check window validity.
        // Current window size is (right - left + 1)
        int windowSize = right - left + 1;
        if (windowSize - maxFrequency > k) {
            // The window is invalid. Shift the left pointer rightward.
            int leftCharIndex = s.charAt(left) - 'A';
            counts[leftCharIndex]--;
            left++;
        }
        
        // Added: Record the size of the valid window.
        // Because of the shift above, (right - left + 1) is always a valid size.
        maxLength = Math.max(maxLength, right - left + 1);
    }

    return maxLength;
}

```

#### Edge-case pass

1. **Empty string / null string**: Covered explicitly at the top of the method.
2. **`k` is very large (e.g., `k >= s.length()`)**: If `k` is huge, `windowSize - maxFrequency > k` will never be true. The `left` pointer will remain at 0, and `maxLength` will grow to `s.length()`. This is correct.
3. **No valid replacements needed (e.g., `s="AAAA", k=0`)**: `windowSize` matches `maxFrequency`, so `windowSize - maxFrequency` is exactly 0, which is `<= k`. The window expands to the end. Correct.

No further patches are needed.

### 8. Analyze expensive sections and optimize

Looking at the final code:

* We iterate over the string exactly once with the `right` pointer.
* The `left` pointer also moves forward, but since we used the `if` statement instead of a `while` loop (the historical maximum optimization), `left` moves at most N times (in fact, it moves exactly in tandem with `right` once the max window size is reached).
* Array lookups (`counts[rightCharIndex]`) are O(1).
* Math operations are O(1).

There are no nested loops scanning arrays, no sorting, and no complex object creation. The complexity is optimal.

* **Time Complexity:** O(N), where N is the length of string `s`.
* **Space Complexity:** O(1), since the `counts` array size is bounded by 26 regardless of the size of the input string.

### 9. Final Answer Structure

Here is the final, clean Java implementation:

```java
class Solution {
    public int characterReplacement(String s, int k) {
        if (s == null || s.isEmpty()) {
            return 0;
        }

        int[] counts = new int[26];
        int left = 0;
        int maxFrequency = 0;
        int maxLength = 0;

        for (int right = 0; right < s.length(); right++) {
            int rightCharIndex = s.charAt(right) - 'A';
            counts[rightCharIndex]++;
            
            // Track the maximum frequency of any single character seen in a window so far.
            maxFrequency = Math.max(maxFrequency, counts[rightCharIndex]);
            
            // If the characters we need to replace exceeds k, shift the window.
            // Note: We use 'if' instead of 'while' because we only care about finding a 
            // *longer* window. If it's invalid, we shift the window rightward without shrinking it.
            int windowSize = right - left + 1;
            if (windowSize - maxFrequency > k) {
                int leftCharIndex = s.charAt(left) - 'A';
                counts[leftCharIndex]--;
                left++;
            }
            
            // The window length at this point is guaranteed to be valid for the historical max.
            maxLength = Math.max(maxLength, right - left + 1);
        }

        return maxLength;
    }
}

```

#### Brief Test Walkthrough

Test case: `s = "AAB", k = 1`

1. `right = 0` ('A'): `counts['A']=1`, `maxFrequency = 1`. Window "A". `1 - 1 = 0 <= 1`. `maxLength = 1`.
2. `right = 1` ('A'): `counts['A']=2`, `maxFrequency = 2`. Window "AA". `2 - 2 = 0 <= 1`. `maxLength = 2`.
3. `right = 2` ('B'): `counts['B']=1`, `maxFrequency = 2`. Window "AAB". `3 - 2 = 1 <= 1`. `maxLength = 3`.

Returns `3`. This aligns with our expectations, as we can replace 'B' with 'A' to get "AAA" (length 3).