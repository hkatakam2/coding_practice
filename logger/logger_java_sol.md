# 1. Restatement

We need to design a logger used like this:

```java
logger.log("request started");
```

Many application threads may call `log()` concurrently, but all messages ultimately go to **one file**.

The interesting part is that the problem evolves through three different concerns:

```text
Correctness
    ↓
Can multiple threads write safely?

Performance
    ↓
Can application threads avoid waiting for disk?

Reliability
    ↓
What happens with overload, shutdown, disk failure,
ordering, crashes, and durability?
```

The architecture we will eventually reach is:

```text
Application threads
      │
      │ log(event)
      ▼
┌──────────────────┐
│  Bounded Queue   │
└──────────────────┘
      │
      ▼
 Dedicated writer
      │
      │ batches
      ▼
 BufferedWriter
      │
      ▼
     File
```

---

# 2. Clarifying questions and assumptions

In an interview, I would establish these assumptions and continue:

* Java 17, standard library.
* Multiple threads call `log()`.
* One output file.
* We don't want partial/interleaved lines.
* Normal successful execution should write every **accepted** message exactly once.
* The logger should preserve the order in which it accepts messages.
* We don't need queued messages to survive a process crash initially.
* Eventually we want bounded memory.
* `close()` must drain accepted messages before returning.

The word **accepted** becomes important later. If the queue is full and we reject a message, we should not claim that message was accepted.

---

# 3. Manual example

Suppose three threads call:

```text
T1: log("A")
T2: log("B")
T3: log("C")
```

With a naive implementation, they might all access the same writer:

```text
T1 ─────┐
T2 ─────┼──► BufferedWriter ──► file
T3 ─────┘
```

That is dangerous because the writer is mutable shared state.

We could serialize them:

```text
T1 ──┐
T2 ──┼──► lock ──► write ──► disk
T3 ──┘
```

Correct, but now:

```text
T1: waits
T2: waits
T3: waits
```

and all three application threads are coupled to disk latency.

Instead:

```text
T1 ──► queue
T2 ──► queue
T3 ──► queue

queue = [A, B, C]

              │
              ▼
         writer thread
              │
              ▼
         A
         B
         C
```

The application threads perform cheap memory operations. Only one thread touches the file.

That is the core idea.

---

# 4. Candidate solutions

There are three reasonable designs.

| Approach                          | Correct? | Producer latency | Memory risk | Complexity |
| --------------------------------- | -------: | ---------------: | ----------: | ---------: |
| Synchronize every file write      |      Yes |             High |         Low |   Very low |
| Unbounded queue + writer          |      Yes |              Low |        High |     Medium |
| Bounded queue + writer + batching |      Yes |              Low |  Controlled |     Medium |

For a serious concurrent logger, I would choose:

```text
bounded BlockingQueue
        +
single writer thread
        +
batching
```

Let's build toward it.

---

# 5. Version 0 — Basic single-threaded logger

Ignore concurrency initially.

```java
import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;

public final class FileLogger implements AutoCloseable {

    private final BufferedWriter writer;

    public FileLogger(Path filePath) throws IOException {
        writer = Files.newBufferedWriter(
                filePath,
                StandardOpenOption.CREATE,
                StandardOpenOption.APPEND
        );
    }

    public void log(String message) throws IOException {
        writer.write(message);
        writer.newLine();
        writer.flush();
    }

    @Override
    public void close() throws IOException {
        writer.close();
    }
}
```

Conceptually:

```text
log()
 │
 ├── writer.write()
 ├── newLine()
 └── flush()
```

There is no concurrency protection.

If only one thread uses this object, that is fine.

---

# 6. Follow-up 1 — Make it thread-safe

The easiest solution is synchronization.

```java
public synchronized void log(String message) throws IOException {
    writer.write(message);
    writer.newLine();
    writer.flush();
}
```

And `close()` should participate in the same synchronization:

```java
@Override
public synchronized void close() throws IOException {
    writer.close();
}
```

Now only one thread can execute either operation at a time.

Conceptually:

```text
T1 ──┐
T2 ──┼──── synchronized ──── writer
T3 ──┘
```

Suppose:

