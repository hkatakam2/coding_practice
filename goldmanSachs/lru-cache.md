### 1. Restate Question

Design a data structure for Least Recently Used (LRU) cache. Support `get(key)` and `put(key, value)` in $O(1)$ time. When capacity is reached, evict the least recently used item.

### 2. Clarifying Questions & I/O

* **Inputs**: Capacity is positive integer. Keys/values are integers.
* **Outputs**: `get` returns value or `-1` if missing. `put` inserts or updates.
* **Constraints**: Strictly $O(1)$ average time complexity for both ops.

### 3. Example By Hand

* Capacity = 2
* `put(1, 1)` -> Cache: `[(1,1)]`
* `put(2, 2)` -> Cache: `[(2,2), (1,1)]` (Most recent first)
* `get(1)` -> returns `1`. Cache becomes: `[(1,1), (2,2)]`
* `put(3, 3)` -> Capacity exceeded. Evict least recent (`2,2`). Cache: `[(3,3), (1,1)]`
* `get(2)` -> returns `-1` (miss)

### 4. Brainstorming & Complexity

* **Approach 1**: Array/List. `get` takes $O(n)$, `put` takes $O(n)$. Too slow.
* **Approach 2**: Hash Map + Doubly Linked List (DLL). Map gives $O(1)$ lookup for keys. DLL gives $O(1)$ insertions/deletions at ends (head = MRU, tail = LRU). Both ops $O(1)$.

### 5. Suggested Solution

Hash map mapping `key -> Node` combined with a Doubly Linked List tracking access order.

### 6. Outline Implementation

```python
def lruCache(capacity):
    """
    Reframe: O(1) cache via hash map + doubly linked list.
    State: Dict(key -> Node), DLL with dummy head/tail.
    Invariant: DLL head = most recently used, tail = least recently used.

    moveToHead(node) = detach node from current pos, insert right after head.
    removeTail() = detach node right before tail, return it.

    Core logic:
    - get(key): check map. If miss return -1. Else move node to head, return val.
    - put(key, val): if key exists, update val and move to head. Else create node, add to map and head. If size > capacity, remove tail and delete from map.
    Edge cases:
    - capacity = 1
    - updating existing key value
    - inserting when capacity full
    - getting non-existent key
    """

```

### 7. Iterative Implementation

**Chunk 1: Skeleton with stubs**

```python
class Node:
    def __init__(self, key=0, val=0):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {} # key -> Node
        # Dummy head and tail to avoid edge checks on empty/full lists
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _add_node(self, node):
        # Insert right after head
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _remove_node(self, node):
        # Remove an existing node from DLL
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def _move_to_head(self, node):
        self._remove_node(node)
        self._add_node(node)

    def _pop_tail(self):
        # Pop current tail (node right before dummy tail)
        res = self.tail.prev
        self._remove_node(res)
        return res

    def get(self, key: int) -> int:
        # Core logic: hit -> move to head, miss -> return -1
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._move_to_head(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        # Core logic: update if exists, else insert. Evict if over capacity.
        if key in self.cache:
            node = self.cache[key]
            node.val = value
            self._move_to_head(node)
        else:
            new_node = Node(key, value)
            self.cache[key] = new_node
            self._add_node(new_node)
            if len(self.cache) > self.capacity:
                tail = self._pop_tail()
                del self.cache[tail.key]

```

**Edge Cases Walkthrough:**

* `capacity = 1`: Handled. Adding 2nd item triggers `_pop_tail` immediately removing the 1st.
* `Key update`: Handled in `put` via `key in self.cache` check, updates value and moves to head.
* `Cache miss`: Handled in `get` via `key not in self.cache` returning `-1`.

### 8. Complexity Analysis

* **Time Complexity**: $O(1)$ for both `get` and `put`. Hash map lookups are $O(1)$ and DLL node insertions/deletions are pointer updates taking $O(1)$.
* **Space Complexity**: $O(C)$ where $C$ is `capacity`, storing up to $C$ nodes in hash map and DLL.