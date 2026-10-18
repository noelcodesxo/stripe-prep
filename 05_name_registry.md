# Problem 5 — Company Name Registry

*An original problem in the shape of Stripe's "Atlas name check" OA. Original wording.*

Founders register company names. To avoid confusion, a name is unavailable if it **normalizes** to the same thing as an already-registered name. The core is one `normalize(name)` function plus a registry `dict` mapping `normalized_name -> owning account`. Store the owner (not just a set) — Part 3 needs it to authorize reclaims.

Input is one list of interleaved lines processed by `Solution.solve(lines, part=...)`.
A registration line is `<account_id>|<proposed_name>` and emits one result. Later
parts add commands to the same registry stream; registration output remains unchanged
and every line is handled in order.

## Part 1 — Basic normalization

Normalize with these rules:

- Case-insensitive (`Llama` == `LLAMA`).
- `&` and `,` become spaces.
- Collapse consecutive spaces to one; trim ends.
- A name that normalizes to **empty / all spaces** is never available.

For each `<account_id>|<name>`, output `<account_id>|Name Available` or `<account_id>|Name Not Available`. Once available, the name is registered and taken for all later requests.

```
acct1|Llama, Inc.   -> acct1|Name Available      (normalized "llama inc.")
acct2|LLAMA  Inc.   -> acct2|Name Not Available   (same normalization)
acct3|              -> acct3|Name Not Available   (empty)
acct4|Llama Inc     -> acct4|Name Available        (no period -> "llama inc", distinct)
```

## Part 2 — Full normalization

Extend `normalize` with, applied consistently:

- Drop standard company suffixes (case-insensitive): `Inc.`, `Corp.`, `LLC`, `L.L.C.`, `LLC.`
- Drop a single **leading** article: `The`, `An`, or `A`.
- Drop the word `And` **everywhere except** as the first token (`Llama And Friend` == `Llama Friend`, but `And Llama Friend` stays distinct).

## Part 3 — Reclamation

New line: `RECLAIM|<account_id>|<name>` — a dissolved company frees its name. Remove the normalized name from the registry **only if the requesting account is the one that registered it**. Reclaim lines emit no output. After a successful reclaim the name is available again.

## Part 4 — WHOIS lookups

New line: `WHOIS|<name>` — output the `account_id` that currently owns the normalized name, or `UNREGISTERED`. WHOIS, registrations, and reclaims are interleaved; process in order. A WHOIS after a successful reclaim observes the freed name; a later registration may take it.

## Traps to watch

- Apply the leading-article and leading-`and` rules only at the **start**, after tokenizing.
- Reclaim must check ownership; a non-owner reclaim is a silent no-op.
- Keep normalization identical across registration, reclaim, and whois — one function, used everywhere.
