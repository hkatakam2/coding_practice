### 1. Restatement

We are given an array of unique integers that was originally sorted in ascending order but has been rotated to the right an unknown number of times.
We need to find a specific `target` integer in this array and return its index. If the `target` is not present, we must return `-1`.

### 2. Ask clarifying questions

* **Input size:** Can the array be empty? *(Assumption: The array has at least one element.)*
* **Duplicates:** The prompt states elements are unique. Are we certain there are no duplicates? *(Assumption: Yes, this is guaranteed, which allows strictly $O(\log n)$ performance.)*
* **Time complexity:** Given it is a sorted (albeit rotated) array, is $O(\log n)$ time expected? *(Assumption: Yes. A linear $O(n)$ scan is too trivial for this interview.)*
* **Output:** Return an `int` representing the index, modifying nothing in place.

### 3. Work through an example by hand

Let's use `nums = [4, 5, 6, 7, 0, 1, 2]` and `target = 0`.

* **Step 1: Find the minimum element (the pivot).**
* The smallest element is `0` at index `4`.
* This index perfectly divides our array into two strictly sorted subarrays: `[4, 5, 6, 7]` (indices 0 to 3) and `[0, 1, 2]` (indices 4 to 6).


* **Step 2: Decide which subarray to search.**
* Our target is `0`.
* We compare `0` against the boundaries of the left subarray: `4` to `7`. It does not fall in this range.
* Therefore, the target must be in the right subarray, from index `4` to `6`.


* **Step 3: Standard binary search on the chosen subarray.**
* Search space: index `4` to `6`.
* Mid index is `5`. Value is `1`.
* `0 < 1`, so we search the left half: index `4` to `4`.
* Mid index is `4`. Value is `0`. We found the target at index `4`.



### 4. Brainstorm solutions aloud

* **Approach 1: Linear Scan**
* *Core idea:* Loop through the array from `0` to `n-1` comparing each element to the target.
* *Complexity:* Time $O(n)$, Space $O(1)$.
* *Tradeoffs:* It works, but it completely ignores the "mostly sorted" nature of the input, failing to meet the expected $O(\log n)$ performance.


* **Approach 2: Two-pass Binary Search** *(Selected per your preference)*
* *Core idea:* The array consists of two sorted halves. We first use binary search to find the index of the minimum element (the "pivot" where the rotation happened). Once we know this pivot, we can easily check whether our target falls into the left sorted portion or the right sorted portion. We then do a standard binary search on that specific portion.
* *Complexity:* Time $O(\log n)$ (two sequential binary searches), Space $O(1)$.
* *Tradeoffs:* By breaking the problem into two distinct, highly recognizable, and modular subproblems, the code becomes easier to reason about and less prone to tricky boundary-condition bugs compared to a single-pass approach.


* **Approach 3: One-pass Binary Search**
* *Core idea:* Perform a single binary search, dynamically determining which half of the current search space is sorted at every step, and routing the target accordingly.
* *Complexity:* Time $O(\log n)$, Space $O(1)$.
* *Tradeoffs:* Slightly less code overall, but the combined `if/else` conditions can be harder to read and trace during an interview.



### 5. Select the solution

We will proceed with **Approach 2: Two-pass Binary Search**. It decomposes the problem into two clean, easily testable standard algorithms: finding the minimum in a rotated array, and a traditional binary search.

### 6. Write the implementation outline

```java
int search(int[] nums, int target) {
    /*
     * Reframe:
     * A rotated array consists of two strictly sorted subarrays.
     * Finding the start of the second subarray (the minimum element)
     * allows us to perform a standard binary search on the correct half.
     *
     * State:
     * Pivot index separating the two sorted halves.
     * Pointers for binary search (left, right, mid).
     *
     * Invariant:
     * During pivot search, the minimum element is always within the [left, right] bounds.
     * During standard search, the target is always within the [left, right] bounds.
     *
     * Helpers:
     * findMinIndex(int[] nums)
     * - binary searches for the index of the smallest element
     * binarySearch(int[] nums, int target, int left, int right)
     * - performs standard binary search within the provided bounds
     *
     * Core logic:
     * - find the pivot index
     * - if the array is perfectly sorted (pivot is 0), search the whole array
     * - if the target is >= the first element, search the left sorted subarray
     * - otherwise, search the right sorted subarray
     *
     * Edge cases:
     * - array of size 1
     * - array that has 0 rotations (perfectly sorted)
     * - target is completely absent
     */
}

```

### 7. Implement iteratively

**Iteration 1: Method skeleton**
First, I'll set up the main control flow and define the helper stubs.

```java
public int search(int[] nums, int target) {
    // TODO: find the pivot index
    int pivot = 0; 
    
    // TODO: route the target to the correct sorted subarray
    
    return -1;
}

private int findMinIndex(int[] nums) {
    // TODO: binary search for minimum
    return 0;
}

private int binarySearch(int[] nums, int target, int left, int right) {
    // TODO: standard binary search
    return -1;
}

```

