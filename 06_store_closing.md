# Problem 6 — Store Closing Time

*An original problem in the shape of a common Stripe "penalty / best cutoff" OA. Original wording.*

A store logs each hour as `Y` (customers present) or `N` (empty). We choose a **closing time** `t` in `0 .. n` (0 = never open, n = open all day). The penalty is:

- `+1` (or a weight) for each hour we were **open but empty** — that's `N` hours in `hours[:t]`.
- `+1` (or a weight) for each hour we were **closed but had customers** — that's `Y` hours in `hours[t:]`.

## Part 1 — Compute penalty

Input: line 1 = space-separated `Y`/`N` log; line 2 = a closing time `t`. Output one line: the penalty.

```
log "Y Y N Y", t=3  -> 2   (hour 3 open+empty = 1; hour 4 closed+customers = 1)
log "Y Y N Y", t=4  -> 1   (open all day: only the empty hour 3 counts)
```

## Part 2 — Best closing time

Input: line 1 = the log. Output one line: the closing time with **minimum penalty**; on a tie, the **smallest** closing time. There are `n+1` candidates (`0..n`) — aim for O(n) with a running count, not O(n²).

## Part 3 — Aggregate parsing

Employees paste many days into one noisy blob (any number of input lines). A **valid log** is a run `BEGIN <Y/N>* END`:

- `BEGIN` with no matching `END` is discarded (unfinished).
- Logs cannot nest — a second `BEGIN` before `END` **restarts** the current log.
- Any token that isn't `BEGIN`, `END`, `Y`, or `N` is garbage; ignore it.
- Logs may span multiple lines; there may be several per line.

Output the best closing time (Part 2) for each valid log, in order, one per line.

## Part 4 — Weighted penalties

Input: line 1 = `WEIGHTS <a> <b>` where `a` is the cost of each empty-open hour and `b` the cost of each closed-with-customers hour; the rest is an aggregate blob as in Part 3. For each valid log, output `<best_time> <min_penalty>` under those weights.

```
WEIGHTS 1 5 / BEGIN Y N Y END  -> "3 1"   (closing at 3 leaves only the one empty hour)
```

## Traps to watch

- Closing time ranges over `0..n` inclusive — that's `n+1` candidates.
- Ties resolve to the **smallest** time (scan ascending with a strict `<`).
- Nested `BEGIN` resets; unfinished logs vanish.
