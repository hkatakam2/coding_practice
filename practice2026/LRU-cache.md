# LRU Cache

# clarifying
1. get, put methods
2. O(1) average complexity
3. cache miss returns -1
4. capacity is decided at initialization

# ideas
1. list of (key, value, updated_time) -> too slow
2. hash map, access O(1) but no order
3. ordered list easy to add at the front and delete at the back; but search is O(n)
4. combine: hashmap for O(1) access, doubly linked list for quick insertions, deletions

# outline
```markdown
LRUCache(capacity):
    map = {} #key -> node
    list = head <-> tail

get(key):
    if not key: return -1
    node = map[key]
    moveToFront(node)
    return node.value

put(key, value):
    if key in map:
        node = map[key]
        node.value = value
        moveToFront(node)
    else:
        if cache is full: evictLRU()
        node = New Node(key, value)
        map[key] = node
        addToFront(node)
```


# implementation

```python
class Node:
    def __init__(self, key=0, value=0):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity=0):
        self.capacity = capacity # capacity < 0 raise error
        self.map = {}

        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def get(self, key):
        if key not in self.map:
            return -1

        node = self.map[key]
        self._moveToFront(node)
        return node.value

    def put(self, key, value):
        # edge case: capacity 0 return 
        if key in self.map:
            node = self.map[key]
            node.value = value
            self._moveToFront(node)
        else:
            if len(self.map) == len(self.capacity):
                self._evictLRU()
            node = Node(key, value)
            self.map[key] = node
            self._addToFront(node)


    def _moveToFront(self, node):
        self._unlink(node)
        self._addToFront(node)

    def _evictLRU():
        node = self.tail.prev
        self._unlink(node)
        del self.map[node.key]

    def _addToFront(self, node):
        node.prev = self.head
        node.next = self.head.next

        self.head.next = node
        self.head.next.prev = node

    def _unlink(self, node):
        next_node = node.next
        prev_node = node.prev

        prev_node.next = next_node
        next_node.prev = prev_node

``` 