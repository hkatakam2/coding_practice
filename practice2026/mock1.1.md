# Driver Payout API — interview revision notes

## 60-second recap

**Problem.** Given a driver and the start of a 24-hour window, fetch their activity from an upstream API, store it, and return base pay, bonus, and total earnings.

**Rules agreed in this mock.** Each order independently earns **30 cents per minute** from acceptance to delivery. Count only the portion inside the requested window. Add the payable seconds across all orders, then round once to the nearest cent, half up. Award **one $5 bonus** if at least three deliveries finish in the window. In a fresh interview, confirm these rules with the interviewer.

**The distinction to remember:** An order earns **base pay for time worked inside the window**. It counts toward the **bonus if its delivery timestamp falls inside the window**. An order can contribute to either calculation independently.

**Implementation in one breath.** Use a half-open UTC window `[start, end)`. Pair acceptance and delivery timestamps by order ID. Clip each order to the window, sum seconds, count completions, and return integer cents. Store upstream events by stable event ID so a retry produces the same payout.

---

## 1. Clarify the contract before coding

| Ask the interviewer | Answer used in this mock |
|---|---|
| “If two orders overlap for ten minutes, what does the driver earn during those ten minutes?” | Both earn independently. Two active orders earn 60 cents per minute together. |
| “Which events start and stop the pay clock?” | `accepted` starts it and `delivered` stops it. `picked_up` does not change the rate. |
| “If an order crosses midnight, which day gets the pay and the completion?” | Split base pay at the boundary. Assign the completion to the window containing the delivery timestamp. |
| “How do rounding and bonuses work?” | Round base pay once after summing. Three or more completions earn one 500-cent bonus. |
| “What can I assume about upstream data?” | Events can arrive out of order. Each returned order is complete and has valid, whole-second timestamps. The upstream client returns full histories for overlapping orders or raises on failure. Event IDs are globally unique and immutable. Confirm boundary coverage as well, especially deliveries exactly at `start`. |

**First example to establish and run:** A runs 10:00–10:20. B runs 10:10–10:30. Each earns $6, so the expected payout is **$12**. If your answer is $9, you merged the overlapping time. If your answer depends on pickup time, you started the clock at the wrong event.

## 2. Memorize the calculation

For every completed order:

```text
payable start   = max(accepted_at, window_start)
payable end     = min(delivered_at, window_end)
payable seconds = max(0, payable end - payable start)  # in seconds
completion      = window_start <= delivered_at < window_end
```

At 30 cents per minute, **each second earns half a cent**. For a nonnegative integer number of seconds, `(total_seconds + 1) // 2` gives cents rounded half up. For example, 3 seconds earn 1.5 cents, rounded to 2. Keeping money in integer cents also makes the API response and test assertions straightforward.

### Reference Python implementation

```python
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone


@dataclass(frozen=True)
class Event:
    order_id: str
    kind: str
    at: datetime


@dataclass(frozen=True)
class Payout:
    base_cents: int
    bonus_cents: int

    @property
    def total_cents(self) -> int:
        return self.base_cents + self.bonus_cents


def calculate_payout(events: list[Event], start: datetime) -> Payout:
    if start.utcoffset() is None:
        raise ValueError("start must include a UTC offset")

    start = start.astimezone(timezone.utc)
    end = start + timedelta(hours=24)
    accepted_at: dict[str, datetime] = {}
    delivered_at: dict[str, datetime] = {}

    for event in events:
        if event.kind == "accepted":
            accepted_at[event.order_id] = event.at.astimezone(timezone.utc)
        elif event.kind == "delivered":
            delivered_at[event.order_id] = event.at.astimezone(timezone.utc)

    total_seconds = 0
    completions = 0

    for order_id, delivered in delivered_at.items():
        overlap_start = max(accepted_at[order_id], start)
        overlap_end = min(delivered, end)

        if overlap_end > overlap_start:
            total_seconds += int((overlap_end - overlap_start).total_seconds())

        if start <= delivered < end:
            completions += 1

    return Payout(
        base_cents=(total_seconds + 1) // 2,
        bonus_cents=500 if completions >= 3 else 0,
    )
```

**Why no sorting?** Each order’s pay depends only on its own two timestamps. A dictionary pairs them even when delivery appears first in the input. For \(n\) events and \(k\) orders, the calculation takes expected **\(O(n)\) time and \(O(k)\) extra space**. The direct lookup `accepted_at[order_id]` relies on the agreed complete-history guarantee.

## 3. Build the API around the calculation

