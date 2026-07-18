### 1. Restate the problem

We are given an array of integers and a target sum. We need to find exactly two distinct elements in the array that add up to the target and return their original indices.

**Given:**

* `nums`: an array of integers.
* `target`: the integer sum we are trying to form.

**Returns:**

* An array of two integers representing the indices of the two numbers.
* The smaller index must come first.

**Constraints & Relationships:**

* There is exactly one valid solution.
* We cannot use the same element (at the same index) twice.

### 2. Ask clarifying questions

In a real interview, I would confirm the following to ensure there are no hidden surprises, though the problem description already hints at some answers:

* *What is the expected size of the array?* (Assume up to $10^5$, meaning an $O(N^2)$ solution will time out).
* *Can the array contain negative numbers or zeroes?* (Assume yes).
* *Can there be duplicate values in the array?* (Assume yes, e.g., `[3, 3]` for `target = 6` is valid and the indices would be `[0, 1]`).
* *Will the target addition exceed the 32-bit signed integer limit?* (Assume the numbers safely fit in standard integers, but if `target` and array values were huge, we'd need to cast to `long` for the sum. Given the problem asks to match `target`, standard `int` arithmetic holds).

### 3. Work through an example by hand

Let's trace an example that exposes the logic, including a case where numbers appear out of order.
**Input:** `nums = [3, 2, 4]`, `target = 6`

* **Step 1:** Look at index `0`, value `3`. To reach `6`, we need another `3`. Have we seen a `3` previously? No. Remember that we saw `3` at index `0`.
* **Step 2:** Look at index `1`, value `2`. To reach `6`, we need a `4`. Have we seen a `4` previously? No. Remember that we saw `2` at index `1`.
* **Step 3:** Look at index `2`, value `4`. To reach `6`, we need a `2`. Have we seen a `2` previously? Yes! We saw it at index `1`.
* **Result:** The matching indices are `1` and `2`. We return `[1, 2]` (smaller index first).

### 4. Brainstorm solutions aloud

**Approach 1: Direct Simulation / Brute Force**

* **Core idea:** Use a nested loop. For every element at index `i`, check all subsequent elements at index `j` to see if `nums[i] + nums[j] == target`.
* **Time complexity:** $O(N^2)$.
* **Space complexity:** $O(1)$.
* **Tradeoffs:** Very simple to write, but fundamentally doesn't scale for large arrays.

**Approach 2: Sorting and Two Pointers**

* **Core idea:** Sort the array, then place one pointer at the beginning and one at the end. If the sum is too small, move the left pointer up. If it's too big, move the right pointer down.
* **Time complexity:** $O(N \log N)$ due to sorting.
* **Space complexity:** $O(N)$ because we have to store the original indices before sorting (since the return value requires original indices).
* **Tradeoffs:** Better time complexity than brute force, but the need to maintain original indices makes the implementation slightly clunky.

**Approach 3: Hash Map (One-Pass)**

* **Core idea:** Iterate through the array once. As we look at each number, calculate what value is needed to hit the target. If we've already stored that needed value in a hash map (value -> index), we are done. If not, store the current number and its index in the map.
* **Time complexity:** Expected $O(N)$, since hash map lookups and insertions are $O(1)$ on average.
* **Space complexity:** $O(N)$ to store elements in the hash map.
* **Tradeoffs:** Uses extra memory, but provides optimal time complexity and the implementation is very clean.

### 5. Select the solution

I will choose **Approach 3: Hash Map (One-Pass)**.

* It comfortably satisfies expected time constraints ($O(N)$).
* It is easy to explain and implement.
* Using a `HashMap` perfectly matches the problem property: we need fast, $O(1)$ value-to-index lookups to check if a previously seen element completes the pair.

### 6. Write the implementation outline

```java
int[] twoSum(int[] nums, int target) {
    /*
     * Reframe:
     * Scan each value and determine whether the exact complement it needs 
     * to reach the target has already been processed.
     *
     * State:
     * Map from `value` to its `original position` (index).
     * Chosen because complement lookup must be fast.
     *
     * Invariant:
     * Before processing the current value, the map contains exactly the
     * previously processed values.
     *
     * Core logic:
     * - create a hash map for previously seen values
     * - inspect each value in the array
     * - compute the 'needed' partner for the current value (target - current)
     * - if the map contains the needed partner, return its index and the current index
     * - otherwise, add the current value and its index to the map
     *
     * Edge cases:
     * - duplicate values in the array (e.g., [3, 3] for target 6)
     * - finding exactly one valid pair (guaranteed by problem constraints)
     */
}

```

### 7. Implement iteratively

**Iteration 1: Method skeleton**
I'll set up the data structure and loop.

```java
public int[] twoSum(int[] nums, int target) {
    Map<Integer, Integer> seen = new HashMap<>();

    // TODO: inspect each value
    // TODO: check whether its partner was seen
    // TODO: store the current value
    
    // Fallback if no solution exists (though problem guarantees exactly one)
    return new int[0]; 
}

```

**Iteration 2: Implement the easiest core section**
I will add the loop and the calculation for the required partner.

```java
public int[] twoSum(int[] nums, int target) {
    Map<Integer, Integer> seen = new HashMap<>();

    for (int i = 0; i < nums.length; i++) {
        int current = nums[i];
        
        // Added: derive what value would complete the answer
        int needed = target - current;

        // TODO: handle a previously seen partner
        
        // Added: store the current value and index for future lookups
        seen.put(current, i);
    }

    return new int[0]; 
}

```

**Iteration 3: Complete the happy path**
Now, I'll connect the logic by checking the map before we insert the current value.

```java
public int[] twoSum(int[] nums, int target) {
    Map<Integer, Integer> seen = new HashMap<>();

    for (int i = 0; i < nums.length; i++) {
        int current = nums[i];
        int needed = target - current;

        // Added: finish immediately when the required partner exists.
        // Because we only look backward, the partner's index is always strictly less than i.
        if (seen.containsKey(needed)) {
            return new int[] { seen.get(needed), i };
        }
        
        seen.put(current, i);
    }

    return new int[0]; 
}

```

**Edge-case pass**
Let's review the edge cases identified:

1. **Duplicate values:** E.g., `nums = [3, 3], target = 6`.
* *Trace:* At `i = 0`, `current = 3`, `needed = 3`. Map is empty. Put `(3 -> 0)`. At `i = 1`, `current = 3`, `needed = 3`. Map has key `3`. Returns `[0, 1]`.
* *Result:* Works perfectly. By checking the map *before* inserting, we safely pair a duplicate with its earlier occurrence without overwriting the map prematurely.


2. **Smaller index first constraint:**
* *Trace:* Because we iterate left-to-right (`i` increases), the previously seen partner in the map will always have an index smaller than the current index `i`. Returning `new int[] { seen.get(needed), i }` guarantees the smaller index is first.
* *Result:* Works perfectly.


3. **No valid pair:**
* The constraints guarantee exactly one solution, but returning `new int[0]` at the end satisfies the compiler.



### 8. Analyze expensive sections and optimize

* **Iteration:** The single `for` loop touches each element once: $O(N)$.
* **Lookups/Insertions:** Calling `containsKey()`, `get()`, and `put()` on a `HashMap` takes expected $O(1)$ time.
* **Bottlenecks:** None. A one-pass hash map is optimal for this problem. No sorting or nested loops are present.
* **Space:** The `HashMap` will store at most $N-1$ elements before finding the solution, which takes $O(N)$ auxiliary space.

### Final code

```java
import java.util.HashMap;
import java.util.Map;

class Solution {
    public int[] twoSum(int[] nums, int target) {
        Map<Integer, Integer> seen = new HashMap<>();

        for (int i = 0; i < nums.length; i++) {
            int current = nums[i];
            int needed = target - current;

            if (seen.containsKey(needed)) {
                return new int[] { seen.get(needed), i };
            }

            seen.put(current, i);
        }

        return new int[0];
    }
}

```

**Complexity**

* **Time Complexity:** $O(N)$ where $N$ is the number of elements in `nums`. We traverse the array exactly once, and Hash Map operations are $O(1)$ on average.
* **Space Complexity:** $O(N)$. The hash map can hold at most $N-1$ elements in the worst case (when the matching pair consists of the last two elements).

### Brief test walkthrough

Let's test with the smallest valid input: `nums = [3, 2, 4]`, `target = 6`.

1. `i = 0`, `current = 3`, `needed = 3`. Map is `{}`. Does not contain `3`. Map becomes `{3: 0}`.
2. `i = 1`, `current = 2`, `needed = 4`. Map is `{3: 0}`. Does not contain `4`. Map becomes `{3: 0, 2: 1}`.
3. `i = 2`, `current = 4`, `needed = 2`. Map is `{3: 0, 2: 1}`. Contains `2`.
4. Returns `[seen.get(2), 2]`, which evaluates to `[1, 2]`.

The result `[1, 2]` is correct, and the smaller index is returned first.