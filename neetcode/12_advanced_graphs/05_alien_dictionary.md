# question
There is a foreign language which uses the latin alphabet, but the order among letters is not "a", "b", "c" ... "z" as in English.
You receive a list of non-empty strings words from the dictionary, where the words are sorted lexicographically based on the rules of this new language.
Derive the order of letters in this language. If the order is invalid, return an empty string. If there are multiple valid order of letters, return any of them.
A string a is lexicographically smaller than a string b if either of the following is true:

The first letter where they differ is smaller in a than in b.
a is a prefix of b and a.length < b.length.

### 1. Restate

Given a list of words sorted by an unknown alien alphabet, determine the letter order. Return the ordered alphabet string. Return empty string if impossible (invalid order/cycle).

### 2. Clarifying Questions

* **Inputs:** Array of strings. All lowercase English letters? (Assume yes).
* **Outputs:** String of unique chars representing order.
* **Missing letters:** Only include characters present in the input array? (Assume yes).
* **Multiple valid orders:** Can return any? (Assume yes).

### 3. Example By Hand

Input: `["wrt", "wrf", "er", "ett", "rftt"]`

* Compare adjacent words. Find first differing character.
* `wrt` vs `wrf`: `w`,`r` match. `t` vs `f` -> `t` comes before `f` (`t -> f`).
* `wrf` vs `er`: `w` vs `e` -> `w -> e`.
* `er` vs `ett`: `e` matches. `r` vs `t` -> `r -> t`.
* `ett` vs `rftt`: `e` vs `r` -> `e -> r`.
* Dependencies: `t->f`, `w->e`, `r->t`, `e->r`.
* Chain: `w -> e -> r -> t -> f`.
* Output: `"wertf"`.

### 4. Brainstorm & Complexity

