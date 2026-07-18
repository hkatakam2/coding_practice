### 1. Restate the problem

We are given an array of integers representing the heights of vertical lines placed along an x-axis.
We need to find two lines that, together with the x-axis, form a container capable of holding the maximum possible amount of water.

* **Given:** An array `heights` where the value represents the height of a bar.
* **Return:** A single integer representing the maximum volume (or area) of water trapped between any two bars.
* **Constraint/Relationship:** The volume between two bars at indices `i` and `j` is defined by the width (`j - i`) multiplied by the height of the *shorter* of the two bars (`Math.min(heights[i], heights[j])`).
* Order matters only insofar as it dictates width.

### 2. Ask clarifying questions

* **Input size:** How large can the `heights` array be? (I will assume up to $10^5$, meaning an $O(n^2)$ solution will time out).
* **Input minimums:** Can the array have fewer than 2 elements? (I will assume the array has at least 2 elements, as a container requires two sides).
* **Values:** Can heights be $0$? (Yes, a line of height $0$ holds no water). Can they be negative? (I will assume heights are non-negative).
* **Integer Overflow:** Could the maximum area exceed the maximum 32-bit signed integer? If the maximum width is $10^5$ and maximum height is $10^4$, the max area is $10^9$, which safely fits in a standard Java `int`. I will use `int` for the area, but if heights or widths could be larger, `long` would be required.

### 3. Work through an example by hand

Let's use `heights = [1, 8, 6, 2, 5, 4, 8, 3, 7]`

1. **Initial State:**
* Consider the widest possible container: the first and last lines.
* Index 0 (height 1) and Index 8 (height 7).
* Width = $8 - 0 = 8$.
* Height = $\min(1, 7) = 1$.
* Area = $8 \times 1 = 8$.
* Current Max Area = 8.


2. **Decision:**
* To find a larger area, we need a taller bounding line. The height of this container was bottlenecked by the left line (height 1). Moving the right line inward would only decrease the width without possibly increasing the bottleneck height. Therefore, we should discard the left line and move inward.


3. **Next Step:**
* Index 1 (height 8) and Index 8 (height 7).
* Width = $8 - 1 = 7$.
* Height = $\min(8, 7) = 7$.
* Area = $7 \times 7 = 49$.
* Current Max Area = $\max(8, 49) = 49$.


4. **Decision:**
* The right line (height 7) is now the bottleneck. Move the right pointer inward.


5. **Next Step:**
* Index 1 (height 8) and Index 7 (height 3).
* Width = $7 - 1 = 6$.
* Height = $\min(8, 3) = 3$.
* Area = $6 \times 3 = 18$.
* Max Area remains 49.



By continually moving the pointer of the shorter line inward, we evaluate the most promising containers until the pointers meet. The result will be 49.

### 4. Brainstorm solutions aloud

**Approach 1: Brute Force**

* **Core idea:** Compare every possible pair of lines and calculate the area.
* **Data structures:** None, just two nested loops.
* **Complexity:** Time is $O(n^2)$ because there are roughly $n^2 / 2$ pairs. Space is $O(1)$.
* **Tradeoffs:** Very easy to write and prove correct, but far too slow for arrays with thousands of elements.

**Approach 2: Two Pointers (Greedy Search)**

* **Core idea:** Maximize the width first by placing pointers at the extreme ends of the array. The area is limited by the shorter line. If we move the taller line inward, the width decreases, and the height can *never* increase above the existing shorter line, guaranteeing a smaller area. Therefore, the only logical move to find a larger area is to move the shorter line inward.
* **Data structures:** Two integer pointers.
* **Complexity:** Time is $O(n)$ because we process each element at most once as the pointers converge. Space is $O(1)$ since we only store a few integers.
* **Implementation difficulty:** Easy.

### 5. Select the solution

I will use the **Two Pointers** approach. It perfectly leverages the property of the problem (area bottlenecked by the shorter side) to achieve an optimal $O(n)$ time complexity. It requires no extra memory and is extremely readable.

### 6. Write the implementation outline

