# Problem 2 — Subscription Billing Engine

**Difficulty:** Medium

**Suggested time:** 18–22 minutes

Time is measured in whole, non-negative days. A customer has at most one active
subscription at a time. Process one ordered event history, then answer its requests.

Use one `Solution.solve(lines, part=...)` processor. Input starts with plan definitions
and dated events, sorted by day, then contains one or more `QUERY` and/or `INVOICE`
requests. All requests come after the events and are emitted in request order. Later
parts add event/request types while retaining earlier ones.

```text
PLAN <name> <daily_rate_cents>
<day> SUBSCRIBE <customer> <plan>
<day> CANCEL <customer>
<day> CHANGE <customer> <new_plan>
<day> REFUND <customer> <cents>
QUERY <day>
INVOICE <customer> <start_day> <end_day>
```

In the examples below, pass the input as a list of strings to
`Solution().solve(lines, part=...)`, using the part number shown. Return the
expected output as a list of strings, one string per displayed line, without
labels or extra blank lines. Each example is a separate call with fresh state.

## Part 1 — Subscription charges

SUBSCRIBE accrues charges from its day inclusive. CANCEL stops accrual on its day
(exclusive). A still-active subscription accrues through the `QUERY` cutoff, also
exclusive. For every `QUERY <day>`, output each customer who has ever subscribed as
`<customer> <cents>`, sorted by customer name. A customer remains in the report even
if the total is zero.

**Example input**

```text
PLAN basic 100
5 SUBSCRIBE alice basic
10 CANCEL alice
QUERY 20
```

**Expected output**

```text
alice 500
```

Alice is charged for days 5–9: 5 × 100 = 500 cents.

## Part 2 — Plan changes

`CHANGE` stops the old rate and starts the new rate on the change day. A change for a
customer without an active subscription is ignored. Previous `QUERY` requests and
their output are unchanged.

**Example input**

```text
PLAN basic 100
PLAN pro 300
0 SUBSCRIBE bob basic
4 CHANGE bob pro
6 CANCEL bob
QUERY 10
```

**Expected output**

```text
bob 1000
```

Bob owes 4 × 100 + 2 × 300 = 1000 cents.

## Part 3 — Re-subscription and refunds

A customer may subscribe again after cancelling; separate intervals add together.
`REFUND` subtracts its cents from the customer's running total on its event day. A
reported total may be negative. `QUERY` includes refunds on or before its cutoff.

**Example input**

```text
PLAN basic 100
0 SUBSCRIBE carol basic
5 CANCEL carol
10 SUBSCRIBE carol basic
12 CANCEL carol
15 REFUND carol 250
QUERY 20
```

**Expected output**

```text
carol 450
```

Carol owes (5 + 2) × 100 − 250 = 450 cents.

## Part 4 — Invoice windows

`INVOICE <customer> <start_day> <end_day>` requests the gross charges in the half-open
window `[start_day, end_day)`, with rate proration at both edges. Refunds do not affect
invoice amounts. Output one `<customer> <cents>` line for each invoice, in request
order. `QUERY` requests continue to work in the same input.

**Example input**

```text
PLAN basic 100
PLAN pro 300
0 SUBSCRIBE carol basic
4 CHANGE carol pro
QUERY 8
INVOICE carol 3 8
INVOICE carol 0 4
INVOICE carol 100 200
```

**Expected output**

```text
carol 1600
carol 1300
carol 400
carol 30000
```

The first row answers `QUERY 8`; the remaining rows answer the three invoices. Carol never cancels, so the final window still accrues charges.

## Things to get right

- Inclusive start, exclusive end governs subscriptions, changes, queries, and invoices.
- Keep enough history to answer multiple cutoffs and invoice windows.
- A change day is billed at the new rate.
- Test same-day cancel/re-subscribe, a change on the subscribe day, an invoice outside
  all subscriptions, and a refund larger than the customer's charges.
