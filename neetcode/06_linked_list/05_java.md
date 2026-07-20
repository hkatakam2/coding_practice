### 1. Restate the problem

We are given a singly linked list and an integer `n`. We need to identify the node that is exactly `n` positions from the very end of the list, remove it by updating the pointers of the surrounding nodes, and return the head of the modified list.

The main constraint is that we must traverse a forward-only structure to find a position defined relative to its end, and we must do this efficiently.

### 2. Ask clarifying questions

Before writing code, I would clarify a few assumptions with the interviewer:

* **Is `n` always valid?** Can I assume `n` is at least 1 and will never exceed the total length of the list? *(Assumption: Yes, `n` is valid.)*
* **Can the list have only one node?** *(Assumption: Yes. In this case, `n` must be 1, and the resulting list should be empty/null.)*
* **Are we returning a new list or modifying in place?** *(Assumption: Modify the existing pointers in place and return the new head.)*
* **Do we have a standard `ListNode` definition?** *(Assumption: Yes, the standard definition with `val` and `next`.)*

### 3. Work through an example by hand

Let's take a representative list: `1 -> 2 -> 3 -> 4 -> 5` and `n = 2`.
The 2nd node from the end is `4`.

* **Goal:** Change `3.next` to point to `5`, dropping `4`.
* **State progression:**
* We don't know where the end is initially.
* If we send a "scout" pointer `2` steps ahead, it lands on `3` (1 -> 2 -> 3).
* Now we move both a `current` pointer (starting at `1`) and the `scout` pointer simultaneously.
* Scout at `4`, Current at `2`.
* Scout at `5`, Current at `3`.
* Scout is at the last node. Current is at `3`, which is exactly the node *before* our target.
* We rewire: `Current.next = Current.next.next` (so `3.next = 5`).


* **Final result:** `1 -> 2 -> 3 -> 5`.

### 4. Brainstorm solutions aloud

**Option 1: Two Passes (Direct Simulation)**
The most straightforward approach is to count the nodes. We iterate through the whole list to find the total length `L`. Then, the node we want to remove is at position `L - n` (0-indexed). We do a second pass, stop right before the target, and rewire.

* **Time complexity:** O(N) where N is the length of the list. We traverse it exactly twice.
* **Space complexity:** O(1).
* **Tradeoffs:** Very simple to explain and implement, but requires traversing the data twice, which is slightly inefficient if the list is extremely long or if we want to minimize memory reads.

**Option 2: One Pass with Two Pointers (Sliding Window)**
As demonstrated in the hand-worked example, we can maintain a gap of exactly `n` nodes between a `fast` pointer and a `slow` pointer. By the time the `fast` pointer hits the end of the list, the `slow` pointer will sit right before the node we need to remove.

* **Time complexity:** O(N) time. We traverse the list only once.
* **Space complexity:** O(1).
* **Tradeoffs:** More elegant. It strictly reads through the list once. Handling the edge case where the head itself needs to be removed requires a bit of care.

### 5. Select the solution

I will use the **One Pass with Two Pointers** approach. It comfortably satisfies the O(N) time and O(1) space constraints while only requiring a single traversal.

To handle the edge case where we need to remove the first node in the list (which lacks a "previous" node to rewire), I will use a standard linked-list pattern: a `dummy` head node. This normalizes the logic so that every node, including the original head, has a preceding node.

### 6. Write the implementation outline

```java
class ListNode {
    int val;
    ListNode next;
    ListNode(int x) { val = x; }
}

ListNode removeNthFromEnd(ListNode head, int n) {
    /*
     * Reframe:
     * Maintain a fixed gap of 'n' between two pointers. When the leading
     * pointer reaches the end, the trailing pointer is ready to bypass the target.
     *
     * State:
     * - 'dummy' node pointing to head: handles head-removal edge case cleanly.
     * - 'fast' pointer: scouts ahead by n + 1 steps.
     * - 'slow' pointer: follows fast, maintaining the gap.
     * Chosen because two pointers allow a single-pass relative lookup.
     *
     * Invariant:
     * The gap between slow and fast is always exactly n + 1 nodes once fast 
     * is initially positioned.
     *
     * Core logic:
     * - attach dummy node to the original head
     * - advance the fast pointer so there is a gap of n between fast and slow
     * - step both pointers forward one node at a time until fast reaches the end
     * - bypass the target node by updating slow's next pointer
     * - return the new list starting at dummy.next
     *
     * Edge cases:
     * - n equals the length of the list (removing the head)
     * - single-node list
     */
}

```

### 7. Implement iteratively

**Iteration 1: Method skeleton and dummy node setup**
First, we establish the dummy node and initialize our pointers. This creates a safe space to work without null pointer exceptions at the head.

