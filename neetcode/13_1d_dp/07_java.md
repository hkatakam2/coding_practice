### 1. Restate the problem

We need to find the total number of valid ways to decode a string of digits into letters, given the mapping A=1, B=2, ... Z=26.

A valid decoding means we partition the string into chunks of 1 or 2 digits such that:

* Every chunk forms a valid number between 1 and 26.
* No chunk has a leading zero (e.g., "01" is invalid).

### 2. Ask clarifying questions

Before writing code, I want to confirm a few details about the constraints and inputs:

* **Can the input string be empty or null?** (Assumption: Null returns 0, empty string might theoretically be 0 or 1 depending on definitions, but I will assume `length >= 1` based on the prompt. I'll handle empty as 0.)
* **Are there non-digit characters in the string?** (Assumption: No, the prompt states it contains *only* digits.)
* **Can the string be un-decodable?** For example, "30" or "00". (Assumption: Yes, and we should return 0 in those cases).
* **Return type:** The prompt says the answer fits in a 32-bit integer, so returning an `int` is perfect.

### 3. Work through an example by hand

Let's trace the string `s = "226"`.

* **Prefix "" (empty):** 1 way to decode (conceptually, the base state).
* **Prefix "2":**
* Valid as 'B'.
* Total ways: 1.


* **Prefix "22":**
* As single digit '2' added to previous: "2" + "2" (B, B).
* As double digit '22' added to empty: "22" (V).
* Total ways: 2.


* **Prefix "226":**
* As single digit '6' added to previous: Valid, so we carry over the 2 ways from "22" -> (B, B, F) and (V, F).
* As double digit '26' added to prefix "2": Valid, so we carry over the 1 way from "2" -> (B, Z).
* Total ways: 2 + 1 = 3.



### 4. Brainstorm solutions aloud

* **Direct Recursion (DFS):** We could branch at every step—try taking 1 digit, then recurse; try taking 2 digits, then recurse. However, this re-evaluates the same suffixes repeatedly. The time complexity would be $O(2^n)$ in the worst case.
* **Top-Down Memoization:** We can cache the recursive calls in a `HashMap` or array based on the current index. This brings the time complexity down to $O(n)$ and requires $O(n)$ space for the call stack and cache.
* **Bottom-Up Dynamic Programming (1D Array):** We can build the solution from left to right exactly like the manual example. We store the number of ways to decode prefixes in an array `dp[]` of size $n+1$. `dp[i]` depends only on `dp[i-1]` (if the last digit is valid) and `dp[i-2]` (if the last two digits are valid). Time is $O(n)$, space is $O(n)$.
* **Space-Optimized DP:** Notice that `dp[i]` only ever looks back at the immediate two previous states. Like calculating the Fibonacci sequence, we only need to keep track of the last two values (`prev1` and `prev2`) instead of the whole array. Time is $O(n)$, space is $O(1)$.

### 5. Select the solution

I'll build the **Bottom-Up Dynamic Programming (1D Array)** first because it maps perfectly to the manual example, is extremely safe to implement without off-by-one errors, and is easy to explain.

While Streams are great for aggregations, they are a poor fit here because this algorithm requires sequential state transitions where the current step intimately depends on previous steps. A standard `for` loop is much more readable here. I will use primitive math instead of creating substrings to avoid unnecessary object allocation.

Later, I will optimize it to $O(1)$ space.

### 6. Write the implementation outline

```java
int numDecodings(String s) {
    /*
     * Reframe:
     * Build the number of valid decodings from left to right, adding the 
     * ways to decode the last 1-digit and 2-digit chunks.
     *
     * State:
     * An integer array `dp` of size n + 1. 
     * Chosen because we need to build answers for prefixes based on smaller prefixes.
     *
     * Invariant:
     * dp[i] contains the exact number of valid decodings for the substring of length i.
     *
     * Core logic:
     * - initialize dp[0] to 1 (base case for successful 2-digit match)
     * - initialize dp[1] based on whether the first digit is non-zero
     * - iterate from length 2 up to n
     * - if the 1-digit chunk is valid (1-9), add dp[i-1] to dp[i]
     * - if the 2-digit chunk is valid (10-26), add dp[i-2] to dp[i]
     * - return dp[n]
     *
     * Edge cases:
     * - leading zero at the start of the string
     * - continuous zeros like "100" (which will safely resolve to 0 in DP)
     */
}

```

### 7. Implement iteratively

**Iteration 1: method skeleton & base cases**
We'll set up the array and handle the first character.

```java
public int numDecodings(String s) {
    if (s == null || s.isEmpty() || s.charAt(0) == '0') {
        return 0; 
    }

    int n = s.length();
    int[] dp = new int[n + 1];
    
    // Base cases
    dp[0] = 1; // 1 way to decode an empty string conceptually
    dp[1] = 1; // We already checked for leading '0', so 1 character has 1 way

    // TODO: Loop from length 2 to n to build the rest of dp array
    
    return dp[n];
}

```

**Iteration 2: Adding the core loop**
Now I will implement the loop, extracting the integer values of the current 1-digit and 2-digit chunks to decide if we inherit previous counts. I'll use character arithmetic (`charAt(i) - '0'`) which is faster and cleaner than `Integer.parseInt(s.substring(...))`.

```java
public int numDecodings(String s) {
    if (s == null || s.isEmpty() || s.charAt(0) == '0') {
        return 0;
    }

    int n = s.length();
    int[] dp = new int[n + 1];
    dp[0] = 1;
    dp[1] = 1; 

    for (int i = 2; i <= n; i++) {
        // Digits are 0-indexed in the string, so i-1 is the current character
        int oneDigit = s.charAt(i - 1) - '0';
        int twoDigits = (s.charAt(i - 2) - '0') * 10 + oneDigit;

        // If a single digit is valid, we can form a letter by itself.
        if (oneDigit >= 1 && oneDigit <= 9) {
            dp[i] += dp[i - 1];
        }

        // If the two digits form a valid letter (10 to 26), 
        // we can form a letter together.
        if (twoDigits >= 10 && twoDigits <= 26) {
            dp[i] += dp[i - 2];
        }
    }

    return dp[n];
}

```

**Edge-case pass:**

* **Empty/Null:** Caught by early return.
* **"06":** Starts with zero. Caught by `s.charAt(0) == '0'` early return.
* **"10":**
* `i = 2`. `oneDigit = 0`, `twoDigits = 10`.
* `oneDigit` is ignored. `twoDigits` is valid (10), so `dp[2] += dp[0]` (which is 1). Returns 1. Correct ('J').


* **"30":**
* `i = 2`. `oneDigit = 0`, `twoDigits = 30`.
* Neither `if` block matches. `dp[2]` remains 0. Loop finishes, returns 0. Correct (invalid).


* **"100":**
* At `i=2`, `dp[2]=1` (from "10").
* At `i=3`, `oneDigit=0`, `twoDigits=00`. Neither matches. `dp[3]` remains 0. Returns 0. Correct.



### 8. Analyze expensive sections and optimize

**Analysis:**
Currently, our solution runs in $O(n)$ time because we iterate through the string once, performing constant-time character arithmetic at each step.
The space complexity is $O(n)$ because we allocate an array of size $n+1$.

**Optimization:**
Notice inside our loop: `dp[i]` only relies on `dp[i - 1]` and `dp[i - 2]`.
We don't need the entire history—we only need to store the two most recent states. We can replace the `dp` array with two integer variables to achieve $O(1)$ space complexity.

**Proposed change:**
Introduce `twoBack` (representing `dp[i-2]`) and `oneBack` (representing `dp[i-1]`).

### Final Code

```java
public class Solution {
    public int numDecodings(String s) {
        // Early exit for invalid starting configurations
        if (s == null || s.isEmpty() || s.charAt(0) == '0') {
            return 0;
        }

        // twoBack represents dp[i-2], oneBack represents dp[i-1]
        int twoBack = 1;
        int oneBack = 1;

        for (int i = 2; i <= s.length(); i++) {
            int currentWays = 0;
            
            int oneDigit = s.charAt(i - 1) - '0';
            int twoDigits = (s.charAt(i - 2) - '0') * 10 + oneDigit;

            // Check if the 1-digit chunk is valid (1-9)
            if (oneDigit >= 1 && oneDigit <= 9) {
                currentWays += oneBack;
            }

            // Check if the 2-digit chunk is valid (10-26)
            if (twoDigits >= 10 && twoDigits <= 26) {
                currentWays += twoBack;
            }

            // Shift states forward for the next iteration
            twoBack = oneBack;
            oneBack = currentWays;
        }

        return oneBack;
    }
}

```

### Complexity

* **Time Complexity:** $O(n)$ where $n$ is the length of the string. We scan the string exactly once. The character lookups and math operations run in $O(1)$ time.
* **Space Complexity:** $O(1)$. We are only storing three integer variables (`twoBack`, `oneBack`, and `currentWays`), completely eliminating the $O(n)$ array allocation.

### Brief test walkthrough

Let's quickly run the optimized code on `s = "226"`:

* `twoBack = 1`, `oneBack = 1`
* **i = 2 ('2'):**
* `oneDigit = 2` (valid) -> `currentWays += 1` (1)
* `twoDigits = 22` (valid) -> `currentWays += 1` (2)
* `twoBack = 1`, `oneBack = 2`


* **i = 3 ('6'):**
* `oneDigit = 6` (valid) -> `currentWays += 2` (2)
* `twoDigits = 26` (valid) -> `currentWays += 1` (3)
* `twoBack = 2`, `oneBack = 3`


* Loop ends. Returns `oneBack` which is 3. Matches expected output!