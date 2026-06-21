### question
Implement an LRUCache that supports O(1) average-time get(key) returning the value or -1 and put(key, value) which inserts or updates a key and, if capacity is exceeded, evicts the least-recently-used key. The core challenge is maintaining key-value storage together with recency ordering to enable constant-time access, updates, and eviction.

### 1. Restating the Question

Design fixed-size cache. Fast lookups, fast inserts. O(1) time constraint. Evict least recently used (LRU) item when full. Reading or updating a key makes it most recently used.

### 2. Clarifying Questions & I/O

* **Input:** Capacity integer `c > 0`. Stream of `get(k)` and `put(k, v)` operations.
* **Output:** `get` returns integer `v` or `-1`. `put` returns `None`.
* **Questions:**
* Can keys/values be negative? *Yes. Return `-1` only for misses, assume valid values won't conflict with `-1` or we use a wrapper.*
* Does updating an existing key count as a use? *Yes.*
* Will capacity ever be 0? *Assume always >= 1.*



### 3. Hand-Trace Example

Capacity = 2.

1. `put(1, 10)` -> Cache holds `(1:10)`. LRU ordering: `[1]`.
2. `put(2, 20)` -> Cache holds `(1:10), (2:20)`. LRU: `[2, 1]`. (2 is newest).
3. `get(1)` -> Returns `10`. Cache: `(1:10), (2:20)`. LRU: `[1, 2]`. (1 moved to front).
4. `put(3, 30)` -> Full. Evict tail of LRU (`2`). Cache: `(1:10), (3:30)`. LRU: `[3, 1]`.
5. `get(2)` -> Returns `-1`.

### 4. Brainstorming & Complexity

* **Array + Hash Map:** Hash map for O(1) lookups. Array for LRU. O(N) to shift array when moving an accessed item to the front. Too slow.
* **Hash Map + Timestamps:** Hash map stores `(value, time)`. `get` is O(1). `put` is O(1) unless full. If full, O(N) to scan map for oldest timestamp. Too slow.
* **Hash Map + Doubly Linked List (DLL):** Map gives O(1) access to nodes. DLL gives O(1) removal and O(1) insertion at the head. Most recent = head, least recent = tail.

### 5. Suggested Solutions

1. **Array/List simulation** (as traced by hand above). Easy to read, but O(N) operations.
2. **Hash Map + Doubly Linked List**. Optimal approach. Meets O(1) requirement. Prefer this.

### 6. Outline of Selected Implementation

```python
class LRUCache:
    """
    Reframe: Cache is a dictionary for fast lookups linked to a queue for fast ordering.
    State: Hash Map (key -> Node), Doubly Linked List (head, tail pointers), chosen because
           Map gives O(1) access, DLL gives O(1) node relocation.
    Invariant: Map keys exactly match DLL nodes. Head is newest, tail is oldest.

    remove_node(node) = Unlinks node from its current DLL neighbors.
    add_to_head(node) = Inserts node right after the dummy head.
    move_to_head(node) = Calls remove_node then add_to_head.
    evict_tail() = Removes the node right before the dummy tail and deletes from map.

    Core logic (Happy Path):
    get(key):
    - lookup node in map
    - move node to head of DLL
    - return node value

    put(key, value):
    - create new node
    - add to map
    - add to head of DLL
    - if map size exceeds capacity, evict tail

    Edge cases:
    - get: key doesn't exist.
    - put: key already exists (update value instead of inserting, move to head).
    """

```

### 7. Iterative Implementation

**Iteration 1: Skeleton with helper stubs.**
Setting up the structure. Humans think in verbs first.

```python
class Node:
    def __init__(self, key, val):
        self.key, self.val = key, val
        self.prev = self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        # dummy nodes to avoid null checks
        self.head, self.tail = Node(0, 0), Node(0, 0)
        self.head.next, self.tail.prev = self.tail, self.head

    def _remove(self, node): pass
    def _add(self, node): pass
    
    def get(self, key: int) -> int:
        node = self.cache[key]
        self._remove(node)
        self._add(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        node = Node(key, value)
        self.cache[key] = node
        self._add(node)
        self._remove(self.tail.prev) # dummy evict

```

**Iteration 2: Fleshing out helpers.**
Implementing the plain English DLL operations.

```python
# ... [Node and __init__ unchanged]

    def _remove(self, node):
        # isolate node, connect neighbors to each other
        prev_node, next_node = node.prev, node.next
        prev_node.next, next_node.prev = next_node, prev_node

    def _add(self, node):
        # insert right after head
        next_node = self.head.next
        self.head.next = node
        node.prev = self.head
        node.next = next_node
        next_node.prev = node
        
    def get(self, key: int) -> int:
        node = self.cache[key]
        self._remove(node)
        self._add(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        node = Node(key, value)
        self.cache[key] = node
        self._add(node)
        
        # basic capacity check
        if len(self.cache) > self.capacity:
            lru = self.tail.prev
            self._remove(lru)
            del self.cache[lru.key]

```

**Iteration 3: Patching edge cases.**
Core logic is done. Now address: `get` miss, `put` existing key.

```python
class Node:
    def __init__(self, key, val):
        self.key, self.val = key, val
        self.prev = self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        self.head, self.tail = Node(0, 0), Node(0, 0)
        self.head.next, self.tail.prev = self.tail, self.head

    def _remove(self, node):
        p, n = node.prev, node.next
        p.next, n.prev = n, p

    def _add(self, node):
        n = self.head.next
        self.head.next, node.prev = node, self.head
        node.next, n.prev = n, node

    def get(self, key: int) -> int:
        # Edge case: key not found
        if key not in self.cache:
            return -1
        
        node = self.cache[key]
        self._remove(node)
        self._add(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        # Edge case: key already exists
        if key in self.cache:
            self._remove(self.cache[key])
            
        node = Node(key, value)
        self.cache[key] = node
        self._add(node)

        # Capacity edge case handled gracefully now
        if len(self.cache) > self.capacity:
            lru = self.tail.prev
            self._remove(lru)
            del self.cache[lru.key]

```

### 8. Complexity & Optimization

* **Time Complexity:** O(1) for `get` and `put`. Dictionary lookups are O(1) average. Pointer reassignment in DLL is strict O(1).
* **Space Complexity:** O(C) where C is capacity. We store at most C nodes and C keys in the map.
* **Optimization/Real-world note:** In Python, standard library `collections.OrderedDict` implements this exact Hash Map + DLL structure under the hood in C. In a production environment, `OrderedDict.move_to_end()` and `OrderedDict.popitem(last=False)` would be used for a much shorter, faster implementation, but demonstrating the manual pointer manipulation is the point of the interview.