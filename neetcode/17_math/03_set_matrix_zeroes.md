### question
Given an m x n matrix of integers matrix, if an element is 0, set its entire row and column to 0's.

You must update the matrix in-place.

**1. Restating the Question**
Given 2D grid of numbers. If cell is 0, make entire row and col 0. Must modify grid directly (in-place).

**2. Clarifying Questions & I/O**

* Q: Empty matrix possible? A: Assume valid m x n grid (m, n >= 1).
* Q: Negative numbers allowed? A: Yes. Any integer.
* Q: Chain reactions? (A 0 created by rule creates more 0s?) A: No. Only original 0s trigger row/col clears.
* I/O:
Input: `matrix = [[1,1,1],[1,0,1],[1,1,1]]`
Output: `None` (Matrix becomes `[[1,0,1],[0,0,0],[1,0,1]]`)

**3. Hand-Tracing Example**
Input:
1 1 1
1 0 1
1 1 1

* Scan row by row.
* Hit row 1, col 1: It's a `0`.
* Remember: "Row 1 needs zeroing. Col 1 needs zeroing."
* Finish scan.
* Second pass:
* Cell (0,1)? Col 1 needs zeroing -> set 0.
* Cell (1,0)? Row 1 needs zeroing -> set 0.
* Cell (1,1)? Both need zeroing -> set 0 (already 0).
* Cell (1,2)? Row 1 needs zeroing -> set 0.
* Cell (2,1)? Col 1 needs zeroing -> set 0.


* Result matches expected output.

**4. Brainstorming & Complexity**

* *App 1 (Brute Force):* Copy matrix. Scan original. If 0, overwrite row/col in copy. Copy back.
Time: O(m*n). Space: O(m*n).
* *App 2 (Sets - Hand Trace):* 2 passes. Pass 1: record indices of rows and cols containing 0 in sets. Pass 2: check if current cell's row or col is in sets. If yes, set to 0.
Time: O(m*n). Space: O(m+n).
* *App 3 (In-place Markers):* Use first row and first col as the "sets" from App 2.
Time: O(m*n). Space: O(1).

**5. Suggesting Solutions**
Suggest App 2 (Sets). Extremely clear, directly maps to hand trace, avoids complex index management of App 3. App 3 is clever optimization, harder to read. Will start with App 2.

**6. Outline of Selected Implementation**

```python
def setZeroes(matrix): 
    """
    Reframe: Isolate discovery of 0s from application of 0s to avoid infinite chain reactions.
    State: Two sets `zero_rows` and `zero_cols`, chosen because they decouple read phase from write phase efficiently.
    Invariant: Cells read during pass 1 reflect original matrix state.

    record_zeros(matrix) = scans grid, populates zero_rows and zero_cols
    is_infected(r, c) = true if r in zero_rows or c in zero_cols

    Core logic:
    - record_zeros(matrix)
    - iterate every cell in grid:
      - if is_infected(row, col):
        - set cell to 0

    Edge cases:
    - empty matrix (no rows or no cols)
    """

```

**7. Iterative Implementation**

*Iteration 1: Skeleton & Stubs*

```python
def setZeroes(matrix):
    # setup state
    zero_rows = set()
    zero_cols = set()
    
    # stubs
    def record_zeros():
        pass # TODO: populate sets
        
    def is_infected(r, c):
        pass # TODO: check sets
        
    # core logic skeleton
    record_zeros()
    
    # TODO: iterate grid and apply zeros

```

*Iteration 2: Fleshing out core logic & stubs (Happy Path)*

```python
def setZeroes(matrix):
    zero_rows = set()
    zero_cols = set()
    
    # Implemented stub 1
    def record_zeros():
        for r in range(len(matrix)):
            for c in range(len(matrix[0])):
                if matrix[r][c] == 0:
                    zero_rows.add(r)
                    zero_cols.add(c)
                    
    # Implemented stub 2
    def is_infected(r, c):
        return r in zero_rows or c in zero_cols
        
    record_zeros()
    
    # Implemented core logic loop
    for r in range(len(matrix)):
        for c in range(len(matrix[0])):
            if is_infected(r, c):
                matrix[r][c] = 0

```

*Iteration 3: Edge Cases Patch*

```python
def setZeroes(matrix):
    # PATCH: Edge case - empty matrix
    if not matrix or not matrix[0]:
        return

    zero_rows = set()
    zero_cols = set()
    
    def record_zeros():
        for r in range(len(matrix)):
            for c in range(len(matrix[0])):
                if matrix[r][c] == 0:
                    zero_rows.add(r)
                    zero_cols.add(c)
                    
    def is_infected(r, c):
        return r in zero_rows or c in zero_cols
        
    record_zeros()
    
    for r in range(len(matrix)):
        for c in range(len(matrix[0])):
            if is_infected(r, c):
                matrix[r][c] = 0

```

**8. Complexity & Optimizations**

* Current Time: O(m*n). Optimal.
* Current Space: O(m+n) due to sets. Expensive memory for massive grids.
* *Optimization (App 3)*: Drop sets. Use `matrix[0][..]` to track column zeros, `matrix[..][0]` to track row zeros. Needs 2 flags to track if first row/col themselves originally had zeros.
* *Refactored O(1) Space Code:*

```python
def setZeroes(matrix):
    if not matrix or not matrix[0]: return
    
    m, n = len(matrix), len(matrix[0])
    first_row_has_zero = any(matrix[0][c] == 0 for c in range(n))
    first_col_has_zero = any(matrix[r][0] == 0 for r in range(m))
    
    # Use first row/col as markers
    for r in range(1, m):
        for c in range(1, n):
            if matrix[r][c] == 0:
                matrix[r][0] = 0
                matrix[0][c] = 0
                
    # Apply zeros based on markers
    for r in range(1, m):
        for c in range(1, n):
            if matrix[r][0] == 0 or matrix[0][c] == 0:
                matrix[r][c] = 0
                
    # Handle the markers themselves
    if first_row_has_zero:
        for c in range(n): matrix[0][c] = 0
    if first_col_has_zero:
        for r in range(m): matrix[r][0] = 0

```