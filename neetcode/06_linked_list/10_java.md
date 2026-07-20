### 1. Restate the problem

We are given an array of $k$ linked lists. Each individual list is already sorted in ascending order. We need to merge all $k$ lists into a single linked list that is also sorted in ascending order, and return its head.

**Given:** An array of `ListNode` objects, where each represents the head of a sorted linked list.
**Return:** The head of a single, fully merged, sorted linked list.
**Constraint/Relationship:** We must maintain ascending order across all nodes.
**Details:** Duplicates are allowed (they just go next to each other). We should ideally rewire the existing nodes rather than allocating new memory for every value.

### 2. Ask clarifying questions

Before designing the algorithm, I would confirm a few assumptions:

* **Can the input array be empty or null?** (Assumption: Yes, we should handle empty arrays and null inputs gracefully.)
* **Can individual lists inside the array be empty (null)?** (Assumption: Yes, we should skip them.)
* **Can we modify the input lists?** (Assumption: Yes, it is standard in linked list problems to rewire the `next` pointers in-place to achieve $O(1)$ auxiliary space beyond the required data structures.)
* **What is the node definition?** (Assumption: A standard singly-linked list node:)
```java
public class ListNode {
    int val;
    ListNode next;
    ListNode(int x) { val = x; }
}

```



### 3. Work through an example by hand

Let's trace a small example with 3 lists:

* List 1: `1 -> 4 -> 5`
* List 2: `1 -> 3 -> 4`
* List 3: `2 -> 6`

**Step 1:** Look at the head of every list: `[1, 1, 2]`.
**Step 2:** The smallest is `1` (from List 1). We add it to our merged list. We advance List 1.
**Step 3:** Current heads are now: `[4, 1, 2]`.
**Step 4:** The smallest is `1` (from List 2). We add it to our merged list. We advance List 2.
**Step 5:** Current heads: `[4, 3, 2]`.
**Step 6:** Smallest is `2` (from List 3). Add it, advance List 3. Current heads: `[4, 3, 6]`.
**Step 7:** We continue this process until all lists are exhausted.

Final Result: `1 -> 1 -> 2 -> 3 -> 4 -> 4 -> 5 -> 6`.

### 4. Brainstorm solutions aloud

* **Approach 1: Brute Force (Flatten and Sort)**
* *Idea:* Traverse all $k$ lists, extract every value into an `ArrayList`, sort the list, and then build a new linked list.
* *Complexity:* Time $O(N \log N)$ where $N$ is the total number of nodes. Space $O(N)$.
* *Tradeoffs:* Very easy to implement, but ignores the fact that the input lists are already sorted. Highly inefficient for memory.


* **Approach 2: Sequential Merge**
* *Idea:* Merge list 1 and list 2. Then merge the result with list 3. Repeat until list $k$.
* *Complexity:* Time $O(k \cdot N)$. Space $O(1)$.
* *Tradeoffs:* If we have many lists, we end up traversing the nodes from the early lists over and over again.


* **Approach 3: Divide and Conquer**
* *Idea:* Pair up the $k$ lists and merge them (like Merge Sort). This gives $k/2$ lists. Repeat until 1 list remains.
* *Complexity:* Time $O(N \log k)$. Space $O(\log k)$ for the recursive call stack.
* *Tradeoffs:* Excellent time complexity, but requires careful recursive pointer management.


* **Approach 4: Min-Heap (Priority Queue)**
* *Idea:* Exactly follow the manual example. Keep the front node of each list in a min-heap. The heap always holds at most $k$ elements. We repeatedly pop the smallest node, attach it to our result, and push that node's `next` back into the heap.
* *Complexity:* Time $O(N \log k)$. Space $O(k)$ for the heap.
* *Tradeoffs:* Highly readable, idiomatic in Java, scales perfectly, and handles empty lists naturally.



### 5. Select the solution

I will go with the **Min-Heap (Priority Queue)** approach.

* It's easy to explain because it directly maps to the manual "look at all the heads and pick the smallest" logic.
* It uses standard Java collections (`PriorityQueue`).
* The space complexity $O(k)$ is excellent since $k$ (the number of lists) is usually much smaller than $N$ (the total number of nodes).

### 6. Write the implementation outline

```java
ListNode mergeKLists(ListNode[] lists) {
    /*
     * Reframe:
     * Keep track of the current head of every non-empty list. 
     * Always pick the smallest available head to build the result.
     *
     * State:
     * PriorityQueue of ListNode.
     * Chosen because we need fast O(log k) access to the minimum element 
     * out of a dynamic set of k items.
     *
     * Invariant:
     * The priority queue contains exactly the current leading nodes 
     * of all lists that haven't been fully consumed yet.
     *
     * Core logic:
     * - set up a dummy head to easily build the resulting linked list
     * - initialize the min-heap with a custom comparator (compare node values)
     * - iterate through the input array and add the head of each list to the heap
     * - while the heap is not empty:
     *     - pop the smallest node
     *     - attach it to the tail of our merged list
     *     - move the tail pointer forward
     *     - if the popped node has a next element, push next into the heap
     * - return the dummy's next pointer
     *
     * Edge cases:
     * - lists array is null or empty
     * - some or all linked lists inside the array are null (empty)
     */
}

```

### 7. Implement iteratively

**Iteration 1: Method skeleton and data structures**
I'll set up the heap and the dummy node to anchor our result list.

