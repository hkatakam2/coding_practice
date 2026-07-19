### 1. Restate the problem

We are given the head node of a singly linked list. We need to reverse the direction of all the pointers in the list so that the last node becomes the new first node, the second-to-last becomes the new second node, and so on. Finally, we must return the new head of the reversed list.

### 2. Ask clarifying questions and assumptions

In a real interview, I would ask the following to ensure I understand the boundaries:

* **Can the input list be empty (`null`) or contain just a single node?**
* *Assumption:* Yes. The code needs to handle 0-node and 1-node lists gracefully.


* **Should I reverse the list in place, or create a completely new set of nodes?**
* *Assumption:* In-place modification is preferred to minimize memory usage (O(1) extra space).


* **What does the `ListNode` class look like?**
* *Assumption:* It is a standard Java singly linked list node with an `int val` and a `ListNode next`.



### 3. Work through an example by hand

Let's take a representative input: `1 -> 2 -> 3 -> null`.
Goal: Transform this into `3 -> 2 -> 1 -> null`.

**Step-by-step:**

* Start at node `1`. I need to point `1` to `null`. But if I do that immediately, I lose the reference to `2`.
* So, I must temporarily save `2`.
* Point `1` to `null`.
* Move to `2`. The previous node was `1`. I need to point `2` to `1`. Again, save `3` first.
* Point `2` to `1`.
* Move to `3`. The previous node was `2`. Save `null` (the end of the list).
* Point `3` to `2`.
* Move to `null`. The list is fully traversed.
* The last node I processed was `3`, which is the new head.

### 4. Candidate solutions

* **Approach 1: Iterative Pointer Reversal (The manual example approach)**
* *Core idea:* Maintain pointers to the previous node and current node. As we iterate, temporarily store the next node, reverse the current node's pointer to the previous node, and step forward.
* *Time complexity:* O(n), where n is the number of nodes. We visit each node exactly once.
* *Space complexity:* O(1), since we only use a few pointer variables.


* **Approach 2: Recursive Reversal**
* *Core idea:* Traverse recursively to the end of the list. The last node becomes the new head. As the recursion unwinds, make the next node point back to the current node, and set the current node's next to null.
* *Time complexity:* O(n) to visit all nodes.
* *Space complexity:* O(n) due to the call stack depth, which could cause a `StackOverflowError` for very large lists.


* **Approach 3: Stack**
* *Core idea:* Traverse the list and push all nodes onto a `Deque` (stack). Pop them off one by one to rebuild the pointers.
* *Time complexity:* O(n).
* *Space complexity:* O(n) to store all nodes in the stack.



### 5. Selected solution and justification

I will proceed with the **Iterative Pointer Reversal (Approach 1)**.
It operates in O(1) space, avoiding the risk of stack overflow present in the recursive approach, and it does not require additional data structures like the stack approach. It directly manipulates the pointers, which is exactly what linked list problems are designed to test.

### 6. Plain-English implementation outline

```java
ListNode reverseList(ListNode head) {
    /*
     * Reframe:
     * Walk through the list and flip each pointer backward one by one.
     *
     * State:
     * `prev` - keeps track of the reversed portion (starts as null).
     * `curr` - the current node we are processing (starts at head).
     *
     * Chosen because:
     * We need to modify a node's pointer without losing the rest of the list.
     *
     * Invariant:
     * At the start of any loop iteration, all nodes strictly behind `curr` 
     * have been fully reversed and are headed by `prev`.
     *
     * Core logic:
     * - iterate while the current node is not null
     * - temporarily save the next node so we don't lose the list
     * - point the current node backward to the previous node
     * - slide the `prev` tracker forward to the current node
     * - slide the `curr` tracker forward to the saved next node
     * - return `prev`, which will be resting on the new head when `curr` hits null
     *
     * Edge cases:
     * - empty list (head is null) -> loop skips, returns prev (null). Correct.
     * - single node list -> loop runs once, points it to null, returns it. Correct.
     */
}

```

### 7. Iterative Java implementation

**Iteration 1: Method skeleton and main state variables**
I'll set up the variables required to maintain the state as we iterate through the list.

```java
public ListNode reverseList(ListNode head) {
    ListNode prev = null;
    ListNode curr = head;
    
    while (curr != null) {
        // TODO: save next node
        // TODO: reverse current pointer
        // TODO: advance prev and curr pointers
    }
    
    return prev;
}

```

**Iteration 2: Complete the core logic**
Now I will implement the pointer swapping logic inside the loop, using a temporary variable to hold the rest of the list safely.

```java
public ListNode reverseList(ListNode head) {
    ListNode prev = null;
    ListNode curr = head;
    
    while (curr != null) {
        // Added: temporarily save the rest of the list
        ListNode nextNode = curr.next;
        
        // Added: reverse the pointer
        curr.next = prev;
        
        // Added: shift our two tracking pointers forward
        prev = curr;
        curr = nextNode;
    }
    
    return prev;
}

```

### 8. Edge-case walkthrough and patches

Let's evaluate the edge cases identified earlier against our completed iteration.

1. **Empty list (`head = null`):**
* `curr` is initialized to `null`.
* The `while` loop condition `(curr != null)` evaluates to `false` immediately.
* The method returns `prev`, which is `null`. This is the correct behavior.


2. **Single element list (`head = Node(1)`):**
* `curr` = Node(1), `prev` = null.
* Loop 1: `nextNode` = null. `curr.next` = null. `prev` = Node(1). `curr` = null.
* Loop terminates. Method returns Node(1), whose `next` is now correctly `null`. This is the correct behavior.



No patches are necessary. The logic naturally covers the edge cases without additional `if (head == null)` defensive checks, which keeps the code clean.

### Final code

For completeness, I'll provide the assumption of the `ListNode` class alongside the final clean method.

```java
// Standard singly linked list node provided by the environment
public class ListNode {
    int val;
    ListNode next;
    ListNode() {}
    ListNode(int val) { this.val = val; }
    ListNode(int val, ListNode next) { this.val = val; this.next = next; }
}

class Solution {
    public ListNode reverseList(ListNode head) {
        ListNode prev = null;
        ListNode curr = head;
        
        while (curr != null) {
            ListNode nextNode = curr.next;
            
            curr.next = prev;
            
            prev = curr;
            curr = nextNode;
        }
        
        return prev;
    }
}

```

### Complexity

* **Time Complexity:** O(n), where n is the number of nodes in the linked list. We traverse the entire list exactly once, performing O(1) operations at each step.
* **Space Complexity:** O(1). We only allocate three object references (`prev`, `curr`, `nextNode`), regardless of the size of the input list.

### Brief test walkthrough

* **Test Case 1:** `1 -> 2 -> 3 -> null`
* *Expected:* `3 -> 2 -> 1 -> null`.
* *Walkthrough:* Loop visits 1, points 1 to null. Visits 2, points 2 to 1. Visits 3, points 3 to 2. Returns 3. Correct.


* **Test Case 2:** `null` (Empty List)
* *Expected:* `null`.
* *Walkthrough:* Loop condition fails immediately, returns `prev` which is `null`. Correct.


* **Test Case 3:** `42 -> null` (Single element)
* *Expected:* `42 -> null`.
* *Walkthrough:* Loop visits 42, points it to null, `curr` becomes null. Returns 42. Correct.