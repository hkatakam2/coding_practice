### 1. Restate the problem

We are given a number of courses we need to take, labeled from `0` to `numCourses - 1`. We are also given a list of dependencies (prerequisites), where taking course `a` requires first completing course `b` (represented as the pair `[a, b]`).

Our goal is to determine if it is logically possible to complete all the courses. In graph terms, the courses are nodes, and the prerequisites are directed edges from `b` to `a` (`b -> a`). The problem is asking us to determine if a directed cycle exists in this graph. If a cycle exists (e.g., A requires B, and B requires A), we can never finish the courses, and we should return `false`. Otherwise, we return `true`.

### 2. Ask clarifying questions

Before writing code, I would confirm a few details:

* **Can there be disconnected components?** (e.g., some courses have no prerequisites and lead to nothing else?) *Assumption: Yes, this is common.*
* **Are there duplicate prerequisites in the input?** (e.g., `[1, 0]` appears twice?) *Assumption: Possible, our algorithm should be resilient to this.*
* **Could `numCourses` be 0 or 1?** *Assumption: Yes. If 0 or 1, we can trivially finish the courses.*
* **Is the input array well-formed?** Are there any out-of-bounds course numbers like `-1` or `numCourses + 5`? *Assumption: No, all values in the pairs are strictly between `0` and `numCourses - 1`.*

### 3. Work through an example by hand

Let's use an example with 4 courses (`numCourses = 4`) and the following `prerequisites`:
`[[1, 0], [2, 1], [3, 2], [1, 3]]`

Let's trace it:

1. `0` has no prerequisites. We can take `0`.
2. To take `1`, we need `0`, `3`.
3. To take `2`, we need `1`.
4. To take `3`, we need `2`.

If we visually map this: `0 -> 1 -> 2 -> 3 -> 1`

* We can take `0`.
* We try to take `1`, but it requires `3`.
* `3` requires `2`.
* `2` requires `1`.

This forms a cycle (`1 -> 2 -> 3 -> 1`). The moment we finish `0`, we are stuck because `1`, `2`, and `3` all wait on each other. We should return `false`.

### 4. Brainstorm solutions aloud

*"There are a couple of standard ways to detect cycles in a directed graph. The first approach that comes to mind is Depth-First Search (DFS).*

