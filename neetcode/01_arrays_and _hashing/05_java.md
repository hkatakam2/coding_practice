Here is a complete interview walkthrough for the Top K Frequent Elements problem.

## 1. Restatement

We are given an array of integers and a target number `k`. We need to find the `k` numbers that appear the most times in the array. The output can be in any order, and we are guaranteed that exactly one unique set of `k` top elements exists.

## 2. Clarifying questions and assumptions

Before writing code, I would confirm a few minor details:

* **Return type:** Since the input is an `int[]`, I will return an `int[]`.
* **Input size:** I assume the array can hold up to standard limits (e.g., 100,000 elements) and contains standard 32-bit signed integers, including negatives.
* **Can `k` equal the number of unique elements?** Yes. If the array has 5 unique elements and `k` is 5, we return all 5.

## 3. Manual example

Let's trace a representative input:
`nums = [1, 1, 1, 2, 2, 3], k = 2`

1. **Count frequencies:**
* 1 appears 3 times.
* 2 appears 2 times.
* 3 appears 1 time.


2. **Filter for top `k=2`:**
* Compare frequencies: 3 (for value 1), 2 (for value 2), 1 (for value 3).
* The highest two frequencies are 3 and 2.


3. **Result:**
* The values corresponding to those frequencies are 1 and 2. Output: `[1, 2]`.



## 4. Candidate solutions

**Option 1: Complete Sorting**
We can count frequencies using a HashMap, put the unique values into a list, and sort the list descending by frequency. Then we take the first `k` elements.

* *Time complexity:* O(N + U log U), where N is the array length and U is the number of unique elements.
* *Space complexity:* O(U) for the map and list.

**Option 2: Min-Heap**
We count frequencies with a HashMap. Then, we use a Min-Heap (PriorityQueue) to keep track of the top `k` elements seen so far. As we iterate through the unique numbers, we push them into the heap. If the heap size exceeds `k`, we pop the top element (which is the one with the lowest frequency currently in the heap).

* *Time complexity:* O(N + U log k).
* *Space complexity:* O(U) for the map, O(k) for the heap.

**Option 3: Bucket Sort**
We count frequencies. Since the maximum possible frequency is the length of the array (N), we can create an array of lists `buckets`, where the index represents the frequency. We place each unique number into the bucket corresponding to its frequency, then scan the buckets backwards from N down to 1 to collect `k` elements.

* *Time complexity:* O(N).
* *Space complexity:* O(N).

## 5. Selected solution and justification

I will use the **Min-Heap (Option 2)**.

While Bucket Sort offers an O(N) time complexity, implementing an array of generic lists in Java (`List<Integer>[] buckets = new List[...]`) generates compiler warnings and is syntactically clunky. The Min-Heap approach uses standard, type-safe Java collections (`PriorityQueue`). It scales well for streaming data, requires minimal memory footprint for the heap (O(k)), and its O(N + U log k) time complexity is highly performant in practice.

To make the heap operations exceptionally readable, I'll use a modern Java `record` to bind the value and its frequency together.

## 6. Plain-English implementation outline

```java
int[] topKFrequent(int[] nums, int k) {
    /*
     * Reframe:
     * Count the occurrences of each number, then maintain a running collection of the 
     * 'k' highest-frequency numbers seen so far.
     *
     * State:
     * - Map<Integer, Integer> 'frequencies' to store value-to-count mappings.
     * - PriorityQueue (min-heap) of a custom record holding (value, frequency).
     * Chosen because a min-heap efficiently maintains the largest elements by automatically 
     * surfacing the smallest element to be discarded.
     *
     * Invariant:
     * The min-heap never exceeds size k. Its root is always the least frequent element 
     * among the top k elements processed so far.
     *
     * Core logic:
     * - iterate through nums to build the frequency map
     * - iterate through the map entries
     * - wrap each entry in a record and push it into the min-heap
     * - if the heap size exceeds k, remove the root
     * - after processing all unique numbers, the heap holds the top k elements
     * - extract the values from the heap into a result array
     *
     * Edge cases:
     * - k equals the total number of unique elements
     */
}

```

## 7. Iterative Java implementation

### Iteration 1: Method skeleton

First, I'll establish the types, the helper record, and the broad control flow.

```java
// Added: A local record to keep value and frequency bundled cleanly in the heap.
record Element(int value, int frequency) {}

public int[] topKFrequent(int[] nums, int k) {
    Map<Integer, Integer> frequencies = new HashMap<>();
    
    // Added: Min-heap ordered by frequency ascending.
    PriorityQueue<Element> minHeap = new PriorityQueue<>(
        Comparator.comparingInt(e -> e.frequency)
    );

    // TODO: count frequencies
    // TODO: maintain top k elements in heap
    // TODO: drain heap into result array

    return new int[0];
}

```

