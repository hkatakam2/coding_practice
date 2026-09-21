I would interpret the prompt as: **design an internal notification platform used by roughly 10–15 applications, initially supporting email and SMS, with delivery tracking/reporting and an architecture that can later add channels such as push or WhatsApp.**

The key is not to start with Kafka, Redis, microservices, etc. The design should come from the requirements, as your system-design framework specifies. 

# 1. Clarify and Scope

I would ask only questions that materially affect the architecture:

* Are these primarily **transactional notifications** such as OTPs, order updates, password resets, and billing alerts, or large marketing campaigns?

  * **Assumption:** transactional notifications. Bulk campaigns are out of scope.
* Can applications request both email and SMS for the same event?

  * **Assumption:** yes.
* Do applications provide raw message content or reference centrally managed templates?

  * **Assumption:** templates are centrally stored and applications supply variables.
* Do we need to know whether the notification was merely accepted by the provider or actually delivered?

  * **Assumption:** track delivery as far as the external provider supports.

## Functional requirements

### FR1 — Submit a notification

Any of our 10–15 applications should be able to request a notification.

For example:

```text
Billing Service
    → send "payment_failed"
    → user@example.com
    → EMAIL
```

The caller should receive a `notification_id` immediately.

### FR2 — Deliver through email or SMS

The system should:

```text
notification request
       ↓
load template
       ↓
render message
       ↓
select channel
       ↓
Email provider / SMS provider
```

The architecture should make adding another channel later relatively isolated.

### FR3 — Track and report delivery

Applications and operations teams should be able to determine:

```text
ACCEPTED
PROCESSING
SENT
DELIVERED
FAILED
```

and retrieve aggregate statistics such as:

```text
Email:
sent       100,000
delivered   98,700
failed       1,300
```

### Out of scope

For this interview I would explicitly defer:

```text
marketing campaign management
complex user notification preferences
A/B testing
notification scheduling
cross-channel fallback policies
UI for editing templates
```

---

# 2. Important Non-Functional Requirements

These are notification-specific rather than generic "scalable/reliable" requirements.

### NFR1 — Accepted notifications should not be lost

Once we respond:

```text
202 Accepted
```

we should have durably recorded the request.

We'll target something like:

```text
99.99%+ accepted notifications are eventually processed
```

Transient provider failures should cause retries rather than message loss.

---

### NFR2 — Fast submission, asynchronous delivery

The producer shouldn't wait for Twilio/SES/etc.

Target:

```text
POST /notifications
P95 < 200 ms
```

Under normal conditions, a message should reach the external provider within roughly:

```text
< 1 second
```

---

### NFR3 — Absorb bursts from multiple applications

With 10–15 producer applications, traffic could be bursty.

For interview purposes I would assume:

```text
hundreds of notifications/sec normally
low thousands/sec during bursts
```

We shouldn't allow a temporary SMS-provider slowdown to bring down the producer applications.

---

### NFR4 — Adding a new channel should require minimal core-system change

If we later introduce:

```text
PUSH
WHATSAPP
SLACK
```

we should primarily add a new channel implementation rather than rewrite the notification workflow.

This NFR has a direct architectural consequence: we'll separate **notification orchestration** from **channel-specific delivery logic**.

---

# 3. Core Entities

Keeping this intentionally lightweight at first:

```text
Application
    Represents one of the 10–15 producer applications.

Notification
    Represents a request to notify a recipient.

Template
    Represents reusable notification content.

DeliveryAttempt
    Represents an attempt to deliver through a channel.
```

I would not define all columns yet. Your framework explicitly recommends introducing fields only when the functional flow requires them. 

---

# 4. APIs

## Submit notification

```http
POST /v1/notifications
Idempotency-Key: payment-8472-failed
```

```json
{
  "recipient": {
    "email": "user@example.com",
    "phone": "+13155551234"
  },
  "channels": ["EMAIL"],
  "template_id": "payment_failed",
  "variables": {
    "amount": "24.99",
    "invoice_id": "inv_8472"
  }
}
```

Response:

```json
{
  "notification_id": "notif_123",
  "status": "ACCEPTED"
}
```

The important API choice here is the `Idempotency-Key`.

If Billing Service retries the API because of a timeout, we don't want:

