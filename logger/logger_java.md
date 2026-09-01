Here is a cleaner way to turn it into a **progressive coding interview problem**, where the initial problem is intentionally simple and the interviewer adds concurrency and systems constraints step by step.

## Base Question — File Logger

Design and implement a simple file logger.

Multiple parts of an application should be able to call:

```java
logger.log("some message");
```

Each call should append the message as a new line to a log file.

Assume Java 17 and the standard library.

### Requirements

* Messages must be appended to a single file.
* Existing contents of the file must not be overwritten.
* Each log message should appear as one complete line.
* The logger should expose something similar to:

```java
class FileLogger {
    FileLogger(Path filePath);

    void log(String message);

    void close();
}
```

### Example

```java
FileLogger logger = new FileLogger(Path.of("application.log"));

logger.log("Application started");
logger.log("User logged in");
logger.log("Request completed");

logger.close();
```

The resulting file should contain:

```text
Application started
User logged in
Request completed
```

---

# Follow-up 1 — Multiple Threads

Now assume many application threads may call:

```java
logger.log(...)
```

at the same time.

For example:

```text
Thread 1 ── log("A")
Thread 2 ── log("B")
Thread 3 ── log("C")
Thread 4 ── log("D")
```

Modify your implementation so that concurrent calls are safe.

### Additional requirements

* Log messages must not become interleaved or corrupted.
* Every accepted message must be written exactly once.
* The implementation must correctly synchronize access to the file.

### Interview discussion

How would you synchronize writes?

Would you use:

```java
synchronized
```

a `Lock`, or some other mechanism?

What happens to throughput if 100 threads are all trying to write?

---

# Follow-up 2 — Optimize Write Throughput

The synchronized implementation is correct, but profiling shows that application threads spend significant time waiting for disk I/O.

Suppose:

```text
Thread 1 ─┐
Thread 2 ─┤
Thread 3 ─┼── waiting for file write
Thread 4 ─┤
Thread 5 ─┘
```

Change the design so that application threads do **not directly write to disk**.

The goal is to optimize throughput when many threads are logging simultaneously.

### Additional requirements

* `log()` should return quickly.
* Disk writes should happen asynchronously.
* Only one component should write to the file.
* Thread synchronization must remain correct.

The interviewer may expect you to move toward:

```text
Producer threads
       │
       │ log(message)
       ▼
Thread-safe queue
       │
       ▼
Dedicated writer thread
       │
       ▼
     File
```

---

# Follow-up 3 — Batch Writes

Writing every message individually still causes many system calls.

Suppose the logger receives:

```text
50,000 log messages / second
```

Improve the writer so that it writes messages in batches.

Instead of:

```text
write(message1)
write(message2)
write(message3)
write(message4)
```

you might do:

```text
write(
    message1
    message2
    message3
    message4
)
```

### Requirements

The writer should flush when either:

* the batch reaches some maximum size, or
* a maximum amount of time has passed.

For example:

```text
batch size = 100 messages
flush interval = 100 ms
```

### Interview questions

How would the writer wait efficiently?

How do you avoid busy spinning?

Would you use something like:

```java
BlockingQueue
```

instead of repeatedly checking an ordinary queue?

---

# Follow-up 4 — Queue Capacity and Backpressure

The application can sometimes produce logs faster than the disk can persist them.

For example:

```text
Producers: 100,000 messages/sec

                 Queue
              ┌───────────┐
Threads ─────►│xxxxxxxxxxx│────► Disk
              └───────────┘

Disk: 20,000 messages/sec
```

If the queue is unbounded, the application may eventually run out of memory.

Modify the design to use a bounded queue.

For example:

```java
new ArrayBlockingQueue<>(10_000);
```

Now answer:

**What should happen when the queue is full?**

Possible policies include:

### Block the producer

```java
queue.put(message);
```

Pros:

* no logs lost

Cons:

* application threads may stall

### Drop logs

```java
queue.offer(message);
```

Pros:

* application threads never wait

Cons:

* logs can be lost

### Drop lower-priority logs

For example:

```text
DEBUG → drop
INFO  → possibly drop
ERROR → block / preserve
```

Ask the candidate to choose and justify a policy.

---

# Follow-up 5 — Preserve Ordering

Suppose the requirement changes:

> Log messages must appear in the file in the same order in which the logger accepted them.

For example:

```text
Thread A: log("A")
Thread B: log("B")
Thread C: log("C")
```

If the logger accepted them in the order:

```text
A → B → C
```

the file must contain:

```text
A
B
C
```

Discuss whether your queue-based architecture guarantees this.

Then make the problem harder:

> Do we need global ordering across threads, or only ordering within each individual thread?

This leads to discussion around synchronization semantics and what "ordering" actually means in concurrent systems.

---

# Follow-up 6 — Graceful Shutdown

The application now calls:

```java
logger.close();
```

while messages may still be in the queue.

For example:

```text
Queue:

A
B
C
D
E
```

`close()` should not immediately terminate the writer and lose those messages.

### Requirements

After `close()`:

