### question
You are given two non-empty linked lists, l1 and l2, where each represents a non-negative integer.

The digits are stored in reverse order, e.g. the number 321 is represented as 1 -> 2 -> 3 -> in the linked list.

Each of the nodes contains a single digit. You may assume the two numbers do not contain any leading zero, except the number 0 itself.

Return the sum of the two numbers as a linked list.

**1. Restating the Question**
Given two linked lists representing positive integers. Digits stored in reverse order (head = 1s place, next = 10s place, etc.). Sum the numbers. Return sum as new linked list in same reverse format.

**2. Clarifying Questions, Inputs, Outputs**

* **Inputs:** `l1`, `l2` (heads of two singly linked lists).
* **Output:** `head` of new singly linked list representing sum.
* **Assumptions to confirm:** * Can lists be different lengths? Yes.
* Modify in place or create new list? Create new to avoid mutating inputs.
* Can numbers be huge? Yes, beyond standard integer limits.



**3. Manual Example Walkthrough**
`l1`: 2 -> 4 -> 3 (Value: 342)
`l2`: 5 -> 6 -> 4 (Value: 465)

* Pos 1 (1s): 2 + 5 = 7. Carry = 0. Output node: 7.
* Pos 2 (10s): 4 + 6 = 10. Carry = 1. Output node: 0.
* Pos 3 (100s): 3 + 4 + carry(1) = 8. Carry = 0. Output node: 8.
* Result: 7 -> 0 -> 8 (Value: 807).

**4. Brainstorming Solutions & Complexity**

* *Idea A: Convert to Int.* Traverse `l1` & `l2`, build string/int, add them, convert back to linked list.
* *Complexity:* Time O(N+M), Space O(N+M).
* *Issue:* Fails for very long lists (integer overflow) unless using BigInt, which masks the algorithmic challenge.


* *Idea B: Grade-School Addition (Pointer Sweep).* Iterate both lists together. Add nodes + carry. Create new node. Move pointers.
* *Complexity:* Time O(max(N, M)), Space O(max(N, M)) for new list.
* *Note:* Handles arbitrary sizes perfectly. Matches manual walkthrough.



**5. Suggested Solution**
Go with Idea B (Grade-School Addition). It is the standard, simple, straightforward approach. Converting to int is a "clever" hack that breaks in strictly typed languages without BigInt. Pointer sweep directly addresses the data structure provided.

**6. Outline of Implementation**

```python
def addTwoNumbers(l1, l2): 
    """
    Reframe: Grade-school column addition, starting from least significant digit.
    State: dummy_head (to anchor output), current_ptr (to build output), carry (int). 
           Chosen because output list grows dynamically and carry bridges loop iterations.
    Invariant: carry is always 0 or 1.

    get_val(node) = returns node value if node exists, else 0
    advance(node) = returns next node if node exists, else null

    Core logic:
    - loop while both lists have digits
    - sum equals l1 value plus l2 value plus carry
    - calculate new carry (sum divided by 10)
    - calculate digit to store (sum modulo 10)
    - attach new node with digit to output
    - advance l1, l2, and output pointers

    Edge cases:
    - l1 is longer than l2
    - l2 is longer than l1
    - remaining carry after both lists exhausted (e.g., 5 + 5 = 10, needs extra node)
    """

```

**7. Iterative Implementation**

*Iteration 1: Skeleton with core logic stubs.*

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def addTwoNumbers(l1, l2):
    dummy_head = ListNode(0)
    curr = dummy_head
    carry = 0
    
    # Loop while both have digits (Happy Path)
    while l1 and l2:
        # TODO: calculate sum of l1.val, l2.val, and carry
        # TODO: update carry and current digit
        # TODO: create new node and append to curr
        # TODO: advance pointers
        pass
        
    return dummy_head.next

```

*Iteration 2: Flesh out math and pointers (Happy Path complete).*

```python
def addTwoNumbers(l1, l2):
    dummy_head = ListNode(0)
    curr = dummy_head
    carry = 0
    
    # Happy Path: Both lists have equal length
    while l1 and l2:
        total = l1.val + l2.val + carry  # Add values
        
        carry = total // 10              # Extract 10s place
        digit = total % 10               # Extract 1s place
        
        curr.next = ListNode(digit)      # Append to output
        
        # Advance all pointers
        curr = curr.next
        l1 = l1.next
        l2 = l2.next
        
    return dummy_head.next

```

*Iteration 3: Patching edge cases (Different lengths & leftover carry).*
*Change note: Merged condition into a single while loop `while l1 or l2 or carry`. Used dummy helpers logic inline to safely extract values even if a list is exhausted.*

```python
def addTwoNumbers(l1, l2):
    dummy_head = ListNode(0)
    curr = dummy_head
    carry = 0
    
    # Patched: Loop continues if either list has nodes, OR if carry remains
    while l1 or l2 or carry:
        # Edge case patch: safely get value if one list is shorter
        val1 = l1.val if l1 else 0
        val2 = l2.val if l2 else 0
        
        total = val1 + val2 + carry
        
        carry = total // 10
        digit = total % 10
        
        curr.next = ListNode(digit)
        curr = curr.next
        
        # Edge case patch: safely advance pointers
        if l1: l1 = l1.next
        if l2: l2 = l2.next
        
    return dummy_head.next

```

**8. Complexity & Optimizations**

* **Time Complexity:** `O(max(N, M))` where N and M are lengths of `l1` and `l2`. We visit each node exactly once. This is optimal; we must process every digit to compute the sum.
* **Space Complexity:** `O(max(N, M))` for the new linked list. If we are allowed to mutate `l1` or `l2`, we could theoretically achieve `O(1)` space by storing the sum in the longer of the two lists.
* **Optimizations:** Mutating inputs saves space but is universally considered bad practice in real-world APIs unless explicitly requested, as it destroys the caller's data. The current clean, out-of-place implementation is the gold standard for this problem. Minimal operations inside the loop ensure optimal constant-factor performance.