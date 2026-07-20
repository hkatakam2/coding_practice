### 1. Restatement

We are given a singly linked list. We need to physically rearrange its nodes so that the order alternates between the nodes from the beginning of the list and the nodes from the end of the list, closing in toward the middle.

Specifically, the $0^{\text{th}}$ node is followed by the last node ($n-1$), which is followed by the $1^{\text{st}}$ node, then the second-to-last node ($n-2$), and so on. We are not allowed to change the integer values stored inside the nodes; we must rewire the actual `next` pointers.

### 2. Clarifying questions and assumptions

Before writing code, I would ask the interviewer to confirm a few details:

* **Input size:** Can the list be empty or contain just one or two nodes? *(Assumption: Yes, the input can be `null` or very short, so we must handle these gracefully.)*
* **Return type:** Should I return the new head of the list, or modify the list in place and return `void`? *(Assumption: Standard LeetCode signature is `void reorderList(ListNode head)`, meaning we modify in place.)*
* **Memory constraints:** Is $O(N)$ auxiliary space acceptable, or is the goal $O(1)$ space? *(Assumption: $O(1)$ auxiliary space is usually expected for linked-list pointer manipulation, though $O(N)$ is a good stepping stone.)*

### 3. Work through an example by hand

Let's take a representative input with an odd number of nodes: `1 -> 2 -> 3 -> 4 -> 5`.
Positions: `0, 1, 2, 3, 4`.
Target: `1 -> 5 -> 2 -> 4 -> 3`.

**Step 1:** Split the list into a first half and a second half.
First half: `1 -> 2 -> 3`
Second half: `4 -> 5`

**Step 2:** Reverse the second half.
Reversed second half: `5 -> 4`

**Step 3:** Merge the two halves alternately.

* Take `1` from the first half. Next is `5` from the second half.
* Take `2` from the first half. Next is `4` from the second half.
* Take `3` from the first half. The second half is empty.
* End of list.
Final result: `1 -> 5 -> 2 -> 4 -> 3 -> null`.

### 4. Brainstorm solutions aloud

**Approach 1: Array of Nodes**
We could traverse the list and add every node to a standard `ArrayList<ListNode>`. Once we have all nodes in an array, we can use a left pointer at `0` and a right pointer at `n - 1` to weave the nodes together, updating their `next` references.

* **Time:** $O(N)$ to traverse and weave.
* **Space:** $O(N)$ to store the nodes.
* **Pros:** Extremely easy to implement.
* **Cons:** Uses $O(N)$ extra memory, which defeats the purpose of pointer manipulation in linked lists.

**Approach 2: Find Middle, Reverse, and Merge**
We can simulate the exact process I walked through by hand.

1. Find the middle of the list using the slow/fast pointer (tortoise and hare) technique.
2. Sever the list into two halves and reverse the second half in place.
3. Merge the two halves by advancing two pointers.

* **Time:** $O(N)$. We do three $O(N)$ passes (find middle, reverse, merge).
* **Space:** $O(1)$ auxiliary memory. We only use a few temporary pointers.
* **Pros:** Optimal space complexity.
* **Cons:** Moderately difficult to implement perfectly without bugs, as it requires three distinct pointer-manipulation steps.

### 5. Select the solution

I will proceed with **Approach 2 (Find Middle, Reverse, Merge)**.
It is the standard optimal approach for this problem and demonstrates three core linked-list techniques in a single solution: finding the middle, reversing a list, and interleaving lists.

### 6. Write the implementation outline

```java
void reorderList(ListNode head) {
    /*
     * Reframe:
     * Split the list in half, reverse the second half, and interleave the two halves.
     *
     * State:
     * Pointers for the heads of the two halves, and temporary pointers for merging.
     * Chosen because $O(1)$ space linked list manipulation only requires local state tracking.
     *
     * Invariant:
     * During the merge, no nodes are lost because we always save the `next`
     * pointer of both lists before rewiring.
     *
     * Helpers:
     * reverseList(node)
     * - standard in-place linked list reversal returning the new head
     *
     * Core logic:
     * - return immediately if the list has 0 or 1 elements
     * - initialize slow and fast pointers to find the middle
     * - detach the first half from the second half
     * - reverse the second half
     * - merge the first half and the reversed second half node by node
     *
     * Edge cases:
     * - Even vs Odd number of elements (middle calculation must be precise).
     * - Forgetting to set the tail of the first half to null (causes a cycle).
     */
}

```