1. stop accepting new messages,
2. write all previously accepted messages,
3. flush the file,
4. stop the writer thread,
5. close the underlying file resource.

Ask the candidate to handle races such as:

```text
Thread A                  Thread B

log("hello")              close()
```

What determines whether `"hello"` should be accepted?

---

# Follow-up 7 — Writer Failure

Suppose the writer thread encounters:

```java
IOException
```

because:

* the disk is full,
* the file becomes unavailable,
* permissions change,
* the filesystem fails.

What should happen?

Ask the candidate to define failure semantics.

Possible questions:

* Should future `log()` calls fail?
* Should the logger retry?
* How should failures be communicated to producer threads?
* Should messages remain queued?
* Can logs simply be dropped?

---

# Follow-up 8 — Log Rotation

Production systems cannot write forever to:

```text
application.log
```

because the file may grow indefinitely.

Add log rotation.

For example:

```text
application.log
application.log.1
application.log.2
```

Rotate when:

```text
file size >= 100 MB
```

or at a time boundary:

```text
every day at midnight
```

Ask:

> Which thread should perform rotation?

A clean answer is generally that the **same writer thread owns both writing and rotation**, avoiding synchronization between multiple file owners.

---

# Follow-up 9 — Multiple Log Levels

Extend the API:

```java
logger.log(LogLevel.INFO, "User logged in");
logger.log(LogLevel.ERROR, "Payment failed");
```

with:

```java
enum LogLevel {
    DEBUG,
    INFO,
    WARN,
    ERROR
}
```

Now support configurable filtering:

```text
minimum level = INFO
```

so that:

```text
DEBUG → ignored
INFO  → written
WARN  → written
ERROR → written
```

Ask where filtering should happen.

Ideally, low-priority messages should often be rejected **before entering the queue**.

---

# Follow-up 10 — Structured Log Events

Instead of sending a preformatted string, modify the API to accept structured log data.

For example:

```java
logger.log(
    LogLevel.INFO,
    "Order completed",
    Map.of(
        "orderId", "12345",
        "userId", "789"
    )
);
```

The writer might output:

```text
2026-08-28T23:40:01Z INFO Order completed orderId=12345 userId=789
```

Ask:

> Should producer threads format the final log line, or should the writer thread format it?

This introduces a throughput tradeoff:

```text
Producer formatting
    ↓
less writer work
    ↓
more CPU work on application threads
```

versus:

```text
Queue structured event
    ↓
writer formats
    ↓
very cheap log()
```

---

# Follow-up 11 — Very High Concurrency

Now assume:

```text
500 application threads
200,000 log calls/sec
```

Ask the candidate to identify the major contention points.

For example:

```text
                 contention?
                      ↓
Threads ───────► BlockingQueue ───────► Writer ─────► Disk
```

Questions:

* Is the queue becoming a contention point?
* Should messages be batched by producers?
* Would multiple producer-side buffers help?
* At what point is the physical disk itself the bottleneck?
* Can additional writer threads improve throughput when writing to **one file**?

The important observation is that adding more writer threads does not necessarily help because a single file still requires coordinated sequential writes.

---

# Follow-up 12 — Durability Semantics

Finally, distinguish:

```java
log("payment completed");
```

returning from:

### Level 1 — queued

```text
application thread
      ↓
   memory queue

log() returns
```

versus:

### Level 2 — written to OS buffer

```text
queue
  ↓
BufferedWriter
  ↓
OS page cache

log() returns
```

versus:

### Level 3 — physically durable

```text
OS cache
   ↓
fsync
   ↓
storage device

log() returns
```

Ask:

> What durability guarantee does your logger provide?

Then optionally introduce:

```java
logger.logSync(...)
```

for rare events requiring stronger durability.

---

# A Good Interview Progression

For a 45–60 minute interview, I would use this sequence:

```text
Base
│
├── Implement basic file logger
│
▼
Follow-up 1
│
├── Make it thread-safe
│
▼
Follow-up 2
│
├── Avoid application threads doing disk I/O
│
▼
Follow-up 3
│
├── Introduce BlockingQueue + writer thread
│
├── Batch writes
│
▼
Follow-up 4
│
├── Bounded queue + backpressure
│
▼
Follow-up 5
│
├── Graceful shutdown
│
▼
Follow-up 6
│
└── Discuss failures / ordering / durability
```

The natural architectural evolution is:

```text
Version 1

Threads
   │
   ▼
synchronized
   │
   ▼
 File
```

then:

```text
Version 2

Producer threads
      │
      ▼
 BlockingQueue
      │
      ▼
 Writer Thread
      │
      ▼
 BufferedWriter
      │
      ▼
    File
```

and finally:

```text
                    ┌── batching
                    │
Producers ─► bounded queue ─► writer ─► buffer ─► file
                    │          │
                    │          ├── flush policy
                    │          ├── rotation
                    │          └── failure handling
                    │
                    └── backpressure policy
```

This makes a strong interview problem because it starts as a small synchronization exercise but naturally expands into **locks, producer-consumer architecture, batching, backpressure, ordering, shutdown semantics, failure handling, and durability**—all without changing the core problem.
