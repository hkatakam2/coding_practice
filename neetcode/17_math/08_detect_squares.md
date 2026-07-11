### question
You are given a stream of points consisting of x-y coordinates on a 2-D plane. Points can be added and queried as follows:

Add - new points can be added to the stream into a data structure. Duplicate points are allowed and should be treated as separate points.
Query - Given a single query point, count the number of ways to choose three additional points from the data structure such that the three points and the query point form a square. The square must have all sides parallel to the x-axis and y-axis, i.e. no diagonal squares are allowed. Recall that a square must have four equal sides.

## 1. Restate

We need design a data structure with two operations:

`add(point)`
Stores a point `(x, y)`. Duplicates are allowed, so adding the same point twice means there are two separate choices.

`count(queryPoint)`
Given `(qx, qy)`, count how many triples of stored points can combine with the query point to form an **axis-aligned square**.

Axis-aligned means square sides are horizontal/vertical only. No rotated squares.

---

## 2. Clarifying assumptions

In interview I would confirm:

1. Can duplicate points exist?
   Yes. They count separately.

2. Does the query point need to be previously added?
   No. It is just the fixed fourth corner.

3. Can coordinates be negative?
   Usually yes. The same logic works.

4. Are zero-area squares allowed?
   No. A square side length must be greater than `0`.

---

## 3. Example by hand

Suppose we add:

```python
(3, 10)
(11, 2)
(3, 2)
```

Query:

```python
(11, 10)
```

Draw the corners:

```text
(3,10) -------- (11,10) query
   |                |
   |                |
(3,2)  -------- (11,2)
```

These four points form a square of side length `8`.

So answer is:

```python
1
```

Now suppose `(3, 10)` was added twice.

Then we have two separate choices for the top-left corner, so answer becomes:

```python
2
```

Duplicates multiply the number of valid square choices.

---

## 4. Brainstorm solutions

### Brute force

For every query, try every triple of stored points.

That is too expensive:

```text
Query: O(n^3)
```

Not good.

---

### Better idea: use square geometry

For an axis-aligned square, if query point is one corner, then we need:

```text
query point:      (qx, qy)
vertical partner: (qx, other_y)
horizontal side:  side = abs(other_y - qy)
```

Then the square can extend either left or right.

Right square needs:

```text
(qx + side, qy)
(qx + side, other_y)
```

Left square needs:

```text
(qx - side, qy)
(qx - side, other_y)
```

So for each stored point sharing the same `x` as the query, we can try building a square.

This is clean and efficient.

---

## 5. Selected solution

Maintain:

```python
by_x[x][y] = count of point (x, y)
```

Example:

```python
by_x[3][10] = 2
```

means point `(3, 10)` was added twice.

Why this structure?

Because during query, we want to quickly find all stored points with the same `x` coordinate as the query point.

Those points can become the vertical side partner.

---

## 6. Implementation outline

```python
def count(point):  # -> int
    """
    Reframe: Use the query point as one square corner, then choose the vertical
    partner with same x-coordinate.

    State:
        by_x[x][y] stores how many times point (x, y) was added.
        Chosen because query needs to scan possible vertical partners quickly.

    Invariant:
        Every stored point count is preserved, including duplicates.

    getCount(x, y) = how many stored copies of point (x, y) exist.

    Core logic:
    - Take query point.
    - Look at every stored point with same x-coordinate.
    - Skip if it has same y-coordinate, because side length would be zero.
    - Compute square side length.
    - Try square extending right.
    - Try square extending left.
    - For each valid square, multiply counts of the three needed stored corners.
    - Add those products to answer.

    Edge cases:
    - no points added yet
    - no points with query x-coordinate
    - candidate vertical point has same y as query
    - missing one or both horizontal corners
    - duplicate points multiply answer
    - query point itself may also exist in structure, but it is not needed
    """
```

---

## 7. Iterative implementation

### Iteration 1: class skeleton

```python
from collections import defaultdict, Counter

class DetectSquares:

    def __init__(self):
        self.by_x = defaultdict(Counter)

    def add(self, point):
        pass

    def count(self, point):
        pass
```

---

### Iteration 2: implement `add`

