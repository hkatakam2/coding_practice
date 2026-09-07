### question
Design a HashMap without using any built-in hash table libraries.

Implement the MyHashMap class:

MyHashMap() initializes the object with an empty map.
void put(int key, int value) inserts a (key, value) pair into the HashMap. If the key already exists in the map, update the corresponding value.
int get(int key) returns the value to which the specified key is mapped, or -1 if this map contains no mapping for the key.
void remove(key) removes the key and its corresponding value if the map contains the mapping for the key.

**Step 1: Restate Question**
Design a key-value map supporting `put(key, value)`, `get(key)`, and `remove(key)` without built-in hash map libraries. Must handle insertions, updates, lookups, and deletions efficiently.

---

**Step 2: Clarifying Questions & Constraints**

* **Key/Value ranges:** Keys and values are non-negative integers ($0 \le \text{key}, \text{value} \le 10^6$).
* **Operations volume:** Up to $10^4$ operations.
* **Missing keys:** `get(key)` returns `-1`; `remove(key)` is a no-op if key absent.
* **Collision resolution:** Chaining (bucket array of key-value pairs).

---

**Step 3: Trace Example by Hand**
Bucket base size = $5$. Hash function: $\text{hash}(\text{key}) = \text{key} \pmod 5$.

| Operation | Hash Index | Target Bucket State Before | Action | Target Bucket State After | Return |
| --- | --- | --- | --- | --- | --- |
| `put(1, 10)` | $1 \pmod 5 = 1$ | `[]` | Append `[1, 10]` | `[[1, 10]]` | — |
| `put(6, 60)` | $6 \pmod 5 = 1$ | `[[1, 10]]` | Collision -> Append `[6, 60]` | `[[1, 10], [6, 60]]` | — |
| `get(1)` | $1 \pmod 5 = 1$ | `[[1, 10], [6, 60]]` | Scan -> found key 1 | — | `10` |
| `get(2)` | $2 \pmod 5 = 2$ | `[]` | Scan -> empty bucket | — | `-1` |
| `put(1, 15)` | $1 \pmod 5 = 1$ | `[[1, 10], [6, 60]]` | Scan -> key 1 exists -> update val | `[[1, 15], [6, 60]]` | — |
| `remove(6)` | $6 \pmod 5 = 1$ | `[[1, 15], [6, 60]]` | Scan -> found key 6 -> pop entry | `[[1, 15]]` | — |

---

**Step 4 & 5: Brainstorming & Solutions**

* **Approach 1: Gigantic Flat Array**
* Allocate `array[1000001]` initialized to `-1`.
* *Time:* $O(1)$ all ops.
* *Space:* $O(M)$ where $M = 10^6$ regardless of element count. Wasteful for sparse maps.


* **Approach 2: Separate Chaining (Chosen)**
* Fixed array of $K$ buckets (e.g., $K = 2069$, a prime to distribute evenly).
* Each bucket holds a list of `[key, value]` pairs.
* *Time:* Average $O(N/K) \approx O(1)$ per operation.
* *Space:* $O(K + N)$, scales with actual entries stored.



---

**Step 6: Outline of Selected Implementation**

```python
class MyHashMap:
    """
    Reframe: Map integer key into bounded bucket index via modulo; store collisions in bucket lists.
    State: Array of size BASE where each slot is a list containing [key, value] pairs.
    Invariant: A key appears at most once across the entire data structure.

    _hash(key) = computes bucket index `key % BASE`.
    _find(bucket, key) = searches bucket; returns index if key found, else -1.

    Core logic:
    - put: calculate bucket index -> if key in bucket, update value; else append pair.
    - get: calculate bucket index -> if key in bucket, return value; else return -1.
    - remove: calculate bucket index -> if key in bucket, delete pair; else do nothing.

    Edge cases:
    - get on empty bucket / non-existent key -> returns -1.
    - remove on non-existent key -> no-op without error.
    - put with existing key -> overwrite existing value, avoid duplicate pairs.
    - hash collision -> multiple distinct keys map to same bucket without conflict.
    """

```

---

**Step 7: Iterative Implementation**

**Iteration 1: Skeleton with helper stubs**

```python
class MyHashMap:
    def __init__(self):
        self.BASE = 2069
        self.buckets = [[] for _ in range(self.BASE)]

    def _hash(self, key: int) -> int:
        # TODO: return key mapped to bucket index
        pass

    def put(self, key: int, value: int) -> None:
        # TODO: hash -> update or insert
        pass

    def get(self, key: int) -> int:
        # TODO: hash -> lookup
        pass

    def remove(self, key: int) -> None:
        # TODO: hash -> delete if present
        pass

```

**Iteration 2: Implement helper & search primitive**

```python
class MyHashMap:
    def __init__(self):
        self.BASE = 2069
        self.buckets = [[] for _ in range(self.BASE)]

    def _hash(self, key: int) -> int:
        # modulo maps key to valid bucket index
        return key % self.BASE

    def _find_index(self, bucket: list, key: int) -> int:
        # Scan bucket linearly for key; return pair index or -1
        for idx, (k, v) in enumerate(bucket):
            if k == key:
                return idx
        return -1

```

**Iteration 3: Implement core `put`, `get`, `remove` logic**

```python
class MyHashMap:
    def __init__(self):
        self.BASE = 2069
        self.buckets = [[] for _ in range(self.BASE)]

    def _hash(self, key: int) -> int:
        return key % self.BASE

    def _find_index(self, bucket: list, key: int) -> int:
        for idx, (k, v) in enumerate(bucket):
            if k == key:
                return idx
        return -1

    def put(self, key: int, value: int) -> None:
        bucket = self.buckets[self._hash(key)]
        idx = self._find_index(bucket, key)
        if idx != -1:
            # key exists -> update value in place
            bucket[idx][1] = value
        else:
            # key absent -> append new key-value pair
            bucket.append([key, value])

    def get(self, key: int) -> int:
        bucket = self.buckets[self._hash(key)]
        idx = self._find_index(bucket, key)
        if idx != -1:
            return bucket[idx][1]
        return -1

    def remove(self, key: int) -> None:
        bucket = self.buckets[self._hash(key)]
        idx = self._find_index(bucket, key)
        if idx != -1:
            # remove pair from bucket
            bucket.pop(idx)

```

**Iteration 4: Edge Case Walkthrough & Final Verification**

* *Key absent on `get`:* `_find_index` returns `-1`, method returns `-1`. Correct.
* *Key absent on `remove`:* `idx == -1`, branch skipped, no exception thrown. Correct.
* *Key present on `put`:* Modifies `bucket[idx][1]` directly without appending. Invariant holds.
* *Hash collisions:* Elements share bucket array; linear search differentiates by exact key match. Correct.

---

**Step 8: Complexity & Optimizations**

* **Time Complexity:**
* `_hash(key)`: $O(1)$.
* `put`, `get`, `remove`: Average $O(N / K) = O(1)$ where $K = 2069$ buckets and $N \le 10^4$ operations. Worst-case $O(N)$ when all keys hash to the same bucket.


* **Space Complexity:**
* $O(K + N)$ total space where $K$ is number of allocated buckets ($2069$) and $N$ is count of unique active keys.


* **Possible Optimization:**
* Dynamic rehashing: Double bucket array size and rehash all elements when load factor $\lambda = N/K > 0.75$ to guarantee $O(1)$ upper bound across arbitrary $N$.