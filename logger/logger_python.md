Here’s a good way to structure this as a **progressive coding interview**, where the candidate first solves a simple synchronization problem and then evolves it into a high-throughput concurrent logger.

## Base Question — Thread-Safe File Logger

You are building a logger used by multiple threads in the same process.

Implement a `FileLogger` class that writes log messages to a single file.

```text
class FileLogger:
    log(message)
```

Multiple threads may call `log()` concurrently.

### Requirements

* Every call to `log(message)` must eventually write the message to the file.
* A log message must never be partially mixed with another log message.
* The logger must be thread-safe.
* Assume each log entry occupies one line.
* Preserve the order in which threads successfully acquire permission to write.

Example:

```text
Thread A: log("A")
Thread B: log("B")
Thread C: log("C")
```

The file should contain complete entries such as:

```text
A
B
C
```

and never corrupted output such as:

```text
AB
C
```

### Candidate task

Implement:

```python
class FileLogger:
    def __init__(self, filename):
        ...

    def log(self, message):
        ...
```

Discuss the synchronization mechanism you use and the complexity of `log()`.

---

# Follow-up 1 — Lock Contention

Assume the logger is now used by **hundreds of application threads**.

The straightforward implementation protects the file write using a mutex:

```text
lock
    write message to file
unlock
```

Profiling shows that application threads spend significant time waiting for the logger lock.

### Question

How would you redesign the logger so that application threads spend less time blocked on file I/O?

Constraints:

* There is still only one output file.
* Messages must not become corrupted.
* It is acceptable for writing to happen asynchronously.
* `log()` should preferably return quickly.

This naturally leads toward:

```text
producer threads
       |
       v
thread-safe queue
       |
       v
single writer thread
       |
       v
file
```

---

# Follow-up 2 — Implement the Asynchronous Logger

Modify the logger so that callers only enqueue messages.

A dedicated background thread should consume messages and write them to the file.

Expose:

```python
class FileLogger:
    def __init__(self, filename):
        ...

    def log(self, message):
        ...

    def close(self):
        ...
```

### Requirements

`log()`:

```text
enqueue message
return
```

Writer thread:

```text
wait for messages
remove messages from queue
write them to file
```

`close()` must:

```text
prevent/handle new writes appropriately
flush all queued messages
terminate writer thread
close the file
```

Questions for the candidate:

* What data structure would you use between producers and the writer?
* How does the writer sleep when no messages exist?
* How do you wake it efficiently?
* How do you terminate it safely?

---

# Follow-up 3 — Batch Writes

The asynchronous version improves application latency, but throughput is still lower than desired because the writer performs:

```text
write(message1)
write(message2)
write(message3)
...
```

Each write introduces overhead.

### Question

Modify the writer so it **batches messages**.

For example:

```text
queue:

A
B
C
D
E
```

Instead of:

```text
write(A)
write(B)
write(C)
write(D)
write(E)
```

perform something similar to:

```text
buffer = A + B + C + D + E

write(buffer)
```

Possible batching policy:

```text
write when:

batch size >= 100 messages

OR

10 milliseconds have elapsed
```

Discuss the tradeoff between:

```text
larger batches
    -> better throughput
    -> higher logging latency

smaller batches
    -> lower latency
    -> more file writes
```

---

# Follow-up 4 — Bounded Queue / Backpressure

Now assume producers can generate logs faster than the disk can write them.

An unbounded queue could eventually consume all available memory.

### Question

Modify the design so the queue has a maximum capacity.

For example:

```text
MAX_QUEUE_SIZE = 100_000
```

What should happen when the queue becomes full?

Possible policies could include:

```text
1. Block the producer.

2. Drop the newest message.

3. Drop the oldest message.

4. Drop low-priority logs but preserve ERROR logs.

5. Write synchronously as a fallback.
```

Ask the candidate to choose and justify a policy.

Then implement the selected behavior.

---

# Follow-up 5 — Preserve Logging Order

Suppose:

```text
Thread A calls log("A")
Thread B calls log("B")
```

at almost exactly the same time.

### Question

What ordering guarantee does your implementation provide?

Possible guarantees:

```text
No ordering guarantee between concurrent callers.

OR

queue insertion order.

OR

global sequence-number order.
```

If strict ordering is required, modify the logger to assign each message a monotonically increasing sequence number:

```text
1 -> A
2 -> B
3 -> C
```

and ensure the writer produces:

```text
A
B
C
```

in sequence order.

Discuss whether this additional guarantee is actually necessary for a production logger.

---

# Follow-up 6 — Flush Semantics

