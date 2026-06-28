### question
Design a time-based key-value data structure that can store multiple values for the same key at different time stamps and retrieve the key's value at a certain timestamp.

Implement the TimeMap class:

TimeMap() Initializes the object of the data structure.
void set(String key, String value, int timestamp) Stores the key key with the value value at the given time timestamp.
String get(String key, int timestamp) Returns a value such that set was called previously, with timestamp_prev <= timestamp. If there are multiple such values, it returns the value associated with the largest timestamp_prev. If there are no values, it returns "".

### 1. Restating the Question

Design a dictionary-like data structure. Keys map to values, but values are versioned by time.

* `set` saves a value at a specific time.
* `get` fetches the value for a key at a specific time. If that exact time doesn't exist, fetch the most recent value *before* that time. If no value exists before or at that time, return `""`.

### 2. Clarifying Questions & Confirmations

* **Q:** Are timestamps in `set` always strictly increasing?
* *Assumption:* Yes. Chronological inserts are standard for this problem.


* **Q:** Can values be empty strings?
* *Assumption:* Yes. Handled like normal strings.


* **Inputs:** `set(string, string, int)`, `get(string, int)`
* **Outputs:** `set` -> `void`, `get` -> `string`

### 3. Example by Hand

Inputs:

1. `set("foo", "bar", 1)`
2. `get("foo", 1)`
3. `get("foo", 3)`
4. `set("foo", "bar2", 4)`
5. `get("foo", 4)`
6. `get("foo", 5)`

Trace:

1. "foo" -> `[(1, "bar")]`
2. Look up "foo" at time 1. Exact match. -> `"bar"`
3. Look up "foo" at time 3. No exact match. Largest time <= 3 is 1. -> `"bar"`
4. "foo" -> `[(1, "bar"), (4, "bar2")]`
5. Look up "foo" at time 4. Exact match. -> `"bar2"`
6. Look up "foo" at time 5. No exact match. Largest time <= 5 is 4. -> `"bar2"`

### 4. Brainstorming & Complexity

* **Idea A (HashMap + Linear Scan):** * Map key to array of `(timestamp, value)`.
* `set`: Append to array. `O(1)` time.
* `get`: Iterate backwards through array until `timestamp_prev <= requested_timestamp`. `O(N)` time. Matches hand-trace exactly.


* **Idea B (HashMap + Binary Search):** * Since timestamps are appended chronologically, the array is inherently sorted.
* `set`: Append to array. `O(1)` time.
* `get`: Binary search the array for largest time `<= requested_timestamp`. `O(log N)` time.



### 5. Suggest Solutions

Prefer simple and clear.

* **Solution A (Linear)** is the by-hand method: just look at the history backwards until we find a valid time. Highly readable, but slow for huge histories.
* **Solution B (Binary Search)** is the standard acceptable answer. Since the history is sorted, binary search is the natural fit. We will implement Solution B.

### 6. Outline of Selected Implementation

```python
def get(self, key: str, timestamp: int) -> str:
    """
    Reframe: Map key to a chronological timeline, search timeline for nearest past event.
    State: Hash map of arrays `store[key] = [(timestamp, value)]`, chosen because timeline is chronological allowing fast binary search.
    Invariant: Timestamps in each key's array are strictly increasing.

    find_closest_value(timeline, target_time) = binary searches the timeline to find the largest timestamp <= target_time and returns its value.

    Core logic:
    - grab timeline array for the key
    - use find_closest_value on the timeline to get the correct string
    - return the string

    Edge cases:
    - key does not exist in our store
    - timeline exists, but all timestamps are strictly greater than the requested timestamp
    """

```

### 7. Iterative Implementation

**Iteration 1: Skeleton with stubs**

```python
class TimeMap:
    def __init__(self):
        self.store = {} # string -> list of (timestamp, value)

    def set(self, key: str, value: str, timestamp: int) -> None:
        # TODO: append to timeline
        pass

    def get(self, key: str, timestamp: int) -> str:
        # TODO: grab timeline
        # TODO: return find_closest_value
        pass

    def _find_closest_value(self, timeline, target_time):
        # TODO: binary search
        pass

```