**Endpoint:** `GET /drivers/{driver_id}/payout?start=2026-11-18T00:00:00Z`

**Example response:** `{"driver_id":"d-17","base_cents":1200,"bonus_cents":0,"total_cents":1200}`

| Step | What to implement | Why it matters |
|---|---|---|
| 1. Validate the window | Require a timestamp with an offset. Convert to UTC, then add 24 hours. | Defines exactly 24 elapsed hours. |
| 2. Fetch upstream activity | Fetch all pages before acquiring a database connection. | A timeout on page two must not turn page one into a partial day’s earnings. |
| 3. Store events | In one transaction, batch insert the events. Make `event_id` the primary key and use `ON CONFLICT (event_id) DO NOTHING`. | The database handles concurrent duplicate inserts. Checking whether a row exists before inserting leaves a race. |
| 4. Read the histories | In the same transaction, load events for the driver and the order IDs returned by the complete fetch. | An acceptance may precede `start`. Filtering individual event timestamps to the window can discard the start of a payable order. |
| 5. Calculate and respond | Run the pure function and return the breakdown after the transaction succeeds. | A repeated request can insert **zero** rows and still correctly return **$12**. |

The storage row needs `event_id`, `driver_id`, `order_id`, `kind`, and `occurred_at`. The calculation function needs only the last three order-related values: `order_id`, `kind`, and the timestamp.

## 4. Know the tests and what each catches

| Test | Expected result | Bug it catches |
|---|---|---|
| Empty successful fetch | 0 base, 0 bonus | Mishandling a legitimate empty day |
| Two overlapping 20-minute orders, events shuffled | 1,200 cents base, 0 bonus | Merging intervals or relying on arrival order |
| Accepted 23:55, delivered 00:05 | 150 cents base in each window. Completion belongs to the new window. | Assigning the entire order to one day |
| Two prior completions, third order delivered exactly at `end` | No bonus in the ending window. Delivery counts in the next window. | Using `delivered <= end`. Two prior completions make the bug visible in dollars. |
| Three one-second orders | 2 cents base + 500 cents bonus = **502 cents** | Rounding each order first would produce 3 cents base. |
| Six completed orders in one window | Bonus is still 500 cents | Accidentally paying $5 per group of three |
| Same six-event request twice | Both responses return $12. Exactly six event rows remain. | Duplicate storage or calculating only from newly inserted rows |
| Upstream times out on page two | Timeout error and no partial batch stored | Treating partial results as a complete payout |

**Verification detail interviewers may probe:** Mocking `fetch_events` to raise proves the endpoint handles an exception. To prove the **client** handles pagination correctly, use the real client with a fake transport that succeeds on page one and times out on page two. To prove **rollback**, run an integration test against PostgreSQL and inspect the committed rows from another connection.

## 5. Be ready for the failure follow-ups

| Interviewer asks | Short answer |
|---|---|
| “What does the driver see if upstream is unavailable?” | A timeout maps to 504. Another upstream failure can map to 502. A successful empty fetch returns 200 with zero earnings. |
| “The fourth insert fails. What happens to the first three?” | Let the exception leave the transaction so the batch rolls back. Previously committed rows remain. Map a temporary database outage to 503 after cleanup. |
| “What if the database committed but the acknowledgment was lost?” | The service cannot know the outcome from the lost acknowledgment. A retry is safe because event IDs are unique and the endpoint recalculates from complete stored history. |
| “What changes if the API actually sends money?” | This design calculates earnings. A transfer would need its own durable payout identity and a way to determine whether a previous transfer succeeded before retrying it. |

## 6. How to execute this in a timed interview

1. **Ask the overlap question.** It determines whether you sum per-order durations or merge intervals.
2. **Write down `$12` before coding.** You now have an expected result independent of your implementation.
3. **Implement and run the pure function first.** A working calculation gives you something concrete before you spend time on HTTP or SQL.
4. **Add midnight and rounding tests.** These expose two errors the $12 example cannot catch.
5. **Connect fetching and storage.** Be ready to explain why the second request still returns $12 when it inserts nothing.
6. **Close with what you verified.** Distinguish tests you ran, cases you traced by hand, and integrations still to implement. In this mock, the code and tests were written as examples and the cases were traced by hand. No tests were executed.

**Last-minute recall:** *Pair by order ID → clip each interval → sum payable seconds → round once → count deliveries in `[start, end)` → apply the bonus once. Fetch fully, store by event ID, and calculate from the full relevant history on every retry.*