```text
T1 gets lock
    writes A
    releases

T2 gets lock
    writes B
    releases

T3 gets lock
    writes C
    releases
```

The file becomes:

```text
A
B
C
```

## Why synchronization works

`BufferedWriter` contains mutable state.

Without synchronization:

```text
T1 ── modify writer state
T2 ── modify writer state simultaneously
```

With synchronization:

```text
T1 ────────┐
           │ exclusive
T2 waits ──┘
```

It also gives us Java memory visibility guarantees through the lock's happens-before relationship.

## But there is a performance problem

Consider:

```java
synchronized void log(String message) {
    writer.write(message);
    writer.flush();
}
```

The lock covers **disk-related work**.

If writing takes 2 ms:

```text
Thread 1: 2 ms
Thread 2: waits 2 ms
Thread 3: waits 4 ms
Thread 4: waits 6 ms
...
```

The logger may be thread-safe but can badly interfere with the application.

This distinction is essential:

> `synchronized` solves correctness. It does not automatically solve scalability.

---

# 7. Follow-up 2 — Move disk I/O off application threads

Now introduce the **producer-consumer pattern**.

Application threads are producers:

```text
Thread 1 ──┐
Thread 2 ──┼──► queue
Thread 3 ──┘
```

One background thread is the consumer:

```text
queue ──► writer thread ──► file
```

This gives us the **single-writer principle**:

> If only one thread owns the file writer, the file writer itself no longer needs synchronization.

That dramatically simplifies correctness.

---

# 8. Why `BlockingQueue`?

Java already gives us the synchronization primitive we need:

```java
BlockingQueue<LogEvent>
```

For example:

```java
ArrayBlockingQueue<LogEvent>
```

It safely supports concurrent producers and a consumer.

Application threads do:

```java
queue.offer(event);
```

Writer thread does:

```java
queue.take();
```

The queue handles the thread synchronization.

We should not reinvent this using:

```java
List
synchronized
wait()
notify()
```

unless explicitly asked.

---

# 9. Iteration 1 — Async logger skeleton

First establish the important state.

```java
import java.io.BufferedWriter;
import java.nio.file.Path;
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.BlockingQueue;

public final class ConcurrentFileLogger implements AutoCloseable {

    private final BlockingQueue<String> queue;
    private final Thread writerThread;

    public ConcurrentFileLogger(Path filePath, int queueCapacity) {
        this.queue = new ArrayBlockingQueue<>(queueCapacity);

        this.writerThread = new Thread(
                () -> runWriter(filePath),
                "file-logger-writer"
        );

        this.writerThread.start();
    }

    public void log(String message) {
        // TODO: enqueue
    }

    private void runWriter(Path filePath) {
        // TODO: consume queue
        // TODO: write messages
    }

    @Override
    public void close() {
        // TODO: stop accepting
        // TODO: drain queue
        // TODO: wait for writer
    }
}
```

The crucial architectural state is:

```text
queue
writerThread
```

Not:

```text
lock around BufferedWriter
```

---

# 10. Iteration 2 — Producer and consumer

Producer:

```java
public void log(String message) {
    queue.add(message);
}
```

Consumer:

```java
private void runWriter(Path filePath) {
    try (BufferedWriter writer = Files.newBufferedWriter(
            filePath,
            StandardOpenOption.CREATE,
            StandardOpenOption.APPEND)) {

        while (true) {
            String message = queue.take();

            writer.write(message);
            writer.newLine();
            writer.flush();
        }

    } catch (IOException | InterruptedException exception) {
        // TODO: failure handling
    }
}
```

The important observation is that this loop:

```java
String message = queue.take();
```

does **not busy-spin**.

If there is nothing available:

```text
writer thread
     │
     ▼
queue.take()
     │
     ▼
   sleeps
```

When a producer adds something, the writer wakes up.

That is one major reason to use `BlockingQueue`.

---

# 11. Why not poll continuously?

Bad:

```java
while (true) {
    String message = queue.poll();

    if (message != null) {
        write(message);
    }
}
```

When the queue is empty:

```text
poll
poll
poll
poll
poll
poll
...
```

The writer consumes CPU doing no useful work.

That is **busy waiting**.

Better:

```java
queue.take();
```

or:

```java
queue.poll(timeout, unit);
```

The thread efficiently blocks.

---

# 12. Follow-up 3 — Batching

Our current writer still does:

```text
write A
flush

write B
flush

write C
flush
```

That loses much of the benefit of asynchronous logging.

Instead:

```text
queue:

A
B
C
D
E
F
```

Take several:

```text
batch = [A, B, C, D, E]
```

Then:

```text
write A
write B
write C
write D
write E
flush once
```

The expensive operation is often not simply copying characters into a Java buffer.

The expensive boundary is ultimately:

```text
user-space memory
       ↓
operating system
       ↓
filesystem
       ↓
storage
```

Reducing flushes and system calls improves throughput.

---

# 13. Batch policy

A common rule is:

```text
flush when:

batch size >= 100

OR

100 ms elapsed
```

Why both?

If traffic is high:

```text
100 messages arrive quickly
        ↓
flush immediately
```

If traffic is low:

```text
3 messages arrive
        ↓
wait no more than 100 ms
        ↓
flush
```

Otherwise a partially filled batch could sit forever.

This is a classic:

```text
throughput vs latency
```

tradeoff.

Large batches:

```text
higher throughput
higher logging latency
```

Small batches:

```text
lower latency
more I/O overhead
```

---

# 14. Iteration 3 — Batch collection

The general algorithm becomes:

```java
private void runWriter(Path filePath) {
    List<String> batch = new ArrayList<>(MAX_BATCH_SIZE);

    while (...) {
        String first = queue.poll(
                FLUSH_INTERVAL_MILLIS,
                TimeUnit.MILLISECONDS
        );

        if (first == null) {
            continue;
        }

        batch.add(first);

        queue.drainTo(
                batch,
                MAX_BATCH_SIZE - batch.size()
        );

        writeBatch(batch);

        batch.clear();
    }
}
```

`drainTo()` is useful here.

Instead of repeatedly acquiring queue synchronization:

```java
queue.poll()
queue.poll()
queue.poll()
queue.poll()
```

we can efficiently transfer several available elements.

---

# 15. Follow-up 4 — Why the queue must be bounded

Consider an unbounded queue.

```java
new LinkedBlockingQueue<>();
```

Suppose:

```text
Application:
100,000 messages/sec

Disk:
20,000 messages/sec
```

Every second:

```text
+80,000 queued messages
```

After 10 seconds:

```text
800,000
```

After 100 seconds:

```text
8,000,000
```

Eventually:

```text
OutOfMemoryError
```

The logger has converted a slow disk into a memory leak.

This is where **backpressure** enters.

---

# 16. Backpressure

Backpressure means:

> What do we do when producers generate work faster than consumers can handle it?

Use:

```java
new ArrayBlockingQueue<>(10_000);
```

Now the logger cannot consume unlimited memory.

When it reaches:

```text
10,000 / 10,000
```

we must make a policy decision.

There is no universally correct policy.

### Policy A — Block

```java
queue.put(event);
```

Meaning:

```text
Logger overloaded
      ↓
application thread waits
```

Benefit:

```text
don't voluntarily drop messages
```

Cost:

```text
logging can slow the actual application
```

For some audit systems, that's appropriate.

---

### Policy B — Reject

```java
if (!queue.offer(event)) {
    throw new RejectedExecutionException();
}
```

Meaning:

```text
logging never waits for queue capacity
```

This is appropriate when protecting application latency is more important.

---

### Policy C — Drop low-priority logs

For example:

```text
DEBUG → drop
INFO  → drop during severe overload
WARN  → try harder
ERROR → block/preserve
```

Many practical logging systems use variations of this.

For the interview implementation, I'll use:

```text
bounded queue + reject when full
```

because the semantics are clean:

> If `log()` returns normally, the event was accepted.

---

# 17. Follow-up 5 — Ordering

Suppose:

```text
T1 -> log("A")
T2 -> log("B")
T3 -> log("C")
```

What does "preserve order" mean?

This needs careful definition.

If calls happen concurrently:

```text
        A
       /
------X-------
       \
        B
```

there isn't necessarily a meaningful external order between them.