```text
Payment failed
Payment failed
Payment failed
```

sent three times.

---

## Notification status

```http
GET /v1/notifications/{notification_id}
```

Response:

```json
{
  "notification_id": "notif_123",
  "channels": {
    "EMAIL": "DELIVERED"
  }
}
```

---

## Reporting

```http
GET /v1/reports/notifications
    ?from=...
    &to=...
    &application_id=billing
    &channel=EMAIL
```

Response:

```json
{
  "sent": 100000,
  "delivered": 98700,
  "failed": 1300
}
```

---

# 5. High-Level Design — Functional Requirements First

I'll deliberately begin with a simple system.

## FR1 — Applications submit notifications

Start with:

```text
                    ┌─────────────────┐
App 1 ─────────────→│                 │
App 2 ─────────────→│ Notification    │
...                 │ Service         │
App 15 ────────────→│                 │
                    └────────┬────────┘
                             │
                             ▼
                       PostgreSQL
```

When a request arrives, Notification Service validates it and creates the notification.

Now we need some actual schema.

### `notifications`

```text
notification_id
application_id
idempotency_key
template_id
recipient
variables JSONB
status
created_at
updated_at
```

And:

```text
UNIQUE(application_id, idempotency_key)
```

That handles application retries.

At this point the application can submit a request and obtain:

```text
notification_id = notif_123
status = ACCEPTED
```

---

# 6. FR2 — Actually Send Email/SMS

Now extend the existing architecture rather than replacing it.

```text
Apps
 │
 ▼
Notification Service
 │
 ├────────────→ PostgreSQL
 │
 ▼
Template Renderer
 │
 ▼
Channel Dispatcher
 ├────────────→ Email Sender → Email Provider
 │
 └────────────→ SMS Sender   → SMS Provider
```

For example:

```text
Billing Service
    ↓
Notification Service
    ↓
template_id = payment_failed
    ↓
Template Renderer
    ↓
"Your payment of $24.99 failed."
    ↓
Email Sender
    ↓
SES / SendGrid
```

Now we introduce the template data.

### `templates`

```text
template_id
channel
subject
body
version
```

For example:

```text
payment_failed | EMAIL
subject:
    Payment failed

body:
    Your payment of {{amount}} for invoice
    {{invoice_id}} could not be processed.
```

For SMS:

```text
payment_failed | SMS
body:
    Your ${{amount}} payment failed.
```

---

## Channel abstraction

I don't want Notification Service to contain:

```java
if (channel == EMAIL) {
   ...
} else if (channel == SMS) {
   ...
}
```

throughout the codebase.

Instead:

```java
interface NotificationChannel {
    SendResult send(RenderedNotification message);
}
```

Implementations:

```text
EmailChannel
SMSChannel
```

Conceptually:

```text
                    NotificationChannel
                           ▲
                    ┌──────┴───────┐
                    │              │
              EmailChannel     SMSChannel
                    │              │
                    ▼              ▼
             Email Provider    SMS Provider
```

That becomes important when we revisit our extensibility NFR.

For now this is still synchronous:

```text
API request
  → DB
  → provider
  → update DB
  → response
```

It works functionally.

But it has an obvious problem:

> If the SMS provider takes five seconds or goes offline, our API request is now blocked.

I'm deliberately leaving that for the NFR deep dive.

---

# 7. FR3 — Status and Reporting

There are actually two different statuses.

When SES/Twilio initially accepts a request:

```text
SENT
```

doesn't necessarily mean:

```text
DELIVERED
```

External providers generally give us asynchronous status callbacks.

So we extend the design:

```text
                           Email Provider
                          /      │
Apps → Notification Service      │ webhook
                          \      ▼
                           SMS Provider
                                │
                                ▼
                      Notification Service
                                │
                                ▼
                            PostgreSQL
```

For each delivery we now need:

### `notification_deliveries`

```text
delivery_id
notification_id
channel
status
provider_message_id
created_at
updated_at
```

And attempts:

### `delivery_attempts`

```text
attempt_id
delivery_id
attempt_number
provider
status
error_code
started_at
completed_at
```

Status might evolve:

```text
ACCEPTED
   ↓
PROCESSING
   ↓
SENT
   ↓
DELIVERED
```

or:

