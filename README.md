# Stripe-Style OA Practice

Three practice problems modeled on the format of Stripe's HackerRank engineering
coding challenge. These are **original** problems written to mimic the *shape* of
the real thing — do not treat any wording as the actual assessment.

## Why they look like this

Stripe's OA is one dense, real-world scenario broken into ~4 escalating parts that
build on the same code. It rewards careful reading, clean data modeling, string
parsing, hash maps, and stateful processing — not clever algorithms. Time/space
complexity barely matters; passing every part with correct, readable code is the goal.

## How to practice

1. **Read the entire problem — all parts — before writing any code.** Later parts
   often reveal how you should have structured Part 1.
2. Give yourself **60 minutes total** across a single problem to simulate real
   pressure. (Or untimed the first pass, timed the second.)
3. Build and test **part by part.** Get Part 1 fully working before touching Part 2.
4. Reference solutions are intentionally **not** included — the value is in doing it
   cold. Language chosen: **Python** (but any language is fine; the real OA is
   language-agnostic).

## The problems (increasing difficulty)

1. `01_card_range_registry.md` — payment-card BIN range mapping & gap filling
2. `02_subscription_billing.md` — subscription lifecycle, proration & invoicing
3. `03_transaction_fraud.md` — streaming transaction fraud detection

## Self-check tips

- Print your intermediate state between parts to make sure it's right.
- Watch for edge cases the prompt hints at: empty input, overlapping ranges,
  ties, corrupted/duplicate records, exact-boundary conditions.
- Match the output format *exactly* — the real grader uses hidden test cases.
