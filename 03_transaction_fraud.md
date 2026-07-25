# Problem 3 — Streaming Transaction Fraud Detection

**Difficulty:** Medium → Hard
**Suggested time:** 20–25 minutes

## Background

You process a stream of card transactions and flag suspicious activity. Each
transaction is a line, already sorted by timestamp ascending:

```
<timestamp> <card_id> <amount_cents> <merchant> <status>
```

- `timestamp` is a non-negative integer (seconds).
- `amount_cents` is a positive integer.
- `status` is `APPROVED` or `DECLINED`.

Read all parts before coding. Parts 3 and 4 both need per-card history kept in a way
that lets you look back over a time window, so design for that from the start.

---

## Part 1 — Basic totals and decline rate

Output, for each card that appears (sorted by `card_id`):

```
<card_id> <approved_count> <total_approved_cents> <decline_rate>
```

where `decline_rate` is `declined / total_transactions` for that card, rounded to
**two decimal places** (e.g. `0.33`). Only APPROVED transactions contribute to
`total_approved_cents` and `approved_count`.

---

## Part 2 — Flag high-velocity cards

A card is **high-velocity** if it has **N or more APPROVED transactions within any
sliding window of W seconds** (window is inclusive on both ends). `N` and `W` are given
on the first line of input as:

```
CONFIG <N> <W>
```

Output the `card_id` of every high-velocity card, sorted ascending, one per line. If
none, output `NONE`.

**Example**

`CONFIG 3 60`, and a card with approved transactions at timestamps
`10, 30, 65, 66` → the window `[10,66]` is 56s wide and holds 4 approvals ≥ 3, so the
card is flagged. (Any qualifying window suffices.)

---

## Part 3 — Detect merchant "testing" bursts

Fraudsters test stolen cards with many small charges at one merchant. Flag a
`(card_id, merchant)` pair as a **testing burst** if, within any W-second window, the
pair has at least `M` transactions (APPROVED **or** DECLINED) **and** the average
amount of those transactions is **below** `T` cents. `M` and `T` are given as:

```
CONFIG2 <M> <T>
```

Output each flagged pair as `<card_id> <merchant>`, sorted by card_id then merchant.
If none, output `NONE`. The "average below T" test applies to the specific window of
transactions that meets the count threshold — if any qualifying window satisfies both
conditions, flag the pair.

---

## Part 4 — Rank cards by a risk score

Compute a **risk score** per card and output the top `K` riskiest, where `K` comes from:

```
CONFIG3 <K>
```

Risk score is the integer sum of:

- `+5` for each DECLINED transaction on the card,
- `+10` if the card was flagged high-velocity in Part 2,
- `+15` for each distinct merchant with which the card had a testing burst in Part 3,
- `+1` for every full 10,000 cents of `total_approved_cents` (integer division).

Output the top `K` cards as `<card_id> <score>`, sorted by score **descending**, then
by `card_id` ascending to break ties. If fewer than `K` cards exist, output them all.

---

## Things to get right

- Sliding windows: because input is time-sorted, a two-pointer / deque over each
  card's transaction times beats re-scanning. But correctness first — a nested scan is
  acceptable to pass.
- "Any window" means you don't get to pick a fixed grid; a qualifying window can start
  at any transaction.
- Decline rate rounding: decide half-up vs. banker's rounding and be consistent; test
  values like `0.125`.
- Keep Part 2 and Part 3 flags around — Part 4's score reads directly from them.
- Test: a card with a single transaction, all-declined cards, ties in the Part 4
  ranking, and `K` larger than the number of cards.
