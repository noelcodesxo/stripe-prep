# Problem 1 — Card Range Registry

**Difficulty:** Warm-up → Medium

**Suggested time:** 15–18 minutes

Every card number begins with a numeric prefix that identifies an issuing bank. The
registry stores inclusive ranges as `<low> <high> <bank>`, where `low` and `high` are
non-negative integers and `low <= high`.

Implement one `Solution.solve(lines, part=...)` processor. The input always has range
definitions first, followed by a literal `QUERIES` line and then zero or more requests.
The separator is required even when the only request is `GAPS` or `CANONICAL`. A
range-only input with no `QUERIES` line has no output. Later parts add request types;
they do not replace lookup requests. Emit each request's result in request order.

In the examples below, pass the input as a list of strings to
`Solution().solve(lines, part=...)`, using the part number shown. Return the
expected output as a list of strings, one string per displayed line, without
labels or extra blank lines. Each example is a separate call with fresh state.

## Part 1 — Look up prefixes

Part 1 ranges do not overlap. After `QUERIES`, each integer line asks for its bank.
Output the bank or `UNKNOWN` on that line.

**Example input**

```text
400000 499999 visa
510000 559999 mastercard
340000 349999 amex
QUERIES
411111
340012
600000
```

**Expected output**

```text
visa
amex
UNKNOWN
```

## Part 2 — Overlapping ranges

Overlapping definitions are allowed; the later range in input order wins on the
overlapping portion only. Prefix lookups remain available with the Part 1 output.

**Example input**

```text
400000 499999 visa
450000 459999 visa_debit
QUERIES
455000
411111
```

**Expected output**

```text
visa_debit
visa
```

The later range owns `455000`; `411111` remains with the original bank.

## Part 3 — Request coverage gaps

The request `GAPS` reports every maximal uncovered span within the domain from the
minimum `low` to the maximum `high`. Emit each as `<gap_low> <gap_high>`, sorted
ascending, or emit `NONE` if there are no gaps. `GAPS` may be mixed with integer
lookups after the same `QUERIES` line.

**Example input**

```text
100 200 a
400 500 b
QUERIES
GAPS
```

**Expected output**

```text
201 399
```

The domain is `[100, 500]`, so the only uncovered span is `[201, 399]`.

## Part 4 — Request canonical ranges

The request `CANONICAL` reports the minimal resolved list of ranges, merging adjacent
or overlapping ranges that map to the same bank. Emit `<low> <high> <bank>` rows
sorted by `low`. It may be mixed with `GAPS` and integer lookups.

**Example input**

```text
10 20 a
30 40 b
QUERIES
15
GAPS
35
CANONICAL
```

**Expected output**

```text
a
21 29
b
10 20 a
30 40 b
```

Results follow request order: lookup, gaps, lookup, then canonical ranges.

## Things to get right

- Inclusive endpoints make both gaps and adjacency sensitive to off-by-one errors.
- A later overlapping range overrides only the portion it covers.
- Keep request processing in one registry flow: later requests must not hide earlier
  lookup behavior.
- Test empty requests, a single range, and queries exactly on both boundaries.
