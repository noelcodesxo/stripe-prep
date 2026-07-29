# Problem 1 — Card Range Registry

**Difficulty:** Warm-up → Medium
**Suggested time:** 15–18 minutes

## Background

At a payments company, every card number begins with a numeric prefix that identifies
the issuing bank. We store this mapping as a set of **ranges**. Each range covers a
contiguous, inclusive span of numeric prefixes and maps every prefix in that span to a
single bank identifier (a string).

You will be given the ranges as lines of text and must answer questions about them.
All prefixes are non-negative integers. Ranges are given as `low high bank`, where
`low <= high` and both bounds are inclusive.

Read the whole problem before you start — the way you store the ranges in Part 1
determines how painful Parts 3 and 4 are.

---

## Part 1 — Build the registry and look up a prefix

You are given a list of range definitions, one per line:

```
<low> <high> <bank>
```

Then a list of query prefixes, one per line, each an integer.

For each query, output the bank that owns that prefix, or `UNKNOWN` if no range
covers it. You may assume in Part 1 that no two ranges overlap.

**Example**

Ranges:

```
400000 499999 visa
510000 559999 mastercard
340000 349999 amex
```

Queries:

```
411111
340012
600000
```

Output:

```
visa
amex
UNKNOWN
```

---

## Part 2 — Overlapping ranges, last-write-wins

Ranges may now overlap. When more than one range covers a queried prefix, the range
that appeared **later in the input** wins (it overrides the earlier ones for the
overlapping portion only).

**Example**

Ranges:

```
400000 499999 visa
450000 459999 visa_debit
```

Query `455000` → `visa_debit`; query `411111` → `visa`.

Note that a later range may only partially cover an earlier one. The earlier range
still owns the prefixes outside the overlap.

---

## Part 3 — Report the coverage gaps

Given the final, resolved registry (after applying Part 2's override rules), report
every **gap**: a maximal contiguous span of prefixes, within the overall covered
domain, that is owned by no bank.

Define the domain as `[minimum low seen, maximum high seen]`. Output each gap as
`<gap_low> <gap_high>` on its own line, sorted ascending. If there are no gaps,
output `NONE`.

**Example**

Ranges:

```
100 200 a
400 500 b
```

Domain is `[100, 500]`. Output:

```
201 399
```

---

## Part 4 — Merge adjacent equal-bank ranges

After resolving overrides (Part 2), produce the **minimal canonical list** of ranges:
merge any two ranges that are adjacent or overlapping **and map to the same bank** into
a single range. Two ranges are adjacent when one ends exactly one below where the next
begins (e.g. `100–200` and `201–300`).

Output the canonical ranges sorted ascending by `low`, one per line, as
`<low> <high> <bank>`.

**Example**

Resolved ranges:

```
100 150 visa
151 200 visa
300 400 amex
```

Output:

```
100 200 visa
300 400 amex
```

---

## Things to get right

- Part 1's data structure choice cascades. A flat list you re-scan per query is fine
  for correctness; think about whether you'd rather resolve to a list of
  non-overlapping segments up front.
- "Last-write-wins" is about the _overlapping portion only_, not the whole earlier range.
- Off-by-one on inclusive bounds is the classic failure here (gaps and adjacency both
  hinge on it).
- Empty input, a single range, and a query exactly on a boundary are all worth testing.
