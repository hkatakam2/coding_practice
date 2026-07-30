### 1. Restatement

We are given a square 2D array (a grid of size $n \times n$) containing integers. We need to rotate the entire grid 90 degrees clockwise.

* **Given**: An $n \times n$ `matrix` of integers.
* **Must modify**: The input `matrix` must be modified directly. We return nothing (void).
* **Main constraint**: The rotation must be done **in-place**. We cannot allocate a new $n \times n$ matrix to easily place elements into their new positions.
* **Other details**: Order definitely matters as we are geometrically rotating the data. Duplicate values might exist but don't affect the positional rotation.

### 2. Clarifying questions

* **Is it possible for the matrix to be null or empty ($n = 0$)?**
*Assumption*: I will assume it can be, and I should handle it safely by returning early.
* **Will the matrix always be perfectly square?**
*Assumption*: Yes, the problem specifies $n \times n$, so `matrix.length == matrix[0].length`.
* **Are there any performance constraints regarding time complexity?**
*Assumption*: We must visit every element, so $O(n^2)$ time is optimal and expected.
* **Do we need to worry about integer overflow?**
*Assumption*: No, we are only moving elements, not performing arithmetic on their values.

### 3. Work through an example by hand

Let's take a $3 \times 3$ matrix:

```text
1 2 3
4 5 6
7 8 9

```

If we rotate it 90 degrees clockwise, the top row `[1, 2, 3]` becomes the rightmost column. The bottom row `[7, 8, 9]` becomes the leftmost column.

Target result:

```text
7 4 1
8 5 2
9 6 3

```

How can we achieve this without a secondary matrix?
If we first **transpose** the matrix (swap elements across the top-left to bottom-right diagonal), we get:

```text
1 4 7
2 5 8
3 6 9

```

Notice that this is extremely close to our target. The rows are just backwards.
If we then **reverse each row** horizontally:

```text
7 4 1
8 5 2
9 6 3

```

This perfectly matches our target result!

### 4. Brainstorm solutions aloud

* **Approach 1: Layer-by-layer 4-way swap**
* *Core idea*: Process the matrix in concentric squares (outer edge, then the inner edge, etc.). For each element in the top row of a layer, move it to the right column, the right column to the bottom row, the bottom row to the left column, and the left column to the top row.
* *Time complexity*: $O(n^2)$ as we visit each cell a constant number of times.
* *Space complexity*: $O(1)$ since we only use a single temporary variable for swapping.
* *Implementation difficulty*: High. Index arithmetic (`n - 1 - i`, etc.) is notoriously difficult to get right under pressure without off-by-one errors.


* **Approach 2: Transpose and Reflect (Reverse Rows)**
* *Core idea*: As discovered in the manual example, rotating 90 degrees clockwise is mathematically equivalent to transposing the matrix across its main diagonal, followed by reversing elements in each row.
* *Time complexity*: $O(n^2)$ to transpose, plus $O(n^2)$ to reverse the rows. Overall $O(n^2)$.
* *Space complexity*: $O(1)$. We just swap elements in place.
* *Implementation difficulty*: Low. Transposing a matrix and reversing arrays are standard, straightforward operations.



### 5. Select the solution

I will select **Approach 2: Transpose and Reflect**.
It strictly satisfies the $O(1)$ auxiliary space constraint while avoiding the complex, error-prone index arithmetic of a 4-way layer swap. It is highly readable, easy to test in isolated parts (one helper for transpose, one for reverse), and perfectly leverages basic array manipulation.

### 6. Plain-English implementation outline

```java
void rotate(int[][] matrix) {
    /*
     * Reframe:
     * A 90-degree clockwise rotation is exactly equivalent to a diagonal 
     * transpose followed by a horizontal reflection.
     *
     * State:
     * No extra state needed. We will modify the matrix in place using 
     * temporary variables for swapping.
     * Chosen because:
     * We are strictly constrained to O(1) auxiliary space.
     *
     * Invariant:
     * During transpose, we only visit the upper triangle of the matrix to 
     * swap with the lower triangle, preventing double-swaps.
     *
     * Helpers:
     * transpose(matrix)
     * - swaps matrix[row][col] with matrix[col][row] for the upper triangle
     * reverseRows(matrix)
     * - uses a two-pointer approach (left and right) on each row to reverse it
     *
     * Core logic:
     * - validate input (null or empty)
     * - call transpose helper
     * - call reverseRows helper
     *
     * Edge cases:
     * - matrix is null
     * - matrix is empty or 1x1
     */
}

```

### 7. Iterative Java implementation

#### Iteration 1: Method skeleton