```text
PROCESSING
   ↓
FAILED
```

---

## Reporting Service

Initially I would keep this very simple:

```text
Apps
 │
 ▼
Notification Service ──────→ PostgreSQL
                                  ▲
                                  │
                           Reporting Service
                                  ▲
                                  │
                             Operations UI
```

Reporting Service can answer:

```text
messages by application
messages by channel
delivery rate
failure rate
provider errors
```

At our initial scale, Postgres can satisfy this functionality.

Again, I'll postpone expensive analytics concerns until the NFR stage.

This is exactly the functional-first progression described in the supplied framework: satisfy each requirement, evolve the same architecture, and defer scale limitations until afterward. 

---

# 8. Now Revisit the NFRs

Our simple design works.

But:

```text
App
 ↓
Notification Service
 ↓
Provider
```

doesn't meet our reliability or latency requirements.

This is where the architecture should become more sophisticated. The reasoning pattern is **requirement → problem → alternatives → choice → architecture change**. 

---

# 9. Deep Dive — Reliable Asynchronous Delivery

## Requirement

Once we say:

```text
ACCEPTED
```

we should not lose the notification.

And producers should not wait for the external provider.

## Problem with current design

Imagine:

```text
Billing Service
      ↓
Notification Service
      ↓
Postgres ✓
      ↓
Twilio
      X
```

If Twilio is down, what happens?

Even worse:

```text
Postgres write ✓
Queue publish X
```

could leave a notification permanently sitting in Postgres.

---

## Possible approaches

### Direct provider call

```text
Service → Twilio
```

Simple, but provider availability directly affects us.

Not acceptable.

### Store then background poll

```text
Service → PostgreSQL

Background worker:
Postgres → provider
```

Reliable enough for a small system, but we're turning the database into a work queue.

### Durable queue

```text
Service → Queue → Workers → Providers
```

Better decoupling and burst handling.

But now we have a dual-write problem:

```text
write DB
publish Queue
```

What if only one succeeds?

---

# 10. Transactional Outbox

I would choose:

```text
Notification Service
       │
       │ one transaction
       ▼
┌────────────────────┐
│ PostgreSQL         │
│                    │
│ notifications      │
│ outbox_events      │
└────────────────────┘
        │
        ▼
  Outbox Publisher
        │
        ▼
   Durable Queue
```

Within one DB transaction:

```text
BEGIN

INSERT notification

INSERT outbox_event

COMMIT
```

So we either record:

```text
notification + delivery event
```

or neither.

Then the outbox publisher eventually produces:

```json
{
  "notification_id": "notif_123",
  "channel": "EMAIL"
}
```

to the queue.

---

# 11. Why a Managed Queue Here?

For this system, I don't actually need Kafka's ordering/replay semantics.

The key things I need are:

```text
durable messages
consumer scaling
visibility timeout / retries
dead-letter queue
```

So something like:

```text
AWS SQS
```

would be simpler operationally.

If this organization already runs Kafka heavily, Kafka would also be reasonable.

But based purely on these requirements, I'd prefer the simpler managed queue.

---

# 12. Separate Channel Queues

I'd use something like:

```text
                      ┌→ Email Queue → Email Workers
Notification events ─┤
                      └→ SMS Queue   → SMS Workers
```

Why?

Because provider characteristics differ.

Imagine:

```text
Email capacity: 20K/sec
SMS capacity:     500/sec
```

If SMS becomes overloaded, I don't want this:

```text
SMS backlog
   ↓
blocks
   ↓
email delivery
```

Separate queues give us failure isolation.

---

# 13. Revised Architecture

Now:

```text
10–15 Producer Applications
              │
              ▼
       Load Balancer/API
              │
              ▼
      Notification Service
              │
              ▼
          PostgreSQL
     ┌────────┴──────────┐
     │ notifications     │
     │ templates         │
     │ deliveries        │
     │ attempts          │
     │ outbox_events     │
     └────────┬──────────┘
              │
              ▼
       Outbox Publisher
              │
      ┌───────┴─────────┐
      ▼                 ▼
 Email Queue         SMS Queue
      │                 │
      ▼                 ▼
Email Workers       SMS Workers
      │                 │
      ▼                 ▼
Email Provider      SMS Provider
      │                 │
      └──── webhooks ────┘
              │
              ▼
      Notification Service
              │
              ▼
           Postgres
```