The logger needs a **linearization point**.

For us, that is the successful queue insertion.

If queue insertion happens:

```text
A
B
C
```

the writer sees:

```text
A
B
C
```

because we have one queue and one consumer.

So our semantics are:

> File order equals logger acceptance order.

Within a single producer thread:

```java
logger.log("A");
logger.log("B");
```

we naturally preserve:

```text
A
B
```

assuming both are accepted.

---

# 18. Follow-up 6 — Graceful shutdown

This is subtler than it looks.

Suppose:

```text
queue = [A, B, C]

main thread:
logger.close();
```

We cannot just:

```java
writerThread.interrupt();
```

and terminate.

Otherwise:

```text
A
B
C
```

may disappear.

The desired lifecycle is:

```text
OPEN
 │
 │ close()
 ▼
DRAINING
 │
 │ queue becomes empty
 ▼
CLOSED
```

After entering `DRAINING`:

```text
new logs rejected
existing logs written
```

---

# 19. The important shutdown race

Suppose:

```text
Thread A                      Thread B

log("hello")                  close()
```

Naive implementation:

```java
if (!closed) {
    queue.offer(message);
}
```

and:

```java
closed = true;
```

can produce ambiguous races.

We want a precise guarantee:

> Either the log operation is accepted before close shuts admission, or it is rejected.

We'll protect **admission state** with a small synchronization section.

Notice what we are synchronizing now.

Old design:

```text
LOCK
 └── disk I/O
```

New design:

```text
LOCK
 └── boolean check + queue insertion
```

The critical section is dramatically smaller.

---

# 20. Lifecycle synchronization

Conceptually:

```java
synchronized (lifecycleLock) {
    if (!accepting) {
        throw ...
    }

    queue.offer(event);
}
```

Close:

```java
synchronized (lifecycleLock) {
    accepting = false;
}
```

This establishes a clean boundary.

Suppose `log()` gets the lock first:

```text
log
 ├── check accepting
 ├── queue event
 └── unlock

close
 ├── accepting = false
 └── unlock
```

The message must be drained.

If `close()` gets it first:

```text
close
 ├── accepting = false
 └── unlock

log
 ├── sees false
 └── rejects
```

Clean semantics.

---

# 21. Follow-up 7 — Writer failure

Suppose the writer gets:

```java
IOException
```

Maybe:

```text
disk full
permission denied
filesystem unavailable
```

We need to remember that failure.

For example:

```java
private volatile IOException writerFailure;
```

Writer:

```java
catch (IOException exception) {
    writerFailure = exception;
}
```

Future producers can check:

```java
if (writerFailure != null) {
    throw new IllegalStateException(
            "Logger writer has failed",
            writerFailure
    );
}
```

A critical systems point:

> Once storage fails, you cannot magically preserve "exactly once" durability.

If disk is full, accepted in-memory events may be impossible to persist.

Our guarantee therefore becomes:

```text
Normal execution:
accepted message → written exactly once

Storage/process failure:
best effort; guarantee no longer possible
```

That is a much more precise statement than simply saying "exactly once."

---

# 22. Plain-English implementation outline

Our selected solution:

```java
void log(String message) {
/*
 * Reframe:
 * Application threads should enqueue log events instead of performing
 * file I/O themselves.
 *
 * State:
 * - bounded BlockingQueue for accepted events
 * - one writer thread
 * - accepting flag controlling lifecycle
 * - writerFailure recording asynchronous I/O failure
 * - lifecycle lock coordinating log() with close()
 *
 * Chosen because:
 * - BlockingQueue safely coordinates multiple producers
 * - one writer eliminates concurrent file mutation
 * - bounded capacity prevents unlimited memory growth
 * - batching reduces write/flush overhead
 *
 * Invariant:
 * Only the writer thread accesses the BufferedWriter.
 *
 * Core logic:
 * - log() checks lifecycle
 * - log() inserts an event into the bounded queue
 * - writer collects events into batches
 * - writer writes the batch and flushes
 *
 * Shutdown:
 * - stop accepting new events
 * - writer drains all accepted events
 * - flush and close file
 * - close() waits for writer termination
 *
 * Edge cases:
 * - full queue => reject
 * - log after close => reject
 * - writer failure => future calls fail
 */
}
```

