### question
You are given the heads of two sorted linked lists list1 and list2.

Merge the two lists into one sorted linked list and return the head of the new sorted linked list.

The new list should be made up of nodes from list1 and list2.

### 1. Restating the Question

Merge two sorted linked lists into one.
Result must be sorted.
Must reuse existing nodes from the two input lists.
Return head of the new list.

### 2. Clarifying Questions & I/O

* **Q:** Can lists be different lengths? **A:** Yes.
* **Q:** Can lists be empty? **A:** Yes.
* **Q:** In-place node splicing or create new nodes? **A:** In-place.
* **Inputs:** `list1 = 1 -> 2 -> 4`, `list2 = 1 -> 3 -> 4`
* **Output:** `1 -> 1 -> 2 -> 3 -> 4 -> 4`

### 3. Hand-Trace Example

`L1 = [1, 2, 4]`, `L2 = [1, 3, 4]`

* Compare L1(1) and L2(1). Tie. Pick L1. List so far: `[1]`
* Compare L1(2) and L2(1). Pick L2. List: `[1, 1]`
* Compare L1(2) and L2(3). Pick L1. List: `[1, 1, 2]`
* Compare L1(4) and L2(3). Pick L2. List: `[1, 1, 2, 3]`
* Compare L1(4) and L2(4). Tie. Pick L1. List: `[1, 1, 2, 3, 4]`
* L1 empty. Append remaining L2. List: `[1, 1, 2, 3, 4, 4]`

### 4. Brainstorming & Complexity

* **Idea 1: Iterative Two Pointers (Hand-Trace Method).** Keep pointer for L1, pointer for L2. Compare, attach smaller to a new tail, advance.
* Time: O(N + M). Space: O(1).


* **Idea 2: Recursive.** If L1 < L2, `L1.next = merge(L1.next, L2)`.
* Time: O(N + M). Space: O(N + M) for call stack. Risk of stack overflow on huge lists.


* **Idea 3: Collect, Sort, Rebuild.** Dump nodes to array, sort, rebuild links.
* Time: O((N+M) log(N+M)). Space: O(N+M). Terrible approach.



### 5. Suggest Solutions

Choose Idea 1 (Iterative Two Pointers). Matches hand-trace. Extremely clear, no extra space overhead, avoids stack overflow risk.

### 6. Outline Implementation

```python
def mergeTwoLists(list1, list2): # -> ListNode
    """
    Reframe: Zipper merge two sorted sequences into one using a dummy head.
    State: A dummy node and a tail pointer, chosen because dummy node avoids complex empty-list/first-node initialization checks.
    Invariant: Merged list up to the tail pointer is always sorted.

    getSmallerAndAdvance(l1, l2) = compares current l1 and l2 values, returns the smaller node, and shifts that list's pointer forward.

    Core logic:
    - Create a dummy head and set tail pointer to it.
    - While both lists have nodes:
        - getSmallerAndAdvance
        - attach smaller node to tail
        - move tail pointer forward
    - Once one list runs out, attach the entire remainder of the non-empty list to the tail.
    - Return node after dummy head.

    Edge cases:
    - list1 is empty
    - list2 is empty
    - both empty
    """

```

### 7. Iterative Implementation

**Iteration 1: Skeleton with stubs**
Drafting the core plain English logic into code placeholders.

```python
def mergeTwoLists(list1, list2):
    dummy = ListNode()
    tail = dummy
    
    # While both lists have nodes
    while list1 and list2:
        # TODO: getSmallerAndAdvance and attach to tail
        pass
        
    # TODO: attach remainder
    
    return dummy.next

```

**Iteration 2: Filling the loop**
Replacing `getSmallerAndAdvance` stub with actual pointer comparisons.

```python
def mergeTwoLists(list1, list2):
    dummy = ListNode()
    tail = dummy
    
    while list1 and list2:
        # Compare and attach smaller
        if list1.val <= list2.val:
            tail.next = list1
            list1 = list1.next # Advance L1
        else:
            tail.next = list2
            list2 = list2.next # Advance L2
            
        # Move tail forward
        tail = tail.next 
        
    # TODO: attach remainder
    
    return dummy.next

```

**Iteration 3: Handling remainders (Core logic complete)**

```python
def mergeTwoLists(list1, list2):
    dummy = ListNode()
    tail = dummy
    
    while list1 and list2:
        if list1.val <= list2.val:
            tail.next = list1
            list1 = list1.next
        else:
            tail.next = list2
            list2 = list2.next
        tail = tail.next
        
    # Attach remainder. If list1 exhausted, list1 is None. 
    # Python 'or' returns first truthy value.
    tail.next = list1 or list2 
    
    return dummy.next

```

**Iteration 4: Walk edge cases and patch**

* *Edge 1: list1 empty.* `list1` is None. Loop `while list1 and list2` never runs. `tail.next = list1 or list2` sets `tail.next` to `list2`. `dummy.next` returns `list2`. Works perfectly.
* *Edge 2: list2 empty.* Same logic. Works perfectly.
* *Edge 3: Both empty.* Loop skips. `tail.next = None or None` (None). `dummy.next` is None. Works perfectly.
* *Conclusion:* No patching needed. The dummy node elegantly absorbs all edge cases.

### 8. Complexity & Optimizations

* **Time Complexity:** O(N + M) where N and M are lengths of the lists. We visit each node exactly once.
* **Space Complexity:** O(1). Only allocating a single dummy node and a few pointers. No memory scaling with input size.
* **Optimizations:** Solution is already optimal for linked lists. No expensive sections exist. Only hardware-level optimization (like cache locality) would be faster, but impossible to implement in Python with standard dispersed linked list memory allocation. Stick with this code.