Now the request path is very short:

```text
Application
    ↓
Notification API
    ↓
Postgres transaction
    ↓
202 Accepted
```

We should comfortably hit our:

```text
P95 < 200 ms
```

submission target.

---

# 14. Deep Dive — Retries and Duplicate Notifications

Queues commonly provide **at-least-once delivery**.

That means the same event might arrive twice.

Example:

```text
Worker → SES → email successfully sent

worker crashes before ACK

queue retries

Worker → SES → email sent again
```

That is dangerous.

We therefore need idempotency at multiple layers.

### Producer idempotency

```text
UNIQUE(application_id, idempotency_key)
```

prevents:

```text
producer retry
→ duplicate Notification
```

### Delivery idempotency

Use:

```text
(notification_id, channel)
```

as the logical delivery identifier.

Where providers support an idempotency token, send that identifier downstream.

Where they don't, we can reduce duplicates significantly, but there is an important distributed-systems limitation:

> We generally cannot guarantee true exactly-once delivery across our database and an arbitrary third-party provider.

So I would promise:

```text
at-least-once processing
+
strong deduplication
```

rather than incorrectly claiming globally exactly-once sending.

---

# 15. Retry Policy

Suppose Twilio responds:

```text
HTTP 503
```

We shouldn't immediately hammer it.

Use exponential backoff:

```text
attempt 1     immediately
attempt 2     +5 sec
attempt 3     +30 sec
attempt 4     +2 min
attempt 5     +10 min
```

Then:

```text
Dead Letter Queue
```

for messages requiring investigation.

But errors like:

```text
invalid phone number
invalid email address
```

are permanent.

Those should become:

```text
FAILED
```

immediately rather than retrying.

---

# 16. Deep Dive — Traffic Bursts

Now consider:

```text
15 applications
       ↓
large operational event
       ↓
5,000 notification requests/sec
```

Because the API only performs:

```text
validation + Postgres insert
```

it can scale horizontally:

```text
                    ┌→ Notification Service
Applications → LB ──┼→ Notification Service
                    ├→ Notification Service
                    └→ Notification Service
                               │
                               ▼
                           PostgreSQL
```

The queues absorb temporary mismatches between:

```text
incoming rate
```

and:

```text
provider throughput
```

For example:

```text
incoming SMS:        4,000/sec
provider capacity:     500/sec

queue absorbs backlog
```

Workers scale independently based on:

```text
queue depth
oldest message age
processing latency
```

I would also enforce provider rate limits in the workers so that autoscaling doesn't accidentally exceed the provider quota.

---

# 17. Deep Dive — Adding New Channels

Suppose six months later the product team asks for:

```text
WhatsApp
```

The core API can remain:

```json
{
  "channels": ["WHATSAPP"],
  "template_id": "payment_failed"
}
```

We add:

```text
WhatsApp template
WhatsApp queue
WhatsApp worker
WhatsApp provider adapter
```

Architecture:

```text
                          ┌→ Email Queue → Email Adapter
Notification Dispatcher ─┼→ SMS Queue   → SMS Adapter
                          └→ WhatsApp Q  → WhatsApp Adapter
```

Rather than modifying the whole notification system.

The logical interface remains:

```java
interface NotificationChannel {
    SendResult send(RenderedNotification notification);
}
```

So the extensibility requirement directly caused the **channel adapter boundary**.

---

# 18. Deep Dive — Reporting

Our original design had:

```text
Reporting Service → primary Postgres
```

That works initially.

But imagine an operations dashboard running:

```sql
GROUP BY application_id, channel, status
```

across millions of delivery records.

That could interfere with the transaction workload.

Two reasonable approaches:

### Option A — Postgres read replica

```text
Primary Postgres
       │
       ▼
 Read Replica
       │
       ▼
Reporting Service
```

Very simple.

A few seconds of reporting lag is acceptable.

### Option B — Dedicated analytics store

Publish delivery events:

```text
DELIVERED
FAILED
BOUNCED
```

into an analytics pipeline and load something like:

```text
ClickHouse
BigQuery
Snowflake
```

