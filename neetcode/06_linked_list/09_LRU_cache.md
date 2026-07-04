### question
Implement the Least Recently Used (LRU) cache class LRUCache. The class should support the following operations

LRUCache(int capacity) Initialize the LRU cache of size capacity.
int get(int key) Return the value corresponding to the key if the key exists, otherwise return -1.
void put(int key, int value) Update the value of the key if the key exists. Otherwise, add the key-value pair to the cache. If the introduction of the new pair causes the cache to exceed its capacity, remove the least recently used key.
A key is considered used if a get or a put operation is called on it.

Ensure that get and put each run in 
O
(
1
)
O(1) average time complexity.

### 1. Restating the Question

Design a data structure with fixed `capacity`.
Stores integer key-value pairs.
`get(key)` returns value or `-1` if missing. Marks key as most recently used.
`put(key, value)` inserts or updates. Marks key as most recently used. Evicts least recently used key if capacity exceeded.
Constraint: Both `get` and `put` must run in $O(1)$ time.

### 2. Clarifying Questions

* **Capacity always $> 0$?** Assume yes.
* **Keys/Values only integers?** Assume yes.
* **Thread safety required?** Assume no.

### 3. Manual Walkthrough (Input -> Output)

Capacity: 2

1. `put(1, 1)` -> Cache state: `[1:1]` (1 is MRU)
2. `put(2, 2)` -> Cache state: `[2:2, 1:1]` (2 is MRU, 1 is LRU)
3. `get(1)`    -> Returns `1`. Cache state: `[1:1, 2:2]` (1 moved to MRU)
4. `put(3, 3)` -> Evicts `2`. Cache state: `[3:3, 1:1]`
5. `get(2)`    -> Returns `-1`.
6. `put(4, 4)` -> Evicts `1`. Cache state: `[4:4, 3:3]`
7. `get(1)`    -> Returns `-1`.
8. `get(3)`    -> Returns `3`. Cache state: `[3:3, 4:4]`
9. `get(4)`    -> Returns `4`. Cache state: `[4:4, 3:3]`

### 4. Brainstorming Solutions & Complexity

* **Array/List:** Append on use, pop front on eviction. `put`/`get` $O(n)$ because finding/shifting elements takes linear time.
* **Hash Map + Queue:** Map gives $O(1)$ lookup. But moving an accessed item from the middle of the queue to the front is $O(n)$.
* **Hash Map + Doubly Linked List (DLL):** Map stores `key -> Node`. Map gives $O(1)$ lookup. DLL maintains order. Given a Node from the map, removing it from DLL is $O(1)$. Inserting at DLL head is $O(1)$.
* *Time:* $O(1)$
* *Space:* $O(N)$ where $N$ is capacity.



### 5. Suggested Solution

Hash Map + Doubly Linked List. It directly satisfies the $O(1)$ time constraints. Simple to explain: map handles access, DLL handles ordering. Dummy head and dummy tail nodes prevent null-pointer checks during node manipulation.

### 6. Outline Implementation

```python
class LRUCache:
    """
    Reframe: Need O(1) key lookup AND O(1) order manipulation.
    State: Hash map (key->Node) and Doubly Linked List, chosen because map provides O(1) access and DLL provides O(1) removal/insertion anywhere.
    Invariant: Head of DLL is most recent, tail is least recent. Map size == DLL size <= capacity.

    remove_node(node) = cuts node out of its current DLL position.
    add_to_head(node) = inserts node right after the DLL dummy head.
    move_to_head(node) = remove_node(node) + add_to_head(node).
    pop_tail() = removes and returns the node right before the dummy tail.

    Core logic:
    - On GET: find node in map. if found, move_to_head(node), return value. else return -1.
    - On PUT: if key exists, update value and move_to_head(node).
    - if key new, create node, add to map, add_to_head(node).
    - check capacity limit. if exceeded, pop_tail() from DLL, delete its key from map.
    
    Edge cases:
    - updating an existing key in PUT should not increase cache size.
    - capacity is 1 (dummy nodes handle adjacent pointers safely).
    """

```

### 7. Iterative Implementation

**Iteration 1: Skeleton and Stubs**
Setting up the classes and placeholders.

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
        self.cache = {} # Map key -> Node
        # Dummy nodes for clean insertions/deletions
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    # TODO: Helper remove_node
    # TODO: Helper add_to_head

    def get(self, key: int) -> int:
        pass # TODO: fetch, move to head

    def put(self, key: int, value: int) -> None:
        pass # TODO: insert/update, check capacity

```

**Iteration 2: Implementing Helpers**
Wiring up the DLL operations first. Dummy nodes make this clean.

```python
    # ... previous init ...

    def _remove_node(self, node):
        # Disconnect node from DLL
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def _add_to_head(self, node):
        # Insert node right after dummy head
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node
        
    def _move_to_head(self, node):
        self._remove_node(node)
        self._add_to_head(node)

```

**Iteration 3: Core Logic (Happy Path)**
Assume keys don't exist on put, no capacity breach yet.

```python
    def get(self, key: int) -> int:
        if key in self.cache:
            node = self.cache[key]
            self._move_to_head(node) # Mark MRU
            return node.val
        return -1

    def put(self, key: int, value: int) -> None:
        # Happy path: just add new node
        new_node = Node(key, value)
        self.cache[key] = new_node
        self._add_to_head(new_node)

```

**Iteration 4: Edge Cases (Existing keys & Eviction)**
Patching `put` to handle existing keys (update instead of duplicate) and capacity limits.

```python
    def _pop_tail(self):
        # Helper to remove LRU item
        res = self.tail.prev
        self._remove_node(res)
        return res

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            # EDGE CASE 1: Key exists. Update value and move to MRU.
            node = self.cache[key]
            node.val = value
            self._move_to_head(node)
        else:
            # Key is new. Insert.
            new_node = Node(key, value)
            self.cache[key] = new_node
            self._add_to_head(new_node)
            
            # EDGE CASE 2: Capacity exceeded. Evict LRU.
            if len(self.cache) > self.capacity:
                tail = self._pop_tail()
                del self.cache[tail.key] # Delete from map using node's key

```

### 8. Complexity & Optimizations

* **Time Complexity:** * `get`: $O(1)$. Hash map lookup is $O(1)$, DLL pointer swap is $O(1)$.
* `put`: $O(1)$. Hash map insertion/deletion is $O(1)$, DLL pointer swap is $O(1)$.


* **Space Complexity:** $O(N)$ where $N$ is `capacity`. The hash map and DLL both store at most $N$ elements.
* **Optimizations:** The standard Map + DLL is theoretically optimal for time complexity. In Python, `collections.OrderedDict` provides this exact functionality natively in highly optimized C code, but manually implementing the DLL proves understanding of pointer manipulation and the mechanics behind $O(1)$ state management.