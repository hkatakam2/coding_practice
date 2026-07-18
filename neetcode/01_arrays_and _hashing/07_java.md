### 1. Restate the problem

We need to take an array of numbers and return a new array where every element at index `i` is the product of all the numbers in the original array *except* the number at index `i`.

The core constraint is that we are building products out of every other element.

### 2. Ask clarifying questions

Before diving in, I would confirm a few assumptions:

* **Is division allowed?** (A common variant of this question strictly forbids division. I will assume it is forbidden, as otherwise the problem trivially reduces to finding the total product and dividing by each element.)
* **Are there zeros in the input?** (If division is forbidden, this naturally handles zeros, but it's good to confirm).
* **What is the minimum size of the array?** (I'll assume `nums.length >= 2` since we need at least one "other" element).
* **Is the output array considered extra space?** (Usually, returning an array of size $O(n)$ does not count towards auxiliary space complexity. I'll aim for $O(1)$ extra space).

### 3. Work through an example by hand

Let's use `nums = [1, 2, 3, 4]`.

To find the product except self at index `i`, we are effectively multiplying all elements to the *left* of `i` by all elements to the *right* of `i`.

Let's map out the "Left Product" and "Right Product" for each index:

* **Index 0 (val 1):** Left = 1 (nothing left), Right = 2 * 3 * 4 = 24. Result = 24.
* **Index 1 (val 2):** Left = 1, Right = 3 * 4 = 12. Result = 1 * 12 = 12.
* **Index 2 (val 3):** Left = 1 * 2 = 2, Right = 4. Result = 2 * 4 = 8.
* **Index 3 (val 4):** Left = 1 * 2 * 3 = 6, Right = 1 (nothing right). Result = 6.

Final array: `[24, 12, 8, 6]`.

### 4. Brainstorm solutions aloud

* **Approach 1: Division (The trivial way)**
Calculate the total product of the array. For each element, divide the total product by the current element.
*Tradeoffs:* This is $O(n)$ time and $O(1)$ space. However, it fails if there are zeros (division by zero), requiring annoying conditional logic (counting zeros). More importantly, the interviewer usually bans the division operator for this specific problem.
* **Approach 2: Left and Right Prefix Arrays**
Just like the manual example, we can create two arrays: `left` and `right`.
`left[i]` stores the product of all elements to the left of `i`.
`right[i]` stores the product of all elements to the right of `i`.
Then, `output[i] = left[i] * right[i]`.
*Tradeoffs:* $O(n)$ time, but $O(n)$ auxiliary space for the two extra arrays.
* **Approach 3: O(1) Auxiliary Space**
We can optimize Approach 2. Instead of building a `left` array, we can use the final `output` array to store the left products.
Then, instead of building a `right` array, we can do a single pass from right to left, keeping track of a running right product in a single integer variable, multiplying it into the `output` array on the fly.
*Tradeoffs:* $O(n)$ time and $O(1)$ auxiliary space (since the output array doesn't count).

### 5. Select the solution

I will go with **Approach 3**. It satisfies the "no division" constraint natively, handles zeros flawlessly, and achieves optimal time and space complexity. It relies on standard array traversal, making it highly readable and easy to implement correctly.

### 6. Write the implementation outline

```java
int[] productExceptSelf(int[] nums) {
    /*
     * Reframe:
     * For each index, multiply the prefix product by the suffix product 
     * without creating extra arrays.
     *
     * State:
     * - output array: initially holds the left-side products.
     * - rightProduct: a running total of the right-side products.
     * Chosen because it drops auxiliary space from O(n) to O(1).
     *
     * Invariant:
     * - After pass 1, output[i] contains the product of all nums[0...i-1].
     * - During pass 2, output[i] is multiplied by the running rightProduct, 
     *   which represents all nums[i+1...n-1].
     *
     * Core logic:
     * - Allocate the output array.
     * - Loop forwards: calculate the running left product and store it in output.
     * - Loop backwards: multiply output[i] by running right product, 
     *   then update the running right product.
     * - Return the output array.
     *
     * Edge cases:
     * - Zeros anywhere in the array.
     * - Negative numbers.
     */
}

```

### 7. Implement iteratively

**Iteration 1: Method skeleton and left pass**
First, we'll set up the output array and do the forward pass. For index 0, there is nothing to its left, so the initial left product is 1.

```java
public int[] productExceptSelf(int[] nums) {
    int n = nums.length;
    int[] output = new int[n];
    
    // Pass 1: Calculate left products.
    // output[i] will contain the product of all elements to the left of i.
    int leftProduct = 1;
    for (int i = 0; i < n; i++) {
        output[i] = leftProduct;
        leftProduct *= nums[i]; // Prepare for the next index
    }
    
    // TODO: Pass 2 to incorporate right products
    
    return output;
}

```

*At this point, if `nums = [1, 2, 3, 4]`, our `output` array is `[1, 1, 2, 6]`.*

**Iteration 2: Completing the right pass**
Now we sweep from right to left. We use a single integer variable to accumulate the right-side product.

```java
public int[] productExceptSelf(int[] nums) {
    int n = nums.length;
    int[] output = new int[n];
    
    // Pass 1: Calculate left products.
    int leftProduct = 1;
    for (int i = 0; i < n; i++) {
        output[i] = leftProduct;
        leftProduct *= nums[i];
    }
    
    // Added: Pass 2 - Calculate right products and multiply into output.
    int rightProduct = 1;
    for (int i = n - 1; i >= 0; i--) {
        output[i] *= rightProduct; // Multiply the accumulated right product with the left product
        rightProduct *= nums[i];   // Prepare for the next index to the left
    }
    
    return output;
}

```

**Edge-case pass**
Let's review the edge cases:

* **Zeros:** If `nums = [1, 0, 3]`:
* Pass 1 (left): `output = [1, 1, 0]` (leftProduct becomes 0 after index 1).
* Pass 2 (right): `output[2] = 0 * 1 = 0`. `rightProduct` becomes 3. `output[1] = 1 * 3 = 3`. `rightProduct` becomes 0. `output[0] = 1 * 0 = 0`. Final: `[0, 3, 0]`. Correct.


* **Multiple zeros:** The multiplications naturally carry the zeros forward and backward, resulting in all `0`s, which is correct.
* **Negative numbers:** Sign rules for multiplication apply seamlessly.

No patches are necessary; the core math naturally covers the invariants.

### 8. Analyze expensive sections and optimize

* **Time Complexity:** $O(n)$. We do exactly two passes over the array of size $n$. The operations inside the loops are primitive multiplications.
* **Space Complexity:** $O(1)$ auxiliary space. We use a few `int` variables. The result array is strictly the requested output and standardly excluded from auxiliary space accounting.

No further optimization is needed.

### Final code

```java
class Solution {
    public int[] productExceptSelf(int[] nums) {
        int n = nums.length;
        int[] output = new int[n];
        
        int leftProduct = 1;
        for (int i = 0; i < n; i++) {
            output[i] = leftProduct;
            leftProduct *= nums[i];
        }
        
        int rightProduct = 1;
        for (int i = n - 1; i >= 0; i--) {
            output[i] *= rightProduct;
            rightProduct *= nums[i];
        }
        
        return output;
    }
}

```

### Brief test walkthrough

Let's test an edge case with a zero: `nums = [-1, 1, 0, -3, 3]`

* Expected output: All indices except the zero should evaluate to `0`. The index with `0` should contain the product of the rest: `-1 * 1 * -3 * 3 = 9`. Expected output: `[0, 0, 9, 0, 0]`.
* **Pass 1 (left):**
* `i=0, val=-1`: `out[0]=1`, `left=-1`
* `i=1, val=1`: `out[1]=-1`, `left=-1`
* `i=2, val=0`: `out[2]=-1`, `left=0`
* `i=3, val=-3`: `out[3]=0`, `left=0`
* `i=4, val=3`: `out[4]=0`, `left=0`
* `output = [1, -1, -1, 0, 0]`


* **Pass 2 (right):**
* `i=4, val=3`: `out[4] = 0 * 1 = 0`, `right = 3`
* `i=3, val=-3`: `out[3] = 0 * 3 = 0`, `right = -9`
* `i=2, val=0`: `out[2] = -1 * -9 = 9`, `right = 0`
* `i=1, val=1`: `out[1] = -1 * 0 = 0`, `right = 0`
* `i=0, val=-1`: `out[0] = 1 * 0 = 0`, `right = 0`


* **Result:** `[0, 0, 9, 0, 0]`. The algorithm accurately handles arrays with zero.