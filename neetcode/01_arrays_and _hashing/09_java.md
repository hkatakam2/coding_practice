### 1. Restate the problem

We are given an array of integers. We need to find the length of the longest sequence of consecutive whole numbers present in the array.
The numbers in the sequence do not need to appear consecutively or in order within the original array.
The critical constraint is that our algorithm must run in strictly $O(n)$ time.

### 2. Ask clarifying questions

Before writing code, I would clarify a few details:

* **Input size:** What is the maximum length of the `nums` array? (Assumption: can fit in standard memory, up to $10^5$).
* **Empty input:** Can the input array be empty? (Assumption: Yes, in which case the answer should be 0).
* **Duplicates:** Can the array contain duplicate numbers? (Assumption: Yes, and duplicates do not count toward the sequence length—e.g., `[1, 2, 2, 3]` has a max sequence length of 3).
* **Integer range:** Can the numbers be negative or zero? (Assumption: Yes, they can be any valid 32-bit integer).
* **Mutation:** Is it okay to modify the input array, or should I treat it as read-only? (Assumption: Read-only is safer, though $O(n)$ limits what modifications we could do anyway).

### 3. Work through an example by hand

Let's take a representative input: `nums = [100, 4, 200, 1, 3, 2]`

1. I need to identify groups of consecutive numbers:
* `100` stands alone (sequence of 1).
* `4, 1, 3, 2` forms a sequence `1, 2, 3, 4` (sequence of 4).
* `200` stands alone (sequence of 1).


2. The longest sequence length here is 4.

If I process this manually, I might look for the smallest number of a sequence.

* Is 100 the start of a sequence? Yes, because 99 isn't there. Count up: only 100 is present. Length = 1.
* Is 4 the start? No, because 3 is present. Skip it.
* Is 200 the start? Yes, 199 isn't there. Length = 1.
* Is 1 the start? Yes, 0 isn't there. Count up: 1, 2, 3, 4 are present. Length = 4.
* Is 3 the start? No, 2 is present.
* Is 2 the start? No, 1 is present.

The maximum length observed is 4.

### 4. Brainstorm solutions aloud

**Approach 1: Brute Force**

* **Idea:** For every number in the array, search the array for `number + 1`, then `number + 2`, etc., keeping track of the streak.
* **Time complexity:** $O(n^3)$ in the worst case (searching the array takes $O(n)$ for each step of a sequence that might be $O(n)$ long).
* **Space complexity:** $O(1)$.
* **Verdict:** Too slow.

**Approach 2: Sorting**

* **Idea:** Sort the array first. Then iterate through it once, keeping a running count of consecutive numbers, resetting the count when the gap is greater than 1, and ignoring duplicates.
* **Time complexity:** $O(n \log n)$ due to the sort.
* **Space complexity:** $O(1)$ or $O(n)$ depending on the sorting algorithm.
* **Verdict:** Very easy to implement, but violates the strict $O(n)$ time constraint.

**Approach 3: HashSet with Intelligent Sequence Building**

* **Idea:** Put all numbers into a `HashSet` to achieve $O(1)$ lookups. To ensure we only do $O(n)$ total work, we only attempt to build a sequence if the current number is the *start* of a sequence. We know a number is a start if `number - 1` is not in the `HashSet`.
* **Time complexity:** $O(n)$. Inserting elements takes $O(n)$. Iterating through the set takes $O(n)$. The inner while-loop only runs for valid consecutive numbers, meaning each number is visited inside the while-loop at most once across the entire algorithm. Total time is $O(n) + O(n) = O(n)$.
* **Space complexity:** $O(n)$ to store the numbers in the `HashSet`.
* **Verdict:** This perfectly satisfies the constraints.

### 5. Select the solution

I will use the **HashSet (Approach 3)**.

* It comfortably satisfies the $O(n)$ time constraint.
* It is easy to explain and implement.
* The use of `HashSet` perfectly matches the problem's need for fast, un-ordered existence checks.

### 6. Write the implementation outline

```java
int longestConsecutive(int[] nums) {
    /*
     * Reframe:
     * Find the longest streak of consecutive numbers in O(n) time by only 
     * evaluating streaks from their true starting point.
     *
     * State:
     * A HashSet containing all unique numbers from the input.
     * Chosen because we need O(1) lookups to check for the presence of n-1 and n+1.
     *
     * Invariant:
     * Every sequence is counted exactly once, starting from its minimum value.
     *
     * Core logic:
     * - handle the empty array edge case immediately
     * - add all array elements to a HashSet to remove duplicates and allow fast lookup
     * - iterate through each number in the set
     * - if the number is the start of a sequence (i.e., set does not contain num - 1):
     *     - count upwards (num + 1, num + 2, etc.) as long as the set contains the next number
     *     - update the maximum sequence length seen so far
     * - return the maximum sequence length
     *
     * Edge cases:
     * - empty input array
     * - arrays with heavy duplicates
     * - negative numbers
     */
}

```

### 7. Implement iteratively

**Iteration 1: Method skeleton and state initialization**
First, I will create the `HashSet`, populate it, and set up the main loop and return variable.

