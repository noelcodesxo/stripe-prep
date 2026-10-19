# Problem 6 — Store Closing Time

*An original problem in the shape of a common Stripe penalty / best-cutoff OA.*

A store logs each hour as `Y` (customers present) or `N` (empty). A closing time `t`
is in `0 .. n`: `0` means never open and `n` means open all day. The unweighted
penalty is:

- one for each `N` in the open prefix `hours[:t]`;
- one for each `Y` in the closed suffix `hours[t:]`.

Use one `Solution.solve(lines, part=...)` processor. Every evaluated log emits the same
row, `<time> <penalty>`. Later parts add automatic selection, multiple logs, and
weights while retaining the earlier explicit-close request.

In the examples below, pass the input as a list of strings to
`Solution().solve(lines, part=...)`, using the part number shown. Return the
expected output as a list of strings, one string per displayed line, without
labels or extra blank lines. Each example is a separate call with fresh state.

## Input records

Each record contains a request prefix followed by one noisy `BEGIN ... END` log. The
prefix applies to the next completed log and can share a line with it or appear on an
earlier line:

```text
CLOSE <t> BEGIN <Y/N and garbage tokens>* END
AUTO BEGIN <Y/N and garbage tokens>* END
```

`CLOSE <t>` requests the penalty at that explicit time. `AUTO` requests the minimum
penalty and chooses the smallest closing time on ties. From Part 3 onward, an
unmarked `BEGIN ... END` record is also an automatic request. Each valid completed
record emits one row in input order. A prefix with no completed record is discarded.

The noisy-log parser follows these rules in every part:

- Any number of records may be present; logs may span lines.
- A second `BEGIN` before `END` restarts that log.
- Tokens other than `Y`, `N`, `BEGIN`, and `END` are garbage and are ignored.
- A `BEGIN` without a matching `END` is discarded.

## Part 1 — Explicit close

Use `CLOSE <t>` with one log. Output `<t> <penalty>`.

**Example input**

```text
CLOSE 3 BEGIN Y Y N Y END
```

**Expected output**

```text
3 2
```

One empty hour is open and one customer hour is closed: penalty 2 at closing time 3.

## Part 2 — Best close

Use `AUTO` with one log. Output `<best_time> <minimum_penalty>`. The chosen time is
the smallest `t` that achieves the minimum.

**Example input**

```text
AUTO BEGIN Y Y N Y END
```

**Expected output**

```text
2 1
```

Times 2 and 4 both have penalty 1; the earlier time wins.

## Part 3 — Aggregate logs

Process any number of noisy logs through the same parser. Unmarked logs default to
`AUTO`; explicit `CLOSE` and `AUTO` requests remain valid in the aggregate stream.

**Example input**

```text
garbage BEGIN Y Y N END trash BEGIN N Y END un
finished BEGIN Y Y
```

**Expected output**

```text
2 0
0 1
```

The two completed logs produce rows; the final unfinished log produces none.

## Part 4 — Weighted penalties

An optional first line `WEIGHTS <a> <b>` changes the costs for every record: `a` per
empty hour while open, `b` per customer hour while closed. All earlier record forms
remain valid, and every output row keeps the `<time> <penalty>` layout.

**Example input**

```text
WEIGHTS 1 5
CLOSE 1 BEGIN N Y END
AUTO BEGIN Y N Y END
garbage BEGIN Y BEGIN N Y END
```

**Expected output**

```text
1 6
3 1
2 1
```

The explicit close costs 1 + 5 = 6. The automatic requests choose time 3 and time 2; the nested `BEGIN` restarts the last log.

## Traps to watch

- Closing time ranges over `0..n`, including both endpoints.
- Ties resolve to the smallest time; scan ascending and update only on a strict
  improvement.
- Keep request mode attached to the record it prefixes, even if a nested `BEGIN`
  restarts that record.
