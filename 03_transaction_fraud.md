# Problem 3 — Streaming Transaction Fraud Detection

**Difficulty:** Medium → Hard

**Suggested time:** 20–25 minutes

The input is an already timestamp-sorted stream of card transactions:

```text
<timestamp> <card_id> <amount_cents> <merchant> <status>
```

Timestamps are non-negative integers, amounts are positive integers, and status is
`APPROVED` or `DECLINED`. Config lines come before transactions. Build one per-card
history in `Solution.solve(lines, part=...)`; later parts append report columns to the
Part 1 metrics. Do not replace the report with a different output mode.

## Part 1 — Base card metrics

Output one row per card, sorted by `card_id`:

```text
<card_id> <approved_count> <total_approved_cents> <decline_rate>
```

`decline_rate` is `declined / total_transactions`, formatted to two decimal places.
Only approved transactions contribute to the count and approved cents.

## Part 2 — High-velocity flag

Add a `VELOCITY <N> <W>` config line. A card is high-velocity if it has at least `N`
approved transactions in any inclusive `W`-second window. Append one `Y` or `N` flag
to every Part 1 row. Keep the four base columns first. If there are no cards, emit no
rows.

## Part 3 — Testing-burst merchants

Add `BURST <M> <T> <W>` after `VELOCITY`. A `(card, merchant)` is a testing burst if
any `W`-second window contains at least `M` transactions (approved or declined) and
the average amount in that window is below `T` cents. Append a comma-separated list
of the card's flagged merchants, sorted ascending; use `-` when the list is empty.
Rows retain all earlier columns and remain sorted by card.

## Part 4 — Risk score and top K

Add `TOPK <K>` after the earlier configs. Compute each card's integer score:

- `+5` per declined transaction;
- `+10` if high-velocity;
- `+15` per distinct testing-burst merchant;
- `+1` per full 10,000 approved cents.

Append the score to each row, retaining every earlier column. Emit only the top `K`
rows, sorted by score descending and then `card_id` ascending. Scores are computed
over the same transaction history and use the Part 2 and Part 3 flags.

The complete stage 4 layout is:

```text
<card_id> <approved_count> <total_approved_cents> <decline_rate> <Y|N> <merchant-list|-> <score>
```

## Things to get right

- Windows may start at any transaction; input is sorted so a deque or two-pointer
  approach is efficient.
- Apply the average test to the same qualifying window as the transaction count.
- Keep all per-card history needed by later flags and the score.
- Test a single-transaction card, all-declined cards, score ties, and `K` larger than
  the number of cards.
