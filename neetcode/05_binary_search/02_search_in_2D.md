### question
You are given an m x n 2-D integer array matrix and an integer target.

Each row in matrix is sorted in non-decreasing order.
The first integer of every row is greater than the last integer of the previous row.
Return true if target exists within matrix or false otherwise.

**1. Restating the Question**
Given a 2D matrix where every row is sorted and every row starts with a number larger than the previous row's end, find if a target number exists. Conceptually, if flattened, the matrix is a single strictly sorted 1D array.

**2. Clarifying Questions & Confirmations**

* Q: Can the matrix be empty? A: Assume yes, need to handle `[]` or `[[]]`.
* Q: Are duplicates possible? A: Yes, but strictly increasing row-to-row means duplicates only happen if a number repeats in a row, which doesn't break binary search.
* Input: `matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]]`, `target = 3`
* Output: `True`

**3. Hand-Tracing Example**
Input: `matrix = [[1,3], [5,7]]`, `target = 5`.

* Treat as 1D array of length 4: `[1, 3, 5, 7]`.
* `left` = 0, `right` = 3. `mid` = 1.
* Value at index 1 is `3`. `3 < 5`, so search right half.
* `left` = 2, `right` = 3. `mid` = 2.
* Value at index 2 is `5`. Matches target. Return `True`.

**4. Brainstorming Solutions & Complexity**

* *Option A (Brute Force):* Loop through every cell. Time: O(m * n). Space: O(1).
* *Option B (Row-by-Row):* Binary search each row. Time: O(m * log n). Space: O(1).
* *Option C (Virtual 1D Array):* Treat the whole matrix as a 1D array. Do binary search from index 0 to `(m * n) - 1`. Time: O(log(m * n)). Space: O(1).

**5. Suggested Solution**
Go with Option C. It directly leverages the "completely sorted if flattened" property. It is simple to explain: we just do a standard binary search, with a small helper to translate a 1D index back into 2D `(row, col)` coordinates.

**6. Implementation Outline**

```python
def searchMatrix(matrix, target):  # -> bool
    """
    Reframe: 2D matrix is conceptually a strictly sorted 1D array.
    State: left and right integer pointers for binary search, chosen because array is sorted.
    Invariant: target, if it exists, is always within [left, right] bounds.

    get_value(index) = converts 1D index to 2D coordinates and returns the matrix cell value.

    Core logic:
    - calculate middle index
    - get middle value using get_value
    - if middle value matches target, return true
    - if middle value is less than target, move left boundary past middle
    - if middle value is greater than target, move right boundary before middle
    - repeat while left boundary is at or behind right boundary
    - return false if loop finishes without finding target
    
    Edge cases:
    - matrix is completely empty
    - matrix has empty rows (no columns)
    """

```

**7. Iterative Implementation**

*Iteration 1: Outline core logic with a dummy helper.*

```python
def searchMatrix(matrix, target):
    # TODO: edge cases
    
    rows = len(matrix)
    cols = len(matrix[0])
    
    left = 0
    right = (rows * cols) - 1
    
    def get_value(idx):
        # TODO: map 1D idx to 2D
        pass
        
    # Standard binary search
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

*Iteration 2: Implement the dummy helper.* *Change note: Replaced `get_value` stub with actual math. `idx // cols` gives the row, `idx % cols` gives the column.*

```python
def searchMatrix(matrix, target):
    # TODO: edge cases
    
    rows = len(matrix)
    cols = len(matrix[0])
    
    left = 0
    right = (rows * cols) - 1
    
    def get_value(idx):
        r = idx // cols
        c = idx % cols
        return matrix[r][c]
        
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

*Iteration 3: Patch in edge cases.*
*Change note: Added check at the top for empty matrix or empty rows to prevent `IndexError` or division by zero.*

```python
def searchMatrix(matrix, target):
    # Edge case patch: check for empty inputs
    if not matrix or not matrix[0]:
        return False
        
    rows = len(matrix)
    cols = len(matrix[0])
    
    left = 0
    right = (rows * cols) - 1
    
    # helper extracts 1D index to 2D cell
    def get_value(idx):
        r = idx // cols
        c = idx % cols
        return matrix[r][c]
        
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

**8. Complexity & Optimizations**

* **Time Complexity:** O(log(m * n)). Standard binary search on a search space of `m * n` elements.
* **Space Complexity:** O(1). Only maintaining a few integer variables (`left`, `right`, `mid`, `rows`, `cols`).
* **Optimization:** Code is optimal. Division `//` and modulo `%` operations are mathematically fast. Inlined `get_value` logic into the while loop could save a marginal function call overhead in Python, but keeping the helper function makes the code highly readable and clearly separates the math map from the binary search logic. Readability wins here.