"""
core problem:
    1. get(key), put(key, value) needs to be O(1)
    2. if cache reaches capacity; evict using LRU
"""


class Node:
    def __init__(self, key=0, value=0):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    def __init__(self, capacity: int):
        self.cache = {}  # Map: key -> value
        self.capacity = capacity

        # Dummy head, tail to avoid edge cases
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    # --- helper functions ---
    def _add_node(self, node: Node):
        """always add the new node right after head(MRU position)"""
        node.prev = self.head
        node.next = self.head.next

        self.head.next.prev = node
        self.head.next = node

    def _remove_node(self, node: Node):
        """remove an existing node from the linked list"""
        prev_node, next_node = node.prev, node.next

        prev_node.next, next_node.prev = next_node, prev_node

    def _move_to_head(self, node: Node):
        """used when an item is accessed or updated"""
        self._remove_node(node)
        self._add_node(node)

    def _pop_tail(self) -> Node:
        """pop the actual LRU item, which is just before the dummy tail"""
        lru_node = self.tail.prev
        self._remove_node(lru_node)
        return lru_node

    # --- Main Interface ---
    def get(self, key: int) -> int:
        node = self.cache[key]
        if not node:
            return -1

        # Mark as recently used
        self._move_to_head(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        node = self.cache[key]
        if node:
            # update the value and mark as recently used
            node.value = value
            self._move_to_head(node)
        else:
            # create a new node
            new_node = Node(key, value)
            self.cache[key] = new_node
            self._add_node(new_node)

            # check if we exceed capacity
            if len(self.cache) > self.capacity:
                lru_node = self._pop_tail()
                del self.cache[lru_node.key]


"""
Time: O(1) for both get, put
Space: O(n); n -> capacity of the cache
"""
