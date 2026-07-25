# Problem 2 — Subscription Billing Engine

**Difficulty:** Medium
**Suggested time:** 18–22 minutes

## Background

You are building the billing core for a subscription product. Time is measured in
**whole days** as non-negative integers (day 0, day 1, …) — no real calendar, no time
zones. You process an ordered **event log** and answer questions about what customers
owe.

A customer subscribes to a **plan**. Each plan has a name and a **daily rate** in
integer cents. A customer has at most one active subscription at a time.

Read all four parts first. The event model you pick in Part 1 has to survive plan
changes and refunds later.

---

## Part 1 — Total charges from a simple lifecycle

You are given plan definitions, one per line:

```
PLAN <name> <daily_rate_cents>
```

Then an event log, one event per line, already sorted by day ascending:

```
<day> SUBSCRIBE <customer> <plan>
<day> CANCEL <customer>
```

A subscription accrues charges for each day the customer is subscribed, from the
SUBSCRIBE day **inclusive** up to (but **not including**) the CANCEL day. A customer
who never cancels is still subscribed "as of" a final query day given at the end of
input as:

```
QUERY <day>
```

For each `QUERY <day>`, output total accrued cents per customer that has ever
subscribed, as `<customer> <cents>`, sorted by customer name. Charges accrue only up
to and not including the query day.

**Example**

```
PLAN basic 100
5 SUBSCRIBE alice basic
10 CANCEL alice
QUERY 20
```
alice was subscribed days 5,6,7,8,9 = 5 days × 100 = `500`.
Output:
```
alice 500
```

---

## Part 2 — Plan changes with proration

A new event appears:

```
<day> CHANGE <customer> <new_plan>
```

On a CHANGE, the customer stops accruing the old plan's rate and starts accruing the
new plan's rate **beginning that day** (the change day is billed at the new rate).
Charges before the change day keep the old rate. A CHANGE for a customer with no active
subscription is invalid input and can be ignored.

**Example**

```
PLAN basic 100
PLAN pro 300
0 SUBSCRIBE bob basic
4 CHANGE bob pro
6 CANCEL bob
QUERY 10
```
Days 0–3 at 100 = 400; days 4–5 at 300 = 600; total `1000`.

---

## Part 3 — Re-subscription and refunds

Two more events:

```
<day> SUBSCRIBE <customer> <plan>   # may now happen again after a CANCEL
<day> REFUND <customer> <cents>
```

A customer may subscribe again after cancelling; charges from separate subscription
intervals **add up**. A REFUND subtracts a fixed number of cents from that customer's
running total. A customer's reported total may go negative; report it as-is.

Output format is unchanged: `<customer> <cents>` sorted by customer.

---

## Part 4 — Invoicing windows

Instead of (or in addition to) a single final query, you may be asked for the amount
billed within a **half-open window** `[start_day, end_day)`:

```
INVOICE <customer> <start_day> <end_day>
```

Output the charges that customer accrued **only within that window** — apply proration
at window edges (a subscription that spans the boundary is counted only for the days
inside `[start_day, end_day)`). Refunds are **not** included in an INVOICE result;
INVOICE reports gross accrued charges for the window only.

Output one line per INVOICE, in input order: `<customer> <cents>`.

**Example**

```
PLAN basic 100
0 SUBSCRIBE carol basic
INVOICE carol 3 8
```
Days 3,4,5,6,7 = 5 × 100 = `500`.

---

## Things to get right

- Inclusive start, exclusive end is the whole game — SUBSCRIBE day counts, CANCEL day
  does not, and the same rule governs INVOICE windows.
- Don't collapse a customer's history into one interval too early; Part 3 needs
  multiple intervals per customer.
- CHANGE bills the change day at the new rate — decide where that boundary lives before
  you write the accrual loop.
- Test: cancel-and-resubscribe same day, a CHANGE on the SUBSCRIBE day, an INVOICE
  window entirely outside any subscription (should be 0), and a refund larger than
  charges (negative total).
