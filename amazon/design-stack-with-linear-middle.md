### question
Designing a stack that supports push, pop, get middle, get top in O(1) time.


### 1. Question Restatement

Design a custom Stack class supporting four operations in $O(1)$ time and space per call:

* `push(val)`: Add element to top of stack.
* `pop()`: Remove and return top element.
* `get_top()`: Read top element without removing.
* `get_middle()`: Read middle element without removing.

---

### 2. Clarifying Questions & Input/Output Confirmation

1. **Middle definition for even count:** If stack size is $N=4$ (elements `1 -> 2 -> 3 -> 4`), which is middle?
* *Assumption:* Lower middle $\lfloor (N+1)/2 \rfloor$ or upper middle $\lceil N/2 \rceil$. We'll use upper middle index $\lfloor N/2 \rfloor$ (0-indexed position $N // 2$).


2. **Empty stack behavior:** What should `pop()`, `get_top()`, or `get_middle()` return on empty stack?
* *Assumption:* Return `None` (or raise `IndexError`).


3. **Data types:** Standard integers/generic objects.

---

### 3. Trace Example by Hand

Operations sequence on initially empty stack:

| Operation | Stack State (Bottom $\to$ Top) | Size $N$ | Mid Index ($\lfloor N/2 \rfloor$) | Top | Mid |
| --- | --- | --- | --- | --- | --- |
| `push(10)` | `[10]` | 1 | 0 (`10`) | 10 | 10 |
| `push(20)` | `[10, 20]` | 2 | 1 (`20`) | 20 | 20 |
| `push(30)` | `[10, 20, 30]` | 3 | 1 (`20`) | 30 | 20 |
| `push(40)` | `[10, 20, 30, 40]` | 4 | 2 (`30`) | 40 | 30 |
| `pop()` | `[10, 20, 30]` | 3 | 1 (`20`) | 30 | 20 |
| `get_middle()` | `[10, 20, 30]` | 3 | 1 (`20`) | 30 | **20** |

---

### 4. Brainstorming & Complexity

* **Approach A: Dynamic Array / Python List**
* `push`, `pop`, `get_top` $\to O(1)$
* `get_middle` via `arr[len // 2]` $\to O(1)$
* *Limitation:* Simple and fast for reading, but if future requirements demand `delete_middle()`, dynamic arrays require $O(N)$ shifting.


* **Approach B: Doubly Linked List (DLL) + Mid Pointer**
* Node pointers: `prev`, `next`, `val`.
* Track `head` (bottom), `tail` (top), `mid` (middle node), and `count`.
* On `push`: attach to `tail`. Move `mid` right if size condition met. $\to O(1)$
* On `pop`: detach from `tail`. Move `mid` left if size condition met. $\to O(1)$
* *Advantage:* Handles all $O(1)$ requirements natively and extends to $O(1)$ middle deletion easily.



---

### 5. Suggested Solution

We choose **Approach B (Doubly Linked List with Mid Pointer)** for strict pointers-based structural guarantees.

---

### 6. Implementation Outline

```python
def fn(args):  # -> returnType
    """
    Reframe: Maintain a doubly linked list with top (tail) and middle pointers, shifting middle pointer by at most 1 step per operation.
    State: double-linked nodes, head, tail, mid pointers, integer size. Chosen because DLL allows O(1) tail mutation and O(1) mid node step updates.
    Invariant: mid points to node at index (size // 2) from head.

    update_mid_on_push(stack) = advance mid to mid.next when size changes from odd to even.
    update_mid_on_pop(stack) = retreat mid to mid.prev when size changes from even to odd.

    Core logic:
    - append node to tail
    - increment size
    - adjust mid pointer using dummy helper logic
    - return val from tail/mid directly
    Edge cases:
    - empty stack operations (pop/get_top/get_middle when size == 0)
    - single node stack (size == 1 -> head == tail == mid)
    - size transitions between 0, 1, and 2
    """

```

---

### 7. Iterative Implementation

#### Step 7a: Skeleton & Stubs (Happy Path Logic)

