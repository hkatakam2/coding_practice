# Coding mock sessions for late-2026 preparation

Prepared November 18, 2026. All 15 topics correspond to the earlier question list. Sections use the same numbering.

These are original practice specifications based on public interview reports. Each session identifies the reported core. Everything labeled **Practice contract**, including numbers, schemas, examples, time limits, acceptance criteria, and follow-ups, is an authored choice unless explicitly described as reported. Public reports are candidate recollections, and some preparation sites themselves reconstruct missing details. Report dates and page-update dates do not necessarily establish interview dates. Company names identify the inspiration for an exercise.

Use any language you can test fluently. Function signatures describe the interface and may be translated into Python, Java, TypeScript, or another language. All amounts are integer cents unless specified. The examples are original. This workbook contains requirements and expected results so you can practice without reading a solution.

**Running a session**

Read the core prompt and contract, start the timer, and explain your assumptions aloud. Spend roughly the first 10% clarifying, the next 15% describing an approach, the next 55% implementing, and the final 20% testing and explaining trade-offs. Reveal follow-ups only after the core passes. If time expires, save the incomplete attempt and record the first missing requirement.

For API exercises, prepare an empty runnable HTTP application and test runner before timing. Use fixture-backed upstream adapters with the contracts below. Implement business logic and tests during the session. Session 8 reserves a separate extension for running multiple local services. Every exercise should be runnable without real accounts, credentials, external APIs, or cloud infrastructure.

Use unaided coding for your first attempt. For an optional AI-assisted replay of an API exercise, keep the same requirements, inspect the generated changes, and explain how your tests establish correctness. DoorDash's published guidance restricts AI to designated AI rounds. Permission for an actual interview comes from the instructions for that round. [Official tool guidance](https://careersatdoordash.com/blog/doordash-engineering-interview-resources/)

| Session | Exercise | Core time | Optional extension |
| --- | --- | --- | --- |
| 1 | Driver payout API | 60 minutes | 20 minutes |
| 2 | Subscription and usage billing | 60 minutes | 15 minutes |
| 3 | Asynchronous payment events | 60 minutes | 15 minutes |
| 4 | Device-event deduplication | 40 minutes | 15 minutes |
| 5 | Root-to-leaf target paths | 30 minutes | 15 minutes |
| 6 | First unique character | 15 minutes | 15 minutes |
| 7 | Merge intervals | 25 minutes | 15 minutes |
| 8 | Refund workflow | 60 minutes | 30 minutes |
| 9 | Profile aggregation API | 60 minutes | 20 minutes |
| 10 | Job scheduler with dependencies | 45 minutes | 20 minutes |
| 11 | Longest consecutive run | 25 minutes | 15 minutes |
| 12 | Keep at most two duplicates | 20 minutes | 10 minutes |
| 13 | Randomized collection | 35 minutes | 15 minutes |
| 14 | Largest histogram rectangle | 40 minutes | 15 minutes |
| 15 | Minimum starting energy | 40 minutes | 15 minutes |

The time limits are practice targets. Sessions 6 and 7 can form one 45-minute round with five minutes for introductions. Sessions 11 and 12 can form a 50-minute round. The reports associate those respective pairs with single interviews.

---

## 1. Driver payout API — DoorDash-inspired

