# Mock 1 — Driver payout API

In this 60-minute exercise, a caller imports a driver's delivery records and later asks how much the driver earned on a particular UTC day. There are two HTTP endpoints and one calculation function. The endpoints share an in-memory store. [Session 1 specification](Coding_Mock_Sessions_2026.md#1-driver-payout-api--doordash-inspired)

## Trace one delivery through the code

A **fixture** is sample data prepared in advance. Imagine the upstream fixture contains delivery `D1` for Alice, accepted November 18 at 10:00 UTC and completed at 10:30 UTC. Alice is in the known-driver fixture, and there are no peak windows in this example. The payout service starts with an empty dictionary.

| Call | Code path | Result |
| --- | --- | --- |
| `GET /drivers/alice/payout?date=2026-11-18` | The handler reads Alice's stored records and passes them to `calculate_payout`. | Zero cents. The fixture has D1, but the store is empty. |
| `POST /drivers/alice/sync?date=2026-11-18` | The handler calls `fetch_deliveries(driver_id, start, end)`. The adapter selects Alice's matching fixture records. The handler validates the batch and saves D1 under its delivery ID. | One stored delivery. |
| Repeat the GET | The calculator receives D1, the UTC day, and the configured peak windows. | 30 × 30 cents base + 100 cents for completion = **1,000 cents**. |
| Repeat the POST, then the GET | The adapter returns D1 again. The stored ID and fields match, so sync skips the duplicate. | Still one delivery and **1,000 cents**. |

The upstream adapter stands in for a delivery service. Its date filter has to include overnight deliveries that were already active when the day started. GET uses only the records that have reached the store.

## Calculate pay by hand first

One **delivery-minute** is one delivery active for one minute. If Alice carries two orders for ten minutes, she earns twenty delivery-minutes. Count each delivery independently, then sum the results.

| Workbook example | Base at 30¢ per delivery-minute | Peak supplement at 15¢ per delivery-minute | Completion | Total |
| --- | ---: | ---: | ---: | ---: |
| A, 10:00–10:30 | 900¢ | 150¢ | 100¢ | 1,150¢ |
| B, 10:10–10:40 | 900¢ | 150¢ | 100¢ | 1,150¢ |
| **Both deliveries** | **1,800¢** | **300¢** | **200¢** | **2,300¢** |

Both deliveries are active throughout the 10:15–10:25 peak window. For each delivery, count active minutes inside the queried day, then count the subset inside each peak window. The overlap starts at the later start time and ends at the earlier end time. Count zero minutes if the end is at or before the start. Cancellation earns base and peak pay through cancellation. Only a completed delivery earns the 100-cent bonus.

The UTC day includes its starting midnight and excludes the next midnight. For a delivery from Monday 23:50 to Tuesday 00:00 outside peak hours, Monday earns **300¢** for ten active minutes. Tuesday earns **100¢** because the completion timestamp falls on Tuesday.

## Make sync safe to retry

Suppose the first POST succeeds but its response gets lost. The caller retries. Appending D1 twice would double Alice's payout. Storing one copy per delivery ID makes the import **idempotent**: the same input can be processed again with the same resulting state.

Records are final and immutable under this contract. An identical record can be skipped. A matching ID with different fields is a conflict. If a batch contains a new D2 followed by a conflicting D1, reject the whole batch with `409`, including D2. Check against both stored records and earlier rows in the incoming batch. Stage additions and commit them only after the whole batch passes.

## Get interviewer buy-in, then build in three passes

> “I understand sync imports finished deliveries and GET calculates earnings from what we've imported. One completed 30-minute delivery outside peak hours should pay 1,000 cents, even if sync runs twice. Does that match your expectation? If so, I'll test the math first, make the import safe to retry, then connect the routes and demonstrate that sequence.”

1. **Build the calculator.** If the prompt is open-ended, ask whether activity arrives as events or as one final record per delivery. Confirm whether overlapping deliveries each earn pay, which timezone defines the day, and what cancellation earns. For the written mock these rules are given. Start with `calculate_payout(deliveries, day, peak_windows)` and test the 2,300-cent example, adjacent deliveries, cancellation, and midnight.
2. **Build the import.** Confirm which records the upstream date filter returns, whether IDs are stable, and what a changed record means. Demonstrate one successful sync, an identical retry, and a conflicting batch. Show that a failed fetch returns `502` and a rejected batch leaves the prior records intact.
3. **Connect the HTTP handlers.** Confirm the success response for POST if the interviewer cares about its shape. GET returns `driver_id`, `date`, `base_cents`, `peak_cents`, `completion_bonus_cents`, and `total_cents`. Demonstrate GET before sync, POST, GET, and a retry. Also check malformed input (`400`) and an unknown driver (`404`).

