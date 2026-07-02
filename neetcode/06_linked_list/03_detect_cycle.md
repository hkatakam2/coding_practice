### question
Given the beginning of a linked list head, return true if there is a cycle in the linked list. Otherwise, return false.


### 1. Restate

Given a singly linked list, determine if it contains a loop (a cycle where a node points back to a previously visited node). Return `True` if a cycle exists, `False` otherwise.

### 2. Clarify

* **Input:** `head` node of a singly linked list.
* **Output:** Boolean (`True` or `False`).
* **Questions:** * Can the list be empty? *Yes. Return `False`.*
* Can we modify node structures? *Assume no.*
* Do node values matter? *No, only memory references (pointers) matter.*



### 3. Example by Hand

Input list: `1 -> 2 -> 3 -> 4 -> 2` (points back to 2)

1. Look at `1`. Remember seeing `1`.
2. Move to next. Look at `2`. Remember seeing `2`.
3. Move to next. Look at `3`. Remember seeing `3`.
4. Move to next. Look at `4`. Remember seeing `4`.
5. Move to next. Look at `2`.
6. Check memory: "Have I seen `2` before?" Yes.
7. Cycle detected. Return `True`.

### 4. Brainstorming & Complexity

* **Approach A (The "By Hand" Method):** Hash Set. Walk the list. Store each node reference in a set. If we encounter a node already in the set, we found a cycle. If we hit `null`, no cycle.
* Time: $O(N)$
* Space: $O(N)$


* **Approach B (Fast/Slow Pointers):** Two runners on a track. Slow moves 1 step, Fast moves 2 steps. If there's a cycle, Fast will eventually lap Slow and they meet. If Fast hits `null`, no cycle.
* Time: $O(N)$
* Space: $O(1)$


* **Approach C (Flagging):** Add a boolean `visited` flag to the node class. Walk list, check flag, set flag.
* Time: $O(N)$
* Space: $O(1)$, but violates "do not modify inputs" constraint.



### 5. Suggest Solutions

Prefer simple, readable solutions. Approach A (Hash Set) directly translates the "by hand" logic into code. It is the clearest to explain and implement. Approach B (Two Pointers) is a clever optimization for space, which we can look at later. We will implement Approach A.

### 6. Outline

```python
def has_cycle(head): 
     """
    Reframe: A cycle exists if we visit the exact same node object twice.
    State: A Hash Set of seen nodes, chosen because checking for existence in a set is O(1).
    Invariant: Every node in the set has been visited exactly once and is part of the path from head.

    is_already_seen(node) = checks if node exists in our state
    record_seen(node) = adds node to our state
    get_next(node) = moves to the next node in the list

    Core logic:
    - start at the head node
    - while there are nodes to process:
        - if current node is already seen, we found a cycle, return true
        - otherwise, record current node as seen
        - move to next node
    - if we run out of nodes (hit null), there is no cycle, return false

    Edge cases:
    - head is None (empty list)
    - head.next is None (single node, no cycle)
     """

```

### 7. Iterative Implementation

**Iteration 1: Skeleton with stubs**

```python
def has_cycle(head):
    # TODO: init state
    current = head
    
    # while current is valid:
        # if is_already_seen(current):
            # return True
        # record_seen(current)
        # current = get_next(current)
        
    # return False

```

**Iteration 2: Translating core logic chunks**

```python
def has_cycle(head):
    seen_nodes = set() # init state
    current = head
    
    while current: # while current is valid
        if current in seen_nodes: # is_already_seen
            return True
        
        seen_nodes.add(current) # record_seen
        current = current.next # get_next
        
    return False # exhausted list, no cycle

```

**Iteration 3: Edge Case Patching**

* *Edge case:* `head` is `None` (empty list).
* Walkthrough: `seen_nodes` initializes. `current` is `None`. `while` loop never triggers. Returns `False`. Correct. No patch needed.


* *Edge case:* `head.next` is `None` (one node).
* Walkthrough: Adds node to set. `current` becomes `None`. Loop exits. Returns `False`. Correct. No patch needed.



Core logic organically handles all edge cases without extra explicit checks.

### 8. Complexity & Optimization

* **Current Complexity:** Time is $O(N)$ because we visit each node at most once. Space is $O(N)$ because in the worst case (no cycle), we store every node in the hash set.
* **Optimization (Floyd's Cycle Finding):** The hash set takes extra memory. We can optimize space to $O(1)$ by using two pointers (Fast and Slow). It sacrifices a bit of initial readability for a clever algorithmic trick.

```python
def has_cycle_optimized(head):
    # Edge case patch needed here to prevent null pointer on fast.next
    if not head or not head.next:
        return False
        
    slow = head
    fast = head.next
    
    while fast and fast.next:
        if slow == fast:
            return True
        slow = slow.next          # moves 1 step
        fast = fast.next.next     # moves 2 steps
        
    return False

```