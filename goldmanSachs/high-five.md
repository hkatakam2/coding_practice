### question
Given a list of scores of different students, return the average score of each student's top five scores in the order of each student's id.

Each entry items[i] has items[i][0] the student's id, and items[i][1] the student's score.  The average score is calculated using integer division.

 

Example 1:

Input: [[1,91],[1,92],[2,93],[2,97],[1,60],[2,77],[1,65],[1,87],[1,100],[2,100],[2,76]]
Output: [[1,87],[2,88]]
Explanation: 
The average of the student with id = 1 is 87.
The average of the student with id = 2 is 88.6. But with integer division their average converts to 88.
 

Note:

1 <= items.length <= 1000
items[i].length == 2
The IDs of the students is between 1 to 1000
The score of the students is between 1 to 100
For each student, there are at least 5 scores

## 1. Restate the problem

We receive pairs:

```text
[studentId, score]
```

For every student:

* find their **5 highest scores**
* compute `sum(top 5) // 5`
* return `[studentId, average]`
* results must be ordered by `studentId`

---

## 2. Clarifying questions

In an interview, I would confirm:

1. Does every student have at least 5 scores? **Yes.**
2. Should we use integer division? **Yes.**
3. Can the input be unsorted? **Yes.**
4. Should output be sorted by student ID? **Yes.**
5. Can the same score occur multiple times? **Yes; each occurrence counts separately.**

---

## 3. Work the example by hand

Input for student `1`:

```text
91, 92, 60, 65, 87, 100
```

Sort descending:

```text
100, 92, 91, 87, 65, 60
```

Top 5:

```text
100 + 92 + 91 + 87 + 65 = 435
435 // 5 = 87
```

Student `2`:

```text
93, 97, 77, 100, 76
```

All five:

```text
100 + 97 + 93 + 77 + 76 = 443
443 // 5 = 88
```

Result:

```text
[[1,87],[2,88]]
```

---

# 4. Brainstorm solutions

### Solution A — group + sort

Store every student's scores:

```text
1 -> [91,92,60,65,87,100]
2 -> [93,97,77,100,76]
```

Then sort each student's scores descending and take the first 5.

Very straightforward.

Complexity:

```text
O(n log n)
```

worst case if one student owns most scores.

Space:

```text
O(n)
```

### Solution B — maintain a min-heap of size 5

We don't actually care about scores outside the top five.

For each student maintain:

```text
minHeap containing their current best 5 scores
```

When a new score arrives:

```text
heap has < 5 scores
    add it

heap already has 5
    if new score > smallest top-five score
        replace smallest
```

The heap's minimum represents:

> the weakest score currently qualifying for that student's top five.

Because heap size is always at most `5`, each heap operation is:

```text
O(log 5) = O(1)
```

Overall:

```text
Time:  O(n + s log s)
Space: O(s)
```

where `s` = number of students.

I would choose **Solution B** because it directly models the requirement: retain only the five scores we care about.

---

# 5. Core idea

For each student:

```text
keep only their best five scores seen so far
```

A size-5 min-heap makes it easy to discard the weakest score whenever a better score appears.

---

# 6. Implementation outline

```python
def high_five(items):  # -> list[list[int]]
    """
    Reframe:
        We never need more than the best five scores for any student.

    State:
        student_id -> min-heap of at most five scores.

        A min-heap is useful because the smallest of the current
        top-five scores is exactly the score we may need to replace.

    Invariant:
        After processing any number of entries, each student's heap
        contains their five highest scores seen so far, or all scores
        if fewer than five have been seen.

    add_score(student, score):
        Update that student's heap while keeping at most five scores.

    Core logic:
        - process every student-score pair
        - maintain the student's five best scores
        - process students in increasing ID order
        - average the five retained scores
        - append student ID and average to the result

    Edge cases:
        - student has exactly five scores
        - student has more than five scores
        - duplicate scores
        - incoming score is smaller than all current top-five scores
        - incoming score equals the smallest current top-five score
        - multiple students
        - input order is arbitrary
    """
```

---

# 7. Iteratively turn it into code

