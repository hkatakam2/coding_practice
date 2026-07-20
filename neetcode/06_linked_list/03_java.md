### 1. Restate the problem

We are given the starting node (`head`) of a singly linked list. We need to determine if the list contains a cycle.

A cycle occurs if following the `next` pointers eventually leads back to a node we have already visited, meaning the list never terminates at `null`. We must return `true` if a cycle exists, and `false` otherwise. The `index` mentioned in the prompt is just for conceptualizing how the cycle is formed under the hood; we only receive the `head` node.

### 2. Ask clarifying questions

Before writing code, I'd like to confirm a few details to ensure we cover all bases:

* **Empty list:** Can the list be empty (`head == null`)? I will assume yes, and it should return `false`.
* **Single node:** Can a list have exactly one node? I will assume yes. If it points to `null`, it's `false`. If it points to itself, it's `true`.
* **Modification:** Are we allowed to modify the list structures (e.g., changing values or pointers to mark them as visited)? I will assume we should not mutate the input list, as it might be used by other parts of the application.
* **Maximum size:** Is there a risk of memory overflow if we store visited nodes, or is there a tight memory constraint? I will assume standard constraints (e.g., up to $10^4$ nodes), but I will aim for the most space-efficient solution.

### 3. Work through an example by hand

Let's trace a list that has a cycle.
Suppose the list is: `3 -> 2 -> 0 -> -4`, and `-4` points back to `2`.

If we iterate one by one, we get: `3, 2, 0, -4, 2, 0, -4...` going on forever.
Because we don't know the list's length beforehand, we need a way to detect this infinite loop.

Let's imagine sending two runners down the list, one slow and one fast.

* **Slow runner** takes 1 step at a time.
* **Fast runner** takes 2 steps at a time.

**Initialization:**
Both start at `3`. (Slow = 3, Fast = 3)

**Step 1:**
Slow moves to `2`.
Fast moves to `0`.

**Step 2:**
Slow moves to `0`.
Fast moves to `2` (from `0` -> `-4` -> `2`).

**Step 3:**
Slow moves to `-4`.
Fast moves to `-4` (from `2` -> `0` -> `-4`).

Both runners are on node `-4`. Because they collided, we know definitively that a cycle exists. If there was no cycle, the fast runner would have just reached the `null` at the end of the list.

### 4. Brainstorm solutions aloud

**Approach 1: HashMap / HashSet (Direct Simulation)**
The most straightforward approach is to simulate moving through the list and remembering every node we've seen.

* **Core idea:** Traverse the list, adding each node's reference to a `HashSet`. If we encounter a node that is already in the set, we found a cycle. If we reach `null`, there is no cycle.
* **Complexity:** Time $O(N)$ to traverse. Space $O(N)$ to store references in the set.
* **Tradeoffs:** It's very easy to implement, but it uses extra memory proportional to the list size.

**Approach 2: Floyd's Cycle-Finding Algorithm (Two Pointers)**
This matches our manual example.

* **Core idea:** Use a `slow` pointer and a `fast` pointer. The fast pointer moves twice as fast. If there is a cycle, the fast pointer loops around and eventually catches the slow pointer from behind. If there is no cycle, the fast pointer hits `null`.
* **Complexity:** Time $O(N)$. If there is no cycle, the fast pointer reaches the end in $N/2$ steps. If there is a cycle, the fast pointer laps the slow pointer in at most $N$ steps. Space $O(1)$ because we only store two references.
* **Tradeoffs:** Much better space complexity. The logic is slightly less intuitive than a `HashSet` at first glance, but it is the industry standard for this specific problem.

### 5. Select the solution