### 7. Implement iteratively

#### Iteration 1: Method skeleton

I'll set up the main flow and stub out the complex pieces.

```java
class ListNode {
    int val;
    ListNode next;
    ListNode(int val) { this.val = val; }
}

public void reorderList(ListNode head) {
    if (head == null || head.next == null) {
        return;
    }

    // TODO: 1. Find the middle of the list
    ListNode middle = head; 
    
    // TODO: 2. Reverse the second half
    ListNode secondHalf = middle.next;
    middle.next = null; // Sever the connection
    secondHalf = reverseList(secondHalf);
    
    // TODO: 3. Merge the two halves
    ListNode firstHalf = head;
}

private ListNode reverseList(ListNode head) {
    // TODO: Standard reversal
    return head;
}

```

#### Iteration 2: Finding the middle and Reversing

Now, I'll implement the slow/fast pointer logic to find the middle, and the helper to reverse the list.

```java
public void reorderList(ListNode head) {
    if (head == null || head.next == null) {
        return;
    }

    // 1. Find the middle of the list
    ListNode slow = head;
    ListNode fast = head;
    
    // Added: Fast advances by 2, slow by 1. 
    // When fast reaches the end, slow is at the midpoint.
    while (fast != null && fast.next != null) {
        slow = slow.next;
        fast = fast.next.next;
    }
    
    // 2. Reverse the second half
    ListNode secondHalf = slow.next;
    slow.next = null; // Sever the connection to prevent cycles
    secondHalf = reverseList(secondHalf);
    
    // TODO: 3. Merge the two halves
    ListNode firstHalf = head;
}

private ListNode reverseList(ListNode head) {
    // Added: Standard in-place reversal
    ListNode prev = null;
    ListNode current = head;
    
    while (current != null) {
        ListNode nextTemp = current.next;
        current.next = prev;
        prev = current;
        current = nextTemp;
    }
    
    return prev;
}

```

#### Iteration 3: Complete the happy path (Merge)

Finally, I need to weave `firstHalf` and `secondHalf` together.

```java
public void reorderList(ListNode head) {
    if (head == null || head.next == null) {
        return;
    }

    // 1. Find the middle
    ListNode slow = head;
    ListNode fast = head;
    while (fast != null && fast.next != null) {
        slow = slow.next;
        fast = fast.next.next;
    }
    
    // 2. Split and reverse
    ListNode secondHalf = slow.next;
    slow.next = null; 
    secondHalf = reverseList(secondHalf);
    
    // 3. Merge the two halves
    ListNode firstHalf = head;
    
    // Added: Interleave nodes. secondHalf will always be the same length 
    // or one shorter than firstHalf.
    while (secondHalf != null) {
        ListNode temp1 = firstHalf.next;
        ListNode temp2 = secondHalf.next;
        
        firstHalf.next = secondHalf;
        secondHalf.next = temp1;
        
        firstHalf = temp1;
        secondHalf = temp2;
    }
}

```

### 8. Edge-case walkthrough and patches

Let's verify a few tricky states:

* **Empty list / 1 element:** Handled cleanly by the `if (head == null || head.next == null)` guard.
* **Even number of elements (e.g., 4 nodes: `1 -> 2 -> 3 -> 4`):**
* `slow` and `fast` both start at `1`.
* Loop 1: `slow` goes to `2`, `fast` goes to `3`.
* Loop 2: `slow` goes to `3`, `fast` goes to `null`.
* Loop terminates. `slow` is at `3`.
* `secondHalf` becomes `4`. `slow.next` becomes `null` (severing list to `1 -> 2 -> 3`).
* `secondHalf` reversed is just `4`.
* Merge:
* `firstHalf` starts at `1`, `secondHalf` starts at `4`.
* `1.next` points to `4`. `4.next` points to `2`.
* Pointers move to `2` and `null`.
* Loop terminates. Result: `1 -> 4 -> 2 -> 3 -> null`.