**Iteration 2: Core logic of get/set (Happy Path)**

```python
class TimeMap:
    def __init__(self):
        self.store = {} # Map key to list of tuples: (timestamp, value)

    def set(self, key: str, value: str, timestamp: int) -> None:
        # ADDED: Handle map insertion (assuming key exists for happy path)
        self.store[key].append((timestamp, value))

    def get(self, key: str, timestamp: int) -> str:
        # ADDED: Grab timeline and call helper (assuming key exists for happy path)
        timeline = self.store[key]
        return self._find_closest_value(timeline, timestamp)

    def _find_closest_value(self, timeline, target_time):
        # TODO: binary search
        pass

```

**Iteration 3: Implement binary search helper (Happy Path)**

```python
class TimeMap:
    def __init__(self):
        self.store = {}

    def set(self, key: str, value: str, timestamp: int) -> None:
        # ADDED: Default dict logic if key is new
        if key not in self.store:
            self.store[key] = []
        self.store[key].append((timestamp, value))

    def get(self, key: str, timestamp: int) -> str:
        timeline = self.store[key]
        return self._find_closest_value(timeline, timestamp)

    def _find_closest_value(self, timeline, target_time):
        # ADDED: Standard binary search for rightmost valid element
        left, right = 0, len(timeline) - 1
        res = ""
        
        while left <= right:
            mid = (left + right) // 2
            mid_time, mid_val = timeline[mid]
            
            if mid_time <= target_time:
                res = mid_val  # Valid candidate, save it
                left = mid + 1 # Try to find a closer one on the right
            else:
                right = mid - 1 # Too large, look left
                
        return res

```

**Iteration 4: Patch Edge Cases (Final Code)**
Walking through edge cases from Step 6:

1. *Key does not exist:* `get` will throw KeyError. Need to return `""`.
2. *All timestamps > requested:* Binary search naturally handles this (never hits `mid_time <= target_time`, `res` stays `""`).

```python
class TimeMap:
    def __init__(self):
        self.store = {}

    def set(self, key: str, value: str, timestamp: int) -> None:
        if key not in self.store:
            self.store[key] = []
        self.store[key].append((timestamp, value))

    def get(self, key: str, timestamp: int) -> str:
        # PATCHED: Edge case 1 - Key does not exist
        if key not in self.store:
            return ""
            
        timeline = self.store[key]
        return self._find_closest_value(timeline, timestamp)

    def _find_closest_value(self, timeline, target_time):
        left, right = 0, len(timeline) - 1
        res = "" # PATCHED: Edge case 2 inherently handled. Defaults to "" if nothing found.
        
        while left <= right:
            mid = (left + right) // 2
            mid_time, mid_val = timeline[mid]
            
            if mid_time <= target_time:
                res = mid_val 
                left = mid + 1 
            else:
                right = mid - 1 
                
        return res

```

### 8. Complexity & Optimizations

* **Time Complexity:** * `set`: `O(1)` amortized. Appending to a list.
* `get`: `O(log N)` where N is the number of entries for the specific key.


* **Space Complexity:** `O(M)` where M is the total number of `set` operations across all keys.
* **Optimization/Refactor:** In Python, writing manual binary search is good for interviews to show you know it, but for production, you would optimize readability by using the built-in `bisect` module.

```python
# Optimization: Using bisect for cleaner code
import bisect

def _find_closest_value_optimized(self, timeline, target_time):
    # Extract just timestamps for bisect (or use a custom key in Python 3.10+)
    times = [t for t, v in timeline] 
    idx = bisect.bisect_right(times, target_time)
    
    if idx == 0:
        return ""
    return timeline[idx - 1][1]

```

*(Note: In a real interview, stick to the manual binary search as `bisect` on a list of tuples requires extra boilerplate or O(N) array slicing in older Python versions. The manual loop is actually more performant here).*