**A clarification that changes correctness:** “If Tuesday is the first day anyone syncs, will the upstream return a delivery that ended exactly at Tuesday 00:00?” Its Tuesday bonus is due, but it has zero active minutes on Tuesday. A fetch based strictly on positive-duration overlap can miss that record. Agree on how it reaches storage before promising that a Tuesday-only sync can produce the bonus.

The workspace also contains a Python exercise that tracks concurrency at acceptance and a walkthrough with a flat completion rate and a database. Use the numbered session for this mock's rates and API contract. [Python event exercise](../dasher_payout.py) · [Alternate payout walkthrough](driverPayout.md)

## Worked solution

The three Python blocks below form one file, `payout.py`, in order. Only the third part needs FastAPI. This example uses Python 3.11+, the workbook's two-delivery fixture, and a single server process.

### Part 1 — Calculate one driver's earnings

Start with deliveries already in memory. The caller supplies records for one driver. Clip each interval to the day first, then reuse that clipped interval for peak pay. Check the completion timestamp separately so a midnight completion can earn a bonus even with zero active minutes that day.

```python
from dataclasses import dataclass
from datetime import UTC, date, datetime, time, timedelta

MINUTE = timedelta(minutes=1)


@dataclass(frozen=True)
class Delivery:
    delivery_id: str
    driver_id: str
    accepted_at: datetime
    ended_at: datetime
    outcome: str


def day_bounds(day):
    start = datetime.combine(day, time.min, UTC)
    return start, start + timedelta(days=1)


def minutes(start, end):
    return max(0, (end - start) // MINUTE)


def calculate_payout(deliveries, day, peak_windows):
    start, end = day_bounds(day)
    active_minutes = peak_minutes = completions = 0
    for delivery in deliveries:
        left = max(start, delivery.accepted_at)
        right = min(end, delivery.ended_at)
        if left < right:
            active_minutes += minutes(left, right)
            for peak_start, peak_end in peak_windows:
                peak_minutes += minutes(max(left, peak_start), min(right, peak_end))
        if delivery.outcome == "completed" and start <= delivery.ended_at < end:
            completions += 1

    base = 30 * active_minutes
    peak = 15 * peak_minutes
    bonus = 100 * completions
    return dict(base_cents=base, peak_cents=peak, completion_bonus_cents=bonus,
                total_cents=base + peak + bonus)
```

With two overlapping orders, the loop visits both orders and counts each one's minutes. There is no need to sort the records or loop over individual minutes. For D deliveries and P disjoint peak windows, the calculator takes O(D × (1 + P)) time and O(1) extra space.

### Part 2 — Fetch, validate, and store the batch

Here the upstream data is a list of dictionaries, just as it might arrive from a JSON API. The fixture adapter includes completed deliveries ending exactly at the start of the day so a first sync can retrieve the midnight bonus. The service stores the full interval under a globally unique delivery ID so the same overnight delivery can contribute to either day's query.

