### 1. Restate the problem

We have an array of unique integers. Originally, it was sorted in ascending order. Then, it was rotated (shifted to the right, with elements wrapping around to the front) an unknown number of times.

We need to find the smallest integer in this array.
The core constraint is that the algorithm must run in `O(log n)` time, meaning we cannot check every element one by one.

### 2. Ask clarifying questions

* **Can the input array be empty?**
* *Assumption:* No, the array length `n` is at least 1.


* **Can the array contain negative numbers?**
* *Assumption:* Yes, negative values are allowed and do not change the logic.


* **What if it is rotated `n` times (meaning it is perfectly sorted)?**
* *Assumption:* The algorithm must handle a fully sorted array naturally.


* **Is it guaranteed that all elements are unique?**
* *Assumption:* Yes, as stated in the prompt, there are no duplicates. (Duplicates would break standard binary search).



### 3. Work through an example by hand

Let `nums = [4, 5, 6, 7, 0, 1, 2]`.
The array was originally `[0, 1, 2, 4, 5, 6, 7]` and was rotated 4 times.

* **Initial state:** Search space is the whole array.
* `left` points to `4` (index 0).
* `right` points to `2` (index 6).


* **Step 1:** Find the middle.
* `mid` is index 3, which is `7`.


* **Decision 1:** Compare `mid` (7) to `right` (2).
* Because `7 > 2`, the array must wrap around to the right of `mid`. The minimum cannot be on the left side, and it cannot be `mid` itself.
* *Update:* Move `left` to `mid + 1` (index 4).


* **Step 2:** Search space is now `[0, 1, 2]`.
* `left` is index 4 (`0`).
* `right` is index 6 (`2`).
* `mid` is index 5 (`1`).


* **Decision 2:** Compare `mid` (1) to `right` (2).
* Because `1 < 2`, this right half is properly sorted. The minimum must be at `mid` or to its left.
* *Update:* Move `right` to `mid` (index 5).


* **Step 3:** Search space is now `[0, 1]`.
* `left` is index 4 (`0`).
* `right` is index 5 (`1`).
* `mid` is index 4 (`0`).


* **Decision 3:** Compare `mid` (0) to `right` (1).
* `0 < 1`. Move `right` to `mid` (index 4).


* **Final result:** `left` equals `right` at index 4. The minimum is `nums[4]`, which is `0`.

### 4. Brainstorm solutions aloud

* **Direct Simulation (Brute Force):**
* Scan the array linearly from left to right. Keep track of the minimum seen so far, or just look for the point where `nums[i] > nums[i+1]`.
* *Time complexity:* `O(n)`.
* *Space complexity:* `O(1)`.
* *Tradeoff:* Fails the `O(log n)` constraint.


* **Binary Search:**
* Because the array is partially sorted, we can use binary search. By comparing the element at the middle of our search space to the element at the far right, we can reliably determine which half contains the "inflection point" (the drop from the highest value to the lowest value).
* If `mid` value is greater than `right` value, the drop happens after `mid`.
* If `mid` value is less than `right` value, the drop happens at or before `mid`.
* *Time complexity:* `O(log n)`.
* *Space complexity:* `O(1)`.



### 5. Select the solution

We will proceed with **Binary Search** to satisfy the strict `O(log n)` requirement. We only need two pointers (`left` and `right`) and standard integer arithmetic.

### 6. Write the implementation outline

```java
int findMin(int[] nums) {
    /*
     * Reframe:
     * Find the inflection point of a rotated sorted array using binary search.
     *
     * State:
     * left and right pointers bounding the current search space.
     * Chosen because binary search requires tracking active boundaries.
     *
     * Invariant:
     * The minimum element is always contained strictly within the inclusive 
     * bounds of [left, right].
     *
     * Core logic:
     * - initialize left to the start and right to the end of the array
     * - loop as long as the search space is larger than one element
     * - calculate the middle index safely to avoid overflow
     * - if the middle element is greater than the rightmost element:
     *     - the drop must be to the right of middle, so move left past middle
     * - otherwise:
     *     - the right half is sorted, so the minimum is at middle or to its left
     *     - pull the right boundary inward to the middle
     * - when left equals right, the search space has narrowed to the minimum
     *
     * Edge cases:
     * - Array of length 1 (loop never runs, returns only element).
     * - Array that is not rotated at all (fully sorted).
     */
}

```