**Reported core.** A candidate described building backend payout APIs using upstream activity data and persisted domain objects. A public practice preview also describes active delivery minutes and overlapping deliveries. Exact rates, overlap semantics, bonuses, and day boundaries below are practice choices. [Candidate report](https://www.aced.io/experiences/doordash-software-engineer-interview-ad8fea?returnPath=%2Fguides%2Fdoordash-software-engineer-interview%2Fexperiences) · [Public preview](https://www.fastprep.io/project-coding/doordash-dasher-payout-service)

**Your task.** Implement an import endpoint and a query endpoint that returns an auditable daily earnings breakdown for a driver.

**Practice contract**

Implement `POST /drivers/{driver_id}/sync?date=YYYY-MM-DD` and `GET /drivers/{driver_id}/payout?date=YYYY-MM-DD`. A sync calls `fetch_deliveries(driver_id, start, end)` and stores the returned records in memory. A payout query reads the stored records. The upstream returns every delivery overlapping the requested UTC day, including deliveries that began the previous day.

Each record has `delivery_id`, `driver_id`, `accepted_at`, `ended_at`, and `outcome`, which is `completed` or `cancelled`. Times are ISO-8601 UTC timestamps on whole-minute boundaries. Each delivery has positive duration. All records represent ended deliveries. Assume the upstream returns final immutable records.

- Base earnings are 30 cents per active delivery-minute. Two simultaneous deliveries earn 60 cents per minute.
- An extra 15 cents per active delivery-minute applies inside configured peak windows. For this mock, peak windows are disjoint and supplied as fixtures.
- A delivery completed inside the queried day earns a 100-cent completion bonus. Cancelled deliveries earn time-based pay through cancellation and receive zero completion bonus.
- Clip active time to the half-open day interval `[00:00, next 00:00)`. The completion bonus belongs to the day containing `ended_at`.
- Reimporting identical delivery IDs has no effect. A conflicting record with the same ID rejects the entire sync with `409`; validate before committing. Malformed data returns `400`, and an upstream failure returns `502` without changing stored records.
- A known driver with no synced deliveries has zero payout. Driver IDs are supplied by a fixture. An unknown driver returns `404`.

Return `driver_id`, `date`, `base_cents`, `peak_cents`, `completion_bonus_cents`, and `total_cents`.

**Example.** All times are on the same UTC day. A runs 10:00–10:30. B runs 10:10–10:40. Both complete. Peak pay runs 10:15–10:25.

```json
{
  "base_cents": 1800,
  "peak_cents": 300,
  "completion_bonus_cents": 200,
  "total_cents": 2300
}
```

There are 60 delivery-minutes and 20 peak delivery-minutes.

**Stages.** First implement `calculate_payout(deliveries, day, peak_windows)`. Then add import deduplication and HTTP handlers. Finish with tests demonstrating the response and status contracts. Up to 100,000 delivery records may be stored for a day.

**Acceptance checks.** Test repeated sync, cancellation, adjacent deliveries, an overnight delivery, completion exactly at midnight, an empty day, and a conflicting sync that leaves the previous state intact.

**Follow-ups.** Implement a second policy paying once per minute whenever at least one delivery is active. For the example, its base is 1,200 cents, peak pay is 150 cents, and bonuses remain 200 cents, totaling 1,550. Then discuss concurrent syncs and persistence across a process restart.

---

## 2. Subscription and usage billing — Stripe-inspired

**Reported core.** A Stripe candidate named a subscription-and-usage billing calculator. A public reconstruction adds fixed charges, prorated plan replacements, and a 30-day cycle, while explicitly marking some later stages as authored practice. This session uses its own schemas and examples. [Candidate report](https://www.aced.io/experiences/stripe-software-engineer-interview-14e132?returnPath=%2Fcompanies%2Fstripe) · [Reconstruction and its provenance note](https://www.fastprep.io/problems/stripe-subscription-and-usage-billing-calculator)

**Your task.** Implement `invoice(subscriptions, changes, usage, pricing) -> list[Invoice]` for one billing cycle.

**Practice contract**

The cycle is `[0,30)` in integer day offsets. Initial subscriptions begin at day 0. An initial row contains `customer_id`, `subscription_id`, and `monthly_cents`. Each subscription belongs to exactly one customer.

A change contains `subscription_id`, `effective_day`, and `new_monthly_cents`. It replaces the price from the beginning of that day through the next change or cycle end. The subscription ID stays the same. Changes may be unordered, but a subscription has at most one change per day. Valid days are 0–29. A price of zero pauses charging while retaining the subscription.

A usage row contains `event_id`, `customer_id`, `product`, and nonnegative integer `quantity`. Identical repeated event IDs count once. Conflicting payloads for an event ID reject the invoice request. Usage can exist for a customer with no subscription.

For the core, each product has a flat integer `unit_cents`. Charge each active subscription segment by `monthly_cents * active_days / 30`. Accumulate exact amounts and floor once per customer after adding usage. Return rows sorted by customer ID, retaining zero-total customers. Return each customer's total as an integer number of cents. Unknown subscriptions or missing product prices are validation errors. Input validation failure returns no invoice results.

**Core example**

```text
Subscriptions for c1:
  s1 monthly_cents=1000
  s2 monthly_cents=500
Change:
  s1 effective_day=10 new_monthly_cents=1600
Usage:
  e1 c1 requests quantity=120
Flat price:
  requests unit_cents=2
Output:
  [{customer_id: "c1", total_cents: 2140}]
```

The subscription portion is 1,900 cents. Usage contributes 240 cents.

**Stages.** Spend approximately 15 minutes on fixed subscriptions, 20 on unordered plan changes and proration, and 15 on usage and duplicate events. Use the final ten minutes for boundary tests. Handle 100,000 total input rows.

**Acceptance checks.** Test changes on days 0 and 29, several independent subscriptions, multiple changes arriving backward in time, a usage-only customer, zero prices, duplicate usage, and final rounding. For a rounding check, thirty subscriptions priced at 1 cent per cycle that all change to zero at day 1 should together charge exactly 1 cent.

**Follow-up.** Add marginal usage tiers. For `requests`, the first 100 units cost 2 cents each and every later unit costs 1 cent. Apply tiers after aggregating all usage for that customer and product. The example then totals 2,120 cents. Splitting 120 units into two events of 60 must produce the same bill. Extend the output with exact intermediate charge components to explain a disputed invoice.

---

## 3. Asynchronous payment-event processor — Stripe-inspired

**Reported core.** A candidate described four cumulative stages involving parsing, dictionaries, state, and rule application. The public account does not specify the actual event vocabulary. The payment state machine below is an original practice scenario. [Candidate report](https://www.aced.io/experiences/stripe-software-engineer-interview-047057?returnPath=%2Fexperiences)

**Your task.** Consume event strings and expose a consistent current state for each payment. Model asynchronous arrival with a deterministic sequence of method calls.

**Practice contract**

Parse each line as `event_id|payment_id|sequence|operation|amount_cents`. IDs are nonempty and contain no pipe. Sequence is a positive integer. Amount is a nonnegative integer. Supported operations are `CREATE`, `AUTHORIZE`, `CAPTURE`, `REFUND`, and `CANCEL`.

Each payment begins at sequence 1 with `CREATE`, which establishes a strictly positive payment amount and status `created`. `AUTHORIZE` requires status `created` and an amount equal to the original amount. `CAPTURE` requires `authorized` and the same amount. Both apply to the full payment. Refunds require `captured` or `partially_refunded`, have positive amounts, and cannot cumulatively exceed the captured amount. The status becomes `partially_refunded` or `refunded`. `CANCEL` has amount zero and is allowed only from `created` or `authorized`.

Implement `ingest(line) -> result` and `get(payment_id) -> snapshot`. An ingestion result has `disposition` (`processed`, `buffered`, `duplicate`, `conflict`, or `invalid_format`) and `outcomes`, a list of `{event_id, sequence, outcome}` entries with outcome `applied` or `rejected`. Empty outcomes are allowed. A rejected business transition is still a processed event. A snapshot contains status, original amount, captured amount, total refunded, last processed sequence, and pending sequence numbers. Unknown payments with no CREATE yet return status `awaiting_create` if they have buffered events, otherwise `not_found`.

**Incremental stages**

1. **Ordered input, 20 minutes.** All lines are well formed and arrive in sequence per payment. Implement parsing, transitions, and snapshots.
2. **Duplicates and errors, 15 minutes.** Repeated identical event IDs have no new effect. Reusing an event ID with different content returns `conflict`. A new event attempting an already-claimed payment/sequence also returns `conflict`. Malformed lines return `invalid_format` and reserve nothing.
3. **Out-of-order arrival, 15 minutes.** Buffer later sequences until missing earlier ones arrive, then process the available consecutive run. A well-formed event with an invalid business transition is recorded as `rejected`, changes no balance or status, and consumes its sequence so subsequent events can proceed. Return outcomes for every event processed by an ingestion, including previously buffered events.
4. **Queries and tests, 10 minutes.** Return stable snapshots and show that replaying the complete input leaves the final state unchanged.

**Example after stage 3**

```text
e3|p7|3|CAPTURE|2400
e1|p7|1|CREATE|2400
e2|p7|2|AUTHORIZE|2400
e3|p7|3|CAPTURE|2400
e4|p7|4|REFUND|600
```

The first line is buffered. The third ingestion processes authorization and then capture. The fourth line is a duplicate. The final snapshot is `partially_refunded`, with original and captured amounts 2,400, refunded amount 600, last sequence 4, and no pending events.

**Acceptance checks.** Test over-refund rejection, refund before capture, duplicate capture, two payments interleaved, a missing CREATE, conflicting sequence ownership, and a malformed amount. Up to 100,000 events may arrive. Every well-formed event's first accepted claim of ID and sequence remains reserved even if its business transition is later rejected.

**Follow-ups.** Impose a per-payment buffer limit and define the response when it is exceeded. Discuss atomically storing the processed event and its state change across a crash. Identify which assumptions must change for two consumers to process the same payment concurrently.

---

## 4. Deduplicate device events — Google-inspired

**Reported core.** The September 3 Google SWE III account describes suppressing repeated timestamped device events within ten seconds, followed by complexity and production questions. It leaves the suppression-clock semantics unspecified. [Firsthand report](https://leetcode.com/discuss/post/8500374/usa-google-swe-iii-1st-round-technical-b-jbji/)

**Your task.** Implement a streaming filter with `should_emit(device_id, message, timestamp_seconds) -> bool`.

**Practice contract**

Timestamps are nonnegative integers and arrive in globally nondecreasing order. An event's identity is the exact pair `(device_id, message)`. Emit the first occurrence. Emit a subsequent occurrence when at least ten seconds have elapsed since the last **emitted** event with that identity. A suppressed event does not reset the clock. Events exactly ten seconds apart may both be emitted. Preserve input order in a `filter(events)` wrapper.

```text
Input                                  Emit?
("d1", "low_battery", 0)               true
("d1", "low_battery", 8)               false
("d2", "low_battery", 9)               true
("d1", "low_battery", 10)              true
("d1", "low_battery", 16)              false
("d1", "overheating", 17)              true
("d1", "low_battery", 20)              true
```

**Acceptance checks.** Handle empty input, repeated equal timestamps, different devices with identical messages, and the exact boundary. Process up to one million events. Describe runtime in terms of both events and message length. First produce a correct implementation, then address memory growth when identities never repeat.

**Follow-up 1.** Change the rule to require ten seconds since the last **received** event. For one identity at times 0, 8, 16, 26, emitted times become 0 and 26. Under the original rule they are 0, 16, and 26.

**Follow-up 2.** Add `advance_time(t)` and remove suppression state that cannot influence future results under the ordered-input contract. Explain how stale cleanup entries interact with an identity that was emitted again.

**Discussion.** What changes if timestamps arrive out of order? Ask whether output may be delayed and how late events can be. What state must be shared if several servers receive the same device's events?

---

## 5. Find target-sum tree paths — Amazon-inspired

**Reported core.** An AWS new-grad candidate reported Path Sum II and an unspecified harder follow-up during an August 2026 loop. The follow-up here is authored practice. [Interview report](https://leetcode.com/discuss/post/8520348/) · [Canonical task](https://leetcode.com/problems/path-sum-ii/)

**Your task.** Implement `find_paths(root, target) -> list[list[int]]`. Return the node values along every root-to-leaf path whose sum equals `target`.

**Practice contract**

Each node has `value`, `left`, and `right`. A leaf has no children. Node values may be negative or zero. Distinct node paths must both appear even when their value sequences are identical. Return paths in left-subtree-before-right-subtree order. An empty tree returns `[]`. Preserve the tree.

For this example, the tree is specified by edges to avoid ambiguity in array encodings.

```text
Root r has value 4.
r.left is a with value 2; r.right is b with value -1.
a.left is c with value 3; a.right is d with value -2.
b.right is e with value 6.
c, d, and e are leaves.

target = 9
output = [[4, 2, 3], [4, -1, 6]]
```

**Constraints.** Up to 10,000 nodes, values between -10,000 and 10,000, and at most one million values across the returned paths. Discuss depth and output size explicitly.

**Acceptance checks.** Include a matching single node, a nonmatching single node, a chain, two equal-valued valid paths, and a root whose value equals the target but has children. Verify that appending a later result does not mutate an earlier returned path.

**Follow-up.** Count every downward path with the target sum when paths may start and stop at any nodes. Each step must follow a parent-to-child edge. For a chain with values `[2, -1, 2]` and target 1, the answer is 2. Return a count, and explain how the changed requirements affect your approach.

---

## 6. First unique character — Amazon-inspired

**Reported core.** The AWS new-grad report names a first-non-repeating-character task. [Interview report](https://leetcode.com/discuss/post/8520348/) · [Canonical practice task](https://leetcode.com/problems/first-unique-character-in-a-string/)

**Your task.** Implement `first_unique_index(text) -> int`. Return the smallest index whose character occurs exactly once in the entire string, or `-1` if none exists.

**Practice contract**

Input is an ASCII string of up to one million characters. Matching is case-sensitive. Spaces and punctuation are characters. Indices are zero-based. Preserve the input.

```text
"swiss" -> 1
"aabbcdd" -> 4
"aabb" -> -1
"" -> -1
"AaA" -> 1
```

**Acceptance checks.** Test uniqueness at the first and last positions, all unique characters, all equal characters, punctuation, and empty input. Explain why the returned index is the earliest unique one.

**Follow-up.** Implement `add(character) -> character_or_null` for a stream. After every insertion, return the first currently unique character in arrival order. For `a, b, a, c, b`, return `a, a, b, b, c`. Handle one million calls without rescanning the full stream on each insertion.

**Discussion.** If input becomes Unicode, agree on whether a character means a code point or a displayed grapheme and what an index measures before revising the implementation.

---

## 7. Merge intervals — Amazon-inspired

**Reported core.** The same AWS report describes a slight Merge Intervals modification without specifying it. The base contract and optional modifications here are original practice choices. [Interview report](https://leetcode.com/discuss/post/8520348/) · [Canonical practice task](https://leetcode.com/problems/merge-intervals/)

**Your task.** Implement `merge_intervals(intervals) -> list[Interval]`. Produce a sorted list covering the same points, with every overlap merged.

**Practice contract**

Each interval is a closed integer range `[start,end]` with `start <= end`. Input order is arbitrary. Ranges sharing an endpoint overlap. Zero-length intervals are allowed. Preserve the input. There may be up to 100,000 intervals with endpoints between -1 billion and 1 billion.

```text
[[8,11], [1,4], [3,6], [6,8], [15,15]]
-> [[1,11], [15,15]]

[[2,3], [3,7]] -> [[2,7]]
[] -> []
```

**Acceptance checks.** Include nesting, duplicate intervals, equal starts, isolated points, negative endpoints, reversed input order, and ranges separated by a one-unit gap. Under this contract `[1,2]` and `[3,4]` remain separate.

**Follow-up 1.** Accept tagged intervals `{start,end,owner}`. Return the merged coverage and the sorted set of owners contributing anywhere to each merged interval. For `{1,4,A}`, `{3,5,B}`, `{8,9,A}`, return `{1,5,[A,B]}` and `{8,9,[A]}`.

**Follow-up 2.** Switch to half-open reservations `[start,end)`, require positive duration, and keep adjacent reservations separate. State exactly which boundary tests now change. Optional further work is a data structure supporting insertion into an already merged collection.

---

## 8. Refund workflow across services — DoorDash-inspired

**Reported core.** A public report compilation describes a refund DAG implemented with local HTTP services. Its preview mentions partial refunds, notifications, repeated calls, and slow execution. The graph and business rules below are authored. [Report compilation](https://www.fastprep.io/experience/2025-2026-ai-coding-phone-screens-and-onsites-at-43-companies-76-reported-proble-1nykp3bzad) · [Task preview](https://www.fastprep.io/project-coding/doordash-refund-dag-local-services)

**Your task.** Implement `POST /refunds` and `GET /refunds/{refund_id}` to run and inspect a refund workflow.

**Practice contract**

A request contains `refund_id`, `order_id`, and positive `amount_cents`. Order fixtures contain `paid_cents`, `refunded_cents`, and an eligibility flag. A request must not exceed the unrefunded amount. The workflow has five named steps and explicit prerequisite lists.

```text
eligibility: []
payment: [eligibility]
inventory: [payment]
notification: [payment]
finalize: [inventory, notification]
```

Use an in-process adapter for each step in the core. `eligibility` reads the order, `payment` records a refund, `inventory` records a reconciliation request, and `notification` records a message. `finalize` marks the workflow complete. The inventory step's meaning is a request for later reconciliation, so it performs no item-count arithmetic.

- Execute a step only after all prerequisites succeed. Sequential execution is acceptable in the core.
- Store each step as `pending`, `running`, `succeeded`, or `failed`, with its output and attempt count. On a failure, stop the run. Completed steps stay complete.
- A second identical POST resumes failed or pending work. It returns the existing result immediately if already complete. Reusing `refund_id` with a changed payload returns `409`.
- Every side-effecting adapter accepts an idempotency key derived from refund ID and step name. A repeated key and payload returns the previous result with no new effect.
- Ineligible or excessive refunds return `422` before financial effects. For this exercise, a rejected business request is recorded as terminal `rejected` for that ID.
- Other failures return `503` with workflow ID and step statuses. Successful completion returns `200`. Unknown GET IDs return `404`.
- Core requests are processed serially, and a retry of one workflow completes before another refund is attempted. Concurrent refunds are a follow-up.

**Example.** Order o1 was paid 5,000 cents and has no refunds. Request r1 refunds 1,200 cents. Make notification fail on its first call. Payment and inventory succeed, notification fails, and finalize remains pending. Retrying r1 completes notification and finalize. The order has exactly 1,200 refunded cents and exactly one successful notification.

**Acceptance checks.** Demonstrate the example, an identical completed retry, an amount conflict, an excessive refund, and an unknown order (`404`). Validate the workflow definition for missing dependencies and cycles before invoking any adapter.

**HTTP extension, 30 minutes.** Put payment, inventory, and notification behind three separate local servers. Use a fixed list of local URLs and seed each with fixture state. Preserve their idempotency contracts. Introduce a payment response timeout after the refund is committed and prove that retrying does not double-refund. Use test doubles or a controlled delay to reproduce the case.

**Discussion follow-ups.** Move slow workflows behind `202 Accepted` and polling. Explain how two concurrent partial refunds avoid exceeding the amount paid, and which state must persist across service restarts.

---

## 9. Aggregate a customer profile — DoorDash-inspired

**Reported core.** A public preview describes an application bootstrap endpoint combining consumer, payment, and address data while tolerating failures. Reported follow-ups include timeouts and retries. The response policy below is authored. [Public preview](https://www.fastprep.io/project-coding/doordash-service-profile-aggregator) · [Report compilation](https://www.fastprep.io/experience/2025-2026-ai-coding-phone-screens-and-onsites-at-43-companies-76-reported-proble-1nykp3bzad)

**Your task.** Implement `GET /customers/{id}/bootstrap` using three independent upstream adapters.

**Practice contract**

```text
get_consumer(id) -> {id, name, email}
get_payment_methods(id) -> [{id, brand, last4}]
get_addresses(id) -> [{id, line1, city, postal_code}]
```

Adapters may succeed, time out, return a non-200 status, or produce malformed content. Tests can configure a response and latency per call. A successful consumer object must match the requested ID. All fields shown are required with string values, and list elements must match their schema. A malformed payload is an upstream failure.

Start the three independent reads concurrently. Each gets a 200 ms timeout and no automatic retry in the core. The consumer response is required. Its `404` maps to endpoint `404`, timeout maps to `504`, and other failures map to `502`. Optional-service failures produce `null` for that field and a warning, while the endpoint returns `200`. Empty successful lists remain `[]`.

Return a stable object with `consumer`, `payment_methods`, `addresses`, and `warnings`. Warnings are sorted strings such as `addresses_timeout`, `addresses_unavailable`, `payments_timeout`, or `payments_unavailable`. Do not expose unused upstream fields.

**Example.** Consumer succeeds after 40 ms, payment methods after 70 ms, and addresses would respond after 600 ms. Return about 200 ms after the request, allowing scheduling overhead.

```json
{
  "consumer": {"id":"c1", "name":"Ravi", "email":"ravi@example.test"},
  "payment_methods": [{"id":"pm1", "brand":"visa", "last4":"4242"}],
  "addresses": null,
  "warnings": ["addresses_timeout"]
}
```

**Stages.** Implement successful aggregation, add timeouts and schema checks, then test partial responses and response timing. Make the HTTP client and clock/scheduler replaceable for tests where your stack supports it. The scope is one aggregator instance with in-memory fixtures.

**Acceptance checks.** Test both optional services failing, consumer `404`, required-service timeout, malformed payment data, valid empty lists, and independent read execution. Pending optional reads should not keep a completed failure response blocked after the required service has failed.

**Follow-up.** Allow one retry for timeouts and `503` responses. Impose a 350 ms overall deadline and a 20 ms delay before retry. Keep each attempt at most 200 ms and cap it to the remaining deadline. Discuss a circuit breaker and whether a stale cached address is acceptable. Make the choice of stale-data behavior explicit before coding it.

---

## 10. Schedule jobs with dependencies — Bloomberg-inspired

**Reported core.** A candidate described implementing a scheduler for jobs with one or multiple dependencies. The public account is brief. Execution semantics below are authored practice. [Candidate report](https://www.aced.io/experiences/bloomberg-senior-software-engineer-interview-32a47e?returnPath=%2Fexperiences)

**Your task.** Implement `execution_batches(jobs) -> list[list[str]]`. Every job has an ID and a list of jobs that must finish before it can start.

**Practice contract**

All jobs take one time unit and succeed. Workers are unlimited in the core. At each time boundary, every ready job starts together. Return the batch of job IDs started at each boundary, sorted lexicographically inside each batch. Input order carries no meaning.

IDs must be unique. A prerequisite must refer to an existing job. Repeated prerequisite IDs within one job count once. Reject cycles, including self-dependencies, with a structured `invalid_graph` result. For invalid input, return no partial schedule. An empty job list returns `[]`.

| Job | Prerequisites |
| --- | --- |
| A | [] |
| B | [A] |
| C | [A] |
| D | [B,C] |
| E | [] |

Expected batches are `[["A","E"], ["B","C"], ["D"]]`.

**Constraints.** Up to 100,000 jobs and 300,000 distinct prerequisite edges. Explain validation, runtime, memory use, and the cost of sorting each batch.

**Acceptance checks.** Include disconnected components, a long chain, several prerequisites for one job, a duplicate prerequisite, an unknown prerequisite, and a cycle in a component unrelated to otherwise runnable jobs. The last case must still reject the entire input.

**Follow-up 1.** Add a worker limit `k >= 1`. At each boundary, start up to `k` ready jobs in lexicographic order. All started jobs finish one unit later. Return batches under this policy. With `k=1`, the example becomes `[["A"],["B"],["C"],["D"],["E"]]`. This policy specifies deterministic scheduling and makes no claim about minimizing overall duration for arbitrary workloads.

**Follow-up 2.** Use callbacks that can fail. A failed job is never retried in this extension. Mark its downstream dependents `blocked`, allow independent jobs to finish, and return every final status. Explain how readiness changes if durations vary and workers finish at different times.

---

## 11. Longest consecutive run — Amazon-inspired

**Reported core.** A September 16 SDE II account links Longest Consecutive Sequence. [Interview report](https://leetcode.com/discuss/post/8523912/amazon-sde-2-interview-experience-by-ano-2sxp/) · [Canonical practice task](https://leetcode.com/problems/longest-consecutive-sequence/)

**Your task.** Implement `longest_consecutive(nums) -> int`. Return the length of the largest set of consecutive integer values present in the input.

**Practice contract**

Input is unsorted and may contain duplicates. Original positions do not matter. Repeating a number does not lengthen a run. Negative values and zero are allowed. Preserve the input. Empty input returns 0. Aim for expected `O(n)` time.

```text
[9, 1, 4, 7, 3, 2, 2, 8] -> 4
[-3, -1, -2, 5] -> 3
[8, 8, 8] -> 1
[] -> 0
```

The first example contains runs 1–4 and 7–9.

**Constraints.** Up to 200,000 elements, each between -1 billion and 1 billion.

**Acceptance checks.** Test reverse-sorted input, a run spanning negative values and zero, many copies of one value, multiple equal-length runs, and one giant run. Explain how often each distinct integer is visited in your algorithm.

**Follow-up 1.** Return `{length,start,end}` for the best run. Break equal-length ties by smaller start. For `[6,7,1,2]`, return `{length:2,start:1,end:2}`. Empty input returns `{length:0,start:null,end:null}`.

**Follow-up 2.** Support an insert-only stream with `add(value) -> longest_length_so_far`. Duplicate insertions have no effect. Aim for expected constant time per insertion. Explain which extra information must be maintained before implementing.

---

## 12. Keep at most two duplicates — Amazon-inspired

**Reported core.** The same September 16 account links Remove Duplicates from Sorted Array II. [Interview report](https://leetcode.com/discuss/post/8523912/amazon-sde-2-interview-experience-by-ano-2sxp/) · [Canonical practice task](https://leetcode.com/problems/remove-duplicates-from-sorted-array-ii/)

**Your task.** Implement `compact(nums) -> k`. Modify the sorted array so that its first `k` positions contain each distinct value at most twice, preserving order.

**Practice contract**

Use `O(1)` auxiliary space. The contents at positions `k` onward are unspecified and ignored. Return only the logical length. Input is guaranteed nondecreasing, may include negative values, and has up to one million elements.

```text
Input:  [-2,-2,-2,0,0,0,0,3]
Return: 5
Prefix: [-2,-2,0,0,3]

Input: [5,5,5,5]
Return: 2
Prefix: [5,5]

Input: []
Return: 0
```

**Acceptance checks.** Handle arrays of length 0, 1, and 2, all unique values, runs of exactly two copies, and long runs at the beginning and end. Tests should compare only the returned prefix. Explain why a write cannot destroy an unread value.

**Follow-up.** Implement `compact(nums, max_occurrences)` for any nonnegative integer limit. A limit of zero returns 0. For `[1,1,1,2,2,3]` and limit 1, the result is length 3 with prefix `[1,2,3]`. Keep constant auxiliary space.

**Discussion.** If the sorted-input guarantee disappears, clarify whether preserving original order still matters and what additional memory is acceptable.

---

## 13. Collection with random selection — Amazon-inspired

**Reported core.** The SDE II account links Insert Delete GetRandom O(1) in the bar-raiser round. [Interview report](https://leetcode.com/discuss/post/8523912/amazon-sde-2-interview-experience-by-ano-2sxp/) · [Canonical practice task](https://leetcode.com/problems/insert-delete-getrandom-o1/)

**Your task.** Implement a collection of unique integers with these methods.

```text
insert(value) -> true if newly inserted, otherwise false
remove(value) -> true if present and removed, otherwise false
get_random() -> one currently stored value
size() -> number of values
```

**Practice contract**

Insertion and removal should take average `O(1)` time. Random selection should take `O(1)` time and give every stored value equal probability. `get_random()` on an empty collection raises a documented `EmptyCollection` error. Up to one million method calls may occur, with signed 32-bit values.

Accept an injectable random-number source capable of selecting a uniform integer in a supplied range. Tests may replace it with a deterministic source. You may use standard collections and a standard random generator.

```text
insert(12) -> true
insert(4)  -> true
insert(12) -> false
remove(12) -> true
get_random() -> 4
remove(99) -> false
remove(4) -> true
size() -> 0
```

**Acceptance checks.** Test removing the only value, removing a middle value from a larger collection, deleting and reinserting, selecting after many deletions, and empty behavior. Check internal consistency after each mutation if you expose a test-only invariant checker. Explain why your sampling gives equal probability. A frequency experiment alone does not establish correctness.

**Follow-up.** Allow duplicates. `insert` always adds an occurrence and returns whether the value was previously absent. `remove` deletes one occurrence. Random selection is uniform over occurrences. With `[4,4,9]`, the chance of 4 is two-thirds. Define how your invariants change, then implement the extension.

---

## 14. Largest rectangle in a histogram — Amazon-inspired

**Reported core.** A September 15 SDE II report describes finding the largest area across consecutive histogram bars. [Interview report](https://leetcode.com/discuss/post/8522985/) · [Canonical practice task](https://leetcode.com/problems/largest-rectangle-in-histogram/)

**Your task.** Implement `largest_rectangle(heights) -> int`. Bars have width 1. Find the maximum area of a rectangle that fits beneath consecutive bars.

**Practice contract**

Heights are nonnegative integers. Empty input returns 0. A rectangle's height cannot exceed any covered bar. Preserve the input. Aim for `O(n)` time after explaining a correct simpler approach.

```text
[3,1,3,3] -> 6
[4,4,4] -> 12
[0,5,0] -> 5
[1,2,3,4] -> 6
[] -> 0
```

In the first example, the last two bars form a width-2 rectangle of height 3.

**Constraints.** Up to 200,000 bars, each up to 1 billion high. The result can exceed signed 32-bit range. Use a representation that preserves the possible integer area exactly.

**Acceptance checks.** Test increasing heights, decreasing heights, repeated equal heights, zero separators, a single bar, and all zeros. Explain how you ensure rectangles reaching the last bar are considered.

**Follow-up 1.** Return `{area,left,right,height}`, with inclusive zero-based boundaries. Break ties by smaller `left`, then smaller `right`. Return `{area:0,left:null,right:null,height:0}` when the best area is zero. For `[3,1,3,3]`, return `{area:6,left:2,right:3,height:3}`.

**Follow-up 2.** Each bar now has a positive integer width supplied in a parallel array. A rectangle still spans entire consecutive bars. For heights `[3,1,3]` and widths `[2,4,2]`, the maximum area is 8. Explain which width calculation changes.

---

## 15. Minimum starting energy — Amazon-inspired

**Reported core.** The September 15 SDE II report describes a grid whose positive and negative values change energy, with a minimum starting-energy objective. This mock specifies movement and boundaries explicitly. [Interview report](https://leetcode.com/discuss/post/8522985/) · [Related canonical task](https://leetcode.com/problems/dungeon-game/)

**Your task.** Implement `minimum_starting_energy(grid) -> int`. Start at the top-left cell and reach the bottom-right cell with strictly positive energy throughout.

**Practice contract**

Choose a positive integer starting energy. Immediately apply the starting cell's value. Each move goes one cell right or down and applies that cell's value. Energy must be at least 1 after every cell, including the start and finish. The grid is a nonempty rectangle. There are no obstacles in the core. Preserve the input.

```text
grid = [
  [-2, -3,  3],
  [-5,-10,  1]
]
answer = 6
```

With starting energy 6, the path right, right, down has energies `4,1,4,5`. Starting with 5 cannot survive any complete path.

```text
[[0]] -> 1
[[7]] -> 1
[[-7]] -> 8
[[2,-5,4]] -> 4
```

**Constraints.** Up to 500 rows and 500 columns, with cell values between -10,000 and 10,000. Target `O(rows * columns)` time.

**Acceptance checks.** Include one row, one column, all positive cells, all negative cells, a large gain available only after an early loss, and a negative destination. Explain why choosing a path only by its final sum can give the wrong answer.

**Follow-up 1.** Return one path that works at the minimum starting energy. When both next moves preserve that minimum requirement, prefer right. For the example, return coordinates `[(0,0),(0,1),(0,2),(1,2)]`.

**Follow-up 2.** Reduce auxiliary memory when only the minimum energy is requested. Then introduce blocked cells represented by `null`, returning `null` if the destination is unreachable. Clarify how the blocked start and blocked finish behave.

---

## Review sheet for each completed session

This rubric is an authored self-assessment tool. Score each dimension from 0 to 2, with 0 meaning absent, 1 meaning partial, and 2 meaning demonstrated.

| Dimension | Evidence for 2 points |
| --- | --- |
| Requirements | You stated boundary semantics and the input/output contract before coding. |
| Core correctness | The implementation passes the examples and the core acceptance cases. |
| State and errors | Invalid input, duplicate operations, or mutation boundaries behave as specified. For pure functions, input/output invariants hold. |
| Complexity and structure | You explained runtime and memory accurately and kept the code understandable. |
| Verification and communication | You tested important edge cases and explained the working implementation and its limitations. |

Record the score, time to first working result, missed requirements, and one concrete change for your next attempt. Keep optional follow-ups separate from the core score. A score here does not predict a company's hiring decision.

## Source notes and evidence limits

- **Sessions 1, 8, and 9.** Public candidate reports and commercial preparation previews support the task themes. The detailed service contracts in this workbook are authored. The report compilation includes sightings through October 2026. A public preview's suggested duration is its practice format and should not be treated as a confirmed interview duration. [Compilation](https://www.fastprep.io/experience/2025-2026-ai-coding-phone-screens-and-onsites-at-43-companies-76-reported-proble-1nykp3bzad)
- **Sessions 2 and 3.** Aced candidate accounts support the named billing exercise and a four-stage event processor. Their displayed relative dates vary with the page snapshot. The linked billing reconstruction explicitly labels some schemas and later stages as its own practice additions. This workbook adds its own fully specified variants. [Billing report](https://www.aced.io/experiences/stripe-software-engineer-interview-14e132?returnPath=%2Fcompanies%2Fstripe) · [Event report](https://www.aced.io/experiences/stripe-software-engineer-interview-047057?returnPath=%2Fexperiences)
- **Session 4.** The Google account is dated September 3, 2026, with a later edit. Its ten-second deduplication theme is explicit. Device identity, exact boundary behavior, and which event resets the clock are specified for this mock. [Google account](https://leetcode.com/discuss/post/8500374/usa-google-swe-iii-1st-round-technical-b-jbji/)
- **Sessions 5–7.** The Amazon account was posted September 14, 2026, and gives interview dates of August 20 and 24. It names Path Sum II, first non-repeating character, and a Merge Intervals variation. The exact harder path-sum and interval variations were not published. [Amazon new-grad account](https://leetcode.com/discuss/post/8520348/)
- **Session 10.** The Bloomberg account supports a scheduler with dependencies. Exact constraints, worker count, deterministic ordering, and failure handling are authored. [Bloomberg account](https://www.aced.io/experiences/bloomberg-senior-software-engineer-interview-32a47e?returnPath=%2Fexperiences)
- **Sessions 11–13.** The September 16 SDE II account directly links the three canonical problem titles. [Amazon SDE II account](https://leetcode.com/discuss/post/8523912/amazon-sde-2-interview-experience-by-ano-2sxp/)
- **Sessions 14–15.** The September 15 SDE II account describes the histogram and minimum-energy tasks. Its compensation link points to a Hyderabad role, so these should not be labeled verified U.S. reports. The problem types remain usable for general coding practice. [Amazon SDE II account](https://leetcode.com/discuss/post/8522985/)
- **Interview format.** DoorDash's official preparation guidance emphasizes explaining assumptions, implementation quality, complexity, and testing. Its official tools page allows AI only when a round explicitly permits it. These support the practice format without establishing one universal late-2026 format. [Preparation guidance](https://careersatdoordash.com/blog/technical-interview-preparation/) · [Tools guidance](https://careersatdoordash.com/blog/doordash-engineering-interview-resources/)