```java
public ListNode removeNthFromEnd(ListNode head, int n) {
    // Added: Dummy node to normalize operations on the head
    ListNode dummy = new ListNode(0);
    dummy.next = head;
    
    ListNode slow = dummy;
    ListNode fast = dummy;

    // TODO: Advance fast pointer by n + 1 steps
    // TODO: Move both pointers until fast is null
    // TODO: Rewire the slow pointer's next reference

    return dummy.next;
}

```

**Iteration 2: Create the gap**
Next, we advance the `fast` pointer. We want a gap of `n + 1` between `slow` and `fast` because `slow` needs to stop *before* the node to be deleted.

```java
public ListNode removeNthFromEnd(ListNode head, int n) {
    ListNode dummy = new ListNode(0);
    dummy.next = head;
    
    ListNode slow = dummy;
    ListNode fast = dummy;

    // Added: Create the required gap.
    // We move fast n + 1 times so that the gap between slow and fast is n nodes.
    for (int i = 0; i <= n; i++) {
        fast = fast.next;
    }

    // TODO: Move both pointers until fast is null
    // TODO: Rewire the slow pointer's next reference

    return dummy.next;
}

```

**Iteration 3: Traverse and delete (Happy Path)**
Now we slide the window forward until `fast` falls off the end of the list. Then, we execute the pointer bypass.

```java
public ListNode removeNthFromEnd(ListNode head, int n) {
    ListNode dummy = new ListNode(0);
    dummy.next = head;
    
    ListNode slow = dummy;
    ListNode fast = dummy;

    for (int i = 0; i <= n; i++) {
        fast = fast.next;
    }

    // Added: Slide both pointers together to maintain the gap
    while (fast != null) {
        slow = slow.next;
        fast = fast.next;
    }
    
    // Added: Bypass the nth node from the end
    slow.next = slow.next.next;

    return dummy.next;
}

```

**Edge-case pass**
Let's evaluate the edge cases listed in the outline against our Iteration 3 code.

1. **Removing the head (`n` equals list length):**
* Input: `1 -> 2`, `n = 2`.
* `dummy -> 1 -> 2 -> null`. Both `slow` and `fast` start at `dummy`.
* Loop `i` from `0` to `2` (3 iterations): `fast` moves to `1`, then `2`, then `null`.
* `while (fast != null)` is skipped because `fast` is already `null`.
* `slow` is still at `dummy`. We execute `slow.next = slow.next.next` (`dummy.next = 2`).
* Returns `dummy.next` (which is `2`).
* *Result:* Works perfectly. The dummy node entirely prevents the need for special `if (head == target)` checks.


2. **Single-node list:**
* Input: `1`, `n = 1`.
* `dummy -> 1 -> null`.
* Gap loop moves `fast` 2 times: `1`, then `null`.
* While loop skipped.
* `slow` is at `dummy`. `dummy.next = dummy.next.next` (`dummy.next = null`).
* Returns `null`.
* *Result:* Works perfectly. No patches needed.



### 8. Analyze expensive sections and optimize

* **Time Complexity:** O(N), where N is the number of nodes in the linked list. The `fast` pointer touches every node exactly once.
* **Space Complexity:** O(1). We only allocate a single `dummy` node and two pointer references, regardless of the size of the list.
* **Bottlenecks:** There are no expensive nested loops, collections overhead, or sorting. This is the optimal theoretical limit since we must at minimum traverse the list to find the relative end.

### Final Code

Here is the clean, complete implementation:

```java
public class Solution {
    public ListNode removeNthFromEnd(ListNode head, int n) {
        ListNode dummy = new ListNode(0);
        dummy.next = head;
        
        ListNode slow = dummy;
        ListNode fast = dummy;

        // Advance fast by n + 1 steps to establish the required gap
        for (int i = 0; i <= n; i++) {
            fast = fast.next;
        }

        // Slide the window forward until fast reaches the end of the list
        while (fast != null) {
            slow = slow.next;
            fast = fast.next;
        }
        
        // slow is now positioned exactly one node before the target node
        slow.next = slow.next.next;

        return dummy.next;
    }
}

```

### Brief test walkthrough

* **Main example:** `[1, 2, 3, 4, 5]`, `n = 2`
* `fast` moves 3 steps to `3`.
* Both step forward. `fast` goes `4 -> 5 -> null`. `slow` goes `dummy -> 1 -> 2 -> 3`.
* `slow` stops at `3`. `3.next` becomes `5`. `4` is bypassed.
* Returns `[1, 2, 3, 5]`. Correct.


* **Smallest valid input:** `[1]`, `n = 1`
* `fast` moves 2 steps: `1 -> null`.
* `slow` remains at `dummy`.
* `dummy.next` becomes `null`.
* Returns `null`. Correct.


* **Invariant stress test:** `[1, 2]`, `n = 2`
* `fast` moves 3 steps: `1 -> 2 -> null`.
* `slow` remains at `dummy`.
* `dummy.next` (which was `1`) becomes `dummy.next.next` (which is `2`).
* Returns `[2]`. Correctly removed the head.