Much better at enormous analytics workloads, but substantially more infrastructure.

Given only **10–15 producer applications**, I would initially choose:

```text
Postgres read replica
+
materialized aggregate tables
```

rather than introduce an OLAP system prematurely.

If reporting eventually becomes a major analytics workload, we can evolve toward the second option.

---

# 19. Reporting Architecture

```text
                                 ┌→ Email Provider
                                 │
Producer Apps → Notification ────┼→ SMS Provider
                                 │
                                 ▼
                          Primary Postgres
                                 │
                              replica
                                 │
                                 ▼
                         Reporting Postgres
                                 │
                                 ▼
                        Reporting Service
                                 │
                                 ▼
                      Dashboard / Applications
```

Useful aggregates might be maintained by:

```text
application
channel
template
hour/day
delivery status
```

so most dashboards don't scan individual attempts.

---

# 20. Technology Stack

I would make fairly conventional choices.

| Concern             | Choice                          | Why                                                             |
| ------------------- | ------------------------------- | --------------------------------------------------------------- |
| API / orchestration | Java + Spring Boot              | Mature HTTP, DB, worker ecosystem                               |
| Primary DB          | PostgreSQL                      | Transactions, idempotency constraints, simple operational model |
| Queue               | AWS SQS-like managed queue      | Durable delivery, retries, DLQ, no ordering requirement         |
| Email               | SES / SendGrid-like provider    | Avoid operating email infrastructure                            |
| SMS                 | Twilio/SNS-like provider        | Carrier integration handled externally                          |
| Reporting           | Postgres read replica initially | Reporting requirements don't justify OLAP yet                   |
| Deployment          | Kubernetes/ECS-style containers | Horizontal API/worker scaling                                   |
| Observability       | OpenTelemetry + metrics/logging | Trace notification lifecycle and failures                       |

Notice what isn't there:

```text
Redis
Elasticsearch
Cassandra
Kafka
distributed locks
CQRS
```

None are currently required by our requirements.

---

# 21. Final Architecture

```text
                   10–15 Producer Applications
                             │
                             ▼
                     API Gateway / LB
                             │
                             ▼
                    Notification Service
                             │
                 ┌───────────┴───────────┐
                 │                       │
                 │ PostgreSQL            │
                 │                       │
                 │ notifications         │
                 │ deliveries            │
                 │ templates             │
                 │ attempts              │
                 │ outbox_events         │
                 └───────────┬───────────┘
                             │
                             ▼
                       Outbox Relay
                             │
                ┌────────────┴────────────┐
                │                         │
                ▼                         ▼
           Email Queue                 SMS Queue
                │                         │
          ┌─────┴─────┐             ┌─────┴─────┐
          │ workers   │             │ workers   │
          │ workers   │             │ workers   │
          └─────┬─────┘             └─────┬─────┘
                │                         │
                ▼                         ▼
          Email Provider             SMS Provider
                │                         │
                └─────── callbacks ───────┘
                             │
                             ▼
                     Delivery Updates
                             │
                             ▼
                         PostgreSQL
                             │
                         replication
                             ▼
                     Reporting Replica
                             │
                             ▼
                     Reporting Service
```

# 22. Validate Against Requirements

**FR1 — Applications submit notifications:** handled by `POST /notifications → Notification Service → PostgreSQL`.

**FR2 — Email and SMS delivery:** handled asynchronously through channel queues, workers, and provider adapters. Adding push/WhatsApp follows the same extension point.

**FR3 — Status/reporting:** delivery callbacks update `notification_deliveries`; Reporting Service reads a reporting replica.

**NFR1 — No lost accepted messages:** database transaction + transactional outbox + durable queue + retries + DLQ.

**NFR2 — Low submission latency:** producer path ends after durable DB persistence rather than waiting for external providers.

**NFR3 — Burst handling:** queues buffer spikes; API and channel workers scale horizontally and independently.

**NFR4 — Extensibility:** stable notification contract plus separate channel adapters/queues isolates new channel implementations.

The most important remaining trade-off is that **true exactly-once user-visible delivery cannot generally be guaranteed across an arbitrary external email/SMS provider**. The system therefore uses durable at-least-once processing plus idempotency and deduplication to make duplicate delivery rare rather than claiming an impossible guarantee.