* **Idea 1:** Compare all pairs of words. Not needed. Adjacent words sufficient for lexicographical sorting.
* **Idea 2:** Graph problem. Letters are nodes. Relative orders are directed edges.
* **Algorithm:** Topological Sort. Two ways:
* **DFS:** Post-order traversal with 3-color cycle detection.
* **BFS (Kahn's):** Count incoming edges (indegrees). Process nodes with 0 incoming edges.


* **Complexity:** * Time: O(C) where C is total characters across all words. Comparing words takes O(C). Graph traversal is O(V+E) where V <= 26, E <= 26^2, making it O(1).
* Space: O(1) auxiliary (max 26 nodes, max 26^2 edges).



### 5. Suggest Solutions

Prefer BFS (Kahn's). Highly intuitive: "Find letters with no prerequisites, add to result, remove them from prerequisite lists of others. Repeat."
Hand trace from step 3 directly maps to Kahn's.

### 6. Outline

```python
def alienOrder(words: list[str]) -> str:
    """
    Reframe: Lexicographical order translates to a directed acyclic graph (DAG) of characters.
    State: Adjacency list (graph) for dependencies, Indegree map for prerequisite counts, chosen because Kahn's algorithm easily handles dependency resolution step-by-step.
    Invariant: Characters with 0 indegree have no remaining prerequisites and can be safely added to the alphabet.

    build_graph(words) = compares adjacent words to extract directed edges and populates unique characters.

    Core logic:
    - build the dependency graph and prerequisite counts from words.
    - collect all characters with zero prerequisites into a queue.
    - while queue is not empty, pop a character, append it to the result.
    - decrement prerequisite counts for all neighbors of the popped character.
    - if a neighbor hits zero prerequisites, add it to the queue.
    - if the result length matches unique character count, return result.
    
    Edge cases:
    - Prefix invalidation: A longer word comes before a shorter word that is its exact prefix (e.g., "abc", "ab"). Graph invalid. Return "".
    - Cycles: Graph contains a cycle (e.g., a->b, b->a). Queue empties before all characters processed. Return "".
    """

```

### 7. Iterative Implementation

**Iteration 1: Skeleton (Plain English to Code Stubs)**

```python
def alienOrder(words: list[str]) -> str:
    # 1. Setup
    graph, indegrees = build_graph_and_indegrees(words)
    
    # 2. Initialize Queue
    queue = get_zero_indegree_nodes(indegrees)
    result = []
    
    # 3. Process Queue
    while queue:
        char = queue.pop(0)
        result.append(char)
        
        # update neighbors
        decrement_neighbors(char, graph, indegrees, queue)
        
    # 4. Check for cycles
    if len(result) == len(indegrees):
        return "".join(result)
    return ""

```

**Iteration 2: Expanding Queue Logic (Fleshing out Core)**

```python
def alienOrder(words: list[str]) -> str:
    # Setup stubs
    graph, indegrees = build_graph_and_indegrees(words)
    
    # Expanded Init
    import collections
    queue = collections.deque([c for c in indegrees if indegrees[c] == 0])
    result = []
    
    # Expanded Queue Loop
    while queue:
        char = queue.popleft()
        result.append(char)
        
        # Expanded neighbor logic
        for neighbor in graph[char]:
            indegrees[neighbor] -= 1
            if indegrees[neighbor] == 0:
                queue.append(neighbor)
                
    if len(result) == len(indegrees):
        return "".join(result)
    return ""

```

**Iteration 3: Expanding Graph Building (Replacing Stub)**

```python
def alienOrder(words: list[str]) -> str:
    import collections
    
    # Expand graph building
    graph = collections.defaultdict(set)
    indegrees = {c: 0 for word in words for c in word} # all unique chars
    
    for i in range(len(words) - 1):
        word1 = words[i]
        word2 = words[i + 1]
        
        # Find first difference
        min_len = min(len(word1), len(word2))
        for j in range(min_len):
            if word1[j] != word2[j]:
                out_char = word1[j]
                in_char = word2[j]
                if in_char not in graph[out_char]:
                    graph[out_char].add(in_char)
                    indegrees[in_char] += 1
                break # only first diff matters
                
    # Queue logic remains same
    queue = collections.deque([c for c in indegrees if indegrees[c] == 0])
    result = []
    
    while queue:
        char = queue.popleft()
        result.append(char)
        for neighbor in graph[char]:
            indegrees[neighbor] -= 1
            if indegrees[neighbor] == 0:
                queue.append(neighbor)
                
    if len(result) == len(indegrees):
        return "".join(result)
    return ""

```

**Iteration 4: Patching Edge Cases**
We need to handle the case where `word1` is a longer prefix of `word2` (e.g., `["abc", "ab"]`). This violates lexicographical rules.
*Change: Add a check inside the graph building loop right after checking minimum length.*

```python
def alienOrder(words: list[str]) -> str:
    import collections
    
    graph = collections.defaultdict(set)
    indegrees = {c: 0 for word in words for c in word} 
    
    for i in range(len(words) - 1):
        word1 = words[i]
        word2 = words[i + 1]
        
        # EDGE CASE PATCH: Invalid prefix
        if len(word1) > len(word2) and word1.startswith(word2):
            return ""
            
        min_len = min(len(word1), len(word2))
        for j in range(min_len):
            if word1[j] != word2[j]:
                out_char = word1[j]
                in_char = word2[j]
                if in_char not in graph[out_char]:
                    graph[out_char].add(in_char)
                    indegrees[in_char] += 1
                break 
                
    queue = collections.deque([c for c in indegrees if indegrees[c] == 0])
    result = []
    
    while queue:
        char = queue.popleft()
        result.append(char)
        for neighbor in graph[char]:
            indegrees[neighbor] -= 1
            if indegrees[neighbor] == 0:
                queue.append(neighbor)
                
    # EDGE CASE COVERED: Cycle detection via result length vs unique chars
    if len(result) == len(indegrees):
        return "".join(result)
    return ""

```

### 8. Complexity & Optimizations

* **Time Complexity:** O(C), where C is the total length of all words combined. Building the indegree map and graph looks at every character. Topo sort runs in O(V + E). Since V ≤ 26 and E ≤ 26², V+E is O(1). Total time is dominated by reading inputs: O(C).
* **Space/Memory:** O(1) auxiliary space. `graph` stores at most 26 keys and 26² edges. `indegrees` stores at most 26 keys. `queue` holds at most 26 elements. Even scaling words indefinitely, space strictly caps at English alphabet constants.
* **Optimizations:** No further structural optimizations needed. Graph uses `set` to prevent duplicate edges, which protects `indegrees` from false double-counting. `collections.deque` provides O(1) pops, optimal over `list.pop(0)`.