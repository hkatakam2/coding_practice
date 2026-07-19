### 1. Restate the problem

We are given the heads of two linked lists that are already sorted in ascending order. We need to merge them into a single sorted linked list. The catch is that we cannot create new nodes for the data; we must reuse the existing nodes from `list1` and `list2` by rearranging their `next` pointers. We then return the head of this newly merged list.

### 2. Ask clarifying questions

In a real interview, I would confirm a few details to ensure my assumptions are correct:

* **Can the lists be empty?** (Assumption: Yes. If both are empty, return `null`. If one is empty, return the other.)
* **Can there be duplicate values?** (Assumption: Yes, we should retain all duplicates.)
* **Can there be negative numbers?** (Assumption: Yes, standard integer rules apply.)
* **Are we allowed to destroy the original lists?** (Assumption: Yes, the problem says "splicing together the nodes," which implies destructive modification of the original `next` pointers.)
* **Is there a constraint on the number of nodes?** (Assumption: Could be up to $10^5$, meaning we should avoid $O(N)$ auxiliary space like recursion depth to prevent stack overflows.)

Since we don't have an interviewer to answer, I will proceed with these assumptions.

### 3. Work through an example by hand

Let's take two lists:
`list1`: `1 -> 2 -> 4`
`list2`: `1 -> 3 -> 4`

We need a way to keep track of the start of our merged list, and a pointer to the current end of the merged list.

* **Start**: `dummy` node. `current` points to `dummy`.
* **Step 1**: Compare `list1` (1) and `list2` (1). They are equal. Pick `list1`'s node.
`current.next = list1` (1)
Move `list1` to 2. Move `current` to 1.
* **Step 2**: Compare `list1` (2) and `list2` (1). Pick `list2` (1).
`current.next = list2` (1)
Move `list2` to 3. Move `current` to 1.
* **Step 3**: Compare `list1` (2) and `list2` (3). Pick `list1` (2).
`current.next = list1` (2)
Move `list1` to 4. Move `current` to 2.
* **Step 4**: Compare `list1` (4) and `list2` (3). Pick `list2` (3).
`current.next = list2` (3)
Move `list2` to 4. Move `current` to 3.
* **Step 5**: Compare `list1` (4) and `list2` (4). Pick `list1` (4).
`current.next = list1` (4)
Move `list1` to `null`. Move `current` to 4.
* **Step 6**: `list1` is exhausted. We append the rest of `list2` (which is the node 4).
`current.next = list2` (4).
* **Result**: Return `dummy.next`, which points to `1 -> 1 -> 2 -> 3 -> 4 -> 4`.

### 4. Brainstorm solutions aloud

**Approach 1: Recursive**

* **Core idea**: `merge(l1, l2)` returns `l1` if `l1.val < l2.val`, with `l1.next` pointing to `merge(l1.next, l2)`.
* **Time complexity**: $O(n + m)$, where $n$ and $m$ are the lengths of the lists. We process one node per call.
* **Space complexity**: $O(n + m)$ due to the recursion stack.
* **Tradeoffs**: Very elegant and short to write, but dangerous for large lists (e.g., $10^5$ nodes) as it will throw a `StackOverflowError`.

**Approach 2: Iterative with a Dummy Node**

* **Core idea**: Use a dummy head to simplify edge cases (like the first node insertion). Iterate while both lists have nodes, comparing and linking the smaller node to our `current` pointer. Once one list is exhausted, link the remaining list to the end.
* **Time complexity**: $O(n + m)$. We visit each node at most once.
* **Space complexity**: $O(1)$. We only use a few pointers (`dummy`, `current`).
* **Tradeoffs**: Slightly more code than recursion, but robust, scalable, and safe from stack overflows.

### 5. Select the solution

I will choose **Approach 2 (Iterative with a Dummy Node)**. It is the most robust solution for production Java environments because it uses $O(1)$ auxiliary space. The dummy node elegantly eliminates the need for special `if (head == null)` checks at the beginning of the merge process.

### 6. Write the implementation outline

```java
ListNode mergeTwoLists(ListNode list1, ListNode list2) {
    /*
     * Reframe:
     * Walk through both sorted lists simultaneously, picking the smaller node 
     * at each step to build a single continuously sorted list.
     *
     * State:
     * dummyHead: A placeholder node to anchor the start of our merged list.
     * current: A pointer tracking the last merged node.
     * Chosen because:
     * A dummy node prevents complex null-checking for the very first insertion.
     *
     * Invariant:
     * All nodes from dummyHead up to current are sorted, and current is the 
     * tail of the merged list so far.
     *
     * Core logic:
     * - create dummyHead and point current to it
     * - while both list1 and list2 have nodes left to process:
     *     - if list1's value is smaller, attach list1 to current and advance list1
     *     - otherwise, attach list2 to current and advance list2
     *     - advance current
     * - attach whichever list still has remaining nodes to current.next
     * - return dummyHead.next (the true start of the list)
     *
     * Edge cases:
     * - list1 is null
     * - list2 is null
     * - both are null
     * - lists of unequal lengths
     */
}

```

