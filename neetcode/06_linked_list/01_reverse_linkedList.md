### question
Given the beginning of a singly linked list head, reverse the list, and return the new beginning of the list.


### 1. Restating

Given the head node of a singly linked list, reverse the direction of all pointers. The last node becomes the new head. Return this new head.

### 2. Clarifying Questions & Inputs/Outputs

* **Input:** `head` (type: `ListNode` or `None`). Node has `val` and `next`.
* **Output:** `new_head` (type: `ListNode` or `None`).
* **Constraints:** Modifying values or moving nodes? Moving nodes (changing pointers) is required.

### 3. Example By Hand

* Input: `1 -> 2 -> 3 -> None`
* Start at `1`. Needs to point to `None`.
* Move to `2`. Needs to point to `1`.
* Move to `3`. Needs to point to `2`.
* List becomes `3 -> 2 -> 1 -> None`. Output is `3`.

### 4. Brainstorming & Complexity

* **Stack:** Push all nodes to stack, pop them to rebuild. Time: O(N), Space: O(N).
* **Recursive:** Reverse the rest of the list, then append current node to the end. Time: O(N), Space: O(N) call stack.
* **Iterative (Hand Method):** Walk list, keep track of previous node, flip current node's pointer to previous. Time: O(N), Space: O(1).

### 5. Suggested Solution

Iterative approach. Matches the by-hand example directly. Simple, clear, straight forward. Constant space.

### 6. Outline

```python
def reverseList(head):
    """
    Reframe: Iteratively flip the direction of each node's next pointer.
    State: `prev` (accumulated reversed list), `curr` (node currently processing). Chosen because we need memory of the previous node to point backwards.
    Invariant: Everything before `curr` is fully reversed. Everything from `curr` onwards is original.

    get_next_node(node) = returns the next node in the original sequence.
    point_backwards(node, target) = sets node's next pointer to target.

    Core logic:
    - start with empty previous list and current at head
    - loop while current node exists
        - remember the next node in sequence
        - point current node backwards to previous
        - advance previous to current node
        - advance current to remembered next node
    - return previous (which is the new head)
    
    Edge cases:
    - head is None (empty list)
    - head.next is None (single node)
    """

```

### 7. Iterative Implementation

**Iteration 1: Skeleton with stubs**

```python
def reverseList(head):
    prev = None
    curr = head
    
    while curr:
        # TODO: remember next
        # TODO: point backwards
        # TODO: step forward
        pass
        
    return prev

```

**Iteration 2: Fleshing out core logic (plain English to code)**

```python
def reverseList(head):
    prev = None
    curr = head
    
    while curr:
        # remember next
        next_temp = curr.next 
        
        # point backwards
        curr.next = prev 
        
        # step forward
        prev = curr 
        curr = next_temp 
        
    return prev

```

**Iteration 3: Edge Cases**

* *Edge 1: Empty list (`head = None`).* If `head` is None, `curr` is None. Loop skips. Returns `prev` (None). Works perfectly.
* *Edge 2: Single node.* `curr` is node. Loop runs once. `curr.next` becomes None. `prev` becomes node. Loop exits. Returns node. Works perfectly.
* No patches needed. Core logic naturally handles stated edge cases.

### 8. Complexity & Optimizations

* **Time:** O(N) where N is list length. Must visit every node once.
* **Space:** O(1). Only using three pointers (`prev`, `curr`, `next_temp`).
* **Optimization:** Already optimal. Cannot traverse list faster than O(N) and cannot use less than O(1) space. The assignments inside the while loop are minimal and straight-forward.