### 7. Implement iteratively

**Iteration 1: Method skeleton**
We set up the bounds and the basic loop structure.

```java
int findMin(int[] nums) {
    int left = 0;
    int right = nums.length - 1;

    // Loop until the pointers converge on a single element.
    // TODO: implement binary search logic inside loop
    while (left < right) {
        // TODO: find middle
        // TODO: decide which half contains the minimum
    }

    // By the loop's exit condition, left == right, pointing to the minimum.
    return nums[left];
}

```

**Iteration 2: Midpoint calculation**
We add the midpoint calculation. Using `left + (right - left) / 2` instead of `(left + right) / 2` prevents integer overflow if the array is massively large.

```java
int findMin(int[] nums) {
    int left = 0;
    int right = nums.length - 1;

    while (left < right) {
        // Added: safe midpoint calculation
        int mid = left + (right - left) / 2;

        // TODO: decide which half contains the minimum
    }

    return nums[left];
}

```

**Iteration 3: Complete the happy path**
We add the comparison that shrinks the search space based on our invariant.

```java
int findMin(int[] nums) {
    int left = 0;
    int right = nums.length - 1;

    while (left < right) {
        int mid = left + (right - left) / 2;

        // Added: Core routing logic based on the rightmost element
        if (nums[mid] > nums[right]) {
            // The drop is definitely to the right of mid
            left = mid + 1;
        } else {
            // The right half is strictly sorted. 
            // The minimum is at mid or in the left half.
            right = mid;
        }
    }

    return nums[left];
}

```

**Edge-case pass**
Let's trace a fully sorted array that wasn't rotated (e.g., `[11, 12, 13, 14, 15]`).

* `left` = 0 (11), `right` = 4 (15).
* `mid` = 2 (13). `13 < 15`, so `right` moves to 2.
* `left` = 0 (11), `right` = 2 (13).
* `mid` = 1 (12). `12 < 13`, so `right` moves to 1.
* `left` = 0 (11), `right` = 1 (12).
* `mid` = 0 (11). `11 < 12`, so `right` moves to 0.
* `left == right == 0`. Loop ends. Returns `11`.
* *Conclusion:* The logic handles a non-rotated array perfectly without any extra checks. No patches needed.

### Final Code

```java
class Solution {
    public int findMin(int[] nums) {
        int left = 0;
        int right = nums.length - 1;

        while (left < right) {
            int mid = left + (right - left) / 2;

            if (nums[mid] > nums[right]) {
                left = mid + 1;
            } else {
                right = mid;
            }
        }

        return nums[left];
    }
}

```

### Complexity

* **Time Complexity:** `O(log n)`. We halve the search space on every iteration of the `while` loop, where `n` is the length of the array.
* **Space Complexity:** `O(1)`. We only allocate memory for a few primitive integer variables (`left`, `right`, `mid`), regardless of the input size.

### Brief test walkthrough

1. **Main Example:** `[4, 5, 6, 7, 0, 1, 2]`.
* *Expected:* `0`.
* *Why:* The mid pointer will eventually land on `0` and bounds will shrink around it.


2. **Smallest valid input:** `[42]`.
* *Expected:* `42`.
* *Why:* `left` starts at 0, `right` starts at 0. `left < right` is `0 < 0` (false). Loop never executes, returns `nums[0]`.


3. **Two elements, rotated:** `[2, 1]`.
* *Expected:* `1`.
* *Why:* `left`=0 (2), `right`=1 (1). `mid`=0 (2). `2 > 1`, so `left`=mid+1 (1). Loop terminates, returns `nums[1]`.