```python
class Node:
    def __init__(self, val):
        self.val = val
        self.prev = None
        self.next = None

class MidStack:
    def __init__(self):
        self.head = None
        self.tail = None
        self.mid = None
        self.size = 0

    def push(self, val):
        # TODO: attach node to tail
        # TODO: update mid pointer on push
        pass

    def pop(self):
        # TODO: remove node from tail
        # TODO: update mid pointer on pop
        pass

    def get_top(self):
        # TODO: return tail value
        pass

    def get_middle(self):
        # TODO: return mid value
        pass

```

#### Step 7b: Iteration 1 — Basic Stack Operations (Push/Pop without Mid logic)

```python
class MidStack:
    def __init__(self):
        self.head = None
        self.tail = None
        self.mid = None
        self.size = 0

    def push(self, val):
        new_node = Node(val)
        if self.size == 0:
            self.head = new_node
            self.tail = new_node
            self.mid = new_node
        else:
            # Attach to tail
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        self.size += 1

    def pop(self):
        val = self.tail.val
        self.tail = self.tail.prev
        if self.tail:
            self.tail.next = None
        self.size -= 1
        return val

    def get_top(self):
        return self.tail.val

    def get_middle(self):
        return self.mid.val

```

#### Step 7c: Iteration 2 — Adding Mid Pointer Shifts (Core Logic Complete)

```python
class MidStack:
    def __init__(self):
        self.head = None
        self.tail = None
        self.mid = None
        self.size = 0

    def push(self, val):
        new_node = Node(val)
        if self.size == 0:
            self.head = new_node
            self.tail = new_node
            self.mid = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
            
            # Mid shift logic: when size was odd before increment, new size is even -> advance mid
            if self.size % 2 == 1:
                self.mid = self.mid.next # Modified: shift mid right on odd->even
                
        self.size += 1

    def pop(self):
        val = self.tail.val
        self.tail = self.tail.prev
        if self.tail:
            self.tail.next = None
            
        # Mid shift logic: when size was even before decrement, new size is odd -> retreat mid
        if self.size % 2 == 0:
            self.mid = self.mid.prev # Modified: shift mid left on even->odd
            
        self.size -= 1
        return val

    def get_top(self):
        return self.tail.val

    def get_middle(self):
        return self.mid.val

```

#### Step 7d: Iteration 3 — Edge Case Patching (Empty Stack & Cleanup)

```python
class Node:
    def __init__(self, val):
        self.val = val
        self.prev = None
        self.next = None

class MidStack:
    def __init__(self):
        self.head = None
        self.tail = None
        self.mid = None
        self.size = 0

    def push(self, val: int) -> None:
        new_node = Node(val)
        if self.size == 0:
            self.head = new_node
            self.tail = new_node
            self.mid = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
            
            # If size was odd, adding 1 makes it even -> mid shifts right
            if self.size % 2 == 1:
                self.mid = self.mid.next
                
        self.size += 1

    def pop(self) -> int | None:
        # Edge Case 1: Empty stack
        if self.size == 0:
            return None
            
        val = self.tail.val
        
        # Edge Case 2: Single element left
        if self.size == 1:
            self.head = None
            self.tail = None
            self.mid = None
        else:
            self.tail = self.tail.prev
            self.tail.next = None
            # If size was even, removing 1 makes it odd -> mid shifts left
            if self.size % 2 == 0:
                self.mid = self.mid.prev
                
        self.size -= 1
        return val

    def get_top(self) -> int | None:
        # Edge Case: Empty stack
        if self.size == 0:
            return None
        return self.tail.val

    def get_middle(self) -> int | None:
        # Edge Case: Empty stack
        if self.size == 0:
            return None
        return self.mid.val

```

---

### 8. Complexity & Optimization Analysis

| Operation | Time Complexity | Space Complexity |
| --- | --- | --- |
| `push(val)` | $O(1)$ | $O(1)$ auxiliary |
| `pop()` | $O(1)$ | $O(1)$ auxiliary |
| `get_top()` | $O(1)$ | $O(1)$ auxiliary |
| `get_middle()` | $O(1)$ | $O(1)$ auxiliary |

* **Total Space Complexity:** $O(N)$ where $N$ is total number of nodes in stack.
* **Optimization Note:** Pointer adjustments in `push` and `pop` run in exact constant steps without loops. No further asymptotic optimization possible.