* **Wait, let's look at the result.** Target for `1, 2, 3, 4` is `1 -> 4 -> 2 -> 3`. This matches!


* **Odd number of elements (e.g., 5 nodes: `1 -> 2 -> 3 -> 4 -> 5`):**
* Loop 1: `slow` at `2`, `fast` at `3`.
* Loop 2: `slow` at `3`, `fast` at `5`.
* Loop terminates because `fast.next` is `null`.
* `slow` is at `3`.
* `secondHalf` becomes `4 -> 5`. List severed to `1 -> 2 -> 3`.
* `secondHalf` reversed becomes `5 -> 4`.
* Merge:
* `1 -> 5 -> 2 -> 4 -> 3 -> null`.


* This works perfectly!


* **Preventing Cycles:**
* Setting `slow.next = null` ensures the tail of the first list does not loop back onto the second list.



No code patches are required. The logic holds up perfectly.

### 9. Final code

```java
/**
 * Definition for singly-linked list.
 * public class ListNode {
 *     int val;
 *     ListNode next;
 *     ListNode() {}
 *     ListNode(int val) { this.val = val; }
 *     ListNode(int val, ListNode next) { this.val = val; this.next = next; }
 * }
 */
class Solution {
    public void reorderList(ListNode head) {
        // Base case: 0 or 1 node lists require no reordering
        if (head == null || head.next == null) {
            return;
        }

        // 1. Find the middle of the linked list
        ListNode slow = head;
        ListNode fast = head;
        
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
        }
        
        // 2. Reverse the second half of the list
        // 'slow' is currently at the median. We sever the list here.
        ListNode secondHalf = slow.next;
        slow.next = null; // Important: prevents cycles in the final list
        
        secondHalf = reverseList(secondHalf);
        
        // 3. Merge the two lists alternately
        ListNode firstHalf = head;
        
        while (secondHalf != null) {
            // Save the next nodes before overwriting pointers
            ListNode nextFirst = firstHalf.next;
            ListNode nextSecond = secondHalf.next;
            
            // Link first list node to second list node
            firstHalf.next = secondHalf;
            // Link second list node to the next node in the first list
            secondHalf.next = nextFirst;
            
            // Advance both pointers
            firstHalf = nextFirst;
            secondHalf = nextSecond;
        }
    }

    /**
     * Reverses a singly linked list in place.
     * Returns the new head of the reversed list.
     */
    private ListNode reverseList(ListNode head) {
        ListNode prev = null;
        ListNode current = head;
        
        while (current != null) {
            ListNode nextNode = current.next;
            current.next = prev;
            prev = current;
            current = nextNode;
        }
        
        return prev;
    }
}

```

### 10. Complexity

* **Time Complexity:** $O(N)$
* Finding the middle of the list requires scanning half the nodes: $O(N/2)$.
* Reversing the second half requires scanning half the nodes: $O(N/2)$.
* Merging the two halves requires iterating through half the nodes: $O(N/2)$.
* Overall Time Complexity: $O(N)$.


* **Space Complexity:** $O(1)$
* We use a fixed number of object references (`slow`, `fast`, `firstHalf`, `secondHalf`, `nextFirst`, `nextSecond`, `prev`, `current`).
* No new instances of `ListNode` are created, making the auxiliary memory usage constant.



### 11. Brief test walkthrough

Let's do a quick final check with the smallest interesting case: `1 -> 2`.

* `head = 1`. `head.next` is not null. Proceed.
* `slow` = `1`, `fast` = `1`. Loop: `fast.next` is `2`. `fast.next.next` is `null`. `slow` moves to `2`, `fast` moves to `null`.
* Loop exits.
* `secondHalf` = `slow.next` which is `null`.
* `slow.next` = `null` (so `1 -> 2 -> null` is now technically unchanged, but `secondHalf` is `null`).
* `reverseList(null)` returns `null`.
* Merge: `while(secondHalf != null)` skips entirely since it's `null`.
* List remains `1 -> 2`. Correct! The ordering of a 2-node list is identical to its original state.