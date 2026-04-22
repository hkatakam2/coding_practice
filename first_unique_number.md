Here is a breakdown of how to approach **Leetcode 1429: First Unique Number** as if we were walking through it together in a Staff-level interview context (like the Uber one on your screen). 

We will break this down into four phases: Understanding the constraints, exploring tradeoffs, designing the system, and writing the code.

### 1. Deeply Understanding the Problem
Whenever a problem asks you to track a "stream" of data and return the "first" or "most recent" of something, you are immediately dealing with two conflicting requirements:
* **Requirement 1: Frequency Tracking.** We need to know exactly how many times we've seen a number. This screams for a Hash Map.
* **Requirement 2: Order Preservation.** We need to know which unique number arrived *first*. Hash Maps inherently lose insertion order (unless using specific language implementations like Python's dict or Java's `LinkedHashMap`).

The core challenge is answering `showFirstUnique()` efficiently as the stream grows indefinitely.

---

### 2. Brainstorming Options & Weighing Tradeoffs

In an interview, you should verbally walk your interviewer through your thought process, starting from the naive approach to the optimal one.

**Option A: The Brute Force (Array + Hash Map)**
* **How it works:** Append every number to a list. Keep a Hash Map of `number -> frequency`. 
* **When asked for the first unique:** Iterate through the list from index 0. Check the map. The first number with a frequency of `1` is your answer.
* **Tradeoffs:** `add()` is fast (`O(1)`). But `showFirstUnique()` is `O(N)`. If the interviewer calls `showFirstUnique()` 10,000 times in a row, the system will crawl. 

**Option B: The "LRU Cache" Style (Doubly Linked List + Hash Map)**
* **How it works:** You maintain a Doubly Linked List (DLL) of *only* the unique numbers. The Hash Map stores pointers to the DLL nodes. 
* **When a new number arrives:** Add it to the map and the tail of the DLL.
* **When a duplicate arrives:** Use the map to find the node in the DLL in `O(1)` time, snip it out of the DLL, and update the map to mark it as a "duplicate."
* **Tradeoffs:** `showFirstUnique()` is strictly `O(1)` (just peek the head of the DLL). `add()` is strictly `O(1)`. However, writing a bug-free DLL with pointer manipulation under 45 minutes of interview pressure is incredibly risky.

**Option C: The "Lazy Evaluation" Approach (Queue + Hash Map)**
* **How it works:** We use a standard Queue to track order and a Hash Map to track frequency. We push everything into the Queue. We don't worry about removing duplicates from the middle of the Queue. Instead, we wait until a duplicate bubbles up to the *front* of the Queue during a `showFirstUnique()` call, and we toss it out then.
* **Tradeoffs:** `add()` is `O(1)`. `showFirstUnique()` is *amortized* `O(1)`. While a single call might take `O(N)` if there are suddenly 1,000 duplicates at the front of the queue, each element is enqueued and dequeued at most once. It is much simpler to implement than a DLL and perfectly valid for production.

**The Verdict:** Option C (Queue + Hash Map) is usually the "sweet spot" for this interview. It shows you understand amortized complexity and prioritizes writing clean, bug-free code.

---

### 3. Step-by-Step System Design (Option C)

Let's define how the components talk to each other:

1.  **The State:**
    * `queue`: A standard FIFO queue storing the incoming numbers.
    * `counts`: A hash map storing `number -> frequency`.
2.  **The `add(value)` component:**
    * Increment the `value`'s frequency in the `counts` map.
    * Add the `value` to the back of the `queue`.
3.  **The `showFirstUnique()` component (The "Lazy" logic):**
    * Look at the front of the `queue`.
    * Check its frequency in `counts`. 
    * If the frequency is > 1, it's no longer unique! **Pop it off the queue and throw it away.**
    * Keep doing this until the front of the queue has a frequency of exactly 1, or the queue is empty.
    * Return the front element (or -1 if empty).

---

### 4. Implementation

Here is how that translates cleanly into Python:

```python
from collections import deque

class FirstUnique:

    def __init__(self, nums: list[int]):
        # Initialize our components
        self.queue = deque()
        self.counts = {}
        
        # Process the initial batch of numbers
        for num in nums:
            self.add(num)

    def showFirstUnique(self) -> int:
        # Lazy evaluation: clean up duplicates at the front of the queue
        while self.queue:
            front = self.queue[0]
            if self.counts[front] > 1:
                # It's a duplicate, we don't care about it anymore
                self.queue.popleft()
            else:
                # We found our first unique!
                return front
                
        # Queue is empty, no unique numbers exist
        return -1

    def add(self, value: int) -> None:
        # Update frequency
        self.counts[value] = self.counts.get(value, 0) + 1
        # Always append to the queue
        self.queue.append(value)

```

