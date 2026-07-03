### question
You are given the head of a linked list of length n. Unlike a singly linked list, each node contains an additional pointer random, which may point to any node in the list, or null.

Create a deep copy of the list.

## 1. Restate the problem

We have a linked list where every node has:

```python
val
next
random
```

`next` points to the next node.
`random` can point to **any node in the same list**, or `None`.

We need to create a **deep copy**.

That means:

Original nodes and copied nodes must be different objects.

So this is **not allowed**:

```python
copy.random = original.random
```

because that would point back into the original list.

---

## 2. Clarifying questions

In interview, I would confirm:

1. Can `random` point to `None`?
   Yes.

2. Can `random` point to itself?
   Yes.

3. Can values repeat?
   Yes, so we cannot use `val` as the key.

4. Should original list remain unchanged?
   Yes.

5. Return value?
   Return the head of the copied list.

---

## 3. Example by hand

Suppose:

```text
A(val=7) -> B(val=13) -> C(val=11) -> None

A.random = None
B.random = A
C.random = A
```

We need:

```text
A'(val=7) -> B'(val=13) -> C'(val=11) -> None

A'.random = None
B'.random = A'
C'.random = A'
```

Important:

```text
B'.random should point to A', not A
C'.random should point to A', not A
```

So we need a way to say:

```text
old A maps to new A'
old B maps to new B'
old C maps to new C'
```

That naturally suggests a hash map.

---

## 4. Brainstorm solutions

### Solution 1: Hash map, two passes

Pass 1:

Create a copied node for every original node.

```text
old node -> copied node
```

Pass 2:

Use the map to connect copied `next` and copied `random`.

This is the cleanest interview solution.

Time:

```text
O(n)
```

Space:

```text
O(n)
```

---

### Solution 2: Weave copied nodes into original list

Example:

```text
A -> B -> C
```

becomes:

```text
A -> A' -> B -> B' -> C -> C'
```

Then assign random pointers using:

```text
copy.random = original.random.next
```

Then separate the two lists.

Time:

```text
O(n)
```

Extra space:

```text
O(1)
```

But it is trickier and temporarily modifies the original list.

---

### Selected solution

Use **hash map two-pass** because it is simple, clear, and easy to explain.

---

## 5. Implementation outline

```python
def copyRandomList(head):  # -> Node
    """
    Reframe: random pointers make this a graph-copy problem, but next gives us a simple traversal order.

    State: old_to_copy map, chosen because each original node must correspond to exactly one copied node.
        This exploits object identity, not node values.

    Invariant: after the first pass, every original node has a copied node.
    After the second pass, every copied node has correct next and random pointers.

    makeCopy(node) = create a new node with the same value as node.
    getCopy(node) = return the copied version of node, or None when node is None.

    Core logic:
    - handle empty list
    - walk through the original list once
    - create one copied node for each original node
    - store the old-node to copied-node relationship
    - walk through the original list again
    - for each original node, find its copy
    - connect the copy's next to the copy of the original next
    - connect the copy's random to the copy of the original random
    - return the copy of the original head

    Edge cases:
    - empty list
    - one node with random as None
    - one node with random pointing to itself
    - random points backward
    - random points forward
    - multiple nodes point random to the same node
    - duplicate values
    """
```

---

## 6. Iterative implementation

### Iteration 1: skeleton

```python
def copyRandomList(head):
    if head is None:
        return None

    old_to_copy = {}

    # pass 1: create copied nodes

    # pass 2: connect copied nodes

    return old_to_copy[head]
```

---

### Iteration 2: create all copied nodes

```python
def copyRandomList(head):
    if head is None:
        return None

    old_to_copy = {}

    curr = head
    while curr:
        old_to_copy[curr] = Node(curr.val)
        curr = curr.next

    # pass 2: connect copied nodes

    return old_to_copy[head]
```

Now we have copied nodes, but they are not connected yet.

---

### Iteration 3: connect `next` and `random`

One issue:

```python
curr.next
```

may be `None`.

Same with:

```python
curr.random
```

So add:

```python
old_to_copy[None] = None
```

That removes special-case checks.

```python
def copyRandomList(head):
    if head is None:
        return None

    old_to_copy = {None: None}

    curr = head
    while curr:
        old_to_copy[curr] = Node(curr.val)
        curr = curr.next

    curr = head
    while curr:
        copy = old_to_copy[curr]
        copy.next = old_to_copy[curr.next]
        copy.random = old_to_copy[curr.random]
        curr = curr.next

    return old_to_copy[head]
```

---

## 7. Final code

```python
class Node:
    def __init__(self, val: int = 0, next: "Node" = None, random: "Node" = None):
        self.val = val
        self.next = next
        self.random = random


def copyRandomList(head: "Node") -> "Node":
    """
    Deep copy a linked list where each node has next and random pointers.

    Approach:
    1. First pass: create a copied node for every original node.
    2. Second pass: wire copied next and copied random using the map.

    Time: O(n)
    Space: O(n)
    """
    if head is None:
        return None

    old_to_copy = {None: None}

    # First pass: create all copied nodes.
    curr = head
    while curr:
        old_to_copy[curr] = Node(curr.val)
        curr = curr.next

    # Second pass: connect next and random pointers.
    curr = head
    while curr:
        copy = old_to_copy[curr]

        copy.next = old_to_copy[curr.next]
        copy.random = old_to_copy[curr.random]

        curr = curr.next

    return old_to_copy[head]
```

---

## 8. Complexity

Let `n` be the number of nodes.

First pass visits every node once:

```text
O(n)
```

Second pass visits every node once:

```text
O(n)
```

Total time:

```text
O(n)
```

The hash map stores one entry per original node:

```text
O(n)
```

Final:

```text
Time:  O(n)
Space: O(n)
```

The key insight: **use the original node object as the key, not the node value**, because values can repeat but node identities are unique.
