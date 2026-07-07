### question
Given a square n x n matrix of integers matrix, rotate it by 90 degrees clockwise.

You must rotate the matrix in-place. Do not allocate another 2D matrix and do the rotation.

## 1. Restating the Question

Given a square `n x n` matrix, rotate it 90 degrees clockwise. Modifying the input matrix directly. Extra 2D arrays strictly forbidden.

## 2. Clarifying Questions

* Is the matrix guaranteed to be square? (Assuming yes, `n x n`).
* Can `n` be 0 or 1? (Assuming yes, need to handle small bounds).
* Data type? (Assuming integers, but algorithm is type-agnostic).

## 3. Example by Hand

Input:

```
1 2 3
4 5 6
7 8 9

```

Human rotates physical object, treating it like concentric rings.
Outer ring: corners shift 90 degrees.

* 1 -> 3's spot
* 3 -> 9's spot
* 9 -> 7's spot
* 7 -> 1's spot

Edge middle elements shift 90 degrees:

* 2 -> 6
* 6 -> 8
* 8 -> 4
* 4 -> 2

Center ring (5) stays unchanged.
Output:

```
7 4 1
8 5 2
9 6 3

```

## 4. Brainstorming Solutions

* **Approach 1: Allocate New Matrix.** Read rows from original, write as columns into new matrix. Time: O(N^2). Space: O(N^2). Fails in-place constraint.
* **Approach 2: 4-Way Cyclic Swap (The "By-Hand" Method).** Process ring by ring, outside in. Track top/bottom/left/right boundaries. Move 4 cells at a time in a cycle. Time: O(N^2). Space: O(1). Complexity: High chance of off-by-one index errors.
* **Approach 3: Transpose + Reverse.** Mathematical property of matrices.
1. Transpose matrix (swap elements across main diagonal: `[i][j]` swaps with `[j][i]`).
2. Reverse elements in each row horizontally.
Time: O(N^2). Space: O(1). Complexity: Two simple isolated operations. Very clean.



## 5. Suggested Solutions

Approach 2 translates the physical by-hand rotation directly into code using 4-way cyclic swaps. Approach 3 uses geometric matrix properties (Transpose then Reverse).

Selecting **Approach 3**. Always prefer simple, clear, straightforward solutions that are easy to read and explain over complex index-arithmetic math. It perfectly isolates the logic into two highly readable steps.

## 6. Implementation Outline

```python
def rotate(matrix): 
    """
    Reframe: 90-degree clockwise rotation is identical to transposing the matrix, then horizontally flipping it.
    State: The matrix itself, manipulated in-place via swapping, chosen because it satisfies O(1) extra space constraints.
    Invariant: Each element transitions to an intermediate state (transposed) exactly once, then to final state (reversed) exactly once, preserving data integrity.

    transpose(matrix) = swap elements across the top-left to bottom-right diagonal.
    reverse_rows(matrix) = reverse the element order of every row independently.

    Core logic:
    - apply transpose helper to the matrix
    - apply reverse_rows helper to the matrix

    Edge cases:
    - n = 1: 1x1 matrix requires no changes.
    - empty matrix / n = 0: no loops trigger, safe exit.
    """

```

## 7. Iterative Implementation

**Iteration 1: Skeleton**

```python
def rotate(matrix):
    # TODO: transpose the matrix in-place
    
    # TODO: reverse each row in-place
    pass

```

**Iteration 2: Adding Transpose Logic**
*Change:* Implemented the transpose step. Iterate rows `i`, but column `j` only iterates from `i+1` to `n`. This prevents swapping cells back to their original spots.

```python
def rotate(matrix):
    n = len(matrix)
    
    # Transpose the matrix
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
            
    # TODO: reverse each row in-place

```

**Iteration 3: Adding Reverse Logic (Final Core Logic)**
*Change:* Implemented row reversal. Using Python's native `reverse()` on lists modifies in-place natively. Could also use manual two-pointer approach, but native list methods are clearer and highly optimized.

```python
def rotate(matrix):
    n = len(matrix)
    
    # Transpose the matrix
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
            
    # Reverse each row
    for i in range(n):
        matrix[i].reverse()

```

**Walking Edge Cases:**

* **n = 1:** `n = 1`. `range(1)` produces `i = 0`. Inner loop `range(0 + 1, 1)` -> `range(1, 1)` is empty. Transpose does nothing. Row loop `i = 0`, `matrix[0].reverse()` on a 1-element list does nothing. Result is correct.
* **Empty Matrix:** `n = 0`. Both outer loops `range(0)` are empty. No operations executed. Result is correct.

## 8. Complexity & Optimizations

**Time Complexity:** O(N^2). The transpose nested loops touch roughly half the matrix elements `(N^2 / 2)` and the reverse loops touch all elements `(N^2)`. Total operations scale strictly with the total number of cells in the `N x N` grid.
**Space/Memory:** O(1). Zero extra space allocated. Swaps use a single implicit temp variable.

**Optimizations:**
Algorithmically optimal; every cell must be read and written to at least once to change positions. Utilizing `matrix[i].reverse()` delegates the row-reversal loop to the underlying C implementation in Python, which is heavily optimized and faster than writing a manual `left`, `right` while-loop.