```python
from threading import Lock

KNOWN_DRIVERS = {"alice", "bob"}
FIXTURE_ROWS = [
    dict(delivery_id="A", driver_id="alice", accepted_at="2026-11-18T10:00Z",
         ended_at="2026-11-18T10:30Z", outcome="completed"),
    dict(delivery_id="B", driver_id="alice", accepted_at="2026-11-18T10:10Z",
         ended_at="2026-11-18T10:40Z", outcome="completed"),
]
STORE = {}
STORE_LOCK = Lock()


class Conflict(Exception):
    pass


class UpstreamFailure(Exception):
    pass


def utc_minute(value):
    if not isinstance(value, str):
        raise ValueError("Expected a UTC timestamp")
    stamp = datetime.fromisoformat(value)
    if stamp.utcoffset() != timedelta(0) or stamp.second or stamp.microsecond:
        raise ValueError("Expected a UTC timestamp on a whole minute")
    return stamp


PEAK_WINDOWS = [(utc_minute("2026-11-18T10:15Z"), utc_minute("2026-11-18T10:25Z"))]


def fetch_deliveries(driver_id, start, end):
    rows = []
    for row in FIXTURE_ROWS:
        if row["driver_id"] != driver_id:
            continue
        accepted = utc_minute(row["accepted_at"])
        ended = utc_minute(row["ended_at"])
        overlaps = accepted < end and ended > start
        midnight_bonus = ended == start and row["outcome"] == "completed"
        if overlaps or midnight_bonus:
            rows.append(row)
    return rows


def parse_delivery(row, driver_id):
    key = row["delivery_id"]
    if not isinstance(key, str) or not key.strip() or row["driver_id"] != driver_id:
        raise ValueError("Invalid delivery ID or driver")
    accepted = utc_minute(row["accepted_at"])
    ended = utc_minute(row["ended_at"])
    if ended <= accepted or row["outcome"] not in ("completed", "cancelled"):
        raise ValueError("Invalid delivery interval or outcome")
    return Delivery(key, driver_id, accepted, ended, row["outcome"])


def sync_deliveries(driver_id, day, fetch):
    start, end = day_bounds(day)
    rows = fetch(driver_id, start, end)
    if not isinstance(rows, list):
        raise ValueError("Expected a list of deliveries")

    pending = {}
    for row in rows:
        delivery = parse_delivery(row, driver_id)
        key = delivery.delivery_id
        if key in pending and pending[key] != delivery:
            raise Conflict(key)
        pending[key] = delivery

    with STORE_LOCK:
        for key, delivery in pending.items():
            if key in STORE and STORE[key] != delivery:
                raise Conflict(key)
        inserted = sum(key not in STORE for key in pending)
        STORE.update(pending)
    return inserted
```

A retry with A and B returns an inserted count of zero. Updating the dictionary with equal records preserves the same two deliveries and the same earnings. The lock covers the conflict check and commit together so two requests cannot both check an old value before writing. A remote adapter implementing the same fetch interface would raise `UpstreamFailure` for a failed upstream call.

### Part 3 — Connect the two HTTP routes

Both routes validate the driver and date. POST delegates to the importer and returns the number of new deliveries. GET takes a snapshot of the driver's stored deliveries, releases the lock, then calls the calculator.

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()


def request_day(driver_id, value):
    if driver_id not in KNOWN_DRIVERS:
        raise HTTPException(404, "Unknown driver")
    try:
        day = date.fromisoformat(value)
        if day.isoformat() != value or day == date.max:
            raise ValueError
        return day
    except (TypeError, ValueError):
        raise HTTPException(400, "Expected a YYYY-MM-DD date with a valid next day")


@app.post("/drivers/{driver_id}/sync")
def post_sync(driver_id: str, date: str | None = None):
    day = request_day(driver_id, date)
    try:
        inserted = sync_deliveries(driver_id, day, fetch_deliveries)
    except Conflict as exc:
        raise HTTPException(409, f"Conflicting delivery {exc}")
    except UpstreamFailure:
        raise HTTPException(502, "Could not fetch deliveries")
    except (KeyError, TypeError, ValueError) as exc:
        raise HTTPException(400, f"Malformed delivery data: {exc}")
    return {"inserted": inserted}


@app.get("/drivers/{driver_id}/payout")
def get_payout(driver_id: str, date: str | None = None):
    day = request_day(driver_id, date)
    with STORE_LOCK:
        deliveries = [d for d in STORE.values() if d.driver_id == driver_id]
    return {"driver_id": driver_id, "date": day.isoformat(),
            **calculate_payout(deliveries, day, PEAK_WINDOWS)}
```

**Try the full flow.** Save the three blocks together, install the dependencies with `python -m pip install fastapi uvicorn`, and start the service with `python -m uvicorn payout:app`. In a second terminal, run these commands in order.

```sh
url='http://127.0.0.1:8000/drivers/alice'
curl "$url/payout?date=2026-11-18"          # total_cents = 0
curl -X POST "$url/sync?date=2026-11-18"    # inserted = 2
curl "$url/payout?date=2026-11-18"          # base 1800 + peak 300 + bonus 200 = 2300
curl -X POST "$url/sync?date=2026-11-18"    # inserted = 0
curl "$url/payout?date=2026-11-18"          # total_cents = 2300
```

The store lives in server memory. Restarting the process gives you an empty store for another practice run.