---

# 23. Final Java 17 implementation

Here is the core implementation I would be comfortable writing in an interview.

```java
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.UncheckedIOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;
import java.time.Instant;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.RejectedExecutionException;
import java.util.concurrent.TimeUnit;

public final class ConcurrentFileLogger implements AutoCloseable {

    public enum Level {
        DEBUG,
        INFO,
        WARN,
        ERROR
    }

    private record LogEvent(
            Instant timestamp,
            Level level,
            String message
    ) {}

    private final Path filePath;
    private final BlockingQueue<LogEvent> queue;

    private final int maxBatchSize;
    private final long flushIntervalMillis;

    private final Object lifecycleLock = new Object();
    private final Thread writerThread;

    private volatile boolean accepting = true;
    private volatile IOException writerFailure;

    public ConcurrentFileLogger(
            Path filePath,
            int queueCapacity,
            int maxBatchSize,
            long flushIntervalMillis
    ) {

        Objects.requireNonNull(filePath);

        if (queueCapacity <= 0) {
            throw new IllegalArgumentException(
                    "queueCapacity must be positive"
            );
        }

        if (maxBatchSize <= 0) {
            throw new IllegalArgumentException(
                    "maxBatchSize must be positive"
            );
        }

        if (flushIntervalMillis <= 0) {
            throw new IllegalArgumentException(
                    "flushIntervalMillis must be positive"
            );
        }

        this.filePath = filePath;
        this.queue = new ArrayBlockingQueue<>(queueCapacity);
        this.maxBatchSize = maxBatchSize;
        this.flushIntervalMillis = flushIntervalMillis;

        this.writerThread = new Thread(
                this::runWriter,
                "concurrent-file-logger"
        );

        this.writerThread.start();
    }

    public void log(String message) {
        log(Level.INFO, message);
    }

    public void log(Level level, String message) {
        Objects.requireNonNull(level);
        Objects.requireNonNull(message);

        LogEvent event = new LogEvent(
                Instant.now(),
                level,
                message
        );

        synchronized (lifecycleLock) {
            ensureHealthy();

            if (!accepting) {
                throw new IllegalStateException(
                        "Logger is closed"
                );
            }

            boolean accepted = queue.offer(event);

            if (!accepted) {
                throw new RejectedExecutionException(
                        "Logger queue is full"
                );
            }
        }
    }

    private void runWriter() {
        List<LogEvent> batch =
                new ArrayList<>(maxBatchSize);

        try (BufferedWriter writer = Files.newBufferedWriter(
                filePath,
                StandardOpenOption.CREATE,
                StandardOpenOption.APPEND)) {

            while (accepting || !queue.isEmpty()) {

                LogEvent first = queue.poll(
                        flushIntervalMillis,
                        TimeUnit.MILLISECONDS
                );

                if (first == null) {
                    continue;
                }

                batch.add(first);

                queue.drainTo(
                        batch,
                        maxBatchSize - batch.size()
                );

                writeBatch(writer, batch);

                batch.clear();
            }

            writer.flush();

        } catch (IOException exception) {
            writerFailure = exception;

        } catch (InterruptedException exception) {
            Thread.currentThread().interrupt();

            writerFailure = new IOException(
                    "Logger writer thread was interrupted",
                    exception
            );
        }
    }

    private void writeBatch(
            BufferedWriter writer,
            List<LogEvent> batch
    ) throws IOException {

        for (LogEvent event : batch) {
            writer.write(format(event));
            writer.newLine();
        }

        writer.flush();
    }

    private String format(LogEvent event) {
        return event.timestamp()
                + " "
                + event.level()
                + " "
                + event.message();
    }

    private void ensureHealthy() {
        IOException failure = writerFailure;

        if (failure != null) {
            throw new IllegalStateException(
                    "Logger writer has failed",
                    failure
            );
        }
    }

    @Override
    public void close() {
        synchronized (lifecycleLock) {
            accepting = false;
        }

        try {
            writerThread.join();

        } catch (InterruptedException exception) {
            Thread.currentThread().interrupt();

            throw new IllegalStateException(
                    "Interrupted while closing logger",
                    exception
            );
        }

        IOException failure = writerFailure;

        if (failure != null) {
            throw new UncheckedIOException(
                    "Logger writer failed",
                    failure
            );
        }
    }
}
```