* **DFS with State Tracking:** We could map every node to a state: `UNVISITED`, `VISITING`, or `VISITED`. We start a DFS on each unvisited node. If we ever encounter a node that is currently in the `VISITING` state during our traversal, we've found a back-edge, which means there's a cycle. This takes $O(V + E)$ time and space. However, deep dependency chains could risk a StackOverflow due to recursion limits, unless we do it iteratively, which is messy.
* **BFS (Kahn's Algorithm / Topological Sort):** We can count the 'in-degree' of every node—how many prerequisites a course has. We place any course with an `inDegree` of 0 into a Queue because it can be taken immediately. As we take a course, we conceptually remove its outgoing edges, decrementing the `inDegree` of its neighbors. If a neighbor drops to 0, it means all its prerequisites are fulfilled, and we add it to the queue. At the end, if the number of courses we successfully took equals `numCourses`, we've finished everything. If not, a cycle prevented some in-degrees from ever reaching 0."

### 5. Select the solution

I'll go with **Kahn's Algorithm (BFS)**.

* **Correct:** It reliably identifies cycles in directed graphs.
* **Easy to explain/implement:** It strictly uses an array to track dependencies and a standard `ArrayDeque` for processing, mimicking how a human would actually complete the courses.
* **Complexity:** Expected $O(V + E)$ time and $O(V + E)$ space.
* **Safety:** Being iterative, it completely avoids recursion depth issues.

### 6. Write the implementation outline

```java
boolean canFinish(int numCourses, int[][] prerequisites) {
    /*
     * Reframe:
     * We need to find if there is a valid topological ordering. If there is a cycle, 
     * a complete ordering is impossible.
     *
     * State:
     * - List of Lists 'adj' for the adjacency list representation of the graph.
     * - int array 'inDegree' to track how many unfulfilled prerequisites a course has.
     * - Queue (ArrayDeque) to hold courses that currently have 0 prerequisites.
     * Chosen because: graph traversal and dependency resolution is naturally a queue problem.
     *
     * Invariant:
     * Only courses with exactly 0 outstanding prerequisites are allowed in the Queue.
     *
     * Core logic:
     * - build the graph by populating 'adj' and 'inDegree' from the 'prerequisites' array
     * - enqueue all courses that initially have an inDegree of 0
     * - while the queue is not empty:
     *     - dequeue a course and increment our count of completed courses
     *     - for each course that depends on this completed course:
     *         - decrement its inDegree
     *         - if its inDegree hits 0, enqueue it
     * - return true if completed courses equals numCourses, false otherwise
     *
     * Edge cases:
     * - empty prerequisites (return true immediately, all courses have 0 inDegree)
     * - disconnected graph components (Kahn's handles this natively)
     */
}

```

### 7. Implement iteratively

#### Iteration 1: Method skeleton & Graph Building

I'll start by setting up our core data structures and populating them.

```java
public boolean canFinish(int numCourses, int[][] prerequisites) {
    // State initialization
    List<List<Integer>> adj = new ArrayList<>();
    for (int i = 0; i < numCourses; i++) {
        adj.add(new ArrayList<>());
    }
    int[] inDegree = new int[numCourses];
    
    // Build the graph
    // prerequisites[i] = [course, preReq]  =>  edge is preReq -> course
    for (int[] pre : prerequisites) {
        int course = pre[0];
        int preReq = pre[1];
        
        adj.get(preReq).add(course);
        inDegree[course]++;
    }
    
    // TODO: Initialize the queue with 0 in-degree nodes
    // TODO: Process the queue to take courses
    // TODO: Check if we took all courses

    return false;
}

```

#### Iteration 2: Initialize queue and tracking state

Next, we identify which courses can be taken right away and prepare our tracking variable.

```java
public boolean canFinish(int numCourses, int[][] prerequisites) {
    List<List<Integer>> adj = new ArrayList<>();
    for (int i = 0; i < numCourses; i++) {
        adj.add(new ArrayList<>());
    }
    int[] inDegree = new int[numCourses];
    
    for (int[] pre : prerequisites) {
        int course = pre[0];
        int preReq = pre[1];
        adj.get(preReq).add(course);
        inDegree[course]++;
    }
    
    // Added: Setup Queue and enqueue independent courses
    Queue<Integer> queue = new ArrayDeque<>();
    for (int i = 0; i < numCourses; i++) {
        if (inDegree[i] == 0) {
            queue.offer(i);
        }
    }
    
    // Added: track how many courses we successfully complete
    int completedCourses = 0;
    
    // TODO: Process the queue to take courses
    
    // Added: if we completed all courses, no cycles existed.
    return completedCourses == numCourses;
}

```

#### Iteration 3: Complete the happy path

Finally, I'll add the BFS loop. For every course we finish, we tell its neighbors they are one step closer to being ready.

```java
public boolean canFinish(int numCourses, int[][] prerequisites) {
    List<List<Integer>> adj = new ArrayList<>();
    for (int i = 0; i < numCourses; i++) {
        adj.add(new ArrayList<>());
    }
    int[] inDegree = new int[numCourses];
    
    for (int[] pre : prerequisites) {
        int course = pre[0];
        int preReq = pre[1];
        adj.get(preReq).add(course);
        inDegree[course]++;
    }
    
    Queue<Integer> queue = new ArrayDeque<>();
    for (int i = 0; i < numCourses; i++) {
        if (inDegree[i] == 0) {
            queue.offer(i);
        }
    }
    
    int completedCourses = 0;
    
    // Added: Process ready courses
    while (!queue.isEmpty()) {
        int current = queue.poll();
        completedCourses++;
        
        for (int neighbor : adj.get(current)) {
            // Fulfill one prerequisite for the neighbor
            inDegree[neighbor]--;
            // If all prerequisites are fulfilled, it's ready to take
            if (inDegree[neighbor] == 0) {
                queue.offer(neighbor);
            }
        }
    }
    
    return completedCourses == numCourses;
}

```

#### Edge-case walkthrough and patches

Let's review edge cases:

* **No prerequisites (`prerequisites.length == 0`)**: The graph-building loop skips. `inDegree` for all nodes is 0. Everything is enqueued. Loop runs `numCourses` times. Returns `true`. *No patch needed.*
* **Disconnected graph components**: Say Course 0 needs 1, Course 2 needs 3. Kahn's starts with 1 and 3 in the queue, processes them, enqueues 0 and 2, and processes them. *No patch needed.*
* **Duplicate prerequisite pairs (e.g., `[1, 0]` and `[1, 0]`)**: `inDegree[1]` becomes 2, and `adj.get(0)` contains `1` twice. When `0` is popped, the neighbor loop runs twice for `1`. `inDegree[1]` decrements twice, hitting 0, and `1` is enqueued exactly once. The math holds perfectly. *No patch needed.*

### 8. Final Code

Here is the clean, final version:

```java
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.List;
import java.util.Queue;

class Solution {
    public boolean canFinish(int numCourses, int[][] prerequisites) {
        // Step 1: Build the graph
        List<List<Integer>> adj = new ArrayList<>();
        for (int i = 0; i < numCourses; i++) {
            adj.add(new ArrayList<>());
        }
        
        int[] inDegree = new int[numCourses];
        
        for (int[] pre : prerequisites) {
            int course = pre[0];
            int preReq = pre[1];
            adj.get(preReq).add(course);
            inDegree[course]++;
        }
        
        // Step 2: Initialize queue with courses having 0 prerequisites
        Queue<Integer> queue = new ArrayDeque<>();
        for (int i = 0; i < numCourses; i++) {
            if (inDegree[i] == 0) {
                queue.offer(i);
            }
        }
        
        // Step 3: Process courses
        int completedCourses = 0;
        
        while (!queue.isEmpty()) {
            int current = queue.poll();
            completedCourses++;
            
            for (int neighbor : adj.get(current)) {
                inDegree[neighbor]--;
                
                if (inDegree[neighbor] == 0) {
                    queue.offer(neighbor);
                }
            }
        }
        
        // Step 4: Validate if all courses were successfully completed
        return completedCourses == numCourses;
    }
}

```

### 9. Complexity

* **Time Complexity:** $O(V + E)$ where $V$ is `numCourses` and $E$ is the length of `prerequisites`. We iterate through `numCourses` to initialize lists/arrays, iterate through `prerequisites` to build the edges, and finally traverse each node and its outgoing edges exactly once in the `while` loop.
* **Space Complexity:** $O(V + E)$. The adjacency list `adj` stores $V$ empty lists and exactly $E$ relationships. The `inDegree` array takes $O(V)$ space. The `queue` takes up to $O(V)$ space.

### 10. Brief test walkthrough

Let's run a small test: `numCourses = 2, prerequisites = [[1, 0]]` (To take 1, you must take 0).

* **Initialization:** `adj = [[1], []]`, `inDegree = [0, 1]`.
* **Queue Setup:** `inDegree[0]` is 0, so `queue` gets `[0]`.
* **Loop - Pop 0:** `completedCourses` becomes `1`. Neighbor of `0` is `1`. `inDegree[1]` drops from 1 to 0. `1` is enqueued.
* **Loop - Pop 1:** `completedCourses` becomes `2`. No neighbors.
* **End:** Queue is empty. `completedCourses` (2) == `numCourses` (2). Expected result: `true`. It correctly returns `true`.