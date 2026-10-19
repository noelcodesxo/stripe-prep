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

In the examples below, pass the input as a list of strings to
`Solution().solve(lines, part=...)`, using the part number shown. Return the
expected output as a list of strings, one string per displayed line, without
labels or extra blank lines. Each example is a separate call with fresh state.

## Part 1 — Base card metrics

Output one row per card, sorted by `card_id`:

```text
<card_id> <approved_count> <total_approved_cents> <decline_rate>
```

`decline_rate` is `declined / total_transactions`, formatted to two decimal places.
Only approved transactions contribute to the count and approved cents.

**Example input**

```text
1 cardA 1000 shopX APPROVED
2 cardA 500 shopY DECLINED
3 cardB 200 shopX APPROVED
4 cardA 700 shopX APPROVED
```

**Expected output**

```text
cardA 2 1700 0.33
cardB 1 200 0.00
```

Card A has two approvals totaling 1700 cents and one decline out of three transactions.

## Part 2 — High-velocity flag

Add a `VELOCITY <N> <W>` config line. A card is high-velocity if it has at least `N`
approved transactions in any inclusive `W`-second window. Append one `Y` or `N` flag
to every Part 1 row. Keep the four base columns first. If there are no cards, emit no
rows.

**Example input**

```text
VELOCITY 3 60
10 cardA 100 m APPROVED
10 cardB 100 m APPROVED
30 cardA 100 m APPROVED
65 cardA 100 m APPROVED
66 cardA 100 m APPROVED
200 cardB 100 m APPROVED
```

**Expected output**

```text
cardA 4 400 0.00 Y
cardB 2 200 0.00 N
```

Both cards keep their base metrics. Only card A has three approvals within 60 seconds.

## Part 3 — Testing-burst merchants

Add `BURST <M> <T> <W>` after `VELOCITY`. A `(card, merchant)` is a testing burst if
any `W`-second window contains at least `M` transactions (approved or declined) and
the average amount in that window is below `T` cents. Append a comma-separated list
of the card's flagged merchants, sorted ascending; use `-` when the list is empty.
Rows retain all earlier columns and remain sorted by card.

**Example input**

```text
VELOCITY 3 60
BURST 3 100 60
0 cardA 10 mtest APPROVED
0 cardA 5000 mbig APPROVED
1 cardA 5000 mbig APPROVED
2 cardA 5000 mbig APPROVED
5 cardA 20 mtest DECLINED
10 cardA 30 mtest APPROVED
```

**Expected output**

```text
cardA 5 15040 0.17 Y mtest
```

The three `mtest` amounts average 20 cents; `mbig` does not qualify. All five approvals contribute to the 15040-cent total.

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

**Example input**

```text
VELOCITY 3 60
BURST 3 100 60
TOPK 2
0 cardB 20000 shop APPROVED
1 cardB 100 shop DECLINED
5 cardC 100 shop DECLINED
10 cardA 100 mtest APPROVED
30 cardA 50 mtest APPROVED
65 cardA 40 mtest DECLINED
66 cardA 30 mtest APPROVED
```

**Expected output**

```text
cardA 3 180 0.25 Y mtest 30
cardB 1 20000 0.50 N - 7
```

Card A scores 5 + 10 + 15 = 30; card B scores 5 + 2 = 7. Card C is outside the top two.

## Things to get right

- Windows may start at any transaction; input is sorted so a deque or two-pointer
  approach is efficient.
- Apply the average test to the same qualifying window as the transaction count.
- Keep all per-card history needed by later flags and the score.
- Test a single-transaction card, all-declined cards, score ties, and `K` larger than
  the number of cards.