---

# 24. Trace the implementation

Suppose:

```text
T1 -> log("A")
T2 -> log("B")
T3 -> log("C")
```

Assume acceptance occurs:

```text
T1
T3
T2
```

Queue:

```text
[A, C, B]
```

Writer:

```java
LogEvent first = queue.poll(...);
```

Gets:

```text
A
```

Then:

```java
queue.drainTo(batch, ...)
```

may produce:

```text
batch = [A, C, B]
```

Then:

```java
writeBatch(...)
```

writes:

```text
A
C
B
```

and calls:

```java
flush()
```

once.

The writer is the only thread touching:

```java
BufferedWriter
```

so there is no file-writer race.

---

# 25. Edge case — Empty logger

```java
ConcurrentFileLogger logger = ...;

logger.close();
```

Writer condition:

```java
while (accepting || !queue.isEmpty())
```

Initially:

```text
accepting = true
```

After close:

```text
accepting = false
queue empty
```

Condition becomes:

```text
false || false
```

Writer terminates.

Correct.

---

# 26. Edge case — Close with queued messages

Suppose:

```text
queue = [A, B, C]
```

Then:

```java
close();
```

sets:

```text
accepting = false
```

Writer checks:

```java
accepting || !queue.isEmpty()
```

which is:

```text
false || true
```

so it continues.

Eventually:

```text
queue = []
```

Now:

```text
false || false
```

and exits.

`close()` calls:

```java
writerThread.join();
```

so it does not return until the draining has finished.

---

# 27. Edge case — `log()` races with `close()`

Case 1:

```text
log obtains lifecycleLock first
```

Then:

```text
accepting = true
queue.offer(event)
```

Afterward close gets the lock:

```text
accepting = false
```

Result:

```text
event accepted
event must be drained
```

Case 2:

```text
close obtains lifecycleLock first
```

Then:

```text
accepting = false
```

Later `log()` sees:

```text
accepting = false
```

and throws.

There is therefore a clean acceptance boundary.

---

# 28. Edge case — Queue full

Suppose capacity is:

```text
10,000
```

and all slots are occupied.

Then:

```java
queue.offer(event)
```

returns:

```java
false
```

We throw:

```java
RejectedExecutionException
```

This is not message loss hidden from the caller.

The contract is:

```text
log() returned
    ↓
accepted

log() threw
    ↓
not accepted
```

---

# 29. Follow-up — Could we block instead?

Yes.

You might say:

```java
queue.put(event);
```

But this changes the fundamental API behavior:

```text
queue full
    ↓
log() blocks
    ↓
application thread stalls
```

For:

```text
ERROR / audit / financial event
```

that may be desirable.

For:

```text
DEBUG logging inside request processing
```

probably not.

So backpressure is a **product/reliability requirement**, not simply a coding decision.

---

# 30. Follow-up 8 — Log rotation

Suppose:

```text
application.log
```

reaches 100 MB.

You want:

```text
application.log
application.log.1
application.log.2
```

The critical architectural answer is:

> The writer thread should also own rotation.

Do not introduce:

```text
writer thread ──► file
rotation thread ──► same file
```

because we have just reintroduced shared mutable file state.

Instead:

```text
Writer thread
    │
    ├── write
    ├── check current size
    ├── close file
    ├── rename file
    ├── create new file
    └── continue
```

The single-writer invariant remains intact.

Pseudo-code:

```java
if (currentFileSize >= MAX_FILE_SIZE) {
    writer.flush();
    writer.close();

    rotateFiles();

    writer = openNewFile();
}
```

This is a good example of why **ownership** is often more powerful than adding locks.

---

# 31. Follow-up 9 — Log levels

We already added:

```java
enum Level {
    DEBUG,
    INFO,
    WARN,
    ERROR
}
```

Suppose minimum level is:

```text
INFO
```

Then filtering should normally happen in the producer:

```java
public void log(Level level, String message) {

    if (level.ordinal() < minimumLevel.ordinal()) {
        return;
    }

    // enqueue
}
```