Add:

```python
logger.flush()
```

Calling `flush()` should guarantee that every message logged **before the call to `flush()`** has reached the operating system/file.

For example:

```text
log("A")
log("B")

flush()

log("C")
```

When `flush()` returns:

```text
A and B must have been written.
```

`C` does not necessarily need to have been written.

### Question

How would the producer thread communicate this requirement to the writer thread?

One possible concept is placing a special queue item:

```text
Message("A")
Message("B")
FlushBarrier(event)
Message("C")
```

The writer:

```text
writes A
writes B
flushes file
signals event
continues
```

---

# Follow-up 7 — Graceful Shutdown

Consider:

```text
100 producer threads
        |
        v
      logger
        |
        v
10,000 queued messages
```

The application begins shutting down.

### Question

Implement:

```python
logger.close()
```

with the guarantee:

> Every message successfully accepted by `log()` before `close()` begins must be written before `close()` returns.

Think about races such as:

```text
Thread A: log(...)
Thread B: close()
Thread C: log(...)
```

Ask the candidate to define the contract for calls racing with `close()`.

For example:

```text
OPEN
  |
  v
CLOSING
  |
  v
CLOSED
```

---

# Follow-up 8 — Error Handling

Suppose the writer encounters:

```text
disk full

permission error

file deleted

I/O error
```

### Question

What happens to producer threads?

An asynchronous logger introduces an important problem:

```text
producer:
    log("hello")
    returns successfully

writer:
    later fails to write
```

The producer is no longer present to receive the error.

Ask the candidate to design an error strategy.

Possible approaches:

```text
store logger error state

future log() calls fail

invoke an error callback

write to stderr

retry

fall back to another file
```

---

# Follow-up 9 — Log Rotation

The log file should not grow indefinitely.

Implement automatic rotation:

```text
application.log

application.log.1
application.log.2
...
```

When:

```text
application.log >= 100 MB
```

the writer should:

```text
close current file
rename/rotate files
open new application.log
continue writing
```

Questions:

* Who should perform rotation?
* Do producer threads need to know about rotation?
* How do you ensure rotation cannot happen in the middle of a log entry?

With the single-writer architecture, rotation can remain entirely inside the writer thread.

---

# Follow-up 10 — Multiple Log Levels

Support:

```python
logger.debug(...)
logger.info(...)
logger.warn(...)
logger.error(...)
```

Under heavy load, the logger should prioritize important messages.

For example:

```text
queue utilization < 80%
    accept everything

queue utilization >= 80%
    start dropping DEBUG

queue utilization >= 95%
    drop DEBUG and INFO

ERROR
    never drop
```

Ask the candidate how this changes the queue/backpressure design.

---

# Follow-up 11 — Multiple Files

Now logs need to go to different files:

```text
application.log
audit.log
metrics.log
```

Example:

```python
logger.log("application", message)
logger.log("audit", message)
```

### Question

Should you use:

```text
one global writer thread

OR

one writer thread per file

OR

a small writer thread pool?
```

Discuss throughput, ordering, synchronization, and resource usage.

---

# Follow-up 12 — Very High Throughput

The system now generates:

```text
1,000,000+ log events / second
```

The queue itself becomes a contention point.

### Question

How could the architecture evolve further?

Possible discussion areas:

```text
per-thread buffers

multiple producer queues

lock-free MPSC queues

ring buffers

memory-mapped files

binary log encoding

zero-copy approaches

dedicated logging processes

Disruptor-style ring buffers
```

The candidate does not necessarily need to implement these. This becomes a systems-design discussion.

---

# Full Interview Progression

I would run the interview in this order:

```text
Level 1
Thread-safe synchronous logger
        |
        v
Level 2
Producer/consumer asynchronous logger
        |
        v
Level 3
Batch writes
        |
        v
Level 4
Bounded queue + backpressure
        |
        v
Level 5
flush() semantics
        |
        v
Level 6
Graceful shutdown
        |
        v
Level 7
Error handling
        |
        v
Level 8
Log rotation
        |
        v
Level 9
Priority / log levels
        |
        v
Level 10
Extreme throughput architecture
```

The **core interview insight** is the progression from:

```text
many threads
    |
mutex
    |
file
```

to:

```text
many producer threads
    |
small synchronized operation
    |
concurrent/bounded queue
    |
single writer thread
    |
batching
    |
file
```

This is a strong interview problem because the first version is just a mutex problem, but the extensions test **producer-consumer design, condition variables, queues, backpressure, batching, lifecycle management, ordering guarantees, failure semantics, and performance engineering**.