```python
from collections import defaultdict, Counter

class DetectSquares:

    def __init__(self):
        self.by_x = defaultdict(Counter)

    def add(self, point):
        x, y = point
        self.by_x[x][y] += 1

    def count(self, point):
        pass
```

Now duplicates are naturally handled.

If we add `(3, 10)` twice:

```python
self.by_x[3][10] == 2
```

---

### Iteration 3: query happy path

```python
from collections import defaultdict, Counter

class DetectSquares:

    def __init__(self):
        self.by_x = defaultdict(Counter)

    def add(self, point):
        x, y = point
        self.by_x[x][y] += 1

    def count(self, point):
        qx, qy = point
        total = 0

        for other_y, vertical_count in self.by_x[qx].items():
            side = abs(other_y - qy)

            right_x = qx + side

            total += (
                vertical_count
                * self.by_x[right_x][qy]
                * self.by_x[right_x][other_y]
            )

        return total
```

This only checks squares to the right.

But there are two possible directions: left and right.

Also, we must skip `side == 0`.

---

### Iteration 4: add left direction and zero-side check

```python
from collections import defaultdict, Counter

class DetectSquares:

    def __init__(self):
        self.by_x = defaultdict(Counter)

    def add(self, point):
        x, y = point
        self.by_x[x][y] += 1

    def count(self, point):
        qx, qy = point
        total = 0

        for other_y, vertical_count in self.by_x[qx].items():
            side = abs(other_y - qy)

            if side == 0:
                continue

            right_x = qx + side
            left_x = qx - side

            total += (
                vertical_count
                * self.by_x[right_x][qy]
                * self.by_x[right_x][other_y]
            )

            total += (
                vertical_count
                * self.by_x[left_x][qy]
                * self.by_x[left_x][other_y]
            )

        return total
```

This works, but `defaultdict` can create empty entries during lookup.

That is acceptable in many interviews, but we can make lookup cleaner.

---

### Final cleaner version

```python
from collections import defaultdict, Counter
from typing import List

class DetectSquares:

    def __init__(self):
        self.by_x = defaultdict(Counter)

    def add(self, point: List[int]) -> None:
        x, y = point
        self.by_x[x][y] += 1

    def count(self, point: List[int]) -> int:
        qx, qy = point
        total = 0

        if qx not in self.by_x:
            return 0

        for other_y, vertical_count in self.by_x[qx].items():
            side = abs(other_y - qy)

            if side == 0:
                continue

            right_x = qx + side
            left_x = qx - side

            # Square extending right.
            total += (
                vertical_count
                * self.by_x.get(right_x, {}).get(qy, 0)
                * self.by_x.get(right_x, {}).get(other_y, 0)
            )

            # Square extending left.
            total += (
                vertical_count
                * self.by_x.get(left_x, {}).get(qy, 0)
                * self.by_x.get(left_x, {}).get(other_y, 0)
            )

        return total
```

---

## 8. Walk edge cases

### Empty structure

```python
ds = DetectSquares()
ds.count([1, 1])
```

Returns `0`.

Handled by:

```python
if qx not in self.by_x:
    return 0
```

---

### Same y-coordinate

Query:

```python
(1, 1)
```

Stored point:

```python
(1, 1)
```

Side length would be `0`, not valid.

Handled by:

```python
if side == 0:
    continue
```

---

### Missing corners

If one required corner is missing, its count is `0`.

Example:

```python
self.by_x.get(right_x, {}).get(qy, 0)
```

So product becomes `0`.

---

### Duplicates

Suppose:

```python
(3, 10) added twice
(3, 2) added once
(11, 2) added once
query = (11, 10)
```

Count:

```python
2 * 1 * 1 = 2
```

The multiplication naturally counts all separate choices.

---

## 9. Complexity

Let `k` be the number of distinct `y` values stored for the query’s `x`.

### `add`

```text
Time:  O(1)
Space: O(1) extra per unique point
```

### `count`

```text
Time:  O(k)
Space: O(1)
```

Worst case, if all points share the same `x`, then:

```text
count = O(n)
```

But this is still much better than checking triples.

Final answer: use a hash map from `x` to a counter of `y` values, then for each query scan vertical candidates and multiply corner counts.
