### 1. Restate the problem

We are given an array of integers, `nums`. We need to find the maximum length of a "strictly increasing subsequence".

A subsequence is formed by picking elements from the array from left to right, skipping some (or no) elements. "Strictly increasing" means each picked element must be strictly greater than the one before it. We must return the length of the longest possible valid sequence, not the sequence itself.

### 2. Ask clarifying questions

Before writing any code, I want to clarify a few assumptions about the input:

* **Input size:** What is the maximum length of `nums`? (Assumption: Up to $10^5$, meaning an $O(N^2)$ algorithm might time out, so we should aim for $O(N \log N)$ if possible).
* **Null or empty input:** Can `nums` be null or empty? (Assumption: The array will not be null, but could have a length of 0. If it's empty, the answer is 0).
* **Negative values:** Can elements be negative? (Assumption: Yes, normal integer range applies).
* **Duplicates:** How should duplicates be handled? (Assumption: The sequence must be *strictly* increasing, so duplicates cannot appear consecutively in our valid subsequence).
* **Modification:** Can I modify the input array? (Assumption: It's best to leave the input array unmodified unless necessary to save space).

### 3. Work through an example by hand

Let's trace a representative input: `nums = [10, 9, 2, 5, 3, 7, 101, 18]`

Instead of storing the whole sequence, I only care about the best possible *ending* value for a sequence of a given length. Smaller endings are always better because they leave more room for future numbers to be appended.

Let's maintain an active list of the smallest tail values for increasing subsequences of length 1, 2, 3, etc.

1. Read `10`: Smallest tail for length 1 is 10. (State: `[10]`)
2. Read `9`: 9 is smaller than 10, so a sequence of length 1 is better off ending in 9. (State: `[9]`)
3. Read `2`: 2 is smaller than 9. Best tail for length 1 is now 2. (State: `[2]`)
4. Read `5`: 5 is greater than 2. We can form a sequence of length 2 ending in 5. (State: `[2, 5]`)
5. Read `3`: 3 is between 2 and 5. We can form a sequence of length 2 ending in 3 (replacing 5). (State: `[2, 3]`)
6. Read `7`: 7 is greater than 3. We form a sequence of length 3 ending in 7. (State: `[2, 3, 7]`)
7. Read `101`: 101 > 7. Sequence of length 4. (State: `[2, 3, 7, 101]`)
8. Read `18`: 18 is between 7 and 101. It replaces 101 for the best tail of length 4. (State: `[2, 3, 7, 18]`)

The length of our tracking state is 4. The longest strictly increasing subsequence is 4.

### 4. Brainstorm solutions aloud

**Approach 1: Direct Simulation / Brute Force DFS**

* **Core idea:** For every element, branch into two paths: either include it in our subsequence (if valid) or skip it.
* **Complexity:** Time is $O(2^N)$ because we explore all subsets. Space is $O(N)$ for the recursion stack.
* **Tradeoffs:** Trivial to verify but far too slow for arrays larger than ~20 elements.

**Approach 2: Dynamic Programming (DP)**

* **Core idea:** Maintain an array `dp` where `dp[i]` stores the length of the longest increasing subsequence ending at index `i`. For each element `nums[i]`, we look back at every previous element `nums[j]` (where `j < i`). If `nums[i] > nums[j]`, we can extend that subsequence: `dp[i] = max(dp[i], dp[j] + 1)`.
* **Complexity:** Time is $O(N^2)$ due to the nested loop. Space is $O(N)$ to store the `dp` array.
* **Tradeoffs:** Reliable and easy to implement, but $O(N^2)$ is too slow if the array has $10^5$ elements.

**Approach 3: Patience Sorting / DP with Binary Search**

* **Core idea:** This mimics the manual example. We maintain an array `tails` where `tails[k]` stores the smallest tail of all increasing subsequences of length `k + 1`. Because `tails` is naturally sorted, we can use binary search to find the correct insertion or replacement index for each new number.
* **Data structures:** A standard integer array to act as `tails`, and a variable tracking its effective size.
* **Complexity:** Time is $O(N \log N)$ because we do a logarithmic binary search for each of the $N$ elements. Space is $O(N)$ for the `tails` array.
* **Tradeoffs:** Slightly harder to reason about the binary search boundaries, but perfectly satisfies the strictest time constraints.

### 5. Select the solution

I will use **Approach 3 (DP with Binary Search)**. It is optimal ($O(N \log N)$) and relies on a fundamental computer science concept (binary search over a monotonic sequence).

To keep the code clear, I will isolate the binary search logic into a small helper method. This makes the main algorithm read like plain English and cleanly separates the state updates from the index math.

### 6. Write the implementation outline

```java
int lengthOfLIS(int[] nums) {
    /*
     * Reframe:
     * We want to build an active sequence of minimum possible tail values 
     * for increasing subsequences. The length of this active sequence is the answer.
     *
     * State:
     * `tails` array: stores the smallest tail value for a subsequence of length `i + 1`.
     * `activeLength`: an integer tracking how many elements in `tails` are currently used.
     * Chosen because:
     * Tracking the smallest possible ending values maximizes our chances 
     * of appending future elements.
     *
     * Invariant:
     * The active portion of the `tails` array (from index 0 to activeLength - 1) 
     * is always strictly increasing.
     *
     * Helpers:
     * findInsertionPoint(tails, activeLength, target)
     * - Performs binary search to find the first index in `tails` that is >= target.
     *
     * Core logic:
     * - initialize `tails` array to size of input
     * - iterate through each number in `nums`:
     *   - use the helper to find where the number belongs in `tails`
     *   - overwrite the value at that index with the current number
     *   - if the index equals `activeLength`, the number is larger than any known tail, 
     *     so we've found a longer subsequence. Increment `activeLength`.
     * - return `activeLength`
     *
     * Edge cases:
     * - empty input array -> return 0 immediately
     */
}

```

### 7. Implement iteratively

#### Iteration 1: Method skeleton

I'll set up the main state variables, the `tails` array, and the loop structure. I'll leave the binary search helper empty for now.

```java
public int lengthOfLIS(int[] nums) {
    int[] tails = new int[nums.length];
    int activeLength = 0;

    for (int num : nums) {
        // TODO: Find the correct index to place or replace 'num'
        // TODO: Update the tails array
        // TODO: Expand activeLength if necessary
    }

    return activeLength;
}

private int findInsertionPoint(int[] tails, int length, int target) {
    // TODO: Binary search logic
    return 0; 
}

```

#### Iteration 2: Binary Search Helper

I'll implement the helper. We need the index of the first element in `tails` that is greater than or equal to the `target`. This is a standard binary search for the lower bound.

```java
private int findInsertionPoint(int[] tails, int length, int target) {
    int left = 0;
    int right = length; // The boundary is 'length', allowing us to append at the end

    while (left < right) {
        int mid = left + (right - left) / 2;
        if (tails[mid] >= target) {
            // Target belongs in the left half, or is exactly at mid.
            right = mid;
        } else {
            // Target is strictly greater than tails[mid], belongs in right half.
            left = mid + 1;
        }
    }

    // left == right at the end, representing the correct insertion/replacement index
    return left;
}

```

#### Iteration 3: Complete the happy path

Now I'll wire the helper into the main loop to perform the updates on the `tails` state.

```java
public int lengthOfLIS(int[] nums) {
    int[] tails = new int[nums.length];
    int activeLength = 0;

    for (int num : nums) {
        // Added: Find exactly where this number belongs to maintain the invariant
        int index = findInsertionPoint(tails, activeLength, num);
        
        // Added: Place or replace the tail value
        tails[index] = num;
        
        // Added: If we placed this at the very end of our tracked tails, our sequence grew
        if (index == activeLength) {
            activeLength++;
        }
    }

    return activeLength;
}

```

#### Edge-case pass

Let's review the edge cases from the outline.

* **Empty input:** If `nums.length == 0`, the current loop skips, and we return `activeLength`, which is 0. This works perfectly. No patch needed. (Though an early exit `if (nums == null || nums.length == 0) return 0;` is a good defensive practice).
* **All elements identical (`[7, 7, 7, 7]`):** `1st 7` placed at index 0. `activeLength`=1. `2nd 7` binary searches, finds `tails[0] >= 7`, replaces index 0 with 7. `activeLength` stays 1. Result is 1. Correct, as subsequences must be *strictly* increasing.
* **Already strictly increasing:** Each element will be placed exactly at `activeLength`. Returns `N`. Correct.

I will add a quick null/empty check at the top just to be completely safe and document the contract.

### 8. Final code

```java
public int lengthOfLIS(int[] nums) {
    if (nums == null || nums.length == 0) {
        return 0;
    }

    int[] tails = new int[nums.length];
    int activeLength = 0;

    for (int num : nums) {
        int index = findInsertionPoint(tails, activeLength, num);
        
        tails[index] = num;
        
        if (index == activeLength) {
            activeLength++;
        }
    }

    return activeLength;
}

private int findInsertionPoint(int[] tails, int length, int target) {
    int left = 0;
    int right = length;

    while (left < right) {
        int mid = left + (right - left) / 2;
        if (tails[mid] >= target) {
            right = mid;
        } else {
            left = mid + 1;
        }
    }

    return left;
}

```

### 9. Complexity

* **Time Complexity:** $O(N \log N)$. We iterate over the `nums` array exactly once, which takes $N$ steps. For each element, we call `findInsertionPoint`, which performs a binary search over at most $N$ elements, taking $O(\log N)$ time. $N \times O(\log N) = O(N \log N)$.
* **Space Complexity:** $O(N)$. We allocate the `tails` array which scales linearly with the size of the input `nums`.

### 10. Brief test walkthrough

Let's do a quick trace of our main code with a stressful sequence: `nums = [4, 10, 4, 3, 8, 9]`.

1. `num = 4`: `tails` is empty. `index`=0. `tails[0]=4`. `activeLength` becomes 1.
2. `num = 10`: Binary search finds `index`=1. `tails[1]=10`. `activeLength` becomes 2. (`tails` is `[4, 10]`)
3. `num = 4`: Binary search finds `tails[0] >= 4`. `index`=0. `tails[0]=4`. `activeLength` stays 2. (`tails` is `[4, 10]`)
4. `num = 3`: Binary search finds `tails[0] >= 3`. `index`=0. `tails[0]=3`. `activeLength` stays 2. (`tails` is `[3, 10]`)
5. `num = 8`: Binary search finds `tails[1] >= 8`. `index`=1. `tails[1]=8`. `activeLength` stays 2. (`tails` is `[3, 8]`)
6. `num = 9`: Binary search finds `index`=2. `tails[2]=9`. `activeLength` becomes 3. (`tails` is `[3, 8, 9]`)

The loop finishes. We return `activeLength`, which is 3. This is correct because `[3, 8, 9]` and `[4, 8, 9]` are the longest strictly increasing subsequences. The invariant held perfectly.