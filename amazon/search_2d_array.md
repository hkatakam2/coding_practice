### question
Given an m×n matrix where each row is sorted and the first element of each row is greater than the last of the previous row, determine whether a target exists in the matrix.

Here is the mock interview beat-by-beat.

### 1. Restate

Given an $m \times n$ 2D grid. Two rules: rows are sorted ascending left-to-right; each row's first value is strictly greater than previous row's last value. Goal: return boolean indicating if a target integer exists in this grid.

### 2. Clarify

* **Inputs:** `matrix` (list of lists of ints), `target` (int).
* **Outputs:** `True` if found, `False` otherwise.
* **Questions:** * Can the matrix be empty? (Assume yes).
* Can rows be empty? (Assume yes).
* Are there duplicates? (Rules imply strictly increasing, so no duplicates).
* Does it fit in memory? (Assume yes).



### 3. By Hand

Input: `matrix = [[1, 3, 5], [7, 9, 11]]`, `target = 9`. $m=2, n=3$. Total elements = 6.
Imagine it flat: `[1, 3, 5, 7, 9, 11]`. Indices $0$ to $5$.

1. Start: low index $0$, high index $5$. Mid index = $(0+5)//2 = 2$.
2. Index 2 maps to row $2//3 = 0$, col $2\%3 = 2$. Value at `matrix[0][2]` is $5$.
3. $5 < 9$. Search right half. Low = $3$, high = $5$.
4. Mid index = $(3+5)//2 = 4$.
5. Index $4$ maps to row $4//3 = 1$, col $4\%3 = 1$. Value at `matrix[1][1]` is $9$.
6. $9 == 9$. Return `True`.

### 4. Brainstorm & Complexity

* **Approach A: Brute Force.** Loop over every cell. Time: $O(m \cdot n)$. Space: $O(1)$. Too slow.
* **Approach B: Two-Step Binary Search (The "Human Eye" Method).** Binary search on the first column to find the potential row. Then binary search within that row. Time: $O(\log m + \log n)$. Space: $O(1)$.
* **Approach C: 1D Virtual Array.** Treat the $m \times n$ matrix as a 1D array of length $m \cdot n$. Run one standard binary search, using modulo/division math to map 1D indices back to 2D coordinates. Time: $O(\log(m \cdot n))$. Space: $O(1)$.

### 5. Suggest Solutions

Approach B represents how a human scans it (finding the row, then the column). Approach C is the "1D Virtual Array" method from Step 3.

Let's proceed with **Approach C**. It is the simplest and clearest to implement because it relies on the standard, unmodified binary search algorithm. We only need one loop instead of two.

### 6. Outline

```python
def searchMatrix(matrix, target): # -> bool
    """
    Reframe: The strict row-to-row sorting means the matrix is identical to a flattened 1D sorted array.
    State: Two pointers (left, right) tracking 1D indices, chosen because standard binary search requires tracking bounds.
    Invariant: If target exists, its mapped 1D index is strictly between left and right bounds (inclusive).

    get_value(index) = converts 1D index to 2D coordinates and returns the matrix value.

    Core logic:
    - calculate total elements to define the theoretical 1D array end.
    - set left pointer to start, right pointer to end.
    - while left is less than or equal to right:
        - calculate middle index.
        - fetch value at middle index using get_value.
        - if value matches target, return True.
        - if value is less than target, shift left boundary up.
        - if value is greater than target, shift right boundary down.
    - return False if search completes without finding target.

    Edge cases:
    - matrix is empty.
    - first row is empty (columns = 0).
    """

```

### 7. Iterative Implementation

**Iteration 1: Skeleton with stubs**

```python
def searchMatrix(matrix: list[list[int]], target: int) -> bool:
    # TODO: edge cases
    
    rows = len(matrix)
    cols = len(matrix[0])
    
    def get_value(idx):
        # Stub: map 1D index to 2D
        pass

    left = 0
    right = (rows * cols) - 1

    # TODO: core binary search loop
    return False

```

**Iteration 2: Adding the Core Logic (Happy Path)**

```python
def searchMatrix(matrix: list[list[int]], target: int) -> bool:
    rows = len(matrix)
    cols = len(matrix[0])
    
    def get_value(idx):
        # Stub
        pass

    left = 0
    right = (rows * cols) - 1

    # Added core binary search logic
    while left <= right:
        mid = (left + right) // 2
        mid_val = get_value(mid)
        
        if mid_val == target:
            return True
        elif mid_val < target:
            left = mid + 1
        else:
            right = mid - 1
            
    return False

```

**Iteration 3: Realizing the helper logic**

```python
def searchMatrix(matrix: list[list[int]], target: int) -> bool:
    rows = len(matrix)
    cols = len(matrix[0])
    
    # Implemented 1D to 2D mapping math
    def get_value(idx):
        r = idx // cols
        c = idx % cols
        return matrix[r][c]

    left = 0
    right = (rows * cols) - 1

    while left <= right:
        mid = (left + right) // 2
        mid_val = get_value(mid)
        
        if mid_val == target:
            return True
        elif mid_val < target:
            left = mid + 1
        else:
            right = mid - 1
            
    return False

```

**Iteration 4: Patching Edge Cases**

```python
def searchMatrix(matrix: list[list[int]], target: int) -> bool:
    # ADDED: Handle empty matrix or empty rows
    if not matrix or not matrix[0]:
        return False
        
    rows = len(matrix)
    cols = len(matrix[0])
    
    def get_value(idx):
        r = idx // cols
        c = idx % cols
        return matrix[r][c]

    left = 0
    right = (rows * cols) - 1

    while left <= right:
        mid = (left + right) // 2
        mid_val = get_value(mid)
        
        if mid_val == target:
            return True
        elif mid_val < target:
            left = mid + 1
        else:
            right = mid - 1
            
    return False

```

### 8. Complexity & Optimizations

* **Time Complexity:** $O(\log(m \cdot n))$. Standard binary search halves the search space each step. Note mathematically that $O(\log(m \cdot n))$ is equivalent to $O(\log m + \log n)$.
* **Space Complexity:** $O(1)$. We only store pointers and calculated indices.
* **Optimization Note:** Division (`//`) and modulo (`%`) are relatively expensive operations at the CPU level compared to bitwise shifts. However, in Python, the overhead of the language masks this, and $O(\log(m \cdot n))$ bounds the number of these operations severely (e.g., a $1000 \times 1000$ matrix requires at most ~20 operations). Avoiding the nested helper function by inlining the math inside the `while` loop removes a tiny bit of call-stack overhead, but at the cost of readability. Stick to the clear version unless profiling demands otherwise.