```java
public ListNode mergeKLists(ListNode[] lists) {
    // Edge cases omitted for now
    
    // Set up a min-heap ordered by node value
    PriorityQueue<ListNode> minHeap = new PriorityQueue<>(
        Comparator.comparingInt(node -> node.val)
    );
    
    ListNode dummy = new ListNode(0);
    ListNode current = dummy;

    // TODO: populate initial heads
    // TODO: process heap until empty

    return dummy.next;
}

```

**Iteration 2: Populate the initial heap**
We need to jump-start the algorithm by pushing the first node of every list into the heap.

```java
public ListNode mergeKLists(ListNode[] lists) {
    PriorityQueue<ListNode> minHeap = new PriorityQueue<>(
        Comparator.comparingInt(node -> node.val)
    );
    
    ListNode dummy = new ListNode(0);
    ListNode current = dummy;

    // Added: push the head of each non-empty list into the heap
    for (ListNode head : lists) {
        if (head != null) {
            minHeap.add(head);
        }
    }

    // TODO: process heap until empty

    return dummy.next;
}

```

**Iteration 3: Complete the core loop (Happy path)**
Now we continually pull the smallest node, wire it into our result, and push its successor.

```java
public ListNode mergeKLists(ListNode[] lists) {
    PriorityQueue<ListNode> minHeap = new PriorityQueue<>(
        Comparator.comparingInt(node -> node.val)
    );
    
    ListNode dummy = new ListNode(0);
    ListNode current = dummy;

    for (ListNode head : lists) {
        if (head != null) {
            minHeap.add(head);
        }
    }

    // Added: Core logic to drain the heap and rewire pointers
    while (!minHeap.isEmpty()) {
        // Retrieve the node with the smallest value
        ListNode smallest = minHeap.poll();
        
        // Attach it to our merged list
        current.next = smallest;
        current = current.next;
        
        // If there are more nodes in this specific list, add the next one
        if (smallest.next != null) {
            minHeap.add(smallest.next);
        }
    }

    return dummy.next;
}

```

### 8. Edge-case pass

Let's check the edge cases listed in the outline:

* **`lists` is null or empty (`[]`):** If `lists` is null, the `for (ListNode head : lists)` will throw a `NullPointerException`. I need to patch this at the very beginning. If `lists` is empty, the loop safely skips, the heap is empty, and it returns `dummy.next` (which is `null`—correct).
* **Array contains null lists (e.g., `[null, 1->2]`):** The `if (head != null)` check during initialization handles this perfectly. When the smallest node is polled, we only add `smallest.next` if it is not null, keeping nulls out of our heap.

**Patching the null array:**

```java
if (lists == null || lists.length == 0) {
    return null;
}

```

### Final Code

Here is the clean, patched version of the code, including the node definition for completeness:

```java
class ListNode {
    int val;
    ListNode next;
    ListNode(int x) { val = x; }
}

public class Solution {
    public ListNode mergeKLists(ListNode[] lists) {
        // Handle complete absence of input
        if (lists == null || lists.length == 0) {
            return null;
        }
        
        // Min-heap ordered by the value of the nodes
        PriorityQueue<ListNode> minHeap = new PriorityQueue<>(
            Comparator.comparingInt(node -> node.val)
        );
        
        // Dummy node acts as the reliable start of our merged list
        ListNode dummy = new ListNode(0);
        ListNode current = dummy;

        // Initialize heap with the head of each non-empty list
        for (ListNode head : lists) {
            if (head != null) {
                minHeap.add(head);
            }
        }

        // Process until all nodes from all lists have been merged
        while (!minHeap.isEmpty()) {
            ListNode smallest = minHeap.poll();
            
            // Link the smallest node to the end of our merged list
            current.next = smallest;
            current = current.next;
            
            // Push the next node from the list we just pulled from
            if (smallest.next != null) {
                minHeap.add(smallest.next);
            }
        }

        // Return the actual head of the merged list
        return dummy.next;
    }
}

```

### Complexity

* **Time Complexity:** $O(N \log k)$, where $N$ is the total number of nodes across all lists, and $k$ is the number of lists. The priority queue never holds more than $k$ elements. Polling from and adding to a heap of size $k$ takes $O(\log k)$. We do this exactly $N$ times.
* **Space Complexity:** $O(k)$ auxiliary space. The only extra memory we allocate is the `PriorityQueue`, which stores at most $k$ nodes at any given time. We rewire the original nodes in place, so no new `ListNode` objects are created (besides the single $O(1)$ dummy node).

### Brief test walkthrough

* **Test 1: Empty Array `[]**`
* Input is empty.
* The `if (lists == null || lists.length == 0)` check catches this.
* Result: returns `null`. Correct.


* **Test 2: Two lists: `[1->4]`, `[2->3]**`
* Heap init: adds `1` and `2`. Heap: `[1, 2]`.
* Loop 1: Poll `1`. `current` points to `1`. Push `4` (since `1.next == 4`). Heap: `[2, 4]`.
* Loop 2: Poll `2`. `current.next` points to `2`. Push `3` (since `2.next == 3`). Heap: `[3, 4]`.
* Loop 3: Poll `3`. `current.next` points to `3`. Push nothing (`3.next == null`). Heap: `[4]`.
* Loop 4: Poll `4`. Push nothing. Heap is empty.
* Result: `dummy.next` returns the sequence `1 -> 2 -> 3 -> 4`. Correct.