### Iteration 1 — skeleton

```python
def high_five(items):
    student_scores = {}

    # process all scores
    for student_id, score in items:
        update_top_five(student_scores, student_id, score)

    result = []

    # calculate averages
    for student_id in sorted(student_scores):
        average = calculate_average(student_scores[student_id])
        result.append([student_id, average])

    return result
```

The main algorithm already reads almost exactly like English.

Now implement the difficult part: maintaining top five.

---

### Iteration 2 — create each student's heap

```python
import heapq


def high_five(items):
    student_scores = {}

    for student_id, score in items:

        # create heap when student appears for first time
        if student_id not in student_scores:
            student_scores[student_id] = []

        heap = student_scores[student_id]

        # TODO: keep only top five

    result = []

    for student_id in sorted(student_scores):
        average = sum(student_scores[student_id]) // 5
        result.append([student_id, average])

    return result
```

---

### Iteration 3 — fill the first five scores

While there are fewer than five scores:

```python
heapq.heappush(heap, score)
```

```python
import heapq


def high_five(items):
    student_scores = {}

    for student_id, score in items:

        if student_id not in student_scores:
            student_scores[student_id] = []

        heap = student_scores[student_id]

        # First five scores automatically qualify.
        if len(heap) < 5:
            heapq.heappush(heap, score)

        # TODO: handle additional scores

    result = []

    for student_id in sorted(student_scores):
        average = sum(student_scores[student_id]) // 5
        result.append([student_id, average])

    return result
```

---

### Iteration 4 — handle scores after the first five

Suppose heap contains:

```text
[65, 87, 91, 92, 100]
 ^
 smallest
```

New score:

```text
95
```

`65` should leave and `95` should enter.

Python provides exactly this operation:

```python
heapq.heapreplace(heap, score)
```

Final core implementation:

```python
import heapq


def high_five(items):
    student_scores = {}

    for student_id, score in items:

        if student_id not in student_scores:
            student_scores[student_id] = []

        heap = student_scores[student_id]

        if len(heap) < 5:
            heapq.heappush(heap, score)

        elif score > heap[0]:
            heapq.heapreplace(heap, score)

    result = []

    for student_id in sorted(student_scores):
        average = sum(student_scores[student_id]) // 5
        result.append([student_id, average])

    return result
```

---

# 8. Walk through edge cases

### Exactly five scores

```text
[90,80,70,60,50]
```

All five enter the heap. Nothing special required.

### More than five scores

```text
90,80,70,60,50,100
```

Before `100`:

```text
50,60,70,80,90
```

`100 > 50`, so replace `50`.

Top five become:

```text
60,70,80,90,100
```

Correct.

### New score is too small

Heap represents:

```text
60,70,80,90,100
```

New score:

```text
40
```

Since:

```python
40 > heap[0]
```

is false, ignore it.

Correct.

### Duplicate scores

```text
100,100,100,100,100,100
```

Five `100`s remain. Duplicate entries are independent scores.

No special handling required.

### Scores arrive randomly

Doesn't matter.

We maintain the invariant after every score, so input ordering is irrelevant.

---

# Final interview implementation

```python
import heapq


def highFive(items):
    top_scores = {}

    for student_id, score in items:
        if student_id not in top_scores:
            top_scores[student_id] = []

        heap = top_scores[student_id]

        if len(heap) < 5:
            heapq.heappush(heap, score)
        elif score > heap[0]:
            heapq.heapreplace(heap, score)

    result = []

    for student_id in sorted(top_scores):
        average = sum(top_scores[student_id]) // 5
        result.append([student_id, average])

    return result
```

### Complexity

For each of `n` scores, heap size never exceeds five:

```text
O(n log 5) = O(n)
```

Sorting the `s` student IDs:

```text
O(s log s)
```

So:

```text
Time:  O(n + s log s)
Space: O(5s) = O(s)
```

The interview sentence to remember is:

> **“I only need five scores per student, so instead of storing and sorting every score, I'll maintain a size-5 min-heap. The root is the weakest member of the current top five, so any better incoming score can replace it.”**