Why before the queue?

Because if DEBUG is disabled, doing:

```text
construct event
      ↓
enqueue
      ↓
dequeue
      ↓
writer discovers it should ignore it
```

is wasted work.

Prefer:

```text
DEBUG disabled
      ↓
return immediately
```

---

# 32. Follow-up 10 — Structured events

Instead of storing:

```java
String
```

we used:

```java
record LogEvent(
    Instant timestamp,
    Level level,
    String message
) {}
```

This is useful because the producer captures semantic data:

```text
timestamp
level
message
```

while the writer decides representation:

```text
2026-08-28T23:45:00Z INFO Payment completed
```

This separation resembles many real systems:

```text
event
   ↓
serialization
   ↓
storage
```

You could later add:

```java
record LogEvent(
        Instant timestamp,
        Level level,
        String message,
        Map<String, String> attributes
) {}
```

without changing the producer-consumer architecture.

---

# 33. Producer-side vs writer-side formatting

There is a subtle CPU tradeoff.

### Producer formatting

```text
application thread
    │
    ├── format timestamp
    ├── build string
    └── queue string
```

Writer does less work.

But the application spends more CPU logging.

### Writer formatting

```text
application thread
    │
    └── queue structured event

writer
    │
    └── formatting
```

Producer latency decreases, but the single writer can become CPU constrained.

At moderate load, writer-side formatting is simple and clean.

At extreme load, you measure.

---

# 34. Follow-up 11 — 500 producer threads

Suppose:

```text
500 producer threads
200,000 logs/sec
```

Our path is now:

```text
                    possible
                    contention
                       ↓
500 threads ──► lifecycle lock ──► ArrayBlockingQueue
                                      │
                                      ▼
                                  one writer
                                      │
                                      ▼
                                     disk
```

There are multiple possible bottlenecks.

First:

```text
lifecycleLock
```

But we only hold it for:

```text
check boolean
queue.offer()
```

not disk I/O.

So it is dramatically cheaper than the original synchronization.

Second:

```text
ArrayBlockingQueue
```

internally coordinates concurrent access and can itself become contended.

Third:

```text
single writer
```

may become CPU bound because of formatting.

Finally:

```text
storage
```

may simply be unable to absorb any more bytes.

And this leads to an important systems principle:

> Concurrency cannot make a fundamentally sequential resource infinitely fast.

---

# 35. Why not use four writer threads?

Imagine:

```text
queue
 │
 ├── writer 1 ──┐
 ├── writer 2 ──┼──► same file
 ├── writer 3 ──┤
 └── writer 4 ──┘
```

Now we need synchronization again to prevent corruption.

And ultimately the file must contain some sequential byte ordering.

We may get:

```text
more coordination
more context switching
more complexity
```

without improving physical throughput.

For a **single file**, one writer is usually the clean architecture.

If throughput requirements exceed that architecture, change the system boundary:

```text
multiple files
partitioning
network log collector
Kafka
stdout + logging agent
```

rather than blindly adding file-writer threads.

---

# 36. Follow-up 12 — Durability

This is one of the most important concepts in this entire problem.

Suppose:

```java
logger.log("payment successful");
```

returns.

What exactly has happened?

In our implementation:

```text
application thread
      │
      ▼
in-memory BlockingQueue
```

At this point, `log()` returns.

So our guarantee is approximately:

> The event has been accepted into process memory.

It does **not** mean:

```text
physically durable on disk
```

---

# 37. Stage 1 — Queued

```text
Java process

BlockingQueue
     │
     │ event exists here
     ▼
```

If the process crashes:

```text
power loss
kill -9
JVM crash
```

the queued message disappears.

---

# 38. Stage 2 — Written and flushed

Our writer calls:

```java
writer.flush();
```

Conceptually:

```text
Java BufferedWriter
      ↓
operating system
      ↓
page cache
```

This usually gets data out of Java's user-space buffer.

But `flush()` does not necessarily mean the physical device has committed the bytes.

---

# 39. Stage 3 — `fsync`

For stronger durability you need something analogous to:

```java
FileChannel.force(true);
```

Conceptually:

