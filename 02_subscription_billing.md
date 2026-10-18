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

## Part 1 — Subscription charges

SUBSCRIBE accrues charges from its day inclusive. CANCEL stops accrual on its day
(exclusive). A still-active subscription accrues through the `QUERY` cutoff, also
exclusive. For every `QUERY <day>`, output each customer who has ever subscribed as
`<customer> <cents>`, sorted by customer name. A customer remains in the report even
if the total is zero.

```text
PLAN basic 100
5 SUBSCRIBE alice basic
10 CANCEL alice
QUERY 20
```

Output:

```text
alice 500
```

## Part 2 — Plan changes

`CHANGE` stops the old rate and starts the new rate on the change day. A change for a
customer without an active subscription is ignored. Previous `QUERY` requests and
their output are unchanged.

## Part 3 — Re-subscription and refunds

A customer may subscribe again after cancelling; separate intervals add together.
`REFUND` subtracts its cents from the customer's running total on its event day. A
reported total may be negative. `QUERY` includes refunds on or before its cutoff.

## Part 4 — Invoice windows

`INVOICE <customer> <start_day> <end_day>` requests the gross charges in the half-open
window `[start_day, end_day)`, with rate proration at both edges. Refunds do not affect
invoice amounts. Output one `<customer> <cents>` line for each invoice, in request
order. `QUERY` requests continue to work in the same input.

## Things to get right

- Inclusive start, exclusive end governs subscriptions, changes, queries, and invoices.
- Keep enough history to answer multiple cutoffs and invoice windows.
- A change day is billed at the new rate.
- Test same-day cancel/re-subscribe, a change on the subscribe day, an invoice outside
  all subscriptions, and a refund larger than the customer's charges.
