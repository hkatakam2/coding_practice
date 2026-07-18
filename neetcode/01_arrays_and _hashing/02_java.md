### 1. Restatement

We are given two strings, `s` and `t`. We need to determine if they are anagrams of each other.
An anagram is a word or phrase formed by rearranging the letters of a different word or phrase, typically using all the original letters exactly once.

* **Given:** Two string variables, `s` and `t`.
* **Returns:** A boolean: `true` if they are anagrams, `false` otherwise.
* **Constraint:** The frequencies of every character in `s` must exactly match the frequencies in `t`. Order does not matter.

### 2. Ask clarifying questions

In a real interview, I would ask the following to bound the problem:

* **Character set:** Are the strings guaranteed to be lowercase English letters, or can they contain uppercase, numbers, symbols, or full Unicode characters?
* **Whitespace and punctuation:** Should spaces or punctuation be ignored, or treated as exact literal characters?
* **Null inputs:** Can `s` or `t` be null?
* **Size:** What is the maximum length of the strings? Will they fit comfortably in memory?

**Assumption to proceed:**
The strings are non-null and consist entirely of lowercase English letters (`a-z`). They can be up to $10^5$ characters long.

### 3. Work through an example by hand

Let's trace `s = "cat"`, `t = "act"`.

1. Check lengths: both are length 3. (If they differed, they couldn't be anagrams).
2. Set up a way to track character frequencies.
3. Scan `s` ("cat"):
* 'c': count becomes 1
* 'a': count becomes 1
* 't': count becomes 1


4. Scan `t` ("act") and subtract from our tracked frequencies:
* 'a': count becomes 0
* 'c': count becomes 0
* 't': count becomes 0


5. Check all counts. They are all 0. The strings are anagrams.

### 4. Brainstorm solutions aloud

**Approach 1: Sorting**

* **Core idea:** Convert both strings to character arrays, sort them, and compare if they are exactly equal.
* **Data structures:** Two `char[]`.
* **Time complexity:** $O(n \log n)$ due to sorting, where $n$ is the length of the strings.
* **Space complexity:** $O(n)$ to hold the character arrays.
* **Tradeoffs:** Very easy to write (a few lines of standard library calls), but $O(n \log n)$ time is suboptimal for a simple frequency check.

**Approach 2: HashMap Frequency Counting**

* **Core idea:** Iterate through `s` and populate a `HashMap<Character, Integer>` with character counts. Then iterate through `t`, decrementing counts. If any count goes below zero or remains above zero, return false.
* **Data structures:** `HashMap`.
* **Time complexity:** Expected $O(n)$.
* **Space complexity:** $O(U)$ where $U$ is the number of unique characters.
* **Tradeoffs:** Great for vast Unicode character sets, but the overhead of object boxing (Character/Integer) and hashing makes it slower than necessary for small, fixed alphabets.

**Approach 3: Array-based Frequency Map**

* **Core idea:** Because we are restricted to lowercase English letters, there are only 26 possible characters. We can use a simple `int[26]` array. We increment the index corresponding to a character for `s`, and decrement for `t`.
* **Data structures:** A fixed-size `int[]`.
* **Time complexity:** $O(n)$ time to scan strings, $O(1)$ time to check the 26 buckets.
* **Space complexity:** $O(1)$ auxiliary space, since the array is always size 26 regardless of string length.
* **Tradeoffs:** Highly performant, avoids garbage collection overhead, but brittle if the requirements suddenly change to support full Unicode.

### 5. Select the solution

I will proceed with **Approach 3: Array-based Frequency Map**.
It perfectly fits the constraint of lowercase English letters, is extremely space-efficient ($O(1)$), and avoids the boxing/unboxing overhead of a HashMap. It's the standard, most readable optimization for string problems with fixed alphabets.

### 6. Write the implementation outline

```java
boolean isAnagram(String s, String t) {
    /*
     * Reframe:
     * Check if two strings have identical character frequencies.
     *
     * State:
     * A 26-element integer array tracking the net balance of characters.
     * Chosen because lowercase English letters map cleanly to indices 0-25.
     *
     * Invariant:
     * After processing both strings, a perfect anagram leaves all array buckets at 0.
     *
     * Core logic:
     * - if lengths differ, return false immediately
     * - initialize the frequency array
     * - loop through both strings simultaneously
     * - increment the count for the character in s
     * - decrement the count for the character in t
     * - loop through the frequency array
     * - if any bucket is not 0, return false
     * - return true if all buckets are 0
     *
     * Edge cases:
     * - Different string lengths (handled by early return)
     * - Empty strings (correctly bypasses loops and returns true)
     */
}

```

### 7. Implement iteratively

**Iteration 1: Method skeleton**
I will set up the fast-fail check, the data structure, and the broad control flow.

```java
public boolean isAnagram(String s, String t) {
    // Fast fail for mismatched lengths
    if (s.length() != t.length()) {
        return false;
    }

    int[] charCounts = new int[26];

    // TODO: Process both strings to calculate net character balance
    // TODO: Verify all balances are zero

    return true;
}

```

**Iteration 2: Populate character counts**
Now, I'll add the single-pass loop. Since we already proved the strings are the same length, we can safely use one index to traverse both strings simultaneously.

```java
public boolean isAnagram(String s, String t) {
    if (s.length() != t.length()) {
        return false;
    }

    int[] charCounts = new int[26];

    // Added: single-pass frequency update
    for (int i = 0; i < s.length(); i++) {
        charCounts[s.charAt(i) - 'a']++;
        charCounts[t.charAt(i) - 'a']--;
    }

    // TODO: Verify all balances are zero

    return true;
}

```

*Note: `s.charAt(i) - 'a'` is a standard Java idiom for mapping 'a'-'z' to 0-25.*

**Iteration 3: Complete the happy path**
Finally, we check the array to enforce our invariant: if they are anagrams, every bucket must be exactly zero.

```java
public boolean isAnagram(String s, String t) {
    if (s.length() != t.length()) {
        return false;
    }

    int[] charCounts = new int[26];

    for (int i = 0; i < s.length(); i++) {
        charCounts[s.charAt(i) - 'a']++;
        charCounts[t.charAt(i) - 'a']--;
    }

    // Added: verify neutral balance
    for (int count : charCounts) {
        if (count != 0) {
            return false;
        }
    }

    return true;
}

```

**Edge-case pass**

* *Empty strings:* `s = ""`, `t = ""`. Lengths match (0 == 0). The `for` loops are skipped. The final verification loop sees 26 zeros. Returns `true`. Correct.
* *Differing lengths:* `s = "a"`, `t = "ab"`. Early length check catches this and returns `false`. Correct.
* *Same characters, different frequencies:* `s = "aab"`, `t = "abb"`. 'a' ends up with `+1`, 'b' ends up with `-1`. The verification loop detects the non-zero and returns `false`. Correct.

No code patches are needed. The logic is robust.

### 8. Analyze expensive sections and optimize

Because we use a primitive array, there are no expensive Object allocations or garbage collection events inside the loop. The `charAt` method on a standard `String` is $O(1)$.
This is virtually optimal for Java.

**Final code**

```java
class Solution {
    public boolean isAnagram(String s, String t) {
        if (s.length() != t.length()) {
            return false;
        }

        int[] charCounts = new int[26];

        for (int i = 0; i < s.length(); i++) {
            charCounts[s.charAt(i) - 'a']++;
            charCounts[t.charAt(i) - 'a']--;
        }

        for (int count : charCounts) {
            if (count != 0) {
                return false;
            }
        }

        return true;
    }
}

```

**Complexity**

* **Time Complexity:** $O(n)$, where $n$ is the length of string `s`. We do one pass over the strings of size $n$, and one pass over a constant-size array of length 26.
* **Space Complexity:** $O(1)$ auxiliary space. The `charCounts` array is always 26 integers, regardless of the input string length.

**Brief test walkthrough**

* **Test 1 (Valid Anagram):** `s = "anagram"`, `t = "nagaram"`. Lengths are both 7. The loop processes characters. `a` is added 3 times and subtracted 3 times. All other letters balance similarly. The final loop confirms all values in `charCounts` are 0. Returns `true`.
* **Test 2 (Different Frequencies):** `s = "rat"`, `t = "car"`. Lengths are both 3. `charCounts['r' - 'a']` gets $+1$ and $-1$. `charCounts['a' - 'a']` gets $+1$ and $-1$. But `charCounts['t' - 'a']` gets $+1$, and `charCounts['c' - 'a']` gets $-1$. The final loop hits the non-zero count for 'c' and returns `false`.