```text
Java
 ↓
OS page cache
 ↓
FileChannel.force()
 ↓
storage
```

This is much more expensive.

If you did:

```java
force(true)
```

after every log:

```text
log
fsync
log
fsync
log
fsync
```

throughput could collapse.

So again we get:

```text
durability
    ↕
throughput
```

---

# 40. Real meaning of batching

Batching isn't merely a small code optimization.

It allows us to amortize expensive operations.

Without batching:

```text
message 1 → flush
message 2 → flush
message 3 → flush
message 4 → flush
```

With batch size 100:

```text
100 messages
     ↓
one flush
```

If strong durability were needed:

```text
100 messages
     ↓
one force()
```

Now the expensive durability operation is shared across 100 records.

This pattern appears everywhere in backend systems:

```text
database batching
Kafka batching
network packet batching
disk writes
metrics aggregation
```

---

# 41. Exactly-once discussion

If an interviewer says:

> Every log must appear exactly once.

You should challenge the exact semantics.

Inside one running JVM, absent storage failure:

```text
one accepted queue item
      ↓
one consumer
      ↓
one write
```

so we can reasonably provide once-only processing.

But consider:

```text
writer writes A
      ↓
process crashes
      ↓
did A reach persistent storage?
```

Without acknowledgment and durable recovery metadata, we may not know.

After restart, retrying could produce:

```text
A
A
```

Not retrying could produce:

```text
nothing
```

This is the classic distributed/storage problem:

```text
at-most-once
at-least-once
exactly-once
```

True crash-safe exactly-once semantics require considerably more machinery.

---

# 42. Complexity

For `log()`:

```java
queue.offer(event);
```

is effectively:

```text
O(1)
```

for the bounded queue operation.

So producer work is approximately:

```text
Time: O(1)
```

plus synchronization contention.

Memory:

```text
O(queueCapacity)
```

because the queue is bounded.

For the writer, if there are `n` messages containing `B` total characters:

```text
O(B)
```

is the meaningful complexity because every character ultimately has to be written.

Batch working memory:

```text
O(maxBatchSize)
```

Total bounded logger memory:

```text
O(queueCapacity + maxBatchSize)
```

---

# 43. Important interview tests

### Main example

```text
T1 -> A
T2 -> B
T3 -> C
```

Expected:

```text
all accepted records appear exactly once
```

Their concurrent global order is determined by acceptance order.

### Smallest case

```java
logger.close();
```

Expected:

```text
clean shutdown
empty file allowed
```

### Important edge case

```text
queue capacity = 1

queue already full

log("new")
```

Expected:

```text
RejectedExecutionException
```

rather than unbounded memory growth.

### Central invariant test

Start many producers:

```text
T1:
A1
A2
A3
...
A1000

T2:
B1
B2
...
B1000
```

After `close()`:

```text
2,000 accepted messages
2,000 output lines
no corrupted/interleaved lines
```

And for each individual producer:

```text
A1 before A2 before A3 ...
```

should hold.

---

# 44. The interview progression you should remember

Don't memorize the final class first. Remember the architectural reasoning:

```text
Step 1
Direct file write

        ↓ concurrency problem

Step 2
synchronized file write

        ↓ correct but blocking application threads

Step 3
BlockingQueue + dedicated writer

        ↓ queue can grow

Step 4
bounded queue

        ↓ overload requires policy

Step 5
backpressure / rejection

        ↓ too many writes

Step 6
batching

        ↓ lifecycle problem

Step 7
graceful shutdown

        ↓ real-world failures

Step 8
writer failure handling

        ↓ production requirements

Step 9
rotation / levels / structured logs

        ↓ stronger guarantees

Step 10
durability semantics
```

The most important insight is the transition from:

```java
synchronized void log(...) {
    writeToDisk();
}
```

to:

```java
void log(...) {
    queue.offer(event);
}
```

with:

```text
ONE dedicated writer thread
```

That change separates **application concurrency** from **disk serialization**.

Once you understand that, the rest of the problem—batching, bounded queues, backpressure, graceful shutdown, ordering, failure handling, and durability—is mostly about defining increasingly precise guarantees around that producer-consumer architecture.
