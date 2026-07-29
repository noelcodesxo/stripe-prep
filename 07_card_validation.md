# Problem 7 — Payment Card Validation

*An original problem in the shape of a common Stripe "Luhn / card" OA. Original wording.*

Build two primitives first — `luhn_ok(num)` and `network(num)` — then every part sits on top of them.

**Networks**

- `VISA` — 16 digits, starts with `4`
- `MASTERCARD` — 16 digits, first two digits `51`–`55`
- `AMEX` — 15 digits, starts with `34` or `37`

**Luhn** — from the rightmost digit, double every 2nd digit; if a doubled value exceeds 9, subtract 9; sum everything; valid iff `sum % 10 == 0`.

Input is one card per line unless a part says otherwise.

## Part 1 — Visa checksum

Input cards are 16 digits starting with `4`. Output `VISA` if Luhn passes, else `INVALID_CHECKSUM`.

```
4532015112830366 -> VISA
4242424242424243 -> INVALID_CHECKSUM
```

## Part 2 — Multi-network

For any input number, output:

- the network name (`VISA` / `MASTERCARD` / `AMEX`) if a network matches **and** Luhn passes,
- `INVALID_CHECKSUM` if a network matches but Luhn fails,
- `UNKNOWN_NETWORK` if no network matches by length/prefix.

Check the network **before** the checksum.

## Part 3 — Redacted cards

Input is a **single line**: one card containing 1–5 `*` wildcards. Try every digit substitution for the wildcards. For each network that has at least one valid completion, output `<NETWORK>,<count>`, sorted **alphabetically by network**. If nothing is valid, output nothing.

```
453201511283036*  -> VISA,1
42424242424242**  -> VISA,10
```

## Part 4 — Corrupted cards

Input is a **single line**: a card ending with `?`, meaning **exactly one** error occurred — either one digit was changed, or two **adjacent** digits were swapped. Reconstruct every distinct card that is a valid network number, and output `<card>,<NETWORK>` sorted **numerically ascending**.

```
340000000000009?  ->  340000000000009,AMEX
                      340000000000090,AMEX
```

## Traps to watch

- Part 3 sorts **alphabetically**; Part 4 sorts **numerically**. Don't mix them.
- Part 4 must **dedupe** — a digit change and an adjacent swap can produce the same number.
- Prune: fix a candidate's length/prefix (network) before running Luhn.
- Watch lengths: only 15/16-digit numbers can match any network here.