### Complexity Wrap-Up
* **Space Complexity:** `O(N)` where N is the number of unique elements stored in the Hash Map and Queue.
* **Time Complexity:** * `add()`: `O(1)`
    * `showFirstUnique()`: Amortized `O(1)`. Even though there is a `while` loop, every element is added to the queue exactly once and removed exactly once. Over the lifetime of the application, the work done in the `while` loop averages out to a constant time operation per call.

Would you like to explore how to implement the stricter `O(1)` Doubly Linked List approach, or would you rather discuss how to test edge cases for this queue-based solution?

### The Real-World Application: Why build this?

This pattern—combining a Hash Map for lookup with a Linked List for ordering—is a foundational backend system architecture. You are effectively building a specialized variant of an **LRU (Least Recently Used) Cache**. 

You see this exact system constraint frequently in high-throughput data ingestion and **algorithmic trading**. 

Imagine you are building the order execution engine for a trading platform. You have a massive stream of incoming limit orders. 
* **The Queue:** Orders must be executed in a strict First-In-First-Out (FIFO) manner based on the time they arrived. The exchange always needs to know the absolute oldest active order to match it against incoming trades.
* **The Map:** However, traders frequently cancel or modify their orders. When a cancellation comes in, you cannot afford an $O(N)$ scan through a million-order queue to find it. You must find it instantly and snip it out of the middle of the line in $O(1)$ time, leaving the rest of the queue perfectly intact. 

This requires the exact "eager evaluation" that a Doubly Linked List + Hash Map provides.

---

### Designing the DLL Approach from First Principles

Let's break down the logic step-by-step, just as you would on the whiteboard.

**1. Why a *Doubly* Linked List?**
If we use an Array, deleting an element from the middle requires shifting everything behind it (an $O(N)$ operation). If we use a Singly Linked List, we can't easily delete a node because we don't have a pointer to the node *before* it to bridge the gap. A Doubly Linked List (DLL) gives us a `prev` pointer, making mid-list deletion a true $O(1)$ operation.

**2. The State Definitions**
We need to track three states for any number in our stream:
* **State 1: Never Seen.** Not in our map at all.
* **State 2: Unique (Seen Once).** It exists in our map, and the map points directly to its active `Node` in the DLL.
* **State 3: Duplicate (Dead).** We've seen it multiple times. We remove it from the DLL, and update the map to point to a "dead" flag (like `None`). We keep it in the map so we know never to add it back.

**3. The "Dummy" Nodes Trick**
Handling edge cases (like deleting the very first or very last node) in an interview is a recipe for `NullPointerExceptions`. The professional trick is to initialize your DLL with two dummy nodes: a `head` and a `tail`.
* `head.next` always points to the first real number.
* `tail.prev` always points to the last real number.
* Now, every real node is guaranteed to be sandwiched between two other nodes. You never have to check if `node.prev` or `node.next` is null.

---

### The Code Implementation

Here is how the logic translates into clean, interview-ready code:

```python
class Node:
    def __init__(self, val=0):
        self.val = val
        self.prev = None
        self.next = None

class FirstUnique:
    def __init__(self, nums: list[int]):
        # The Map: maps integer -> Node (if unique) OR None (if duplicate)
        self.map = {} 
        
        # The DLL: Setup dummy head and tail
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head
        
        # Process initial stream
        for num in nums:
            self.add(num)

    def _remove(self, node: Node):
        # First principle of DLL removal: bridge the gap over the target node
        prev_node = node.prev
        next_node = node.next
        
        prev_node.next = next_node
        next_node.prev = prev_node

    def add(self, value: int) -> None:
        if value not in self.map:
            # STATE 1: Never seen. Create a node, add to map, and insert at the end of DLL
            new_node = Node(value)
            self.map[value] = new_node
            
            # Insert right before the dummy tail
            last_real_node = self.tail.prev
            last_real_node.next = new_node
            new_node.prev = last_real_node
            new_node.next = self.tail
            self.tail.prev = new_node
            
        elif self.map[value] is not None:
            # STATE 2: Seen exactly once. It's in the DLL. 
            # We must snip it out and mark it as dead in the map.
            node_to_remove = self.map[value]
            self._remove(node_to_remove)
            self.map[value] = None 
            
        # STATE 3: If value is in map but is None, it's a 3rd+ occurrence.
        # We do absolutely nothing. It's already dead.

    def showFirstUnique(self) -> int:
        # If the head is pointing directly to the tail, the list is empty
        if self.head.next == self.tail:
            return -1
        
        # Otherwise, the very first real node is our first unique
        return self.head.next.val
```

