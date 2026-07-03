### question
Given the head of a linked list and an integer n, remove the nth node from the end of the list and return its head.


**1. Restating**
Remove the $n$-th node from the end of a singly linked list. Return updated list head.

**2. Clarifying**

* **Inputs:** `head` of `ListNode`, integer `n`.
* **Outputs:** `head` of `ListNode`.
* **Constraints confirmed:** $1 \le n \le$ list length. Single-node lists valid.

**3. Hand-trace**
Input: `1 -> 2 -> 3 -> 4 -> 5`, $n = 2$. Target: `4`.

* Use gap method. Pointer A and B.
* Start both before head (dummy node).
* Move B forward $n$ steps. B now at `2`. Gap is 2.
* Move A and B together.
* B to `3`, A to `1`.
* B to `4`, A to `2`.
* B to `5` (tail), A to `3`.
* A sits exactly at target's predecessor.
* Skip target: A points to `5`.
* Output: `1 -> 2 -> 3 -> 5`.

**4. Brainstorming**

* **Two passes:** Count total length $L$. Iterate again to node $L - n$. Update pointer. Time: O(N). Space: O(1). Simple, traverses twice.
* **Two pointers (gap):** Fast pointer $n$ steps ahead. Move both. Fast hits tail, slow at predecessor. Time: O(N). Space: O(1). One pass. Matches hand-trace.
* **Recursion:** Recurse to tail, pass back a counter. Remove when counter equals $n$. Time: O(N). Space: O(N) call stack. Expensive.

**5. Suggest Solutions**

* **Solution 1:** Two passes. Very clear logically.
* **Solution 2:** Two pointers gap method. Clean, one pass, simple to explain. (Selected, matches step 3).

**6. Outline**

```python
def removeNthFromEnd(head: Optional[ListNode], n: int) -> Optional[ListNode]:
    """
    Reframe: Maintain n-step gap between pointers to halt exactly at target's predecessor.
    State: `slow` pointer, `fast` pointer, `dummy` head. Chosen because gap ensures `slow` stops before target when `fast` hits tail.
    Invariant: `fast` is strictly n steps ahead of `slow`.

    advance_pointer(ptr, steps) = moves pointer forward by given step count.

    Core logic:
    - Attach dummy node before head (simplifies deleting head).
    - Initialize fast and slow pointers at dummy.
    - Advance fast pointer by n steps to create gap.
    - Move fast and slow pointers simultaneously until fast hits the last node.
    - Slow pointer is now immediately before the node to delete.
    - Bypass target node by updating slow's next pointer.
    - Return dummy's next node.

    Edge cases:
    - Removing the only node in list (length 1, n=1).
    - Removing the head node of list (length L, n=L).
    """

```

**7. Iterative Implementation**

*Iteration 1: Outline core logic into skeleton*

```python
def removeNthFromEnd(head: Optional[ListNode], n: int) -> Optional[ListNode]:
    # create dummy node, attach to head
    # init slow and fast pointers at dummy
    
    # move fast pointer n steps ahead
    
    # move both until fast reaches tail
    
    # slow is at predecessor. skip target node.
    
    # return true head
    pass

```

*Iteration 2: Add pointers and target bypass*

```python
def removeNthFromEnd(head: Optional[ListNode], n: int) -> Optional[ListNode]:
    # added dummy node to easily handle head removals
    dummy = ListNode(0, head)
    slow = dummy
    fast = dummy
    
    # TODO: move fast pointer n steps ahead
    
    # TODO: move both until fast reaches tail
    
    # skip target node
    slow.next = slow.next.next
    
    return dummy.next

```

*Iteration 3: Full core logic*

```python
def removeNthFromEnd(head: Optional[ListNode], n: int) -> Optional[ListNode]:
    dummy = ListNode(0, head)
    slow = dummy
    fast = dummy
    
    # create n-step gap
    for _ in range(n):
        fast = fast.next
        
    # move both until fast is at the tail
    while fast.next is not None:
        slow = slow.next
        fast = fast.next
        
    # slow is at predecessor. skip target node.
    slow.next = slow.next.next
    
    return dummy.next

```

*Patching Edge Cases:*
Walked one by one:

* **1 node, n=1:** `dummy -> 1`. Fast moves 1 step to `1`. `fast.next` is None. `while` loop skips. `slow.next` (which is `1`) becomes `slow.next.next` (which is `None`). Returns `dummy.next` (None). Works perfectly.
* **Remove head (n=length):** `dummy -> 1 -> 2`. n=2. Fast moves to `2`. `while` loop skips. `slow` stays at `dummy`. `dummy.next` becomes `2`. Returns `2`. Works perfectly.
* *Result:* Dummy node elegantly absorbs all edge cases. No patching required.

**8. Complexity & Optimizations**

* **Time Complexity:** O(N). Strict one-pass traversal. `fast` touches each node exactly once.
* **Space Complexity:** O(1). Only allocating one dummy node and two pointers, regardless of list size.
* **Optimizations:** This is mathematically optimal for a singly linked list. No further optimizations needed over the plain implementation.