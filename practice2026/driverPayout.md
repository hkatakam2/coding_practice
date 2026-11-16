# question
Build a driver payout API. Fetch a driver’s activity from an upstream API, store it, and calculate the driver’s pay for a 24-hour period, including base pay and bonuses.

I’d solve this in three passes during the interview. First, calculate pay for a small list of activities you already have. Second, fetch and store those activities so retries are safe. Third, connect the two pieces with an API endpoint. That gives you something you can demonstrate even before the upstream integration is finished.

## Step 1. Clarify what earns money

The biggest ambiguity is what the upstream means by **activity**. I’d ask the interviewer three questions:

1. “Does the upstream return one record per completed delivery, or events such as `accepted`, `picked_up`, and `completed`?”
2. “What are the base-pay and bonus rules? Is the bonus earned once per period or on every qualifying delivery?”
3. “Does the caller choose the start of a rolling 24-hour window, or are we calculating pay for a specific local calendar day?”

For a concrete walkthrough, assume the interviewer gives us these rules:

- The upstream returns one record per delivery, with a stable delivery ID, status, and completion timestamp.
- Each completed delivery earns **$5**. Completing **at least three** in the window earns a **one-time $10 bonus**. These are example rates.
- The caller supplies a timezone-aware start time. The window covers exactly 24 elapsed hours. A delivery belongs to the window containing its **completion time**.

## Step 2. Work one example by hand

Suppose the window starts November 14 at 09:00 UTC and ends November 15 at 09:00 UTC.

| Delivery | Activity | Counts? |
|---|---|---|
| A | Completed Nov 14 at 09:00 | Yes, exactly at the start |
| B | Completed Nov 14 at 16:30 | Yes |
| C | Accepted Nov 14 at 08:55, completed Nov 15 at 08:59 | Yes, completion determines eligibility |
| D | Completed Nov 15 at 09:00 | No, it belongs to the next window |
| E | Canceled Nov 14 at 12:00 | No |

The expected answer is **3 deliveries, $15 base pay, $10 bonus, $25 total**. If the upstream sends B twice, the answer should still be $25.

That example gives you two implementation decisions immediately. Use the interval `start <= completed_at < end`, and count each delivery ID once.

## Step 3. Write the payout calculation first

Once storage gives us the number of eligible deliveries, the payout function is small. I’d use integer cents so money calculations stay exact.

```python
BASE_CENTS_PER_DELIVERY = 500
BONUS_THRESHOLD = 3
BONUS_CENTS = 1_000


def calculate_payout(completed_count: int) -> dict:
    base = completed_count * BASE_CENTS_PER_DELIVERY
    bonus = BONUS_CENTS if completed_count >= BONUS_THRESHOLD else 0

    return {
        "completed_deliveries": completed_count,
        "base_pay_cents": base,
        "bonus_cents": bonus,
        "total_pay_cents": base + bonus,
        "currency": "USD",
    }
```

I’d test **two, three, and four** deliveries right away. The expected totals are `$10`, `$25`, and `$30`. The jump at three checks the threshold. The fourth delivery checks that we award the bonus only once.

## Step 4. Store activity so a retry produces the same answer

Here’s the bug the interviewer may be looking for. The client calls the endpoint, the server stores three deliveries, and the response gets lost. The client retries. If we blindly append three more rows, we calculate pay for six deliveries.

Give each delivery a unique key in storage. Here’s a PostgreSQL schema:

```sql
CREATE TABLE driver_deliveries (
    driver_id      TEXT NOT NULL,
    delivery_id    TEXT NOT NULL,
    status         TEXT NOT NULL,
    completed_at   TIMESTAMPTZ,
    PRIMARY KEY (driver_id, delivery_id)
);
```

For this version, assume the upstream returns the current delivery record and completed records are final. Store each fetched record with an upsert:

```sql
INSERT INTO driver_deliveries (driver_id, delivery_id, status, completed_at)
VALUES ($1, $2, $3, $4)
ON CONFLICT (driver_id, delivery_id) DO UPDATE
SET status = EXCLUDED.status,
    completed_at = EXCLUDED.completed_at;
```

Then ask storage for precisely the count the payout function needs:

```sql
SELECT COUNT(*)
FROM driver_deliveries
WHERE driver_id = $1
  AND status = 'completed'
  AND completed_at >= $2
  AND completed_at < $3;
```

One question is worth asking before writing the upstream call: **“Which timestamp does the upstream date filter use?”** In our example, delivery C was accepted before the window but completed inside it. If the upstream filters by acceptance time, fetching only records accepted during these 24 hours silently misses C. The implementation below assumes the upstream can fetch by completion time.

## Step 5. Connect the pieces with an endpoint

I’d use `POST /drivers/{driver_id}/payout-calculations` because the request fetches and persists activity. It calculates a payout amount. Moving money would be a separate operation.

Here’s the FastAPI handler. `upstream` and `repo` stand for the upstream HTTP client and the repository implementing the SQL above. Their exact implementations depend on the upstream response format and database driver.

```python
from datetime import datetime, timedelta, timezone

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class PayoutRequest(BaseModel):
    start: datetime


@app.post("/drivers/{driver_id}/payout-calculations")
async def create_payout_calculation(driver_id: str, body: PayoutRequest):
    if body.start.utcoffset() is None:
        raise HTTPException(422, "start must include a timezone offset")

    start = body.start.astimezone(timezone.utc)
    end = start + timedelta(hours=24)

    # The client follows pagination and raises if any page fails.
    try:
        deliveries = await upstream.fetch_all_by_completion(driver_id, start, end)
    except UpstreamError as exc:
        raise HTTPException(502, "Could not load driver activity") from exc

    async with repo.transaction() as tx:
        await tx.upsert_deliveries(driver_id, deliveries)
        count = await tx.count_completed(driver_id, start, end)

    return {
        "driver_id": driver_id,
        "start": start,
        "end": end,
        **calculate_payout(count),
    }
```

The order matters. **Fetch every page before returning a payout.** Suppose page one contains two deliveries and page two contains the third. Returning a result after page two times out would give the driver `$10` when they earned `$25`. For a single driver and a 24-hour window, fetching the pages into memory before opening the database transaction is a reasonable interview assumption.

## Step 6. Demonstrate it to the interviewer

| Test | What you should observe |
|---|---|
| No completed deliveries | Successful response with zero base, bonus, and total |
| Two, three, then four completions | Totals of `$10`, `$25`, and `$30` |
| Completion exactly at either boundary | Start included, end excluded |
| Same delivery appears on two pages or the request is retried | One stored delivery and one base payment for that delivery |
| Another driver completes a delivery in the same period | First driver’s payout stays the same |
| Second upstream page fails | Error response, no partial payout |

If the interviewer changes the premise and says **“Actually, base pay is per active minute”**, revisit Step 1 before changing the code. A delivery active from 08:50 to 09:10 contributes ten minutes to a window starting at 09:00. Two simultaneous deliveries introduce another question: does the driver earn once per active minute or once per delivery-minute? The fetching and storage pattern still helps, but the unit you calculate has changed. Getting that unit right is the most important decision in this problem.