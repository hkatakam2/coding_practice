"""
The Architecture
We need two main data structures to wire this together for $O(1)$ access:
key_map (Dictionary):
Input: keyOutput: Node (holds value, frequency, and pointers)
Purpose: Instant access to data for get and put.

freq_map (Dictionary of Lists):
Input: frequency (integer)
Output: DoublyLinkedListPurpose: To organize items by frequency. The list maintains the LRU order for that specific frequency count.

min_freq (Integer Variable):
Purpose: A simple pointer to the smallest frequency currently in the system. This tells us exactly which bucket to look at when we need to kick someone out.
"""

import collections


class Node:
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.freq = 1
        self.prev = None
        self.next = None


class DoublyLinkedList:
    def __init__(self):
        self.head = Node(0, 0)
        self.tail = Node(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head
        self._size = 0

    def __len__(self):
        return self._size

    def append(self, node):
        # Add to head (Most Recently Used)
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node
        self._size += 1

    def pop(self, node=None):
        if self._size == 0:
            return None
        if not node:
            node = self.tail.prev  # Default to tail (LRU)

        node.prev.next = node.next
        node.next.prev = node.prev
        self._size -= 1
        return node


class LFUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.size = 0
        self.min_freq = 0
        self.key_map = {}
        self.freq_map = collections.defaultdict(DoublyLinkedList)

    def _update(self, node):
        cur_freq = node.freq
        self.freq_map[cur_freq].pop(node)

        if self.min_freq == cur_freq and not self.freq_map[cur_freq]:
            self.min_freq += 1

        node.freq += 1
        self.freq_map[node.freq].append(node)

    def get(self, key: int) -> int:
        if key not in self.key_map:
            return -1
        node = self.key_map[key]
        self._update(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        if self.cap == 0:
            return

        if key in self.key_map:
            node = self.key_map[key]
            node.val = value
            self._update(node)
            return

        if self.size == self.cap:
            evicted = self.freq_map[self.min_freq].pop()
            del self.key_map[evicted.key]
            self.size -= 1

        new_node = Node(key, value)
        self.key_map[key] = new_node
        self.freq_map[1].append(new_node)
        self.min_freq = 1
        self.size += 1