```java
int maxArea(int[] heights) {
    /*
     * Reframe:
     * Start with the widest possible container, then greedily shrink the width
     * by discarding the shorter boundary, seeking a taller replacement.
     *
     * State:
     * - `left`: pointer to the start of the array.
     * - `right`: pointer to the end of the array.
     * - `maxWater`: tracking the largest area found so far.
     * Chosen because tracking the two current boundaries allows us to calculate width instantly.
     *
     * Invariant:
     * The maximum possible area using the discarded lines has already been evaluated.
     *
     * Core logic:
     * - initialize pointers at both ends of the array
     * - while the left pointer is strictly less than the right pointer:
     *     - calculate the current width
     *     - calculate the height (the minimum of the two pointed values)
     *     - compute the area and update maxWater if it's larger
     *     - move the pointer pointing to the shorter line inward
     * - return maxWater
     *
     * Edge cases:
     * - Both lines are the same height (it doesn't matter which we move; either works safely).
     * - Input array has only two elements.
     */
}

```

### 7. Implement iteratively

**Iteration 1: Method skeleton and state variables**
I'll set up the boundaries and the loop condition.

```java
public int maxArea(int[] heights) {
    int left = 0;
    int right = heights.length - 1;
    int maxWater = 0;

    while (left < right) {
        // TODO: Calculate the area for the current container
        // TODO: Update maxWater
        // TODO: Move the pointer of the shorter line inward
    }

    return maxWater;
}

```

**Iteration 2: Core logic (Computing area and moving pointers)**
Now I'll implement the math to find the area and the condition to step the pointers inward.

```java
public int maxArea(int[] heights) {
    int left = 0;
    int right = heights.length - 1;
    int maxWater = 0;

    while (left < right) {
        // Added: Calculate area based on width and the bottleneck height
        int currentWidth = right - left;
        int currentHeight = Math.min(heights[left], heights[right]);
        int currentArea = currentWidth * currentHeight;

        maxWater = Math.max(maxWater, currentArea);

        // Added: Shrink the window by moving the shorter line
        if (heights[left] < heights[right]) {
            left++;
        } else {
            right--;
        }
    }

    return maxWater;
}

```

**Edge-case pass**

* *Smallest input (`length = 2`):* `left = 0`, `right = 1`. Calculates the one and only container, updates `maxWater`, increments a pointer, loop terminates. Works perfectly.
* *Equal heights:* If `heights[left] == heights[right]`, the code executes the `else` block (`right--`). Since the current lines are equal, moving either line will bottleneck the *next* configuration against the remaining static line. Moving either one is mathematically sound.
* *Heights of $0$:* Handled correctly; height becomes $0$, area becomes $0$, which won't override a strictly positive `maxWater`.

### 8. Analyze expensive sections and optimize

The algorithm uses a single loop where the distance between `left` and `right` decreases by $1$ on every iteration.

* **Time Complexity:** $O(n)$, where $n$ is the length of `heights`. Every element is inspected at most once. There are no expensive calls or nested loops.
* **Space Complexity:** $O(1)$. We are strictly using primitive integer variables (`left`, `right`, `maxWater`, `currentWidth`, `currentHeight`, `currentArea`), resulting in zero allocation overhead.

No further optimization is structurally needed. However, we can inline `currentWidth`, `currentHeight`, and `currentArea` slightly for compactness without losing readability.

**Final Code:**

```java
public int maxArea(int[] heights) {
    int left = 0;
    int right = heights.length - 1;
    int maxWater = 0;

    while (left < right) {
        int width = right - left;
        
        if (heights[left] < heights[right]) {
            maxWater = Math.max(maxWater, width * heights[left]);
            left++;
        } else {
            maxWater = Math.max(maxWater, width * heights[right]);
            right--;
        }
    }

    return maxWater;
}

```

### Brief test walkthrough

Let's trace a small edge-case test: `heights = [1, 1]`

1. `left = 0` (val 1), `right = 1` (val 1). `maxWater = 0`.
2. `left < right` (0 < 1) is true.
3. `width` = $1 - 0 = 1$.
4. `heights[left] < heights[right]` is `1 < 1`, which is false.
5. Goes to `else`: `maxWater = Math.max(0, 1 * 1) = 1`.
6. `right` decrements to 0.
7. `left < right` (0 < 0) is false.
8. Loop exits. Returns 1. Expected result: 1.