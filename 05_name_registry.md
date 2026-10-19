# Problem 5 — Company Name Registry

*An original problem in the shape of Stripe's "Atlas name check" OA. Original wording.*

Founders register company names. To avoid confusion, a name is unavailable if it **normalizes** to the same thing as an already-registered name. The core is one `normalize(name)` function plus a registry `dict` mapping `normalized_name -> owning account`. Store the owner (not just a set) — Part 3 needs it to authorize reclaims.

Input is one list of interleaved lines processed by `Solution.solve(lines, part=...)`.
A registration line is `<account_id>|<proposed_name>` and emits one result. Later
parts add commands to the same registry stream; registration output remains unchanged
and every line is handled in order.

In the examples below, pass the input as a list of strings to
`Solution().solve(lines, part=...)`, using the part number shown. Return the
expected output as a list of strings, one string per displayed line, without
labels or extra blank lines. Each example is a separate call with fresh state.

## Part 1 — Basic normalization

Normalize with these rules:

- Case-insensitive (`Llama` == `LLAMA`).
- `&` and `,` become spaces.
- Collapse consecutive spaces to one; trim ends.
- A name that normalizes to **empty / all spaces** is never available.

For each `<account_id>|<name>`, output `<account_id>|Name Available` or `<account_id>|Name Not Available`. Once available, the name is registered and taken for all later requests.

**Example input**

```text
acct1|Llama, Inc.
acct2|LLAMA  Inc.
acct3|
acct4|Llama Inc
```

**Expected output**

```text
acct1|Name Available
acct2|Name Not Available
acct3|Name Not Available
acct4|Name Available
```

An empty name is unavailable. The period remains significant in Part 1, so `Llama Inc` is distinct from `Llama, Inc.`.

## Part 2 — Full normalization

Extend `normalize` with, applied consistently:

- Drop standard company suffixes (case-insensitive): `Inc.`, `Corp.`, `LLC`, `L.L.C.`, `LLC.`
- Drop a single **leading** article: `The`, `An`, or `A`.
- Drop the word `And` **everywhere except** as the first token (`Llama And Friend` == `Llama Friend`, but `And Llama Friend` stays distinct).

**Example input**

```text
a1|The Llama, Inc.
a2|Llama LLC
a3|Llama And Friend
a4|Llama Friend
```

**Expected output**

```text
a1|Name Available
a2|Name Not Available
a3|Name Available
a4|Name Not Available
```

Suffixes and the leading article collapse the first two names to `llama`; removing the internal `And` makes the last two names match.

## Part 3 — Reclamation

New line: `RECLAIM|<account_id>|<name>` — a dissolved company frees its name. Remove the normalized name from the registry **only if the requesting account is the one that registered it**. Reclaim lines emit no output. After a successful reclaim the name is available again.

**Example input**

```text
a1|Llama Inc.
RECLAIM|a2|Llama Inc.
a2|Llama
```

**Expected output**

```text
a1|Name Available
a2|Name Not Available
```

Account `a2` cannot reclaim a name owned by `a1`. The reclaim emits no row, and the next registration is denied.

## Part 4 — WHOIS lookups

New line: `WHOIS|<name>` — output the `account_id` that currently owns the normalized name, or `UNREGISTERED`. WHOIS, registrations, and reclaims are interleaved; process in order. A WHOIS after a successful reclaim observes the freed name; a later registration may take it.

**Example input**

```text
a1|Llama Inc.
WHOIS|the llama
WHOIS|Acme
RECLAIM|a1|Llama Inc.
WHOIS|Llama
a2|Llama
WHOIS|Llama
```

**Expected output**

```text
a1|Name Available
a1
UNREGISTERED
UNREGISTERED
a2|Name Available
a2
```

Reclaim emits no row. WHOIS observes the freed name, then the new owner after re-registration.

## Traps to watch

- Apply the leading-article and leading-`and` rules only at the **start**, after tokenizing.
- Reclaim must check ownership; a non-owner reclaim is a silent no-op.
- Keep normalization identical across registration, reclaim, and whois — one function, used everywhere.
