# Stripe-Style OA Practice

Three practice problems modeled on the format of Stripe's HackerRank engineering
coding challenge, each with a starter (boilerplate) file and a runnable test suite.
These are **original** problems written to mimic the *shape* of the real thing — do
not treat any wording as the actual assessment.

## Why they look like this

Stripe's OA is one dense, real-world scenario broken into ~4 escalating parts that
build on the same code. It rewards careful reading, clean data modeling, string
parsing, hash maps, and stateful processing — not clever algorithms. Time/space
complexity barely matters; passing every part with correct, readable code is the goal.

## Layout

```
stripe-oa/
  01_card_range_registry.md      full problem statements (read these first)
  02_subscription_billing.md
  03_transaction_fraud.md
  problems/
    p1_card_range/
      solution_p1.py             <- your code goes here (stub with the I/O contract)
      test_p1.py                 <- runnable tests
    p2_subscription/
      solution_p2.py
      test_p2.py
    p3_fraud/
      solution_p3.py
      test_p3.py
  requirements.txt
  run_tests.sh
```

## How it works

Each `solution_pX.py` mirrors a HackerRank stub: four functions (`part1`..`part4`),
one per part of the problem. Each function takes the input for that part as a **list
of lines** and returns a **list of output lines**. The docstring at the top of every
stub spells out the exact input format and expected output for each part. There's also
a `__main__` block so you can run a part against stdin manually:

```
python problems/p1_card_range/solution_p1.py 2 < some_input.txt
```

The tests call your functions directly and compare against hand-verified expected
outputs — they fail with `NotImplementedError` until you fill each part in.

## Running the tests

```
pip install -r requirements.txt        # once
./run_tests.sh                          # all problems
./run_tests.sh problems/p1_card_range   # just problem 1
```

Or straight through pytest: `python3 -m pytest problems -v`.

## How to practice

1. **Read the entire problem — all parts — before writing any code.** Later parts
   often reveal how you should have structured Part 1.
2. Simulate the real thing: give yourself **60 minutes total** on one problem.
3. Build and test **part by part.** Get Part 1 green before touching Part 2.
4. Reference solutions are intentionally **not** included — the value is in doing it
   cold. (The tests show input/output examples, not the algorithm.) Language: Python,
   but the real OA is language-agnostic.

## Edge cases worth testing yourself

Empty input, a single record, values exactly on inclusive/exclusive boundaries,
overlapping vs. merely adjacent ranges, ties in any ranking, and duplicate or
"corrupted" records. The bundled tests cover some of these; add your own.
