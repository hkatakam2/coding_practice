### question
Design a stack class that supports the `push`, `pop`, `top`, and `getMin` operations.

* `MinStack()` initializes the stack object.
* `void push(int val)` pushes the element `val` onto the stack.
* `void pop()` removes the element on the top of the stack.
* `int top()` gets the top element of the stack.
* `int getMin()` retrieves the minimum element in the stack.
Each function should run in O(1)O(1) time.

## 1. Restate

Build a stack supporting normal stack operations plus retrieving the current minimum.

All operations must take constant time:

- `push(val)`
- `pop()`
- `top()`
- `getMin()`

## 2. Clarifying questions

- Can values be negative or duplicated? Assume yes.
- What happens when operations are called on an empty stack? Assume `pop`, `top`, and `getMin` are called only when nonempty, as in the standard problem.
- Must each operation be `O(1)` worst-case? Yes.
- May we use extra space? Yes, up to `O(n)`.

## 3. Example by hand

```text
push(5)     stack: [5]          minimum: 5
push(2)     stack: [5, 2]       minimum: 2
push(2)     stack: [5, 2, 2]    minimum: 2
push(4)     stack: [5, 2, 2, 4] minimum: 2

pop()       stack: [5, 2, 2]    minimum: 2
pop()       stack: [5, 2]       minimum: 2
pop()       stack: [5]          minimum: 5
```

Important observation: after removing the minimum, we need know the previous minimum immediately.

## 4. Brainstorm solutions

### Scan for minimum

Store values normally. For `getMin`, inspect every value.

- `push`, `pop`, `top`: `O(1)`
- `getMin`: `O(n)`
- Fails requirement

This matches how we might solve it manually: inspect all remaining values whenever asked for the minimum.

### Store one minimum variable

Update it during `push`.

Problem: when the minimum is popped, we do not know the previous minimum without scanning the stack.

### Two stacks

Maintain:

- normal value stack
- minimum stack tracking the minimum at every depth

All operations: `O(1)`. Clear, but requires synchronizing two stacks.

### Store value and minimum together

Each stack entry stores:

```text
(value, minimum at this depth)
```

Then the top entry always contains both the top value and current minimum.

Selected: store `(value, minimum_so_far)` together. Local, readable, and difficult to desynchronize.

## 5. Selected solution

When pushing a value:

- if stack is empty, its minimum is itself
- otherwise, its minimum is the smaller of the new value and previous minimum
- store both together

When popping, the previous entry already remembers the previous minimum.

## 6. Plain-English implementation outline

```python
class MinStack:
    """
    Reframe: Store the minimum for every stack depth, so removing an
    element automatically restores the previous minimum.

    State: A stack of (value, minimum_at_this_depth) pairs, chosen because
    each stack state needs its own minimum.

    Invariant: The minimum stored in the top entry equals the minimum of
    every value currently in the stack.

    currentMinimum() = minimum stored with the top entry.

    Core logic:
    - initialize an empty collection of entries
    - push:
        - if this is the first value, its minimum is itself
        - otherwise, compare it with the current minimum
        - store the value together with the resulting minimum
    - pop:
        - remove the latest entry
    - top:
        - return the value from the latest entry
    - getMin:
        - return the minimum from the latest entry

    Edge cases:
    - first pushed value has no previous minimum
    - new value is smaller than the current minimum
    - new value equals the current minimum
    - duplicate minimum is popped
    - only minimum is popped, revealing an older minimum
    - negative values
    - operations requested on an empty stack
    """
```

## 7. Iterative implementation

### Iteration 1: skeleton

```python
class MinStack:

    def __init__(self):
        self.entries = []

    def push(self, val: int) -> None:
        new_minimum = determine_new_minimum(val)
        store_value_and_minimum(val, new_minimum)

    def pop(self) -> None:
        remove_latest_entry()

    def top(self) -> int:
        return value_from_latest_entry()

    def getMin(self) -> int:
        return minimum_from_latest_entry()
```

### Iteration 2: implement basic stack operations

```python
class MinStack:

    def __init__(self):
        self.entries = []

    def push(self, val: int) -> None:
        new_minimum = determine_new_minimum(val)
        self.entries.append((val, new_minimum))  # Store entry.

    def pop(self) -> None:
        self.entries.pop()  # Remove latest entry.

    def top(self) -> int:
        return self.entries[-1][0]  # Read latest value.

    def getMin(self) -> int:
        return self.entries[-1][1]  # Read latest minimum.
```

Only minimum calculation remains.

### Iteration 3: implement minimum calculation

```python
class MinStack:

    def __init__(self):
        self.entries = []

    def push(self, val: int) -> None:
        if not self.entries:
            new_minimum = val
        else:
            current_minimum = self.entries[-1][1]
            new_minimum = min(val, current_minimum)

        self.entries.append((val, new_minimum))

    def pop(self) -> None:
        self.entries.pop()

    def top(self) -> int:
        return self.entries[-1][0]

    def getMin(self) -> int:
        return self.entries[-1][1]
```

Core logic complete.

## Edge-case walkthrough

### First pushed value

```text
push(5) → stores (5, 5)
```

Handled by the empty-stack branch.

### New minimum

```text
push(5), push(2) → stores (2, 2)
```

Handled by `min`.

### Duplicate minimum

```text
push(2), push(2)
```

Both entries store minimum `2`. Popping one still leaves minimum `2`. No patch.

### Revealing an older minimum

```text
push(5), push(2), pop()
```

The remaining top entry stores minimum `5`. No patch.

### Negative values

`min` works normally with negative integers. No patch.

### Empty operations

Under the standard problem contract, `pop`, `top`, and `getMin` are only called on a nonempty stack. No patch needed.

## 8. Final implementation

```python
class MinStack:

    def __init__(self):
        self.entries = []

    def push(self, val: int) -> None:
        if not self.entries:
            minimum = val
        else:
            minimum = min(val, self.entries[-1][1])

        self.entries.append((val, minimum))

    def pop(self) -> None:
        self.entries.pop()

    def top(self) -> int:
        return self.entries[-1][0]

    def getMin(self) -> int:
        return self.entries[-1][1]
```

Complexity:

- `push`: `O(1)`
- `pop`: `O(1)`
- `top`: `O(1)`
- `getMin`: `O(1)`
- Total space: `O(n)` — one value/minimum pair per pushed element.