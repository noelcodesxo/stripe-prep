# Stripe-Style OA Practice

A self-contained, **offline** practice kit modeled on the format of Stripe's HackerRank
engineering coding challenge: seven original problems, each one dense scenario split
into four escalating parts, each with a starter (boilerplate) file and a runnable test
suite. These are **original** problems written to mimic the *shape* of the real thing —
do not treat any wording as the actual assessment.

## Why they look like this

Stripe's OA is one real-world scenario broken into ~4 parts that build on the same code.
It rewards careful reading, clean data modeling, string parsing, hash maps, stateful
processing, and — for the load balancer — object-oriented design. Time/space complexity
barely matters; passing every part with correct, readable code, and matching the output
format exactly, is the goal.

## The problems

| # | Folder | Scenario | Core patterns |
|---|--------|----------|---------------|
| 1 | `p1_card_range` | Card Range Registry | interval lookup, override precedence, gap/merge |
| 2 | `p2_subscription` | Subscription Billing Engine | timeline sim, proration, half-open windows |
| 3 | `p3_fraud` | Transaction Fraud Detection | grouped counting, sliding windows, risk scoring |
| 4 | `p4_load_balancer` | Multi-Stage Load Balancer | **OOD**, least-loaded, sticky routing, capacity |
| 5 | `p5_name_registry` | Company Name Registry | string normalization, registry + owner-only undo |
| 6 | `p6_store_closing` | Store Closing Time | prefix-sum penalty, BEGIN/END state-machine parse |
| 7 | `p7_card_validation` | Payment Card Validation | Luhn, network detect, redacted/corrupted brute force |

Read `STUDY_GUIDE.md` first — it's the strategy + pattern reference, and it maps each
pattern to the problem that drills it. Problem statements live in the numbered `.md`
files at the repo root (`04_load_balancer.md`, etc.).

## Layout

```
stripe-prep/
  STUDY_GUIDE.md                 strategy, the reusable pattern toolkit, time budget
  practice.py                    timed offline practice driver (see below)
  01_card_range_registry.md      full problem statements (read these first)
  02_subscription_billing.md
  03_transaction_fraud.md
  04_load_balancer.md
  05_name_registry.md
  06_store_closing.md
  07_card_validation.md
  problems/
    p4_load_balancer/
      solution_p4.py             <- your code goes here (Solution class with I/O contract)
      test_p4.py                 <- runnable, hand-verified tests
    ...one folder per problem...
  requirements.txt
  run_tests.sh
```

## How it works

Each `solution_pX.py` mirrors a HackerRank stub: a `Solution` class with one stable
entry point, `solve(lines, part=1)`. Pass the cumulative input as a **list of lines**;
it returns a **list of output lines**. `part` selects the latest feature or rule you
are practicing. Later parts extend the same state and retain earlier request types
and output fields instead of switching to a separate program. Implement the shared
flow in `solve` and its domain helpers, leaving the CLI harness alone. The docstring
at the top of every stub summarizes its input and output contract. Run a part against
stdin manually with:

```
python problems/p4_load_balancer/solution_p4.py 3 < some_input.txt
```

The tests call `Solution.solve` and compare against hand-verified expected outputs —
they fail with `NotImplementedError` until you fill in the cumulative features.

## Timed practice driver

`practice.py` turns the repo into a mock exam:

```
python practice.py                 # list all problems
python practice.py p4              # start a 60-minute timed session on problem 4
python practice.py p4 --minutes 45 # custom budget
python practice.py p4 --test       # just run its tests, no timer
```

A session prints the problem, runs its tests once so you see the stubs fail, then shows
a live countdown. Press Ctrl-C when you're done (or let it expire) and it re-grades and
prints a pass/fail summary. Stdlib-only, no network.

## Running the tests directly

```
pip install -r requirements.txt        # once (pytest only)
./run_tests.sh                          # all problems
./run_tests.sh problems/p4_load_balancer   # just one
python -m pytest problems -v            # or straight through pytest
```

## How to practice

1. **Read the entire problem — all parts — before writing any code.** Later parts
   add requests and rules to the same processor. (The load balancer is the clearest
   example: design one stateful class up front.)
2. Simulate the real thing: **60 minutes total** on one problem, via `practice.py`.
3. Build and test **part by part.** Keep earlier requests working as each feature is
   added; later tests include earlier behavior.
4. Reference solutions are intentionally **not** included — the value is in doing it
   cold. The tests show input/output examples, not the algorithm. Language: Python,
   but the real OA is language-agnostic.

## Edge cases worth testing yourself

Empty input, a single record, values exactly on inclusive/exclusive boundaries, ties in
any ranking (resolve to the smallest/first), duplicate or "corrupted" records, and undo
operations (reclaim, disconnect, dispute) that must cleanly reverse state. The bundled
tests cover some of these; add your own.
