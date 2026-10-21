# question 
Rate limiter

# clarification
1. scope: inside a process or a distributed limiter shared by many services? in-process to shart
2. unique id: IP address, user ID, API key etc. use `key` a string
3. interface: does the caller needs to allow/deny or do they also have to retry? 
4. burst behavior: should the client be able to burst? eg 10 requests at once, as long as average rate holds? Yes, upto a cap
5. concurrency: many threads calling? Yes
6. scale: how many distinct keys? assume millions over time, so memory per key and clean up of idle keys matter
7. failure mode: if we're unsure, do we fail open or close? for in-process this is mute but matters for distributed one 


# ideas:
1. fixed window counter; count requests per minute bucket
   1. simplest O(1), boundary problem: 2X burst across a window edge
2. sliding window log; store every timestamp and drop old ones
   1. exact logic; O(n) memory per key, too large for millions of keys
3. sliding window counter: weighted blend of current and previous windows
   1. O(1), smooth ; approximate
4. leaky buket: queue drains at constant rate
   1. smooths output perfectly; no bursts, need a queue
5. Token buckets: buckets refills at rate r upto capacity C;
   1. O(1) memory, allows controlled bursts;  two parameters to tune

# outline
tocken bucket: it satisfies burst requirement and O(1) memory requirement. 
the key trick is lazy fill: no background timer, we compute how many tockens might have arrived since the last we looked

allow(key):
    bucket = find_or_create_bucket(key) # new callers start with a full bucket
    refill(bucket) # add tokens for the time lapsed, capped at capacity
    return try_consume(bucket) 

refill(bucket):
    elapsed = now - bucket.last_refill
    bucket.tokens = min(capacity, bucket.tokens + elapsed * rate)
    bucket.last_refill = now

try_consume(bucket):
    if bucket.tokens >= 1:
        bucket.tokens -= 1
        return ALLOW
    else:
        return DENY

# implement
```python
import time

class _Bucket:
    def __init__(self, tokens, last_refill):
        self.tokens = tokens
        self.last_refill = last_refill

class TokenBucketLimiter:
    def __init__(self, capacity, refill_rate):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.buckets = {}

    def allow(self, key):
        bucket = self._find_or_create_bucket(key)
        self._refill(bucket)
        return self._try_consume(bucket)

    def _find_or_create_bucket(key):
        if key not in self.buckets:
            self.buckets[key] = _Bucket(self.capacity, time.monotonic())
        return self.buckets[key]

    def _refill(bucket):
        now = time.monotonic()
        elapsed = now - bucket.last_refill
        bucket.tokens = max(self.capacity, bucket.tokens + elapsed * self.refill_rate)
        bucket.last_refill = now

    def _try_comsume(bucket):
        if bucket.tokens >= 1:
            bucket.tokens -= 1
            return True
        else:
            return False
```

# edge cases:
1. find_or_create_bucket
   1. race on creation; guard the dict with a registry lock
   2. unbounded memory: millions of kwys that never return stay forever; preiodically evict idle buckets
2. refill
   1. clock goes backwards. elabsed can be negative, calmp it
   2. lond idle period; elapsed can be huge max(capacity, elapsed * rate) handles it
3. try_consume
   1. concurrent requests on one key: read-modify-write; a per bucket lock, so different keys never contend
   2. wighted requests
   3. denied callers want to know when they can comeback
4. config
   1. capacity <= 0, rate <= 0 should fail fast; ValueError

```python
import math
import threading
import time
from dataclasses import dataclass


@dataclass
class Decision:
    allowed: bool
    retry_after: float = 0.0   # seconds until a retry could succeed


class _Bucket:
    __slots__ = ("tokens", "last_refill", "lock")

    def __init__(self, tokens, last_refill):
        self.tokens = tokens
        self.last_refill = last_refill
        self.lock = threading.Lock()          # EDGE: per-key lock, no cross-key contention


class TokenBucketLimiter:
    def __init__(self, capacity, refill_rate, idle_ttl=3600, clock=time.monotonic):
        # EDGE: fail fast on nonsense config
        if capacity <= 0 or refill_rate <= 0:
            raise ValueError("capacity and refill_rate must be positive")
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.clock = clock                     # EDGE: injectable clock for tests
        # EDGE: TTL below full-refill time would make eviction lossy
        self.idle_ttl = max(idle_ttl, capacity / refill_rate)
        self.buckets = {}
        self._registry_lock = threading.Lock() # EDGE: protects dict creation/eviction
        self._last_sweep = clock()

    # allow(key):
    def allow(self, key, cost=1):
        # EDGE: cost > capacity can never succeed, so deny without a retry hint
        if cost <= 0:
            raise ValueError("cost must be positive")
        if cost > self.capacity:
            return Decision(False, math.inf)

        self._maybe_sweep_idle()               # EDGE: bound memory

        # bucket = find_or_create_bucket(key)
        bucket = self._find_or_create_bucket(key)

        # EDGE: refill + consume must be atomic per key
        with bucket.lock:
            # refill(bucket)
            self._refill(bucket)
            # return try_consume(bucket)
            return self._try_consume(bucket, cost)

    # find_or_create_bucket(key): new callers start with a full bucket
    def _find_or_create_bucket(self, key):
        with self._registry_lock:              # EDGE: no double-creation race
            bucket = self.buckets.get(key)
            if bucket is None:
                bucket = _Bucket(self.capacity, self.clock())
                self.buckets[key] = bucket
            return bucket

    # refill(bucket):
    def _refill(self, bucket):
        now = self.clock()
        # elapsed = now - bucket.last_refill   (EDGE: clamp if clock misbehaves)
        elapsed = max(0.0, now - bucket.last_refill)
        # bucket.tokens = min(capacity, bucket.tokens + elapsed * rate)
        #   (the min() also handles very long idle periods)
        bucket.tokens = min(self.capacity, bucket.tokens + elapsed * self.refill_rate)
        # bucket.last_refill = now
        bucket.last_refill = now

    # try_consume(bucket):
    def _try_consume(self, bucket, cost):
        # if bucket.tokens >= cost: bucket.tokens -= cost; return ALLOW
        if bucket.tokens >= cost:
            bucket.tokens -= cost
            return Decision(True)
        # else: return DENY  (EDGE: tell the caller when to come back)
        return Decision(False, (cost - bucket.tokens) / self.refill_rate)

    # EDGE: evict buckets idle longer than the TTL (equivalent to a full bucket)
    def _maybe_sweep_idle(self):
        now = self.clock()
        if now - self._last_sweep < self.idle_ttl:
            return
        with self._registry_lock:
            self._last_sweep = now
            stale = [k for k, b in self.buckets.items()
                     if now - b.last_refill > self.idle_ttl]
            for k in stale:
                del self.buckets[k]


```

# quick testing
```python
t = [0.0]
rl = TokenBucketLimiter(capacity=3, refill_rate=1, clock=lambda: t[0])

assert all(rl.allow("u1").allowed for _ in range(3))   # burst of 3 OK
d = rl.allow("u1")
assert not d.allowed and d.retry_after == 1.0          # 4th denied, retry in 1s
t[0] += 1.0
assert rl.allow("u1").allowed                          # one token refilled
assert rl.allow("u2").allowed                          # keys are independent
```