### The Tradeoff Summary for the Interviewer
By taking this approach, we've traded a bit of memory overhead (extra pointers for `prev`/`next` on every node) and code complexity for absolute strict performance. Both `add()` and `showFirstUnique()` are strictly bounded to $O(1)$ time, making this system incredibly predictable under high, volatile loads.

Mastering the HashMap + Doubly Linked List (DLL) combination is the ultimate "80/20" leverage point for coding interviews. Once you understand the first principles behind it—using a HashMap for $O(1)$ lookups and a DLL for $O(1)$ structural modifications (like moving an element to the front or removing it entirely)—you unlock a whole class of notoriously difficult Big Tech interview questions.

Here are the most common questions that rely heavily on this exact pattern, prioritized by how often they show up in Staff-level and backend engineering loops.

### 1. The Blueprint: [LeetCode 146. LRU Cache](https://leetcode.com/problems/lru-cache/)
* **Who asks it:** Meta, Amazon, Microsoft, Google (This is arguably the most asked interview question of all time).
* **The Concept:** This is the foundational problem. You are asked to implement `get` and `put` operations in $O(1)$ time, evicting the least recently used item when capacity is reached. 
* **How the pattern applies:** The HashMap stores `Key -> DLL Node`. The DLL strictly enforces recency. Every time a node is touched via `get` or `put`, you snip it out of the DLL and move it to the `head` (most recent). When capacity is hit, you pop the `tail` (least recent) and remove it from the map.

### 2. The Step-Up: [LeetCode 460. LFU Cache](https://leetcode.com/problems/lfu-cache/)
* **Who asks it:** Amazon, Google, LinkedIn.
* **The Concept:** Least *Frequently* Used cache. Instead of just tracking recency, you must track how often an item is accessed. If there is a tie in frequency, you evict the least *recently* used among the tie.
* **How the pattern applies:** This requires a **2D application** of the pattern. You need:
  1. A HashMap mapping `Key -> Node` (just like LRU).
  2. A second HashMap mapping `Frequency -> DLL`. 
  Whenever an item is accessed, its frequency increases. You look up its current frequency DLL, remove the node, and append it to the `Frequency + 1` DLL. It perfectly isolates the logic so everything remains $O(1)$.

### 3. The Analytics Tracker: [LeetCode 432. All O`one Data Structure](https://leetcode.com/problems/all-oone-data-structure/)
* **Who asks it:** Uber, LinkedIn, Pinterest.
* **The Concept:** You are given a stream of strings and asked to increment/decrement their counts. You must be able to return the string with the **Maximum** count and the **Minimum** count in strictly $O(1)$ time. 
* **How the pattern applies:** You cannot use a Heap here because Heaps are $O(\log N)$ for extraction/updates. Instead, you build a DLL where *each node represents a frequency* (e.g., Node 1 holds all strings seen once, Node 5 holds all strings seen 5 times). The DLL is kept sorted.
  * A HashMap maps `String -> DLL Node`.
  * When a string is incremented, you move it from its current Node to the `next` Node. The `head` of the DLL always gives you the minimum frequency strings, and the `tail` gives you the maximum frequency strings.

### 4. The Real-World Variant: Priority / Expiration LRU Cache
* **Who asks it:** Tesla, LinkedIn, British Petroleum.
* **The Concept:** This is a hybrid problem often given in machine rounds or systems-heavy loops. You implement an LRU cache, but entries also have a Time-To-Live (TTL) expiration or a Priority score.
* **How the pattern applies:** You still use the core HashMap + DLL. However, you might augment it with a secondary structure (like a Min-Heap or a background thread) to handle the time-based expirations lazily. When `get()` is called, you first check if the node has expired; if it has, you use the DLL's $O(1)$ removal to cleanly sever it from the cache before returning `-1`.

### Why this pattern is a Staff-level favorite
In highly concurrent backend systems or ML data ingestion pipelines, you rarely have the luxury of scanning arrays. State mutations must be instant. By separating *lookup* (the map) from *ordering* (the pointers), you create predictable, flat-latency data structures. 

If you are setting up a disposable environment to practice these, start by coding the base `Node` class and the `add_node` / `remove_node` helper functions. Getting the pointer manipulation perfect on the first try is the key to passing these rounds. 

What's your current comfort level with writing out the four-step pointer swaps for deleting a node in a Doubly Linked List?
