### 1. Restate the problem

We are given a 2D grid of numbers. If we find a `0` anywhere in the grid, we need to change every number in that same row and every number in that same column to `0`.

**Given:** An $m \times n$ integer array `matrix`.
**Returns:** Nothing. We must modify the given `matrix` directly (in-place).
**Main constraint:** If we change a cell to `0` during our process, it should *not* trigger its own row and column to become `0`. Only the *original* `0`s should influence the outcome.

### 2. Ask clarifying questions

In a real interview, I would confirm the following details:

* **What does "in-place" mean here?** Does it just mean modifying the input array, or does it specifically imply $O(1)$ additional space? *(Assumption: The interviewer wants the optimal $O(1)$ auxiliary space solution, as $O(m+n)$ space is trivial).*
* **Can the matrix be empty or null?** *(Assumption: The matrix will have at least 1 row and 1 column, but I will add a quick safeguard).*
* **Can the grid contain negative numbers?** *(Assumption: Yes, the grid can contain any valid integer. We cannot use special integer values like `-1` as temporary markers).*

### 3. Work through an example by hand

Let's trace a representative input to understand the "cascading zeroes" trap.

**Input:**

```
[0, 1, 2, 0]
[3, 4, 5, 2]
[1, 3, 1, 5]

```

* If we just scan left-to-right, top-to-bottom:
* At `(0,0)`, we see a `0`. We set row 0 to `0`s and col 0 to `0`s.
* Now the matrix looks like:
`[0, 0, 0, 0]`
`[0, 4, 5, 2]`
`[0, 3, 1, 5]`
* When we reach `(0,1)`, we see a `0`. But this is a *new* `0`, not an original one. If we act on this, we'll wipe out column 1. Eventually, the entire matrix becomes `0`.



**Correct logical progression:**

1. Identify original `0`s: at `(0,0)` and `(0,3)`.
2. Determine which rows and columns are affected: Row 0, Col 0, Col 3.
3. Apply the `0`s based only on that information.

**Expected Output:**

```
[0, 0, 0, 0]
[0, 4, 5, 0]
[0, 3, 1, 0]

```

### 4. Brainstorm solutions aloud

* **Approach 1: The Duplicate Matrix**
We could create a full copy of the matrix. We iterate over the copy to find the `0`s, and write the new `0`s to the original matrix.
*Time:* $O(m \times n)$. *Space:* $O(m \times n)$.
*Tradeoff:* Violates the spirit of an optimal in-place algorithm.
* **Approach 2: Row and Column Sets**
Instead of copying the whole matrix, we only need to remember *which* rows and *which* columns contain a `0`. We can use two boolean arrays: `boolean[] zeroRows` of size $m$ and `boolean[] zeroCols` of size $n$. We do one pass to populate these arrays, and a second pass over the matrix to set cells to `0` if their row or column is flagged.
*Time:* $O(m \times n)$. *Space:* $O(m + n)$.
*Tradeoff:* Much better memory usage, but still uses extra space.
* **Approach 3: Matrix as its Own Memory ($O(1)$ Space)**
We can use the first row and the first column of the matrix itself to act as our `zeroRows` and `zeroCols` tracking arrays.
If `matrix[i][j] == 0`, we set `matrix[i][0] = 0` and `matrix[0][j] = 0`.
Because we are overwriting the first row and column, we need two boolean variables to remember if the *original* first row and first column had any `0`s in them before we started using them as storage.
*Time:* $O(m \times n)$. *Space:* $O(1)$.

### 5. Select the solution

I will implement **Approach 3**. It satisfies the core $O(1)$ space requirement of the classic "Set Matrix Zeroes" problem. It relies on standard array traversal and uses the data structure's existing memory dynamically. We don't need Streams or complex collections; readable nested loops are exactly what this algorithm requires.

### 6. Write the implementation outline