```java
int longestConsecutive(int[] nums) {
    if (nums == null || nums.length == 0) {
        return 0;
    }

    Set<Integer> numSet = new HashSet<>();
    for (int num : nums) {
        numSet.add(num);
    }

    int maxLength = 0;

    // TODO: iterate over numSet and find sequences

    return maxLength;
}

```

**Iteration 2: Finding sequence starts**
Now, I'll iterate through the set. I only care about a number if it's the start of a sequence.

```java
int longestConsecutive(int[] nums) {
    if (nums == null || nums.length == 0) {
        return 0;
    }

    Set<Integer> numSet = new HashSet<>();
    for (int num : nums) {
        numSet.add(num);
    }

    int maxLength = 0;

    for (int num : numSet) {
        // Added: Only start counting if 'num' is the first number of a sequence
        if (!numSet.contains(num - 1)) {
            // TODO: count consecutive numbers starting from 'num'
        }
    }

    return maxLength;
}

```

**Iteration 3: Complete the happy path**
Finally, I will add the logic to trace the sequence and update the maximum length.

```java
int longestConsecutive(int[] nums) {
    if (nums == null || nums.length == 0) {
        return 0;
    }

    Set<Integer> numSet = new HashSet<>();
    for (int num : nums) {
        numSet.add(num);
    }

    int maxLength = 0;

    for (int num : numSet) {
        if (!numSet.contains(num - 1)) {
            // Added: Count the length of the sequence
            int currentNum = num;
            int currentLength = 1;

            while (numSet.contains(currentNum + 1)) {
                currentNum += 1;
                currentLength += 1;
            }

            maxLength = Math.max(maxLength, currentLength);
        }
    }

    return maxLength;
}

```

**Edge-case pass**

* *Empty input:* Handled gracefully at the very beginning (returns 0).
* *Duplicates:* Handled perfectly because `HashSet` inherently deduplicates. `[1, 2, 2, 3]` results in a set of `{1, 2, 3}`.
* *Negative numbers:* `num - 1` and `currentNum + 1` work identically for negative numbers (e.g., `-1 - 1 = -2`).
* *Integer Overflow:* Could `currentNum + 1` overflow? If the array contains `Integer.MAX_VALUE`, `currentNum + 1` overflows to `Integer.MIN_VALUE`. The `HashSet.contains()` would return false (unless `Integer.MIN_VALUE` happens to be in the array, which breaks the sequence anyway since it's the wrap-around). Because a consecutive sequence logically ends at `Integer.MAX_VALUE`, this wrap-around correctly terminates the sequence without crashing. No patch is strictly needed.

### 8. Final Code

```java
public int longestConsecutive(int[] nums) {
    if (nums == null || nums.length == 0) {
        return 0;
    }

    // Populate the HashSet for O(1) lookups
    Set<Integer> numSet = new HashSet<>();
    for (int num : nums) {
        numSet.add(num);
    }

    int maxLength = 0;

    // Iterate through the unique numbers
    for (int num : numSet) {
        // Only evaluate a sequence if 'num' is its starting point
        if (!numSet.contains(num - 1)) {
            int currentNum = num;
            int currentLength = 1;

            // Incrementally find the next consecutive number
            while (numSet.contains(currentNum + 1)) {
                currentNum++;
                currentLength++;
            }

            // Update the global maximum
            maxLength = Math.max(maxLength, currentLength);
        }
    }

    return maxLength;
}

```

### 9. Complexity

* **Time Complexity:** $O(n)$. We iterate through the array once to build the `HashSet`. Then, we iterate through the set. The `while` loop only increments `currentNum` for elements that are part of a valid sequence. Because we only start the `while` loop at the *beginning* of a sequence, each element in the set is visited exactly once by the outer `for` loop and at most once by the inner `while` loop. $O(n) + O(n) = O(n)$.
* **Space Complexity:** $O(n)$ to store the array elements in the `HashSet`.
* *Note on boxing overhead:* Java's `HashSet<Integer>` requires boxing primitives (`int` to `Integer`). In extremely performance-sensitive environments, this $O(n)$ memory allocation and boxing overhead can be slow compared to primitive arrays, but mathematically it remains bounded strictly in $O(n)$ time and space.

### 10. Brief test walkthrough

Let's test with `nums = [100, 4, 200, 1, 3, 2]`.

1. `numSet` is built: `{100, 4, 200, 1, 3, 2}`.
2. Loop over `numSet`:
* Say we check `4`: `contains(3)` is true. Skip.
* Check `100`: `contains(99)` is false. Start sequence. `contains(101)` is false. `maxLength` = 1.
* Check `1`: `contains(0)` is false. Start sequence. `contains(2)` is true, `contains(3)` is true, `contains(4)` is true, `contains(5)` is false. `currentLength` = 4. `maxLength` updates to 4.
* Check `3`: `contains(2)` is true. Skip.
* Check `200`: `contains(199)` is false. Start sequence. Length 1. `maxLength` stays 4.
* Check `2`: `contains(1)` is true. Skip.


3. Final output is `4`. The logic holds up perfectly.