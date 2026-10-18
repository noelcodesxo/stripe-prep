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

```text
CLOSE 3 BEGIN Y Y N Y END  ->  3 2
```

## Part 2 — Best close

Use `AUTO` with one log. Output `<best_time> <minimum_penalty>`. The chosen time is
the smallest `t` that achieves the minimum.

```text
AUTO BEGIN Y Y N Y END  ->  2 1
```

## Part 3 — Aggregate logs

Process any number of noisy logs through the same parser. Unmarked logs default to
`AUTO`; explicit `CLOSE` and `AUTO` requests remain valid in the aggregate stream.

## Part 4 — Weighted penalties

An optional first line `WEIGHTS <a> <b>` changes the costs for every record: `a` per
empty hour while open, `b` per customer hour while closed. All earlier record forms
remain valid, and every output row keeps the `<time> <penalty>` layout.

```text
WEIGHTS 1 5
BEGIN Y N Y END  ->  3 1
```

## Traps to watch

- Closing time ranges over `0..n`, including both endpoints.
- Ties resolve to the smallest time; scan ascending and update only on a strict
  improvement.
- Keep request mode attached to the record it prefixes, even if a nested `BEGIN`
  restarts that record.
