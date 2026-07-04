### question
You are given an array of k linked lists lists, where each list is sorted in ascending order.

Return the sorted linked list that is the result of merging all of the individual linked lists.

### 1. Restate

Combine multiple separate, pre-sorted linked lists into one single, fully sorted linked list.

### 2. Clarify Inputs & Outputs

* **Input:** Array/List of `k` linked list heads.
* **Output:** Head of the final merged linked list.
* **Empty inputs?** Array can be empty. Individual lists can be empty.
* **In-place?** Yes, reuse existing nodes. Just rewire `next` pointers.

### 3. Example by Hand

Input: `[[1->4->5], [1->3->4], [2->6]]`

* Current heads: `1`, `1`, `2`.
* Smallest is `1` (from list 1). Extract. List 1 is now `4->5`.
* Current heads: `4`, `1`, `2`.
* Smallest is `1` (from list 2). Extract. List 2 is now `3->4`.
* Current heads: `4`, `3`, `2`.
* Smallest is `2` (from list 3). Extract. List 3 is now `6`.
* Continue until all lists empty. Output: `1->1->2->3->4->4->5->6`.

### 4. Brainstorm & Complexity

* **Brute Force:** Collect all node values in an array, sort array, build new list.
* Time: $O(N \log N)$ where $N$ is total nodes. Space: $O(N)$.


* **Iterative Compare (Matches Step 3):** Look at all `k` heads every time. Find min.
* Time: $O(N \cdot k)$ because finding min takes $O(k)$ for $N$ nodes. Space: $O(1)$.


* **Min-Heap:** Optimize iterative compare. Store `k` heads in a min-heap.
* Time: $O(N \log k)$ because extracting/pushing takes $O(\log k)$. Space: $O(k)$ for heap.


* **Divide & Conquer:** Merge pairs of lists. Merge lists 1&2, 3&4, etc. Then merge the results.
* Time: $O(N \log k)$. Space: $O(1)$ if done iteratively.



### 5. Suggest Solutions

Min-Heap is simplest, clearest, and directly maps to our manual simulation. We will implement Min-Heap. Divide & Conquer is mathematically elegant but conceptually harder to trace quickly.

### 6. Outline (Core Logic & Edge Cases)

```python
def mergeKLists(lists):
    """
    Reframe: Repeatedly find and extract global minimum among current list heads.
    State: Min-heap of nodes, chosen because we need fast repeated access to minimum of dynamic set.
    Invariant: Heap always contains exactly the current head of every non-empty list.

    push_to_heap(heap, node) = adds node to heap, prioritized by node value.
    pop_min(heap) = removes and returns node with smallest value.

    Core logic:
    - Initialize min-heap.
    - Put head of every list into heap.
    - Setup dummy head and tail pointer to build result list.
    - While heap has nodes:
      - Get smallest node from heap.
      - Attach to tail of result list.
      - If extracted node has a next node, put next node into heap.
      - Advance tail pointer.
      
    Edge cases:
    - Lists array is empty.
    - Arrays contain empty lists (None).
    """

```

### 7. Iterative Implementation

**Iteration 1: Skeleton with helpers**

```python
import heapq

def mergeKLists(lists):
    heap = []
    
    # Init heap
    for l in lists:
        push_to_heap(heap, l)
        
    dummy = ListNode()
    tail = dummy
    
    # Process
    while heap:
        smallest_node = pop_min(heap)
        tail.next = smallest_node
        tail = tail.next
        
        if smallest_node.next:
            push_to_heap(heap, smallest_node.next)
            
    return dummy.next

```

**Iteration 2: Fleshing out Core Logic (Python specifics)**
*Issue:* Python `heapq` compares tuple elements in order. If values tie, it compares nodes, which throws `TypeError` without `__lt__`.
*Fix:* Push `(node.val, list_index, node)` to ensure unique tie-breaker.

```python
import heapq

def mergeKLists(lists):
    heap = []
    
    # CHANGED: Added index 'i' to handle tie-breakers in Python heap
    for i, l in enumerate(lists):
        heapq.heappush(heap, (l.val, i, l))
        
    dummy = ListNode()
    tail = dummy
    
    while heap:
        # CHANGED: unpack tuple
        val, i, smallest_node = heapq.heappop(heap)
        
        tail.next = smallest_node
        tail = tail.next
        
        if smallest_node.next:
            # CHANGED: Push next node with same list index
            heapq.heappush(heap, (smallest_node.next.val, i, smallest_node.next))
            
    return dummy.next

```

**Iteration 3: Patching Edge Cases**
*Edge cases:* What if `lists` is empty? What if `l` is `None`? `l.val` will throw AttributeError.

```python
import heapq

# Assuming ListNode is defined:
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

def mergeKLists(lists):
    heap = []
    
    for i, l in enumerate(lists):
        if l: # PATCH: Only push non-empty lists
            heapq.heappush(heap, (l.val, i, l))
            
    dummy = ListNode()
    tail = dummy
    
    while heap:
        val, i, smallest_node = heapq.heappop(heap)
        
        tail.next = smallest_node
        tail = tail.next
        
        if smallest_node.next:
            heapq.heappush(heap, (smallest_node.next.val, i, smallest_node.next))
            
    return dummy.next

```

### 8. Complexity & Optimization

* **Time Complexity:** $O(N \log k)$. Pushing/popping from heap takes $O(\log k)$. We do this for all $N$ nodes.
* **Space Complexity:** $O(k)$. The heap stores at most `k` elements at any time.

*Optimization via Divide & Conquer:*
If interviewer pushes back on $O(k)$ space requirement, we can optimize space to $O(1)$ by using iterative Divide & Conquer.
*Idea:* Reuse standard `mergeTwoLists` helper. Iteratively merge lists in pairs (0 & 1, 2 & 3...). Append merged lists to end of array, keep traversing.
*Tradeoff:* Space drops to $O(1)$, but time remains $O(N \log k)$. Code is slightly less intuitive to write out cleanly without state-tracking bugs, making Min-Heap the safer "plain english" interview choice.