### Iteration 2: Frequency map population

Next, I'll populate the frequency map using a standard Java Map utility.

```java
record Element(int value, int frequency) {}

public int[] topKFrequent(int[] nums, int k) {
    Map<Integer, Integer> frequencies = new HashMap<>();
    
    // Added: Build the frequency map.
    for (int num : nums) {
        frequencies.put(num, frequencies.getOrDefault(num, 0) + 1);
    }
    
    PriorityQueue<Element> minHeap = new PriorityQueue<>(
        Comparator.comparingInt(e -> e.frequency)
    );

    // TODO: maintain top k elements in heap
    // TODO: drain heap into result array

    return new int[0];
}

```

### Iteration 3: Complete the happy path

Finally, I'll implement the heap maintenance and extract the results.

```java
record Element(int value, int frequency) {}

public int[] topKFrequent(int[] nums, int k) {
    Map<Integer, Integer> frequencies = new HashMap<>();
    for (int num : nums) {
        frequencies.put(num, frequencies.getOrDefault(num, 0) + 1);
    }
    
    PriorityQueue<Element> minHeap = new PriorityQueue<>(
        Comparator.comparingInt(e -> e.frequency)
    );

    // Added: Push to heap, pop if we exceed capacity 'k'.
    for (Map.Entry<Integer, Integer> entry : frequencies.entrySet()) {
        minHeap.offer(new Element(entry.getKey(), entry.getValue()));
        
        if (minHeap.size() > k) {
            minHeap.poll();
        }
    }

    // Added: Drain the heap into the result array.
    int[] result = new int[k];
    for (int i = 0; i < k; i++) {
        result[i] = minHeap.poll().value;
    }

    return result;
}

```

### Edge-case walkthrough and patches

* **`k` equals the number of unique elements:** The heap logic works perfectly. The size will grow to `k`, the `if (minHeap.size() > k)` condition will never trigger, and it will drain exactly `k` elements.
* **Output order:** The problem states the output can be in any order. Draining the min-heap sequentially puts the elements in ascending order of frequency (least frequent to most frequent). This is perfectly acceptable.
* **Negative numbers:** Handled naturally; they are just keys in the `HashMap`.

No patches are necessary for the edge cases. The logic is robust.

## 8. Final code

Here is the clean, complete implementation:

```java
import java.util.Comparator;
import java.util.HashMap;
import java.util.Map;
import java.util.PriorityQueue;

class Solution {
    
    private record Element(int value, int frequency) {}

    public int[] topKFrequent(int[] nums, int k) {
        Map<Integer, Integer> frequencies = new HashMap<>();
        for (int num : nums) {
            frequencies.put(num, frequencies.getOrDefault(num, 0) + 1);
        }
        
        PriorityQueue<Element> minHeap = new PriorityQueue<>(
            Comparator.comparingInt(e -> e.frequency)
        );

        for (Map.Entry<Integer, Integer> entry : frequencies.entrySet()) {
            minHeap.offer(new Element(entry.getKey(), entry.getValue()));
            
            if (minHeap.size() > k) {
                minHeap.poll();
            }
        }

        int[] result = new int[k];
        for (int i = 0; i < k; i++) {
            result[i] = minHeap.poll().value;
        }

        return result;
    }
}

```

## 9. Complexity

* **Time Complexity:** O(N + U log k). Building the hash map takes O(N) where N is the number of elements in the array. Inserting into the heap of size `k` takes O(log k). Doing this for U unique elements takes O(U log k). Total time is O(N + U log k).
* **Space Complexity:** O(U + k). The HashMap requires O(U) space to store the unique elements and their counts. The PriorityQueue requires O(k) space. In the worst case, this simplifies to O(N) auxiliary space.

## 10. Brief test walkthrough

Let's test `nums = [1, 1, 1, 2, 2, 3]`, `k = 2`.

1. **Map:** `{1=3, 2=2, 3=1}`.
2. **Heap processing:**
* Add `(1, 3)`. Heap: `[(1, 3)]`. Size is 1.
* Add `(2, 2)`. Heap: `[(2, 2), (1, 3)]`. Size is 2.
* Add `(3, 1)`. Heap: `[(3, 1), (1, 3), (2, 2)]`. Size is 3.
* Size > 2, so `poll()` removes `(3, 1)`. Heap: `[(2, 2), (1, 3)]`.


3. **Extraction:**
* Pop `(2, 2)`, assign `result[0] = 2`.
* Pop `(1, 3)`, assign `result[1] = 1`.


4. **Result:** `[2, 1]`. This contains the top 2 elements correctly.