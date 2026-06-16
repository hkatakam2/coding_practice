### question
Given an integer array `nums`, return an array `output` where `output[i]` is the product of all the elements of `nums` except `nums[i]`.
Each product is guaranteed to fit in a 32-bit integer.
Follow-up: Could you solve it in O(n)O(n) time without using the division operation?

### 1. Restating the Question

Given integer array `nums`. Return array `output` where each element is the product of all elements in `nums` except the element at the current index.
Constraints: $O(n)$ time complexity, no division operation.

### 2. Clarifying Questions

* Minimum length of `nums`? Assumed 2.
* Can `nums` contain zeros? Yes.
* Can `nums` contain negative numbers? Yes.
* Output space counts towards space complexity? Usually no in interview contexts.

### 3. Example by Hand

Input: `[1, 2, 3, 4]`

* Index 0 (val 1): Left elements = none, Right = `[2, 3, 4]`. Product = `2 * 3 * 4 = 24`
* Index 1 (val 2): Left elements = `[1]`, Right = `[3, 4]`. Product = `1 * 3 * 4 = 12`
* Index 2 (val 3): Left elements = `[1, 2]`, Right = `[4]`. Product = `1 * 2 * 4 = 8`
* Index 3 (val 4): Left elements = `[1, 2, 3]`, Right = none. Product = `1 * 2 * 3 = 6`
Output: `[24, 12, 8, 6]`

### 4. Brainstorming and Complexity

* **Brute Force:** Nested loops. For each element, iterate through rest to find product. Time: $O(n^2)$. Space: $O(1)$. Too slow.
* **Division:** Multiply all elements for total product. Divide by current element. Fails "no division" constraint. Fails if array contains zeros. Time: $O(n)$. Space: $O(1)$.
* **Prefix/Suffix Products:** From manual example, product except self is just (product of everything to the left) $\times$ (product of everything to the right). Precompute left and right products. Time: $O(n)$. Space: $O(n)$.

### 5. Suggest Solutions

Prefer simple, clear approach. Prefix/Suffix products directly translates human logic (Step 3) into code. Will implement this.

### 6. Outline

```python
def productExceptSelf(nums):
    """
    Reframe: Product except self is the product of all left elements multiplied by product of all right elements.
    State: Two cumulative product arrays, chosen because caching these prevents redundant nested looping.
    Invariant: Cumulative running product up to the current element is maintained.

    get_left_products(nums) = builds list of products strictly to the left of current item
    get_right_products(nums) = builds list of products strictly to the right of current item

    Core logic:
    - calculate left products using helper
    - calculate right products using helper
    - combine both products by multiplying corresponding elements
    - return combined list
    
    Edge cases:
    - Array contains one zero (running product handles zeroes naturally).
    - Array contains multiple zeroes (handled naturally).
    """
    pass

```

### 7. Iterative Implementation

**Iteration 1: Skeleton**

```python
def productExceptSelf(nums):
    # TODO: implement helper
    left_products = get_left_products(nums)
    
    # TODO: implement helper
    right_products = get_right_products(nums)
    
    # TODO: combine
    return []

```

**Iteration 2: Implement helpers (Core Logic)**

```python
def get_left_products(nums):
    left = []
    running_product = 1
    for num in nums:
        left.append(running_product)
        running_product *= num
    return left

def get_right_products(nums):
    right = []
    running_product = 1
    # Iterate backwards
    for num in reversed(nums):
        right.append(running_product)
        running_product *= num
    # Reverse back to match original order
    return right[::-1]

def productExceptSelf(nums):
    left_products = get_left_products(nums) # [1, 1, 2, 6] for [1,2,3,4]
    right_products = get_right_products(nums) # [24, 12, 4, 1] for [1,2,3,4]
    
    # Combine
    output = []
    for left_val, right_val in zip(left_products, right_products):
        output.append(left_val * right_val)
        
    return output

```

**Iteration 3: Check Edge Cases**

* Single zero in input (e.g., `[1, 0, 3]`). `left` becomes `[1, 1, 0]`. `right` becomes `[0, 3, 1]`. Result: `[0, 3, 0]`. Correct.
* Multiple zeros in input (e.g., `[0, 0]`). `left` becomes `[1, 0]`. `right` becomes `[0, 1]`. Result: `[0, 0]`. Correct.
No edge-case patching needed. Core logic is robust.

### 8. Complexity and Optimization

Current Complexity: Time $O(n)$, Space $O(n)$ due to `left_products` and `right_products` arrays.

**Optimization:** Can achieve $O(1)$ auxiliary space. The output array does not count towards space complexity. We can calculate the left products directly into the `output` array. Then, calculate the right products on the fly using a single integer variable while iterating backward, multiplying directly into the `output` array.

**Optimized Code:**

```python
def productExceptSelf(nums):
    length = len(nums)
    output = [1] * length
    
    # Build left products directly in output
    running_left = 1
    for i in range(length):
        output[i] = running_left
        running_left *= nums[i]
        
    # Multiply by right products on the fly
    running_right = 1
    for i in range(length - 1, -1, -1):
        output[i] *= running_right
        running_right *= nums[i]
        
    return output

```

Time: $O(n)$. Space: $O(1)$ auxiliary.