```java
void setZeroes(int[][] matrix) {
    /*
     * Reframe:
     * Use the first row and first column to keep track of which other 
     * rows and columns need to be zeroed out.
     *
     * State:
     * Two booleans: firstRowHasZero and firstColHasZero.
     * The first row (matrix[0][...]) and first col (matrix[...][0]) act 
     * as our boolean tracking arrays for the rest of the matrix.
     * Chosen because this achieves O(1) extra space.
     *
     * Invariant:
     * The state of original zeroes in the inner matrix is perfectly 
     * reflected in the first row/col before we mutate the inner matrix.
     *
     * Core logic:
     * - scan the first row to see if it inherently contains a zero
     * - scan the first col to see if it inherently contains a zero
     * - iterate through the rest of the matrix (rows 1 to m-1, cols 1 to n-1)
     * - if an element is 0, mark its corresponding first row and col cell as 0
     * - iterate through the rest of the matrix again
     * - if a cell's row-header or col-header is 0, set the cell to 0
     * - finally, zero out the first row and first col if their flags are true
     *
     * Edge cases:
     * - matrix is empty
     * - matrix consists of a single row or column
     */
}

```

### 7. Implement iteratively

**Iteration 1: Method skeleton and checking the first row/column.**
I will set up the boundaries and check if the first row and first column originally contain zeros, storing this in two boolean flags.

```java
public void setZeroes(int[][] matrix) {
    if (matrix == null || matrix.length == 0 || matrix[0].length == 0) {
        return;
    }

    int rows = matrix.length;
    int cols = matrix[0].length;

    boolean firstRowHasZero = false;
    boolean firstColHasZero = false;

    // Check if first column has any zeroes
    for (int r = 0; r < rows; r++) {
        if (matrix[r][0] == 0) {
            firstColHasZero = true;
            break;
        }
    }

    // Check if first row has any zeroes
    for (int c = 0; c < cols; c++) {
        if (matrix[0][c] == 0) {
            firstRowHasZero = true;
            break;
        }
    }

    // TODO: use first row/col as markers for the rest of the matrix
    // TODO: zero out the inner matrix based on markers
    // TODO: zero out the first row/col based on the boolean flags
}

```

**Iteration 2: Using the first row/column as markers.**
Now, I will scan the "inner matrix" (ignoring the first row and column). If I find a `0`, I will place a `0` at the very top of that column and the far left of that row.

```java
public void setZeroes(int[][] matrix) {
    int rows = matrix.length;
    int cols = matrix[0].length;

    boolean firstRowHasZero = false;
    boolean firstColHasZero = false;

    for (int r = 0; r < rows; r++) {
        if (matrix[r][0] == 0) firstColHasZero = true;
    }
    for (int c = 0; c < cols; c++) {
        if (matrix[0][c] == 0) firstRowHasZero = true;
    }

    // Added: Mark zeroes on first row and column
    for (int r = 1; r < rows; r++) {
        for (int c = 1; c < cols; c++) {
            if (matrix[r][c] == 0) {
                matrix[r][0] = 0; // Mark the row
                matrix[0][c] = 0; // Mark the col
            }
        }
    }

    // TODO: zero out the inner matrix based on markers
    // TODO: zero out the first row/col based on the boolean flags
}

```

**Iteration 3: Applying the zeroes.**
Finally, I will do a second pass over the inner matrix to actually apply the zeroes based on the markers. Once the inner matrix is resolved, I will handle the first row and first column using the flags from Iteration 1.

```java
public void setZeroes(int[][] matrix) {
    int rows = matrix.length;
    int cols = matrix[0].length;

    boolean firstRowHasZero = false;
    boolean firstColHasZero = false;

    for (int r = 0; r < rows; r++) {
        if (matrix[r][0] == 0) firstColHasZero = true;
    }
    for (int c = 0; c < cols; c++) {
        if (matrix[0][c] == 0) firstRowHasZero = true;
    }

    for (int r = 1; r < rows; r++) {
        for (int c = 1; c < cols; c++) {
            if (matrix[r][c] == 0) {
                matrix[r][0] = 0;
                matrix[0][c] = 0;
            }
        }
    }

    // Added: Zero out cells based on markers in the first row/col
    for (int r = 1; r < rows; r++) {
        for (int c = 1; c < cols; c++) {
            if (matrix[r][0] == 0 || matrix[0][c] == 0) {
                matrix[r][c] = 0;
            }
        }
    }

    // Added: Zero out the first row if needed
    if (firstRowHasZero) {
        for (int c = 0; c < cols; c++) {
            matrix[0][c] = 0;
        }
    }

    // Added: Zero out the first column if needed
    if (firstColHasZero) {
        for (int r = 0; r < rows; r++) {
            matrix[r][0] = 0;
        }
    }
}

```