I will use **Floyd's Cycle-Finding Algorithm (Two Pointers)**.
It provides the optimal $O(1)$ space complexity while remaining strictly $O(N)$ in time. Since we only need to return a boolean indicating *if* a cycle exists (not the cycle's starting index), two pointers tracking distance are a perfect fit.

### 6. Write the implementation outline

```java
boolean hasCycle(ListNode head) {
    /*
     * Reframe:
     * Detect if a path traverses the same node twice without allocating O(N) memory.
     *
     * State:
     * Two pointers, `slow` and `fast`.
     * Chosen because if a cycle exists, the faster pointer will eventually lap 
     * the slower one, proving an infinite loop exists.
     *
     * Invariant:
     * `slow` is always strictly behind or on the same node as `fast`. If they ever 
     * point to the exact same memory address after leaving the start line, a cycle exists.
     *
     * Core logic:
     * - initialize `slow` and `fast` pointers at the head of the list
     * - loop as long as `fast` and `fast.next` are not null
     * - move `slow` forward by 1 node
     * - move `fast` forward by 2 nodes
     * - return true immediately if `slow` == `fast`
     * - return false if the loop terminates (fast reached the end)
     *
     * Edge cases:
     * - empty list (head is null)
     * - list with 1 node pointing to null
     * - list with 1 node pointing to itself
     */
}

```

### 7. Implement iteratively

*(Assuming a standard `ListNode` definition exists for compilation purposes:)*

```java
class ListNode {
    int val;
    ListNode next;
    ListNode(int x) { val = x; next = null; }
}

```

**Iteration 1: Method skeleton**
First, let's set up the basic state variables and control flow.

```java
public boolean hasCycle(ListNode head) {
    // Both runners start at the beginning of the list.
    ListNode slow = head;
    ListNode fast = head;

    // TODO: loop through the list
    // TODO: advance pointers at different speeds
    // TODO: check for collision

    // If we exit the loop, we hit a null, meaning no cycle.
    return false;
}

```

*I set both to `head`. The loop will act as the track.*

**Iteration 2: Implement the core loop**
Now I'll add the traversal logic. We need to check `fast != null` and `fast.next != null` to safely jump two steps.

```java
public boolean hasCycle(ListNode head) {
    ListNode slow = head;
    ListNode fast = head;

    // Added: traverse as long as we can safely look 2 steps ahead.
    while (fast != null && fast.next != null) {
        slow = slow.next;          // 1 step
        fast = fast.next.next;     // 2 steps

        // Added: collision check
        if (slow == fast) {
            return true;
        }
    }

    return false;
}

```

**Edge-case pass**
Let's review the edge cases identified in our outline against our current code.

1. **Empty list (`head == null`):**
* `slow = null`, `fast = null`.
* The `while (fast != null)` condition immediately evaluates to false.
* Returns `false`. Correct.


2. **Single node, no cycle (`head -> null`):**
* `slow = head`, `fast = head`.
* `fast != null` is true, but `fast.next != null` evaluates to false.
* Loop bypassed, returns `false`. Correct.


3. **Single node, with cycle (`head -> head`):**
* Loop starts. `fast != null` and `fast.next != null` (both are true).
* `slow = head.next` (which is head).
* `fast = head.next.next` (which is head).
* `slow == fast` evaluates to true. Returns `true`. Correct.



No code changes are necessary to handle the edge cases! The condition `fast != null && fast.next != null` perfectly encapsulates all null-safety checks required.

### 8. Analyze expensive sections and optimize

This code is already highly optimized.

* **Time Complexity:** $O(N)$.
* If there is no cycle, `fast` pointer reaches the end in exactly $N/2$ iterations.
* If there is a cycle of length $K$ and a straight path of length $M$ leading up to it, `slow` takes $M$ steps to reach the cycle. By then, `fast` is already inside the cycle. `fast` closes the gap on `slow` by 1 node per iteration. The gap is at most $K$. Thus, the maximum number of iterations is bounded by $M + K$, which is at most $N$. Time is strictly $O(N)$.


* **Space Complexity:** $O(1)$. We are only creating two local pointer variables (`slow` and `fast`), regardless of the size of the linked list.

There are no nested loops, object creations, recursive calls, or heavy library imports.

### Final Code

```java
/**
 * Definition for singly-linked list.
 * class ListNode {
 *     int val;
 *     ListNode next;
 *     ListNode(int x) {
 *         val = x;
 *         next = null;
 *     }
 * }
 */
public class Solution {
    public boolean hasCycle(ListNode head) {
        ListNode slow = head;
        ListNode fast = head;

        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
            
            if (slow == fast) {
                return true;
            }
        }
        
        return false;
    }
}

```

### Brief test walkthrough

Let's mentally test one more acyclic case to stress the invariant: `1 -> 2 -> 3 -> null`.

1. **Init:** `slow` at 1, `fast` at 1.
2. **Loop Condition:** `fast` (1) != null, `fast.next` (2) != null. (Proceed)
3. **Move:** `slow` moves to 2, `fast` jumps to 3. (1 step vs 2 steps).
4. **Check:** `slow` (2) != `fast` (3).
5. **Loop Condition:** `fast` (3) != null, but `fast.next` is `null`. (Terminate loop)
6. **Return:** `false`.

The logic behaves exactly as expected, safely preventing `NullPointerException` when attempting to step `fast.next.next` by checking `fast.next` in the while loop condition beforehand.