**Iteration 2: Implement the pivot search**
I will implement `findMinIndex`. By comparing `mid` to the `right` pointer, we can figure out where the "drop-off" happens.

```java
private int findMinIndex(int[] nums) {
    int left = 0;
    int right = nums.length - 1;

    // Added: When left == right, we have isolated the minimum element.
    while (left < right) {
        int mid = left + (right - left) / 2;

        if (nums[mid] > nums[right]) {
            // The drop-off is to the right of mid.
            left = mid + 1;
        } else {
            // The drop-off is at mid or to the left of mid.
            right = mid;
        }
    }

    return left;
}

```

**Iteration 3: Implement standard binary search**
Now I will implement a classic, strictly bounded binary search helper.

```java
private int binarySearch(int[] nums, int target, int left, int right) {
    while (left <= right) {
        int mid = left + (right - left) / 2;

        if (nums[mid] == target) {
            return mid;
        } else if (nums[mid] < target) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }
    return -1;
}

```

**Iteration 4: Complete the main routing logic**
Finally, I will tie it all together by using the pivot to decide which half to search.

```java
public int search(int[] nums, int target) {
    int pivot = findMinIndex(nums);

    // Added: If the array wasn't rotated at all, search the whole thing.
    if (pivot == 0) {
        return binarySearch(nums, target, 0, nums.length - 1);
    }

    // Added: If target is >= the very first element, it must be in the left subarray.
    // e.g., in [4, 5, 6, 7, 0, 1, 2], target 5 is >= 4, so it's in [4, 5, 6, 7].
    if (target >= nums[0] && target <= nums[pivot - 1]) {
        return binarySearch(nums, target, 0, pivot - 1);
    } 
    // Added: Otherwise, it must be in the right subarray.
    else {
        return binarySearch(nums, target, pivot, nums.length - 1);
    }
}

```

**Edge-case walkthrough and patches**

* **Array size 1 (e.g., `nums = [5], target = 5`):**
* `findMinIndex`: `left(0) < right(0)` is false. Returns `0`.
* Main logic: `pivot == 0` is true. Calls `binarySearch(nums, 5, 0, 0)`.
* `binarySearch`: finds `5` at index `0`. Handled perfectly. No patch needed.


* **Array rotated 0 times (e.g., `nums = [1, 2, 3], target = 3`):**
* `findMinIndex`: returns `0`.
* Main logic: intercepts `pivot == 0`, searches `0` to `2`. Handled perfectly. No patch needed.


* **Target not in array:**
* Properly constrained to one of the bounds, `binarySearch` naturally returns `-1`. Handled perfectly. No patch needed.



### 8. Final code

```java
class Solution {
    public int search(int[] nums, int target) {
        if (nums == null || nums.length == 0) {
            return -1;
        }

        int pivot = findMinIndex(nums);

        // If the array is perfectly sorted, search the entire array.
        if (pivot == 0) {
            return binarySearch(nums, target, 0, nums.length - 1);
        }

        // Target falls within the boundaries of the left sorted subarray.
        if (target >= nums[0] && target <= nums[pivot - 1]) {
            return binarySearch(nums, target, 0, pivot - 1);
        } 
        // Target must be in the right sorted subarray.
        else {
            return binarySearch(nums, target, pivot, nums.length - 1);
        }
    }

    private int findMinIndex(int[] nums) {
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

        return left; // left == right, pointing to the minimum element
    }

    private int binarySearch(int[] nums, int target, int left, int right) {
        while (left <= right) {
            int mid = left + (right - left) / 2;

            if (nums[mid] == target) {
                return mid;
            } else if (nums[mid] < target) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        
        return -1;
    }
}

```

### Complexity

* **Time Complexity:** $O(\log n)$. Finding the pivot takes $\approx \log_{2}(n)$ steps. The subsequent binary search takes at most $\approx \log_{2}(n)$ steps. Since they are sequential, the total time is strictly logarithmic.
* **Space Complexity:** $O(1)$. We only use a few integer variables (`left`, `right`, `mid`, `pivot`) regardless of the array's size.

### Brief test walkthrough

Let's run `nums = [5, 1, 3]`, `target = 3`:

1. `findMinIndex([5, 1, 3])`:
* `left=0`, `right=2`. `mid=1` (value `1`).
* `1 > 3` is false, so `right = mid = 1`.
* Next loop: `left=0`, `right=1`. `mid=0` (value `5`).
* `5 > 1` is true, so `left = mid + 1 = 1`.
* `left == right (1)`. Loop exits. Returns index `1`. (Pivot is `1`).


2. Main method:
* `pivot = 1`.
* `pivot == 0` is false.
* Is `target (3) >= nums[0] (5)`? False.
* So, route to right subarray: `binarySearch([5, 1, 3], 3, 1, 2)`.


3. `binarySearch` on indices `1` to `2`:
* `left=1`, `right=2`. `mid=1` (value `1`).
* `1 < 3`, so `left = mid + 1 = 2`.
* `left=2`, `right=2`. `mid=2` (value `3`).
* `nums[mid] == 3`. Returns `2`. Correct.