### 8. Edge-case walkthrough

* **1x1 Matrix:** `[[0]]`.
* `firstColHasZero` becomes true. `firstRowHasZero` becomes true.
* Inner matrix loop (`r=1`, `c=1`) doesn't run.
* Cleanup flags trigger, `matrix[0][0]` is set to `0`. Works perfectly.


* **No zeroes at all:** `[[1, 2], [3, 4]]`.
* Flags remain false.
* Inner markers remain unchanged.
* Inner matrix zeroing conditions (`matrix[r][0] == 0`) are false.
* Matrix remains unchanged. Works perfectly.


* **First element is zero:** `[[0, 1], [1, 1]]`.
* `firstColHasZero` and `firstRowHasZero` both become true.
* Inner loop finds no 0s.
* Final step zeroes out row 0 and col 0.
* Result is `[[0, 0], [0, 1]]`. Works perfectly.



No patches are necessary; the logic holds up well against edge conditions because bounds checks natively handle missing inner matrices or 1D inputs.

### 9. Final code, Complexity, & Tests

Here is the final, clean implementation:

```java
public void setZeroes(int[][] matrix) {
    if (matrix == null || matrix.length == 0 || matrix[0].length == 0) {
        return;
    }

    int rows = matrix.length;
    int cols = matrix[0].length;

    boolean firstRowHasZero = false;
    boolean firstColHasZero = false;

    // Step 1: Determine if the first row or first column inherently have zeroes
    for (int r = 0; r < rows; r++) {
        if (matrix[r][0] == 0) {
            firstColHasZero = true;
            break;
        }
    }
    
    for (int c = 0; c < cols; c++) {
        if (matrix[0][c] == 0) {
            firstRowHasZero = true;
            break;
        }
    }

    // Step 2: Use the first row and first column as marker arrays
    for (int r = 1; r < rows; r++) {
        for (int c = 1; c < cols; c++) {
            if (matrix[r][c] == 0) {
                matrix[r][0] = 0;
                matrix[0][c] = 0;
            }
        }
    }

    // Step 3: Zero out the inner matrix based on the markers
    for (int r = 1; r < rows; r++) {
        for (int c = 1; c < cols; c++) {
            if (matrix[r][0] == 0 || matrix[0][c] == 0) {
                matrix[r][c] = 0;
            }
        }
    }

    // Step 4: Zero out the original first row and column if necessary
    if (firstRowHasZero) {
        for (int c = 0; c < cols; c++) {
            matrix[0][c] = 0;
        }
    }

    if (firstColHasZero) {
        for (int r = 0; r < rows; r++) {
            matrix[r][0] = 0;
        }
    }
}

```

**Complexity Analysis**

* **Time Complexity:** $O(m \times n)$. We iterate through the matrix a constant number of times (checking flags, setting markers, applying zeroes). All operations inside the loop are $O(1)$.
* **Space Complexity:** $O(1)$. We are using only two boolean variables (`firstRowHasZero` and `firstColHasZero`) to keep track of state, reusing the input matrix itself as storage for the rest.

**Test Walkthrough**
Let's briefly trace the stress test invariant: `[[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]]`.

* *Step 1:* `firstRowHasZero` becomes `true` (due to `0,0`). `firstColHasZero` becomes `true` (due to `0,0`).
* *Step 2:* Inner loops evaluate. None are zero.
* *Step 3:* Inner loop checks headers. `matrix[0][1]`, `matrix[0][2]` are not zero, but `matrix[0][3]` is `0` (from the input). So `matrix[1][3]` and `matrix[2][3]` become `0`.
* *Step 4:* `firstRowHasZero` zeroes out `[0, 1, 2, 0]` to `[0, 0, 0, 0]`. `firstColHasZero` zeroes out `[0, 3, 1]` to `[0, 0, 0]`.
* *Final grid:* `[[0, 0, 0, 0], [0, 4, 5, 0], [0, 3, 1, 0]]`. This matches our manual example perfectly.