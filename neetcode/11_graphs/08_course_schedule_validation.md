# question
You are given an array prerequisites where prerequisites[i] = [a, b] indicates that you must take course b first if you want to take course a.
The pair [0, 1], indicates that must take course 1 before taking course 0.
There are a total of numCourses courses you are required to take, labeled from 0 to numCourses - 1.
Return true if it is possible to finish all courses, otherwise return false.

### 1. Restate

Given a number of courses and a list of dependencies (course A needs course B), determine if it's possible to complete all courses. Essentially: detect if there are circular dependencies (cycles) in a directed graph.

### 2. Clarifying Questions

* Can `prerequisites` be empty? (Yes -> assume we can take all courses).
* Can there be disconnected courses with no prerequisites? (Yes -> take them anytime).
* Can there be self-dependencies like `[0, 0]`? (Yes -> immediate failure, impossible to take).
* Are there duplicate pairs in the input? (Assume no, but logic should handle it or we use a set).

### 3. Hand Trace

Input: `numCourses = 3`, `prerequisites = [[1,0], [2,1]]`.

* Course 0 needs nothing.
* Course 1 needs 0.
* Course 2 needs 1.

Action:

1. Cross off 0. It unlocks 1.
2. 1 has no more blockers. Cross off 1. It unlocks 2.
3. 2 has no more blockers. Cross off 2.
4. Crossed off 3 courses. 3 == `numCourses`. Return True.

Input: `numCourses = 2`, `prerequisites = [[1,0], [0,1]]`.

* Course 0 needs 1.
* Course 1 needs 0.
* No courses have 0 blockers. Cross off nothing. 0 != 2. Return False.

### 4. Brainstorm & Complexity

* **Option A: Counting Dependencies (Kahn's Algorithm / BFS).** Keep a tally of how many prerequisites each course has. Find ones with 0 tally, "take" them, and subtract 1 from the tally of courses they unlock. Repeat.
* Time: $O(V + E)$ where $V$ is courses, $E$ is dependencies. Space: $O(V + E)$ to map unlocks.


* **Option B: Path Finding (DFS).** Pick a course, follow its dependencies deep down. Keep a "visiting" set. If we see a course already in the "visiting" set, we found a cycle.
* Time: $O(V + E)$. Space: $O(V + E)$.



### 5. Suggest Solutions

Option A (BFS / Dependency Counting) is highly preferred here. It perfectly matches the physical "by-hand" trace from step 3. It directly models the real-world action of finishing a prerequisite to unlock the next class. It avoids recursion limits and is extremely easy to explain.

### 6. Outline Selected Implementation

```python
def canFinish(numCourses, prerequisites):
    """
    Reframe: Find if a directed graph of dependencies has a cycle by checking if we can topologically sort it.
    State: Array of in-degrees (prereq counts), Hashmap of adjacencies (course -> unlocks), chosen because they let us find 0-dependency courses and resolve them in O(1) time per edge.
    Invariant: Queue only ever contains courses with 0 pending prerequisites.

    buildGraph(prereqs) = maps each course to courses it unlocks, and counts prereqs for each course.
    getZeroPrereqCourses(counts) = returns list of courses with 0 prereqs.

    Core logic:
    - Build the dependency graph and count prerequisites per course.
    - Find all courses that have zero prerequisites to start.
    - While we have courses we can take:
        - Take the course, increment our completed count.
        - For every course this newly completed course unlocks:
            - Decrease its prerequisite count.
            - If its prerequisite count hits zero, it's ready to take. Add to our list.
    - If our completed count matches total courses, we finish. Else, cycle exists.

    Edge cases:
    - prerequisites list is empty.
    - Disconnected courses.
    - Self-dependencies like [0, 0].
    """

```

### 7. Iterative Implementation

**Iteration 1: Skeleton with stubs**

```python
def canFinish(numCourses, prerequisites):
    # 1. Setup state
    adj_list, in_degrees = buildGraph(numCourses, prerequisites)
    
    # 2. Find starting points
    queue = getZeroPrereqCourses(in_degrees)
    
    # 3. Process courses
    completed_count = processQueue(queue, adj_list, in_degrees)
    
    # 4. Verify
    return completed_count == numCourses

```

**Iteration 2: Expand setup and starting points (removing stubs)**

```python
from collections import deque

def canFinish(numCourses, prerequisites):
    # CHANGED: Inline buildGraph logic. Array for fast lookup, hashmap for edges.
    adj_list = {i: [] for i in range(numCourses)}
    in_degrees = [0] * numCourses
    
    for course, prereq in prerequisites:
        adj_list[prereq].append(course)  # prereq unlocks course
        in_degrees[course] += 1          # course has +1 blocker

    # CHANGED: Inline getZeroPrereqCourses logic using deque for fast pops
    queue = deque([i for i in range(numCourses) if in_degrees[i] == 0])
    
    # 3. Process courses (STUB)
    completed_count = processQueue(queue, adj_list, in_degrees)
    
    return completed_count == numCourses

```

**Iteration 3: Expand processing logic (Core complete)**

```python
from collections import deque

def canFinish(numCourses, prerequisites):
    adj_list = {i: [] for i in range(numCourses)}
    in_degrees = [0] * numCourses
    
    for course, prereq in prerequisites:
        adj_list[prereq].append(course)
        in_degrees[course] += 1

    queue = deque([i for i in range(numCourses) if in_degrees[i] == 0])
    
    # CHANGED: Inline processQueue logic. Simulate taking classes.
    completed_count = 0
    while queue:
        current = queue.popleft() # Take class
        completed_count += 1
        
        # Free up classes this one blocked
        for unlocked in adj_list[current]:
            in_degrees[unlocked] -= 1
            if in_degrees[unlocked] == 0:
                queue.append(unlocked) # Ready to take
                
    return completed_count == numCourses

```

**Walk Edge Cases:**

* *Empty prereqs:* Loop 1 skips. `in_degrees` all 0. Queue gets all courses. Loop 2 pops all, `completed_count` hits `numCourses`. Returns True. (Handled natively).
* *Disconnected courses:* They get 0 `in_degree`, dumped straight into queue, processed instantly. (Handled natively).
* *Self-dependency `[0,0]`:* `in_degree[0]` becomes 1. Never hits queue. `completed_count` falls short. Returns False. (Handled natively).

No code patching needed. The core logic is robust.

### 8. Complexity & Optimizations

* **Time Complexity:** $O(V + E)$ where $V$ is `numCourses` and $E$ is the length of `prerequisites`. We build the graph in $O(E)$ time. Processing the queue visits each node once $O(V)$ and iterates over every outgoing edge once $O(E)$.
* **Space Complexity:** $O(V + E)$. The adjacency list stores $E$ edges. `in_degrees` array uses $O(V)$ space. Queue uses up to $O(V)$ space.
* **Optimization check:** We are already utilizing `collections.deque` for $O(1)$ pop operations, which is crucial because a standard list `.pop(0)` is $O(N)$. We use a fixed array for `in_degrees` which is cache-friendly and faster than a hash map. Code is optimal for the framework.