### 7. Implement iteratively

**Iteration 1: Method skeleton**
I'll set up the dummy node, the `current` pointer, and the broad control flow.

```java
class Solution {
    public ListNode mergeTwoLists(ListNode list1, ListNode list2) {
        ListNode dummyHead = new ListNode(-1);
        ListNode current = dummyHead;
        
        // TODO: iterate while both lists are not null
        // TODO: attach the remaining elements of the non-empty list
        
        return dummyHead.next;
    }
}

```

*Why this skeleton?* It sets up our $O(1)$ state. We use `-1` for the dummy node's value, though any value is fine since it's never included in the result.

**Iteration 2: Core loop logic**
Now I'll implement the main traversal and comparison.

```java
class Solution {
    public ListNode mergeTwoLists(ListNode list1, ListNode list2) {
        ListNode dummyHead = new ListNode(-1);
        ListNode current = dummyHead;
        
        // Added: loop to compare and splice nodes
        while (list1 != null && list2 != null) {
            if (list1.val <= list2.val) {
                current.next = list1;
                list1 = list1.next;
            } else {
                current.next = list2;
                list2 = list2.next;
            }
            current = current.next;
        }
        
        // TODO: attach the remaining elements of the non-empty list
        
        return dummyHead.next;
    }
}

```

*Invariant update:* After each iteration of the `while` loop, `current` points to the highest value currently in the merged list, and `current.next` is ready to receive the next node.

**Iteration 3: Complete the happy path**
Once the loop terminates, at least one of the lists is `null`. The other list might still have remaining nodes, which are already sorted and larger than everything processed so far.

```java
class Solution {
    public ListNode mergeTwoLists(ListNode list1, ListNode list2) {
        ListNode dummyHead = new ListNode(-1);
        ListNode current = dummyHead;
        
        while (list1 != null && list2 != null) {
            if (list1.val <= list2.val) {
                current.next = list1;
                list1 = list1.next;
            } else {
                current.next = list2;
                list2 = list2.next;
            }
            current = current.next;
        }
        
        // Added: attach whichever list is not null. 
        // If both are null, this safely attaches null.
        if (list1 != null) {
            current.next = list1;
        } else {
            current.next = list2;
        }
        
        return dummyHead.next;
    }
}

```

**Edge-case pass**
Let's check the edge cases from the outline:

* *Both lists are empty (`list1 = null, list2 = null`)*: The `while` loop is skipped. `current.next` is set to `list2` (which is `null`). Returns `dummyHead.next` which is `null`. Correct.
* *One list is empty (`list1 = null, list2 = 1->2`)*: `while` loop skipped. `current.next` set to `list2`. Returns `1->2`. Correct.
* *Unequal lengths*: The loop terminates when the shorter list is exhausted. The `if/else` block safely appends the entirety of the remaining longer list in $O(1)$ time. Correct.

The iterative approach naturally handles all edge cases without requiring explicit upfront guard clauses (like `if (list1 == null) return list2;`).

### 8. Analyze expensive sections and optimize

* **Time Complexity**: $O(n + m)$, where $n$ and $m$ are the lengths of `list1` and `list2`. We do exactly one comparison per node appended, and the loop runs until one list is exhausted. Appending the remainder takes $O(1)$ operations.
* **Space Complexity**: $O(1)$. We allocate exactly one `ListNode` (the dummy head) and use a few object references (`current`, `list1`, `list2`). We do not instantiate any new nodes for the data.

There are no nested loops, expensive allocations, or recursive calls. This is the optimal solution.

### Final code

Here is the clean, final version:

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
    public ListNode mergeTwoLists(ListNode list1, ListNode list2) {
        ListNode dummyHead = new ListNode(0);
        ListNode current = dummyHead;

        while (list1 != null && list2 != null) {
            if (list1.val <= list2.val) {
                current.next = list1;
                list1 = list1.next;
            } else {
                current.next = list2;
                list2 = list2.next;
            }
            current = current.next;
        }

        if (list1 != null) {
            current.next = list1;
        } else {
            current.next = list2;
        }

        return dummyHead.next;
    }
}

```

### Brief test walkthrough

* **Main example**: `list1 = [1, 2, 4]`, `list2 = [1, 3, 4]`.
* Compare 1 & 1 $\rightarrow$ link 1, advance `list1`.
* Compare 2 & 1 $\rightarrow$ link 1, advance `list2`.
* Compare 2 & 3 $\rightarrow$ link 2, advance `list1`.
* Compare 4 & 3 $\rightarrow$ link 3, advance `list2`.
* Compare 4 & 4 $\rightarrow$ link 4, advance `list1`.
* `list1` is null. Loop ends. Attach remaining `list2` (4). Result: `[1, 1, 2, 3, 4, 4]`. (Pass)


* **Smallest valid input**: `list1 = []`, `list2 = []`.
* Loop skips. `list1` is null, so attach `list2` (null). Returns null. (Pass)


* **One empty**: `list1 = []`, `list2 = [0]`.
* Loop skips. `list1` is null, attach `list2`. Returns `[0]`. (Pass)