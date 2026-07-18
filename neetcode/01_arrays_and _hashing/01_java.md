### 1. Restatement

We are given an array of integers. Our task is to determine whether any integer appears more than once in the array.

* **Given:** An array of integers (`nums`).
* **Return:** A boolean (`true` if a duplicate exists, `false` if all elements are unique).
* **Constraints & Relationships:** We only need to find *if* a duplicate exists, not *which* one it is or *how many* there are. Order does not matter. The first duplicate we encounter allows us to immediately return.

### 2. Clarifying questions and assumptions

Before writing code, I would clarify a few assumptions with the interviewer:

* **Input size:** Can the array be very large? (Assumption: Yes, up to standard competitive programming bounds like $10^5$, meaning an $O(n^2)$ solution will be too slow).
* **Array constraints:** Can the array be empty or contain only one element? (Assumption: Yes. In these cases, it's impossible to have duplicates, so we should return `false`).
* **Values:** Are the elements standard 32-bit signed integers? (Assumption: Yes, negative numbers and zero are allowed and fit inside standard `int`).
* **Modifiability:** Are we allowed to modify the input array? (Assumption: For this problem, read-only is preferred, but I will consider in-place mutation like sorting if memory is strictly limited).

### 3. Manual example

Let's trace a representative input: `nums = [3, 1, -4, 1, 2]`

* **Current state:** `seen = {}` (empty)
* **Step 1:** Look at `3`. Is `3` in `seen`? No. Add `3` to `seen`. (`seen = {3}`)
* **Step 2:** Look at `1`. Is `1` in `seen`? No. Add `1` to `seen`. (`seen = {3, 1}`)
* **Step 3:** Look at `-4`. Is `-4` in `seen`? No. Add `-4` to `seen`. (`seen = {3, 1, -4}`)
* **Step 4:** Look at `1`. Is `1` in `seen`? Yes! `1` is already in our tracked items.
* **Final result:** Return `true`.

### 4. Candidate solutions

1. **Brute Force:**
* **Core idea:** Compare every element with every other element using two nested loops.
* **Time complexity:** $O(n^2)$.
* **Space complexity:** $O(1)$.
* **Tradeoffs:** Very slow for large inputs, but requires no extra memory.


2. **Sorting:**
* **Core idea:** Sort the array first. If there are duplicates, they will end up adjacent to each other. We can then do a single pass to check for `nums[i] == nums[i+1]`.
* **Time complexity:** $O(n \log n)$ due to sorting.
* **Space complexity:** $O(1)$ or $O(n)$ depending on the sorting algorithm and if we are allowed to mutate the input array.
* **Tradeoffs:** Better time than brute force, but mutates the input array (or requires copying it, which defeats the $O(1)$ space advantage).


3. **Hashing (HashSet):**
* **Core idea:** Iterate through the array while adding elements to a Hash Set. Before adding, check if the element is already in the set.
* **Time complexity:** $O(n)$ expected time, as set lookups and insertions are $O(1)$ on average.
* **Space complexity:** $O(n)$ to store up to $n$ elements in the worst case (no duplicates).
* **Tradeoffs:** Optimal time complexity, requires extra memory.



### 5. Selected solution and justification

I will use the **Hashing (HashSet)** approach.

It is the simplest, most readable solution and provides the optimal $O(n)$ time complexity. Standard `HashSet` naturally fits this problem since it is designed exactly for $O(1)$ membership testing and guarantees unique keys. While it requires $O(n)$ space, memory is rarely the bottleneck for basic array validation tasks unless strictly specified.

### 6. Plain-English implementation outline

```java
boolean containsDuplicate(int[] nums) {
    /*
     * Reframe:
     * Scan the array and remember each value. If we see a value we already 
     * remembered, a duplicate exists.
     *
     * State:
     * HashSet of integers.
     * Chosen because we need expected O(1) lookup time to check if a value 
     * was previously encountered.
     *
     * Invariant:
     * At the start of any iteration, the set contains exactly the unique 
     * elements processed from previous indices.
     *
     * Core logic:
     * - create an empty set to track seen numbers
     * - iterate through each number in the input array
     * - if the set already contains the number, return true immediately
     * - otherwise, add the number to the set
     * - if the loop finishes without finding any matches, return false
     *
     * Edge cases:
     * - empty array (returns false)
     * - array with one element (returns false)
     * - negative integers (handled naturally by standard hashing)
     */
}

```

### 7. Iterative Java implementation

**Iteration 1: Method skeleton**
First, I will set up the method signature, the primary data structure, and the default return value.

```java
public boolean containsDuplicate(int[] nums) {
    Set<Integer> seen = new HashSet<>();

    // TODO: iterate through the numbers
    // TODO: check for duplicates and add to the set

    return false;
}

```

**Iteration 2: Core loop**
Next, I will add the loop to process every element in the array and put it into our state tracker.

```java
public boolean containsDuplicate(int[] nums) {
    Set<Integer> seen = new HashSet<>();

    for (int num : nums) {
        // TODO: finish early if 'num' is already in 'seen'
        
        // Added: track the current number
        seen.add(num);
    }

    return false;
}

```

**Iteration 3: Complete the happy path**
Now I will add the duplicate-check logic to satisfy the core requirement.

```java
public boolean containsDuplicate(int[] nums) {
    Set<Integer> seen = new HashSet<>();

    for (int num : nums) {
        // Added: check for the duplicate before modifying the set
        if (seen.contains(num)) {
            return true;
        }
        seen.add(num);
    }

    return false;
}

```

**Edge-case walkthrough and patches:**

* *Empty array:* The enhanced for-loop will not execute, and the method will return `false`. This is correct.
* *Single element:* The loop runs once, adds the element to the set, and finishes. Returns `false`. This is correct.
* *Java-specific optimization:* In Java, `HashSet.add()` returns `false` if the element is already present in the set. We can condense `contains()` and `add()` into a single operation, avoiding a double-lookup in the underlying `HashMap` structure.

Let's patch the logic to use the return value of `add()`.

```java
// Patching Iteration 3 for slight performance/readability improvement:
for (int num : nums) {
    if (!seen.add(num)) {
        return true;
    }
}

```

### 8. Final code

```java
import java.util.HashSet;
import java.util.Set;

public class Solution {
    public boolean containsDuplicate(int[] nums) {
        Set<Integer> seen = new HashSet<>();
        
        for (int num : nums) {
            if (!seen.add(num)) {
                return true;
            }
        }
        
        return false;
    }
}

```

### Complexity

* **Time Complexity:** $O(n)$. We iterate through the array of length $n$ at most once. The `add` operation on a `HashSet` takes expected $O(1)$ time.
* **Space Complexity:** $O(n)$. In the worst-case scenario (an array with entirely unique elements), the `HashSet` will store all $n$ elements.

### Brief test walkthrough

1. **Main Example:** `nums = [3, 1, -4, 1, 2]`
* `seen.add(3)` -> returns `true`, set is `{3}`.
* `seen.add(1)` -> returns `true`, set is `{3, 1}`.
* `seen.add(-4)` -> returns `true`, set is `{3, 1, -4}`.
* `seen.add(1)` -> returns `false` because `1` is already in the set. The `if` condition triggers.
* **Result:** returns `true`. (Expected).


2. **Smallest Valid Input:** `nums = []`
* Loop doesn't run.
* **Result:** returns `false`. (Expected).


3. **Worst Case/No Duplicates:** `nums = [1, 2, 3]`
* `seen` successfully adds `1`, `2`, and `3`. Loop completes.
* **Result:** returns `false`. (Expected).