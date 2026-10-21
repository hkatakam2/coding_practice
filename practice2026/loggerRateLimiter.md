# question
Logger rate limiter: Allow printing if the message is not printed in the last 10 seconds

# calrifiations:
1. what is the rule? a message prints only if the same message was not printed in the last 10 seconds
2. boundary? gap must be >= 10
3. does the suppressed call reset the window? No
4. is the window per message or global? per message
5. single threded? memory limits? assume multiple threads can call it. Memory should not grow forever with distinct messages

# ideas
1. hashmap message -> last printed timestamp; O(1) access but, memory grows
2. hashset + queue ordered by time; 
   1. timestamps only move forward, so the queue is naturally sorted by print time
   2. on each call pop expired entries from the front, removing from the set too
   3. Then membership in the set answers, "printed within the time window?" 
   4. memory is bounded by the messages printed in the last 10 seconds 

# outline
should_print(now, msg):
    forget_expired(now) # drop anything older than the window
    if recently_printed(msg): 
        return False
    remember(now, msg) # start a fresh window for this msg
    return True 

forget_expired(now):
    while oldest entry exists and expires at `now`:
        drop it from queue and from set


# implement
```python
class Logger:
    def __init__(self, window=10):
        self.window = window
        self.recent = set()
        self.queue = deque()

    def should_print(self, now, msg):
        self._forget_expired(now)
        if msg in self.recent:
            return False
        
        self.recent.add(msg)
        self.queue.append((now, msg))
        return True

    def _forget_expired(self, now):
        while self.queue and self.order[0][0] <= now - self.window:
            _, old_msg = self.queue.popleft()
            self.recent.discard(old_msg)
```

# edge cases
1. forget_expired: out of order timestamps? if `now` goes backwards? fix treat the late arriving msg treated as now
2. recently-printed: set and queue drift? we only add if msg not in set, so no duplicates in queue and discard is safe
3. multithreading? two can see not seen and print, use lock

```python
import threading
from collections import deque

class Logger:
    def __init__(self, window=10):
        # EDGE: invalid window makes the limiter meaningless
        if window <= 0:
            raise ValueError("window must be positive")
        self.window = window
        self.recent = set()
        self.order = deque()
        self.latest = float("-inf")     # EDGE: track newest timestamp seen
        self.lock = threading.Lock()    # EDGE: check-then-act race

    def should_print(self, now, msg):
        with self.lock:
            # EDGE: out-of-order timestamp -> clamp so the queue stays sorted
            now = max(now, self.latest)
            self.latest = now

            # forget_expired(now)
            self._forget_expired(now)

            # if recently_printed(msg): return False
            # (throttled calls exit here, so the window is never refreshed)
            if msg in self.recent:
                return False

            # remember(now, msg)
            self.recent.add(msg)
            self.order.append((now, msg))
            return True

    def _forget_expired(self, now):
        # while oldest entry exists and is expired at `now`: drop it
        # EDGE: `<=` makes a gap of exactly `window` allowed (inclusive boundary)
        while self.order and self.order[0][0] <= now - self.window:
            _, old_msg = self.order.popleft()
            self.recent.discard(old_msg)
```

# followups
1. Distributed system: keep per-message state in Redis, using SET key NX EX 10. It’s atomic, and TTL handles expiry, so no queue is needed.
2. Max N prints per window instead of 1: replace the set with a map of message → deque of timestamps, or use a token bucket.
3. Huge message cardinality: hash messages to fixed-size keys, or accept a Bloom-filter-style approximation if occasional false suppression is tolerable.