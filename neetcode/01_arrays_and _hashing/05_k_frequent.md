### question
Given an integer array `nums` and an integer `k`, return the `k` most frequent elements within the array.
The test cases are generated such that the answer is always unique.
You may return the output in any order.
### 1. Restate

Find `k` numbers appearing most often in array `nums`.

### 2. Clarify

* **Input**: `nums` (integer array), `k` (integer).
* **Output**: Array of `k` integers.
* **Constraints/Questions**:
* Can array be empty? No, problem implies valid `k`.
* Negative numbers? Yes.
* Ties? Problem says answer is unique.
* Order? Any order allowed.



### 3. By Hand

Input: `nums = [1,1,1,2,2,3]`, `k = 2`

1. Count elements:
* 1 -> 3 times
* 2 -> 2 times
* 3 -> 1 time


2. Sort elements by count descending: 1 (count 3), 2 (count 2), 3 (count 1).
3. Take top `k=2` elements: `[1, 2]`.

### 4. Brainstorming & Complexity

* **Idea 1 (By Hand)**: Hash map to count. Sort hash map keys based on values.
* *Time*: $O(N \log N)$ to sort.
* *Space*: $O(N)$ for map.


* **Idea 2 (Min-Heap)**: Hash map to count. Keep min-heap of size `k`.
* *Time*: $O(N \log k)$.
* *Space*: $O(N)$ for map + $O(k)$ for heap.


* **Idea 3 (Bucket Sort)**: Hash map to count. Create array of lists where index = frequency. Max frequency is $N$. Scan right to left.
* *Time*: $O(N)$.
* *Space*: $O(N)$.



### 5. Suggest Solutions

Prefer simple, readable code over clever tricks.

1. **Count and Sort** (maps exactly to Idea 1/By Hand step). Easiest to write, read, and explain.
2. **Bucket Sort**. Faster analytically ($O(N)$ vs $O(N \log N)$), but requires maintaining lists inside arrays.
*Selection*: Count and Sort for core logic. Unbeatable clarity.

### 6. Outline

```python
def topKFrequent(nums: list[int], k: int) -> list[int]:
    """
    Reframe: Count occurrences, sort unique elements by their counts.
    State: Hash map. Chosen because constant time lookups make counting frequencies O(N).
    Invariant: Hash map values exactly represent frequency of keys seen so far.

    count_frequencies(array) = returns dictionary mapping element -> frequency.
    sort_keys_by_value_descending(dictionary) = returns list of keys ordered by dictionary values (highest first).
    take_first_k(list, limit) = returns first limit elements.

    Core logic:
    - get frequency map using count_frequencies on nums
    - get sorted unique numbers using sort_keys_by_value_descending on frequency map
    - return take_first_k on the sorted unique numbers

    Edge cases:
    - nums has only 1 element (k=1)
    - k equals total number of unique elements
    """
    pass

```

### 7. Iterative Implementation

**Iteration 1: Skeleton code**
Translating plain english outline to function calls.

```python
def topKFrequent(nums, k):
    # Skeleton
    freq_map = count_frequencies(nums)
    sorted_nums = sort_keys_by_value_descending(freq_map)
    return take_first_k(sorted_nums, k)

```

**Iteration 2: Expanding `count_frequencies**`
Implementing the frequency map inline.

```python
def topKFrequent(nums, k):
    # Changed: implemented count_frequencies inline
    freq_map = {}
    for num in nums:
        freq_map[num] = freq_map.get(num, 0) + 1
        
    sorted_nums = sort_keys_by_value_descending(freq_map)
    return take_first_k(sorted_nums, k)

```

**Iteration 3: Expanding `sort_keys_by_value_descending**`
Using standard library sorting with a custom key.

```python
def topKFrequent(nums, k):
    freq_map = {}
    for num in nums:
        freq_map[num] = freq_map.get(num, 0) + 1
        
    # Changed: implemented sort_keys_by_value_descending inline
    # Sort the dictionary keys. The sorting key is the value from freq_map. 
    # reverse=True makes it descending.
    sorted_nums = sorted(freq_map.keys(), key=freq_map.get, reverse=True)
    
    return take_first_k(sorted_nums, k)

```

**Iteration 4: Expanding `take_first_k` (Final Core Logic)**
Applying python slicing.

```python
def topKFrequent(nums, k):
    freq_map = {}
    for num in nums:
        freq_map[num] = freq_map.get(num, 0) + 1
        
    sorted_nums = sorted(freq_map.keys(), key=freq_map.get, reverse=True)
    
    # Changed: implemented take_first_k inline using slice
    return sorted_nums[:k]

```

**Edge Case Patching**

* *Edge case*: `nums` has 1 element. Logic handles it (map gets 1 item, sorted gets 1 item, slice `[:1]` returns 1 item).
* *Edge case*: `k` = unique elements. Logic handles it (slice `[:k]` safely returns the whole list).
* *Result*: No patching needed. Core logic is inherently robust to listed edge cases.

### 8. Complexity & Optimization

* **Current Time Complexity**: $O(N \log N)$ due to sorting unique elements. (Strictly $O(N + U \log U)$ where $U$ is unique elements).
* **Current Space Complexity**: $O(U)$ for map and sorted array.

*Optimization Note*: If interviewer presses for $O(N)$ time complexity constraint, implement Bucket Sort. Sorting is the expensive section.

**Optimized code (Bucket Sort)**:

```python
def topKFrequent(nums, k):
    # 1. Count frequencies O(N)
    freq_map = {}
    for num in nums:
        freq_map[num] = freq_map.get(num, 0) + 1
        
    # 2. Array of lists where index represents frequency O(N)
    # len(nums) + 1 because highest possible frequency is size of array
    buckets = [[] for _ in range(len(nums) + 1)]
    for num, count in freq_map.items():
        buckets[count].append(num)
        
    # 3. Gather top k O(N)
    result = []
    # Traverse buckets backwards (highest frequency to lowest)
    for i in range(len(buckets) - 1, 0, -1):
        for num in buckets[i]:
            result.append(num)
            if len(result) == k:
                return result

```