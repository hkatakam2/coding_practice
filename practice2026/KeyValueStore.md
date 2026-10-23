# time based key value store

# calrifications
1. what does get(key, t) return? the value from the latest set with timestamp <= t, or "" if none exists
2. is the key always known? unknown keys return ""
3. do timestamps arrive in increasing order per key? usually yes, make sure correctness does not depend on it
4. can the same (key, timestamp) be set twice? yes, the later write overwrites
5. value is string, timestamp is int
6. scale and access pattern? many sets, many gets; get should be fast (sub linear)
7. thread safety, persistence, deletes? out of scope

# ideas
the shape of the problem is: for each key, i keep history of (timestamp, value), and a 
query asks for the floor of t in this history
1. nested hashmap(key -> {timestamp -> value})
   1. set O(1)
   2. get has to find the largest timestamp <= t. I will have to walk down t one tick at a time
2. per key sorted array + binary search
   1. if writes arrive in order set is O(1) as we are appending at the end of an array
   2. get is binary search for the floor, O(log n)
   3. out of order writes cost O(n)
3. sortedDict
   1. both set, get O(log n) even out of order
   2. not native to python implementation

# outline
the access pattern is append heavy, and read heavy. 
outline:
set(key, value, ts):
    history = history_of(key) # create if missing
    record(history, ts, value) # keep history sorted by ts

get(key, ts):
    history = history_of(key) # if missing -> nothing found
    i = last_index_at_or_before(history, ts)
    if i is nothing: return ""
    return value_at(history, i)

# implementation
```python
from bisect import bisect_right
class TimeMap:
    def __init__(self):
        # history_of(key) -> (times, values); two parallel lists sorted by time
        self.history = {}

    def set(self, key, value, ts):
        times, values = self.history.setDefault(key, ([], []))

        # append at the end
        times.append(ts)
        values.append(value)

    def get(self, key, ts):
        times, values = self.history[key]

        i = bisect_right(times, ts) - 1

        return values[i]
# two parallel list let me use bisect directly on times
```

# edge cases
1. history_of(key):
   1. unknown key in set: raised keyError, instead use .get to return ""
   2. don't use defaultDict for reads, that silently creates empty lists for missing keys
2. last_index_at_or_before(h, ts):
   1. ts earlier than the first record: bisect_right returns -1 and python wraps around giving wrong answer. need to check i < 0
   2. ts matched the exact stored timestamp: we need bisect_right; bisect_left worn't work
   3. ts after the last entry; bisect_right return the floor, already works
3. record(history, timestamp, value):
   1. same ts set twice: append only created duplicates; so overwrite in place
   2. out-of-order ts: appending would break sortedness. keep a fast path for inorder writes and binary search for out of order

```python
from bisect import bisect_left, bisect_right


class TimeMap:
    def __init__(self):
        # history_of(key) -> (times, values): parallel lists, sorted by time
        self.history = {}

    def set(self, key: str, value: str, timestamp: int) -> None:
        # history = history_of(key)
        times, values = self.history.setdefault(key, ([], []))

        # record(history, ts, value)
        # Fast path: in-order write (the common case) -> O(1) append
        if not times or timestamp > times[-1]:
            times.append(timestamp)
            values.append(value)
            return

        # EDGE: out-of-order or duplicate timestamp -> binary search for the slot
        i = bisect_left(times, timestamp)
        if times[i] == timestamp:
            values[i] = value              # EDGE: same (key, ts) -> overwrite
        else:
            times.insert(i, timestamp)     # EDGE: out-of-order -> O(n) insert,
            values.insert(i, value)        #       keeps the lists sorted

    def get(self, key: str, timestamp: int) -> str:
        # history = history_of(key)
        record = self.history.get(key)     # EDGE: unknown key, and a read never creates an entry
        if record is None:
            return ""
        times, values = record

        # i = last_index_at_or_before(history, ts)
        i = bisect_right(times, timestamp) - 1   # right: ts == stored time counts as a match

        # if i is nothing: return ""
        if i < 0:                          # EDGE: ts earlier than every record
            return ""                      #       (don't let -1 wrap to the last item)

        # return value_at(history, i)
        return values[i]
```

# follow-ups
1.  time complexity
    1.  set O(1) for in-order; O(log n) to search, O(n) to shift if out-of-order
    2.  get O(log n); where n is the number of writes for that key
2.  space complexity: O(total writes)
3. 