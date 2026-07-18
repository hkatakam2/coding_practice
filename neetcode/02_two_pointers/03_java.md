### 1. Restate the problem

We need to find all unique groups of three numbers within a given integer array that add up to exactly zero.

* **Given:** An array of integers.
* **Return:** A list of triplets (lists of three integers) that sum to zero.
* **Constraints & Relationships:** The three numbers must come from distinct indices in the original array. We cannot include the exact same triplet of values more than once in our final answer, even if they were formed by different indices. The order of the triplets, and the order of the numbers within them, does not matter.

### 2. Ask clarifying questions

Before writing code, I would confirm a few details with the interviewer:

* **Input size:** What is the maximum length of the array? *(Assumption: Up to a few thousand, so an $O(n^2)$ algorithm is acceptable, but $O(n^3)$ is too slow).*
* **Null or empty input:** How should we handle null or arrays with fewer than 3 elements? *(Assumption: Return an empty list).*
* **Duplicates:** Since the array can contain duplicate values, we must be careful not to output the same triplet twice.
* **Sorting/Mutation:** Are we allowed to modify the input array, for example, by sorting it? *(Assumption: Yes, modifying the input array is fine. If not, we'd need to work on a clone).*
* **Integer overflow:** Can the sum of three integers exceed the 32-bit integer limit? *(Assumption: Yes, to be safe, I will compute the sum using a `long` to prevent overflow).*
* **Output type:** I will return `List<List<Integer>>`.

### 3. Work through an example by hand

Let's trace a representative input: `nums = [-1, 0, 1, 2, -1, -4]`

First, we sort the array to make finding duplicates and pairing values easier:
`Sorted: [-4, -1, -1, 0, 1, 2]`

We want `A + B + C = 0`.

* **Fix A = -4 (index 0).** We need B + C = 4 from `[-1, -1, 0, 1, 2]`.
* Left pointer at -1, Right pointer at 2. Sum = -4 + (-1) + 2 = -3.
* -3 < 0, so we need a larger sum. Move Left up.
* Eventually, no pair adds up to 4.


* **Fix A = -1 (index 1).** We need B + C = 1 from `[-1, 0, 1, 2]`.
* Left at -1, Right at 2. Sum = -1 + (-1) + 2 = 0. **Match!** Record `[-1, -1, 2]`.
* Move Left up, Right down: Left at 0, Right at 1. Sum = -1 + 0 + 1 = 0. **Match!** Record `[-1, 0, 1]`.


* **Fix A = -1 (index 2).**
* This is the same value as the previous A. To avoid duplicate triplets, we skip this step entirely.


* **Fix A = 0 (index 3).** We need B + C = 0 from `[1, 2]`.
* Left at 1, Right at 2. Sum = 3.
* 3 > 0, we need a smaller sum. Move Right down. Pointers cross. No match.



Final Result: `[[-1, -1, 2], [-1, 0, 1]]`

### 4. Brainstorm solutions aloud

* **Direct Brute Force:** Use three nested loops to check every possible combination of `i`, `j`, and `k`. To handle duplicates, we would sort each triplet and add it to a `HashSet`.
* *Complexity:* Time is $O(n^3)$ to check all triplets. Space is $O(n)$ or more for the HashSet. This is too slow for typical interview constraints.


* **Hashing (Two Sum variation):** We can fix one number, and then use a `HashSet` to find the remaining two numbers that sum to the target, much like the classic Two Sum problem.
* *Complexity:* Time is $O(n^2)$. Space is $O(n)$ for the HashSet.
* *Tradeoffs:* Handling duplicate triplets with a HashSet can get very messy and requires extra space and overhead.


* **Sorting + Two Pointers:** Sort the array first. Iterate through the array to fix the first number. Then, use two pointers (one at the beginning of the remaining elements, one at the end) to find pairs that sum to the required target. Because the array is sorted, we can easily skip duplicate values by advancing our pointers past identical adjacent elements.
* *Complexity:* Time is $O(n \log n)$ for sorting + $O(n^2)$ for the pointer traversal = $O(n^2)$. Space is $O(1)$ auxiliary (or $O(\log n)$ to $O(n)$ depending on Java's underlying sort implementation).
* *Tradeoffs:* This modifies the input array, but it handles deduplication elegantly without needing a `HashSet`.



### 5. Select the solution

I will choose **Sorting + Two Pointers**.
It comfortably satisfies the $O(n^2)$ time constraint, minimizes auxiliary memory, and the mechanism for skipping duplicates is much cleaner and less prone to bugs than managing a `HashSet` of lists. Sorting is the perfect tool here because creating a monotonic order allows us to intelligently shrink our search window and instantly identify duplicate values.

### 6. Write the implementation outline

```java
List<List<Integer>> threeSum(int[] nums) {
    /*
     * Reframe:
     * Sort the array, pick a starting number, and use a two-pointer 
     * search on the rest of the array to find pairs that sum to its negation.
     *
     * State:
     * A result list to hold valid triplets.
     * Chosen because we must return a collection of lists.
     *
     * Invariant:
     * The array is strictly sorted. As the two pointers move inward, 
     * all elements outside their bounds have been fully evaluated for the current fixed number.
     *
     * Helpers:
     * (None needed, logic is straightforward enough for a single method)
     *
     * Core logic:
     * - handle edge cases (null or length < 3)
     * - sort the array
     * - iterate over the array to fix the first number
     * - skip if the fixed number is the same as the previous one (deduplication)
     * - initialize left pointer just after the fixed number, right pointer at the end
     * - while left < right:
     *      - calculate sum of all three numbers
     *      - if sum is zero, add to results, move both pointers inward, and skip duplicate values
     *      - if sum is too small, advance left pointer to increase sum
     *      - if sum is too large, decrement right pointer to decrease sum
     *
     * Edge cases:
     * - duplicate triplets (handled by skipping adjacent identical values)
     * - integer overflow when adding three integers
     * - early optimization: if the fixed number > 0, we can stop, since no positive numbers can sum to zero.
     */
}

```

### 7. Implement iteratively

#### Iteration 1: Method skeleton

First, I will set up the method signature, basic validation, sorting, and the outer loop.

```java
public List<List<Integer>> threeSum(int[] nums) {
    List<List<Integer>> results = new ArrayList<>();
    
    if (nums == null || nums.length < 3) {
        return results;
    }
    
    Arrays.sort(nums);
    
    for (int i = 0; i < nums.length - 2; i++) {
        // TODO: Skip duplicates for the first number
        // TODO: Set up two pointers to find the remaining two numbers
    }
    
    return results;
}

```

#### Iteration 2: Core two-pointer logic

Next, I'll add the two-pointer sweep inside the loop. For now, I will skip the deduplication logic for the pointers to keep it simple.

```java
public List<List<Integer>> threeSum(int[] nums) {
    List<List<Integer>> results = new ArrayList<>();
    
    if (nums == null || nums.length < 3) {
        return results;
    }
    
    Arrays.sort(nums);
    
    for (int i = 0; i < nums.length - 2; i++) {
        // Added: Deduplicate the outer loop
        if (i > 0 && nums[i] == nums[i - 1]) {
            continue;
        }
        
        int left = i + 1;
        int right = nums.length - 1;
        
        while (left < right) {
            // Use long to prevent integer overflow during addition
            long sum = (long) nums[i] + nums[left] + nums[right];
            
            if (sum == 0) {
                results.add(Arrays.asList(nums[i], nums[left], nums[right]));
                
                // TODO: Deduplicate inner pointers before advancing them
                left++;
                right--;
            } else if (sum < 0) {
                left++;
            } else {
                right--;
            }
        }
    }
    
    return results;
}

```

#### Iteration 3: Complete happy path and inner deduplication

Finally, I will add the logic to safely skip duplicate values for the `left` and `right` pointers after finding a successful triplet. I'll also add a small optimization: if `nums[i] > 0`, we can break early.

```java
public List<List<Integer>> threeSum(int[] nums) {
    List<List<Integer>> results = new ArrayList<>();
    
    if (nums == null || nums.length < 3) {
        return results;
    }
    
    Arrays.sort(nums);
    
    for (int i = 0; i < nums.length - 2; i++) {
        // Optimization: If the smallest number is > 0, sum can never be 0
        if (nums[i] > 0) {
            break;
        }
        
        // Skip duplicate values for the fixed first element
        if (i > 0 && nums[i] == nums[i - 1]) {
            continue;
        }
        
        int left = i + 1;
        int right = nums.length - 1;
        
        while (left < right) {
            long sum = (long) nums[i] + nums[left] + nums[right];
            
            if (sum == 0) {
                results.add(Arrays.asList(nums[i], nums[left], nums[right]));
                
                // Advance pointers past any duplicate values to avoid duplicate triplets
                while (left < right && nums[left] == nums[left + 1]) {
                    left++;
                }
                while (left < right && nums[right] == nums[right - 1]) {
                    right--;
                }
                
                left++;
                right--;
            } else if (sum < 0) {
                left++;
            } else {
                right--;
            }
        }
    }
    
    return results;
}

```

#### Edge-case pass

* **All zeroes (`[0, 0, 0, 0]`):**
* Sorted: `[0, 0, 0, 0]`.
* `i = 0`: left at 1, right at 3. Sum = 0. Adds `[0, 0, 0]`.
* inner loops advance `left` to 2, `right` to 2.
* `left++`, `right--` -> `left` = 3, `right` = 1. Inner `while` ends.
* `i = 1`: `nums[1] == nums[0]`, skips.
* Result is `[[0, 0, 0]]`. Correct.


* **Integer Overflow:** Addressed by casting to `long` before summing: `(long) nums[i] + nums[left] + nums[right]`. This perfectly protects against inputs like `[2000000000, 2000000000, -4000000000]` wrapping around.

### 8. Analyze expensive sections and optimize

* **Time Complexity:**
* `Arrays.sort(nums)` runs in $O(n \log n)$.
* The outer loop runs $O(n)$ times.
* The inner `while` loop sweeps the remainder of the array, taking $O(n)$ time per outer iteration.
* Total Time Complexity: $O(n \log n) + O(n^2) = O(n^2)$.


* **Space Complexity:**
* We do not use any extra data structures other than the output list.
* However, Java's `Arrays.sort()` on primitives uses a Dual-Pivot Quicksort which requires $O(\log n)$ space on the call stack.
* Total Space Complexity: $O(\log n)$ auxiliary space.


* **Optimization:** The addition of `if (nums[i] > 0) break;` is a helpful real-world optimization. Because the array is sorted, if our lowest number is positive, we can never reach a sum of zero by adding larger positive numbers.

### Final Code

```java
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

class Solution {
    public List<List<Integer>> threeSum(int[] nums) {
        List<List<Integer>> results = new ArrayList<>();
        
        if (nums == null || nums.length < 3) {
            return results;
        }
        
        Arrays.sort(nums);
        
        for (int i = 0; i < nums.length - 2; i++) {
            // If the smallest number is positive, no sum can be zero
            if (nums[i] > 0) {
                break;
            }
            
            // Deduplicate outer loop to prevent duplicate triplets
            if (i > 0 && nums[i] == nums[i - 1]) {
                continue;
            }
            
            int left = i + 1;
            int right = nums.length - 1;
            
            while (left < right) {
                // Use long to protect against integer overflow
                long sum = (long) nums[i] + nums[left] + nums[right];
                
                if (sum == 0) {
                    results.add(Arrays.asList(nums[i], nums[left], nums[right]));
                    
                    // Deduplicate inner pointers
                    while (left < right && nums[left] == nums[left + 1]) {
                        left++;
                    }
                    while (left < right && nums[right] == nums[right - 1]) {
                        right--;
                    }
                    
                    left++;
                    right--;
                } else if (sum < 0) {
                    left++;
                } else {
                    right--;
                }
            }
        }
        
        return results;
    }
}

```

### Brief test walkthrough

Let's quickly run through the smallest valid input with no answer: `[1, 2, 3]`.

* Sorted: `[1, 2, 3]`.
* Outer loop `i = 0`, `nums[0] = 1`.
* Because `1 > 0`, the optimization triggers and `break`s the loop.
* Returns an empty list `[]`. Expected result achieved correctly and instantly.