First, I will set up the main control flow and stub out the helpers.

```java
public void rotate(int[][] matrix) {
    if (matrix == null || matrix.length <= 1) {
        return; 
    }

    // TODO: Transpose the matrix (swap elements across the main diagonal)
    
    // TODO: Reverse each row horizontally
}

```

*Why this skeleton?* It addresses the core logic and handles the early return edge cases immediately.

#### Iteration 2: Implement transpose

Next, I will implement the transposition step.

```java
public void rotate(int[][] matrix) {
    if (matrix == null || matrix.length <= 1) {
        return; 
    }

    int n = matrix.length;

    // Added: Transpose the matrix
    // We only iterate col from row to n to ensure we only touch the upper triangle.
    // If we started col from 0, we would swap things twice, undoing our work.
    for (int row = 0; row < n; row++) {
        for (int col = row; col < n; col++) {
            int temp = matrix[row][col];
            matrix[row][col] = matrix[col][row];
            matrix[col][row] = temp;
        }
    }
    
    // TODO: Reverse each row horizontally
}

```

*Invariant established:* Every element above the main diagonal is perfectly swapped with its counterpart below the diagonal.

#### Iteration 3: Complete the happy path (Reverse rows)

Finally, I will reverse the items within each row using two pointers.

```java
public void rotate(int[][] matrix) {
    if (matrix == null || matrix.length <= 1) {
        return; 
    }

    int n = matrix.length;

    for (int row = 0; row < n; row++) {
        for (int col = row; col < n; col++) {
            int temp = matrix[row][col];
            matrix[row][col] = matrix[col][row];
            matrix[col][row] = temp;
        }
    }

    // Added: Reverse each row using two pointers
    for (int row = 0; row < n; row++) {
        int left = 0;
        int right = n - 1;
        while (left < right) {
            int temp = matrix[row][left];
            matrix[row][left] = matrix[row][right];
            matrix[row][right] = temp;
            left++;
            right--;
        }
    }
}

```

#### Edge-case walkthrough and patches

* *Edge case: matrix is null or $n = 0, n = 1$.*
* Walkthrough: Handled perfectly by the guard clause `if (matrix == null || matrix.length <= 1) return;`. A 1x1 matrix requires no rotation, so doing nothing is correct.


* *Edge case: odd vs. even $n$.*
* Walkthrough:
* If $n=3$, row reversal's `while (left < right)` stops when `left == right` (the middle element), which correctly stays in place.
* If $n=2$, `while (left < right)` swaps index 0 and 1, then stops, which is also correct.


* No patches needed.



### 8. Final code

```java
class Solution {
    public void rotate(int[][] matrix) {
        if (matrix == null || matrix.length <= 1) {
            return;
        }

        int n = matrix.length;

        // Step 1: Transpose the matrix
        for (int row = 0; row < n; row++) {
            for (int col = row; col < n; col++) {
                int temp = matrix[row][col];
                matrix[row][col] = matrix[col][row];
                matrix[col][row] = temp;
            }
        }

        // Step 2: Reverse each row
        for (int row = 0; row < n; row++) {
            int left = 0;
            int right = n - 1;
            while (left < right) {
                int temp = matrix[row][left];
                matrix[row][left] = matrix[row][right];
                matrix[row][right] = temp;
                left++;
                right--;
            }
        }
    }
}

```

### 9. Complexity

* **Time Complexity:** $O(n^2)$. The transpose step visits roughly half the elements in the matrix: $(n^2) / 2$ operations. The reverse step visits half the elements of every row: $(n^2) / 2$ operations. This sums strictly to $O(n^2)$ time, which is optimal since we must read and write every cell.
* **Space Complexity:** $O(1)$. We strictly mutate the original matrix using a single `temp` integer variable, satisfying the in-place constraint. No auxiliary matrices or collections are created.

### 10. Brief test walkthrough

* **Input:** `[[1]]` (Smallest valid input)
* Expected: `[[1]]`.
* Walkthrough: `matrix.length == 1`, triggers the guard clause and safely returns early.


* **Input:** `[[1, 2], [3, 4]]` (Stresses the central invariant with even dimensions)
* Expected: `[[3, 1], [4, 2]]`.
* Walkthrough:
* Transpose: `[0][1]` (2) swaps with `[1][0]` (3). Matrix becomes `[[1, 3], [2, 4]]`.
* Reverse row 0: 1 and 3 swap $\rightarrow$ `[3, 1]`.
* Reverse row 1: 2 and 4 swap $\rightarrow$ `[4, 2]`.
* Result matches expected perfectly.