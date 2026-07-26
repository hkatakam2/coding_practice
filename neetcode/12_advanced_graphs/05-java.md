### 1. Restate the problem

We are given a list of words from an alien dictionary. The words are sorted lexicographically according to the alien language's alphabet.
We need to deduce the alphabetical order of the letters.
If the given words represent a valid ordering, we return a string containing all unique characters in their deduced alphabetical order.
If the ordering contradicts itself (a cycle) or breaks the rules of lexicographical sorting (e.g., a longer word appearing before its prefix), we return `""`.
If multiple valid alphabets exist, returning any valid one is acceptable.

### 2. Ask clarifying questions

* **Input size:** What is the maximum number of words and maximum word length? *(Assume ~1000 words, ~100 characters each.)*
* **Characters:** Is the dictionary restricted to lowercase English letters? *(Assume yes, 'a' through 'z'.)*
* **Duplicate characters/words:** Can the input contain duplicate words or adjacent words that are identical? *(Assume yes, they provide no new ordering information and should be ignored.)*
* **Isolated characters:** If a character appears in the dictionary but has no defined order relative to other characters, where should it go? *(Anywhere in the output string is fine as long as it's included.)*

### 3. Work through an example by hand

Input: `words = ["wrt", "wrf", "er", "ett", "rftt"]`

* Unique letters: `w, r, t, f, e`
* Compare `wrt` and `wrf`: First difference is `t` vs `f`. So, `t < f`.
* Compare `wrf` and `er`: First difference is `w` vs `e`. So, `w < e`.
* Compare `er` and `ett`: First difference is `r` vs `t`. So, `r < t`.
* Compare `ett` and `rftt`: First difference is `e` vs `r`. So, `e < r`.

Extracted relations (edges):
`t -> f`
`w -> e`
`r -> t`
`e -> r`

Chain them together: `w -> e -> r -> t -> f`.
Result: `"wertf"`.

### 4. Brainstorm solutions aloud

* **Approach 1: Directed Graph + Topological Sort (DFS)**
We can build a graph where each unique character is a node. A directed edge from `u` to `v` means `u` comes before `v`. We can use DFS to visit nodes, pushing them to a stack on the post-order traversal. We track visiting states (`UNVISITED`, `VISITING`, `VISITED`) to detect cycles.
*Tradeoffs:* Very efficient, but cycle detection requires a separate state map and DFS recursion can sometimes be slightly harder to follow.
* **Approach 2: Directed Graph + Topological Sort (BFS / Kahn's Algorithm)**
We build the same graph, but also track the `in-degree` (number of incoming edges) for each character.
We place all characters with an `in-degree` of 0 into a Queue.
While the queue is not empty, we pop a character, append it to our result string, and decrement the `in-degree` of all its neighbors. If a neighbor's `in-degree` becomes 0, it joins the Queue.
If the final string length equals the number of unique characters, we found a valid order. Otherwise, a cycle exists.
*Tradeoffs:* Easy to implement iteratively, natively detects cycles, naturally builds the string left-to-right.

### 5. Select the solution

I will use **Directed Graph + BFS (Kahn's Algorithm)**.

* It is easy to explain and implement without bugs.
* Cycle detection requires no extra states—just a length comparison at the end.
* Data structures:
* `Map<Character, Set<Character>>` for the adjacency list (a `Set` prevents duplicate edges from skewing the in-degree count).
* `Map<Character, Integer>` for the in-degree counts.
* `Queue<Character>` (`ArrayDeque`) for BFS.



### 6. Write the implementation outline

```java
String alienOrder(String[] words) {
    /*
     * Reframe:
     * Translate adjacent word comparisons into directed graph edges, 
     * then perform a topological sort to find the character order.
     *
     * State:
     * adj: Map from character to a Set of characters that come after it.
     * inDegree: Map from character to the count of characters that must come before it.
     * Chosen because they directly support Kahn's BFS algorithm for topological sorting.
     *
     * Invariant:
     * Characters in the queue always have all their prerequisites met (in-degree == 0).
     *
     * Core logic:
     * - Initialize the graph: every unique character gets an empty adjacency set and 0 in-degree.
     * - Build the graph: compare each word with the next word.
     *   - Find the first differing character to establish an edge.
     *   - If an edge is new, add it and increment the target's in-degree.
     * - Topo sort: push all 0 in-degree characters into a queue.
     * - Dequeue characters, append to result, and reduce neighbors' in-degrees.
     * - Push neighbors to the queue when their in-degree hits 0.
     * - Return result if it contains all unique characters, else "" (cycle detected).
     *
     * Edge cases:
     * - An invalid prefix relationship (e.g., "abc" appears before "ab").
     * - Graph contains a cycle (e.g., a->b and b->a).
     */
}

```

### 7. Implement iteratively

#### Iteration 1: Method skeleton and graph initialization

First, extract all unique characters so we know exactly what nodes exist in our graph.

```java
public String alienOrder(String[] words) {
    Map<Character, Set<Character>> adj = new HashMap<>();
    Map<Character, Integer> inDegree = new HashMap<>();

    // Initialize graph with every unique character
    for (String word : words) {
        for (char c : word.toCharArray()) {
            adj.putIfAbsent(c, new HashSet<>());
            inDegree.putIfAbsent(c, 0);
        }
    }

    // TODO: Build the graph by comparing adjacent words
    // TODO: Perform BFS topological sort

    return "";
}

```

#### Iteration 2: Build the graph

Now we compare adjacent words to find relationships. We also handle the invalid prefix edge case here.

```java
public String alienOrder(String[] words) {
    Map<Character, Set<Character>> adj = new HashMap<>();
    Map<Character, Integer> inDegree = new HashMap<>();

    for (String word : words) {
        for (char c : word.toCharArray()) {
            adj.putIfAbsent(c, new HashSet<>());
            inDegree.putIfAbsent(c, 0);
        }
    }

    // Added: Build the graph
    for (int i = 0; i < words.length - 1; i++) {
        String word1 = words[i];
        String word2 = words[i + 1];

        // Edge case: word1 is longer but starts with word2 (e.g., "abc" before "ab")
        if (word1.length() > word2.length() && word1.startsWith(word2)) {
            return ""; // Invalid dictionary
        }

        // Find the first non-matching character
        int minLength = Math.min(word1.length(), word2.length());
        for (int j = 0; j < minLength; j++) {
            char u = word1.charAt(j);
            char v = word2.charAt(j);

            if (u != v) {
                // Only process if this is a new directed edge
                if (!adj.get(u).contains(v)) {
                    adj.get(u).add(v);
                    inDegree.put(v, inDegree.get(v) + 1);
                }
                break; // Only the first differing character dictates order
            }
        }
    }

    // TODO: Perform BFS topological sort

    return "";
}

```

#### Iteration 3: Complete topological sort (Happy path & Cycle check)

We use a queue to process all characters that have no prerequisites.

```java
public String alienOrder(String[] words) {
    Map<Character, Set<Character>> adj = new HashMap<>();
    Map<Character, Integer> inDegree = new HashMap<>();

    for (String word : words) {
        for (char c : word.toCharArray()) {
            adj.putIfAbsent(c, new HashSet<>());
            inDegree.putIfAbsent(c, 0);
        }
    }

    for (int i = 0; i < words.length - 1; i++) {
        String word1 = words[i];
        String word2 = words[i + 1];

        if (word1.length() > word2.length() && word1.startsWith(word2)) {
            return ""; 
        }

        int minLength = Math.min(word1.length(), word2.length());
        for (int j = 0; j < minLength; j++) {
            char u = word1.charAt(j);
            char v = word2.charAt(j);

            if (u != v) {
                if (!adj.get(u).contains(v)) {
                    adj.get(u).add(v);
                    inDegree.put(v, inDegree.get(v) + 1);
                }
                break; 
            }
        }
    }

    // Added: BFS Topological Sort
    Queue<Character> queue = new ArrayDeque<>();
    for (Map.Entry<Character, Integer> entry : inDegree.entrySet()) {
        if (entry.getValue() == 0) {
            queue.add(entry.getKey());
        }
    }

    StringBuilder sb = new StringBuilder();
    while (!queue.isEmpty()) {
        char current = queue.poll();
        sb.append(current);

        for (char neighbor : adj.get(current)) {
            inDegree.put(neighbor, inDegree.get(neighbor) - 1);
            if (inDegree.get(neighbor) == 0) {
                queue.add(neighbor);
            }
        }
    }

    // If the valid string contains all unique characters, return it.
    // Otherwise, a cycle prevented some nodes from reaching 0 in-degree.
    if (sb.length() == inDegree.size()) {
        return sb.toString();
    }
    
    return "";
}

```

#### Edge-case pass

* **Duplicate words:** Handled gracefully. `word1.charAt(j) != word2.charAt(j)` will never be true, no edges added.
* **Disconnected components / Isolated letters:** Handled gracefully. For a letter like `'z'` that never differs from anything, it gets an in-degree of `0`, gets pushed to the queue immediately, and added to the result.
* **Invalid Prefix (`"abc"` before `"ab"`):** Explicitly handled during graph building by returning `""`.
* **Cycles (`a -> b` and `b -> a`):** Handled gracefully. The queue will run dry before `sb.length()` reaches `inDegree.size()`, returning `""`.

### 8. Analyze expensive sections and optimize

* **Time Complexity:**
* **Graph Initialization:** We iterate over all characters in all words. If `C` is the total length of all words combined, this takes `O(C)`.
* **Graph Building:** We compare each adjacent pair of words up to the length of the shorter word. In the worst case, we look at every character once, taking `O(C)`.
* **Topological Sort:** We process each unique character (vertex) and each relationship (edge) exactly once. There are at most `V = 26` vertices and `E = 26^2` edges. Time is `O(V + E)`.
* **Total Time:** `O(C)` where `C` is the total number of characters in the `words` array. This is strictly linear with respect to the input size. No optimization needed.


* **Space Complexity:**
* The `adj` map holds at most 26 keys and at most `26 * 26` edges.
* The `inDegree` map holds at most 26 keys.
* The `queue` holds at most 26 elements.
* **Total Space:** `O(1)` auxiliary space, bounded entirely by the fixed maximum of 26 English letters.



### Final Code

```java
import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Queue;
import java.util.Set;

public class AlienDictionary {

    public String alienOrder(String[] words) {
        Map<Character, Set<Character>> adj = new HashMap<>();
        Map<Character, Integer> inDegree = new HashMap<>();

        // Initialize graph structure for every unique character
        for (String word : words) {
            for (char c : word.toCharArray()) {
                adj.putIfAbsent(c, new HashSet<>());
                inDegree.putIfAbsent(c, 0);
            }
        }

        // Build the dependency graph
        for (int i = 0; i < words.length - 1; i++) {
            String word1 = words[i];
            String word2 = words[i + 1];

            // A longer word cannot legally precede its own prefix in sorted order
            if (word1.length() > word2.length() && word1.startsWith(word2)) {
                return "";
            }

            // Find the first differing character to establish relative order
            int minLength = Math.min(word1.length(), word2.length());
            for (int j = 0; j < minLength; j++) {
                char u = word1.charAt(j);
                char v = word2.charAt(j);

                if (u != v) {
                    // Only add the edge if it's new to avoid skewing in-degree counts
                    if (!adj.get(u).contains(v)) {
                        adj.get(u).add(v);
                        inDegree.put(v, inDegree.get(v) + 1);
                    }
                    // Remaining characters in these words yield no further ordering rules
                    break;
                }
            }
        }

        // Perform Kahn's BFS Topological Sort
        Queue<Character> queue = new ArrayDeque<>();
        for (Map.Entry<Character, Integer> entry : inDegree.entrySet()) {
            if (entry.getValue() == 0) {
                queue.add(entry.getKey());
            }
        }

        StringBuilder alienAlphabet = new StringBuilder();
        while (!queue.isEmpty()) {
            char current = queue.poll();
            alienAlphabet.append(current);

            for (char neighbor : adj.get(current)) {
                inDegree.put(neighbor, inDegree.get(neighbor) - 1);
                if (inDegree.get(neighbor) == 0) {
                    queue.add(neighbor);
                }
            }
        }

        // Check if graph contained a cycle (not all vertices processed)
        if (alienAlphabet.length() == inDegree.size()) {
            return alienAlphabet.toString();
        }

        return "";
    }
}

```

### Brief test walkthrough

* **Main Example:** `["wrt","wrf","er","ett","rftt"]`
Graph builds correctly (`w->e, e->r, r->t, t->f`). `w` goes in queue. Queue empties left-to-right. Returns `"wertf"`.
* **Invalid Prefix Edge Case:** `["abc", "ab"]`
Prefix check fires immediately on first outer iteration. Returns `""`.
* **Cycle Stress Test:** `["z", "x", "z"]`
`z -> x` edge created. Then `x -> z` edge created. In-degrees: `z:1, x:1`. Queue is initially empty. `alienAlphabet.length()` is 0, which does not equal `inDegree.size()` (2). Returns `""`.