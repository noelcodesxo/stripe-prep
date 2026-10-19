# Problem 8 — Chat Token Billing

**Difficulty:** Medium · **Suggested time:** 60 minutes · **Three parts**

## Context and sources

Build a monthly billing calculator for a chat platform. This practice exercise is
adapted from public reports, not an official Stripe assessment statement:

- [Candidate thread confirming the topic](https://www.reddit.com/r/leetcode/comments/1rjsdxt/anyone_who_took_stripe_oa_recently/)
- [Problem reconstruction and examples](https://www.fastprep.io/problems/stripe-chat-billing-calculation)
- [Detailed reported requirements](https://www.reddit.com/r/OfferEngineering/comments/1s3w191/stripe_software_engineer_online_assessment_full/)

The aggregation and rounding conventions below make this exercise deterministic;
the public accounts do not fully establish every detail of the actual assessment.

## Input and output contract

Each `partN(sessions)` takes a list of CSV strings, one chat session per string:

```text
user_id,input_tokens,output_tokens,plan
```

There is no header or record count. IDs contain ASCII letters, digits, or underscores.
Token counts are nonnegative integers; plans are `payg` or `fixed`. Input is valid,
may be unordered, and may contain repeated users. Each call covers one month.
Every row counts as a session, including zero-token rows and identical rows.

Return one string per user, sorted lexicographically by ID, in the exact format
`user_id: $xx.xx` (two decimal places, no thousands separators). Include zero bills.
Empty input returns `[]`.

## Part 1 — Pay as you go

All sessions use `payg`. Input costs 3 cents per complete 100 tokens; output costs
4 cents per complete 100 tokens. First sum a user's tokens across sessions, keeping
input and output separate; then discard partial blocks. Thus two sessions of 60
input tokens produce one billable input block. Do not round blocks up.

```python
sessions = ["userA,100,120,payg", "userB,150,100,payg", "userB,100,130,payg"]
# ["userA: $0.07", "userB: $0.14"]
```

## Part 2 — Fixed monthly plan

Users may use either plan, but each user's sessions all have the same plan.
A fixed user pays $15 once for the month, with 40,000 input and 20,000 output tokens
included. Aggregate usage by direction, subtract the corresponding allowance, clamp
negative excess to zero, and charge complete excess blocks at the PAYG rates.
Unused input allowance cannot cover output usage, or vice versa.

```python
sessions = ["userA,100,100,payg", "userB,20000,10000,fixed", "userB,25000,12000,fixed"]
# ["userA: $0.07", "userB: $17.30"]
```

## Part 3 — Switching plans

A user may now have both kinds of session. Let `r` be that user's number of fixed
sessions divided by their total number of sessions. Their fixed fee is `$15 * r`,
and their included input/output allowances are `40000 * r` and `20000 * r`.
Proration depends on session count, not token volume or row order.

Aggregate PAYG and fixed usage separately for each user and direction. PAYG tokens
do not consume fixed allowances. If there are no fixed sessions, charge only PAYG.

**Practice rounding rule:** preserve exact prorated fees and allowances, including
fractional tokens. Subtract the exact allowance before flooring excess to complete
100-token blocks. Add PAYG charges, the prorated fee, and fixed overage charges;
round the final bill once to the nearest cent, with exact half cents rounded up.

```python
sessions = [
    "userA,100,100,payg", "userA,100,100,payg",
    "userA,20000,10000,fixed", "userA,100,100,fixed",
    "userB,100,100,payg",
]
# ["userA: $7.71", "userB: $0.07"]
```

Implement `part1`, `part2`, and `part3` in `problems/p8_chat_billing/solution_p8.py`.
No fourth part or reference solution is included. Run `python practice.py p8` for
a timed session, or `python practice.py p8 --test` to grade your work.
