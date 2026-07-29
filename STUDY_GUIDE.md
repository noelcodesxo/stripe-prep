# Stripe HackerRank OA — Study Plan & Pattern Guide (Python)

*Prep doc for a 60-minute, single-problem-in-4-parts assessment.*

> **How this maps to the practice repo.** The seven problems in `problems/` are
> concrete drills for the patterns below: name registry (P5) → §3A/B, card range
> (P1) & card validation (P7) → §3C/G, subscription (P2) → §3F, fraud (P3) → the
> grouped-threshold pattern, store closing (P6) → §3D/E, load balancer (P4) → §8.
> Read a problem's `.md`, solve its stub cold, run its tests. Use `practice.py` to
> time yourself.

---

## 1. What this OA actually tests (read this first)

These are **implementation / simulation** problems, not classic LeetCode algorithm puzzles. The hard part is almost never "find the clever algorithm." The hard parts are:

1. **Reading comprehension** — the prompts are long and full of business rules. Half your mistakes will come from misreading a rule, not from bad code.
2. **Translating messy rules into clean state** — normalization rules, thresholds, event timelines.
3. **Edge cases** — empty inputs, ties, inclusive vs. exclusive endpoints, ordering.
4. **Exact output formatting** — separators, sort order, trailing characters. This is the #1 *silent* failure: your logic is right but the string doesn't match, so the test says "wrong answer."

The data-structure toolkit you actually need is small: **hash maps/sets, sorting, prefix sums, interval merging, and a bit of brute force.** No graphs, no DP, no segment trees. If you find yourself reaching for something fancy, re-read the prompt — you've probably overcomplicated it.

---

## 2. The meta-strategy for progressive parts

Every one of these problems is **one scenario revealed in 4 escalating parts**, where each part reuses the previous part's code. This structure rewards a specific way of working:

**Design Part 1 to be extended, not just to pass.**
- Put the core logic in **small, named functions** (`normalize(name)`, `compute_penalty(log, t)`, `luhn_ok(num)`), not one giant `main`.
- Keep your **state explicit** — a dict/set/class you can inspect and *mutate* later. Part 3 almost always adds "undo" (reclaim a name, dispute a charge, dissolve a company), so store enough information to reverse an action, not just the final answer.
- Use a **line dispatcher** for input. Later parts add new line types (`RECLAIM,...`, `DISPUTE,...`, `BEGIN...END`). If Part 1 already routes each line by its prefix, adding a case is a two-line change.

**Time budget (60 min, guideline):**
- **~15 min:** read the *whole* problem if all parts are visible, and get Part 1 rock-solid. Part 1 gates everything — a bug here cascades.
- **~15 min:** Part 2 (usually a variation: percentage instead of count, plan changes).
- **~20 min:** Part 3 / Part 4 (the "undo" or "brute force" twist — the meaty part).
- **~10 min:** buffer for edge cases and output-format fixes.

**Work test-first.** HackerRank gives you sample input/output. Before submitting, run the sample locally and **diff your output character-for-character**. Watch for trailing spaces, empty trailing lines, `,` vs `, `, and sort order.

**When stuck on a part, lock in the earlier parts.** Partial credit is real. A clean Part 1+2 beats a broken attempt at all four.

---

## 3. The recurring pattern toolkit

These few patterns cover all six problems. Get fast at each in Python.

### A. Normalization & tokenization (Problem 1)
Reduce a messy string to a canonical form, then compare canonical forms.
```python
def normalize(name: str) -> str:
    s = name.lower()
    for ch in "&,":
        s = s.replace(ch, " ")
    tokens = s.split()                      # collapses runs of whitespace
    suffixes = {"inc.", "corp.", "llc", "l.l.c.", "llc."}
    tokens = [t for t in tokens if t not in suffixes]
    if tokens and tokens[0] in {"the", "an", "a"}:
        tokens = tokens[1:]
    # drop "and" unless it's the first token
    tokens = [t for i, t in enumerate(tokens) if not (t == "and" and i > 0)]
    return " ".join(tokens)                 # "" => treat as unavailable
```
> Trap: apply the "leading The/A/An" and "leading And" rules **in the right order** and only at the *start*. Decide whether suffix-stripping happens before or after — read the examples and make canonical output match them.

### B. Hash set as a registry with undo (Problems 1, 3)
```python
registered = {}                 # normalized_name -> owner_account
def register(acct, name):
    key = normalize(name)
    if not key or key in registered:
        return "Name Not Available"
    registered[key] = acct
    return "Name Available"

def reclaim(acct, original_name):
    key = normalize(original_name)
    if registered.get(key) == acct:     # only the owner may reclaim
        del registered[key]
```

### C. Interval sorting + gap filling (Problem 2)
```python
def fill(bin_str, intervals, lo=0, hi=9_999_999_999):
    intervals.sort(key=lambda x: x[0])          # (start, end, brand)
    out, cursor = [], lo
    for s, e, brand in intervals:
        if s > cursor:                          # gap before this interval
            out.append((cursor, s - 1, <fill_brand>))
        out.append((s, e, brand))
        cursor = e + 1
    if cursor <= hi:                            # trailing gap
        out.append((cursor, hi, <fill_brand>))
    bin_int = int(bin_str)
    return [(bin_int * 10**10 + s, bin_int * 10**10 + e, b) for s, e, b in out]
```
> Traps: endpoints are **inclusive** (use `s - 1` and `e + 1`, not `s`/`e`). Read how a gap should be labeled — extend the previous interval's brand, the next one's, or a sentinel. Format the output as full **16-digit** numbers (BIN + zero-padded 10-digit offset).

### D. Prefix sums for O(1) range counts (Problem 4)
The penalty for a closing time is "empties before close" + "customers after close." Precompute cumulative customer counts so every candidate close time is O(1), and the whole day is O(n).
```python
def best_closing_time(log: str) -> int:
    hours = log.split()
    n = len(hours)
    # penalty(t) = (# 'N' in hours[:t]) + (# 'Y' in hours[t:])
    prefix_N = [0] * (n + 1)
    total_Y = 0
    for i, h in enumerate(hours):
        prefix_N[i + 1] = prefix_N[i] + (h == "N")
        total_Y += (h == "Y")
    best_t, best_pen = 0, None
    suffix_Y = total_Y
    for t in range(n + 1):
        if t > 0 and hours[t - 1] == "Y":
            suffix_Y -= 1                    # customers now to the right of t
        pen = prefix_N[t] + suffix_Y
        if best_pen is None or pen < best_pen:   # strict < => smallest t wins ties
            best_pen, best_t = pen, t
    return best_t
```
> Trap: ties must return the **smallest** closing time — use strict `<` when scanning ascending.

### E. State-machine parsing (Problem 4, Part 3)
Extract `BEGIN ... END` logs from noisy text; no nesting, ignore unfinished/garbage.
```python
def extract_logs(text):
    tokens = text.split()
    logs, cur, inside = [], [], False
    for tok in tokens:
        if tok == "BEGIN":
            cur, inside = [], True           # a new BEGIN restarts; no nesting
        elif tok == "END":
            if inside:
                logs.append(" ".join(cur))
                inside = False
        elif inside and tok in ("Y", "N"):
            cur.append(tok)
        # else: garbage -> ignore
    return logs                              # unfinished (no END) is dropped
```

### F. Event simulation sorted by day (Problem 5)
Emit `(day, type, payload)` events, then sort. Use a **tuple sort key** that encodes tie-breaks so same-day events come out in the required order.
```python
events = []
events.append((start_day, "start", name, plan))
for offset in negative_offsets:              # e.g. -15 => 15 days before end
    events.append((end_day + offset, "reminder", name, plan))
events.append((end_day, "end", name, plan))
events.sort(key=lambda e: (e[0], type_rank[e[1]]))
```
> When a plan **changes** or **renews**, recompute `end_day` and **regenerate** that user's future events from the change date forward — don't try to patch individual emails.

### G. Brute force with validation & pruning (Problem 6)
Luhn is the validator; redacted (`*`) and corrupted (`?`) cards are generate-and-test.
```python
def luhn_ok(num: str) -> bool:
    total, dbl = 0, False
    for ch in reversed(num):
        d = int(ch)
        if dbl:
            d *= 2
            if d > 9: d -= 9
        total += d
        dbl = not dbl
    return total % 10 == 0

def network(num: str):
    if len(num) == 16 and num[0] == "4":                       return "VISA"
    if len(num) == 16 and 51 <= int(num[:2]) <= 55:            return "MASTERCARD"
    if len(num) == 15 and num[:2] in ("34", "37"):            return "AMEX"
    return None
```
For `*` redaction: `itertools.product("0123456789", repeat=k)` over the star positions, count valid-by-network. For `?` corruption: generate every single-digit change and every adjacent swap, keep the ones that are valid, dedup, sort numerically.

---

## 4. Per-problem strategy

### Problem 1 — Atlas Company Name Check *(string normalization + registry with undo)*
- **Core:** `normalize()` (pattern A) + a `dict` registry (pattern B).
- **Part 1:** normalize, check against registered set, register on success. Empty-after-normalization ⇒ Not Available.
- **Part 2:** just *don't reset* the registry between requests — persistent across all lines. (If your Part 1 already keeps one dict, Part 2 is nearly free.)
- **Part 3:** add `RECLAIM,account_id,name` handling — remove the normalized key, but **only if the requesting account is the owner.** This is why the registry stores `name -> owner`, not just a set.
- **Watch:** rule ordering in normalization; case-insensitivity everywhere; output is `account_id|Name Available` / `account_id|Name Not Available`.

### Problem 2 — Card Range Obfuscation *(interval gap-filling)*
- **Core:** sort by start, sweep, fill gaps at front/middle/end (pattern C).
- **Watch:** inclusive endpoints (off-by-one is the whole problem); zero-pad offsets to 10 digits; emit full 16-digit numbers; decide the fill brand per the spec/examples; the full range is offset `0` … `9999999999`.

### Problem 3 — Fraud Detection *(grouped counting + thresholds + undo)*
- **Core:** group charges by `account_id`, track total and fraudulent counts; classify fraud codes via a set.
- **Part 1 (count):** mark merchant fraudulent once `fraud_count` exceeds the MCC threshold, but **only after** the minimum total-transactions gate.
- **Part 2 (percentage):** same, but compare `fraud_count / total >= mcc_fraction`. Note: **"stays fraudulent even if the percentage later drops"** — once flagged, latch it (until Part 3 disputes change that).
- **Part 3 (disputes):** `DISPUTE,charge_id` makes that charge count as non-fraudulent everywhere. Recompute — a merchant flagged *only* because of disputed charges can drop back to clean. Store per-charge fraud status so a dispute can flip one charge and you re-evaluate.
- **Watch:** output is a **lexicographically sorted, comma-separated** list of account_ids; the min-transactions gate; latching vs. re-evaluation semantics differ across parts — read carefully.

### Problem 4 — Store Closing Time Penalty *(prefix sums + state-machine parsing)*
- **Part 1:** `compute_penalty(log, t)` — empties in `[:t]` + customers in `[t:]`.
- **Part 2:** `find_best_closing_time` — scan all `t` in `0..n`, smallest `t` wins ties (pattern D; do it in O(n), not O(n²)).
- **Part 3:** parse many logs from noisy text with a `BEGIN...END` state machine (pattern E), run Part 2 on each, return the list.
- **Watch:** closing time ranges `0..n` inclusive (n+1 candidates); ties → smallest; unfinished logs and nested `BEGIN` are dropped/reset.

### Problem 5 — Subscription Notification Scheduler *(event simulation)*
- **Core:** build events, sort by `(day, type_priority)` (pattern F).
- **Part 1:** `start` on start day, negative offsets before end, `end` on end day.
- **Part 2 (plan change):** emit `[Changed]` on the change date, recompute remaining duration from the change date under the new plan, regenerate future events.
- **Part 3 (renewal):** `[Renewed]` on renewal date, extend end date by N days, reschedule.
- **Watch:** output ordering when multiple events share a day; recompute end dates rather than editing individual emails; format `"<day>: [<Type>] Subscription for <name> (<plan>)"` exactly.

### Problem 6 — Card Validation *(Luhn + brute force with pruning)*
- **Part 1:** Visa-only Luhn (pattern G): `VISA` or `INVALID_CHECKSUM`.
- **Part 2:** detect VISA/MASTERCARD/AMEX by length+prefix; `UNKNOWN_NETWORK` if nothing matches, `INVALID_CHECKSUM` if network matches but Luhn fails. Check network **before** checksum.
- **Part 3 (redacted `*`, 1–5 digits):** enumerate digit combos over star positions, count valids **per network**, output sorted alphabetically by network (`NETWORK,count`).
- **Part 4 (corrupted `?`):** exactly one error — one digit changed OR two adjacent digits swapped. Generate all candidates, keep valid ones, dedup, output `card,NETWORK` sorted **numerically ascending**.
- **Watch:** Part 3 sorts **alphabetically by network**, Part 4 sorts **numerically**; dedup candidates in Part 4 (a change and a swap can produce the same number); prune early (fix the network's length/prefix before Luhn).

---

## 5. Universal edge-case checklist (run through this before submitting each part)

- **Empty / whitespace-only input** → does it produce the "unavailable"/"skip" branch, not a crash?
- **Case sensitivity** — normalized consistently everywhere?
- **Duplicates / re-submissions** — handled per the "persistent" rule?
- **Ties** — returning the *smallest* / *lexicographically first* as specified?
- **Inclusive vs. exclusive endpoints** — the classic off-by-one in interval and range problems.
- **Number formatting** — zero-padding, fixed widths (10-digit offset, 16-digit card)?
- **Sort order** — lexicographic vs. numeric, ascending vs. by-network? (These differ *within* Problem 6.)
- **Undo/reversal** (reclaim, dispute) — did you keep enough state to reverse cleanly?
- **Output separators & trailing characters** — `|`, `,`, `, `, no stray trailing newline/space?
- **Ordering gate** — min-transaction thresholds, "only evaluate after N."
- **Latching semantics** — "stays fraudulent even if it later drops" vs. "can return to clean after dispute."

---

## 6. A concrete prep schedule

Adapt to how many days you have. If it's short, do Day 1 and Day 3.

**Day 1 — Pattern fluency (the highest-ROI day).**
Implement each toolkit snippet in §3 from scratch, from memory, timing yourself. Target: Luhn in <3 min, prefix-sum penalty in <8 min, a normalization function in <8 min, interval fill in <10 min. These *are* the building blocks; speed here is what buys you time for edge cases.

**Day 2 — Full run-throughs.**
Solve Problems 1, 4, and 6 end-to-end (all parts), self-timed at ~50 min each. These three cover the widest spread of patterns (registry+undo, prefix-sum+parsing, brute-force+validation). Diff against the sample outputs character-for-character.

**Day 3 — Simulation + the twist parts.**
Solve Problems 2, 3, 5. Focus specifically on the Part-3/Part-4 "twist" (disputes, reclamation, renewals, corruption) — that's where the difficulty and the differentiation live. Practice the *"design Part 1 so Part 3 is easy"* habit.

**Day before — Warm, don't cram.**
Re-derive the toolkit snippets once. Re-read §2 (time budget) and §5 (edge cases). Set up your local scratch environment exactly like test day: a `main.py` reading from stdin, a way to paste sample input, and a diff habit.

**Test-day habits.**
Read all visible parts first. Write the parser/dispatcher and core function before wiring output. Run the sample, diff it, *then* submit. Lock in earlier parts before gambling on the last one.

---

## 7. Two honest reminders

- **Match output format exactly.** More correct solutions fail on formatting than on logic. Build the diff-the-sample habit now so it's automatic under time pressure.
- **The OA is a gate, not the finish line.** Stripe's later rounds are live, integration-heavy, and involve extending real code with an interviewer watching — the same "read the rules, extend clean state, handle edge cases" muscle. Prep that makes you genuinely fast here is exactly what carries you through those. That's the version of "an edge" that actually holds up.

Good luck — you've got a very learnable target here.

---

## 8. Bonus high-frequency problem: Multi-Stage Load Balancer (OOD)

This one shows up **very** often and is worth a dedicated dry-run, because it's a different flavor from the six above: less string-parsing, more **object-oriented design**. Stripe grades this on clean class structure and correct rule ordering, not on any clever algorithm.

### The stages
- **Part 1 — Basic load balancing.** On `CONNECT`, route to the server with the **fewest active connections**; ties → **smallest index**. Maintain a per-server count array. Output `connectionId,userId,targetIndex`.
- **Part 2 — Disconnect.** On `DISCONNECT`, look up which server the connection is on, decrement that server's count, and drop the mapping. **Invalid/unknown connection IDs are silently ignored** (no error).
- **Part 3 — Sticky routing by objectId.** Requests sharing an `objectId` must **always** hit the same server — even if it's more loaded. Order matters: check the binding *first*, fall back to load balancing only if unbound, then record the binding.

### Why OOD helps here
Model it as one class holding three pieces of state. Every stage is then a small method that touches that state — Part 2 and Part 3 become additive, not rewrites. This is the "design Part 1 to be extended" principle in its purest form.

```python
class LoadBalancer:
    def __init__(self, num_servers, index_base=0):
        self.counts = [0] * num_servers      # active connections per server
        self.index_base = index_base         # 0 or 1 — set from the spec!
        self.conn_to_server = {}             # connectionId -> server (0-based)
        self.object_to_server = {}           # objectId  -> server (sticky, permanent)

    def _least_loaded(self):
        best = 0                             # ties resolve to smallest index
        for i in range(1, len(self.counts)):
            if self.counts[i] < self.counts[best]:
                best = i
        return best

    def connect(self, connection_id, user_id, object_id=None):
        # Part 3: sticky binding takes priority over load balancing
        if object_id is not None and object_id in self.object_to_server:
            server = self.object_to_server[object_id]
        else:
            server = self._least_loaded()            # Part 1 rule
            if object_id is not None:
                self.object_to_server[object_id] = server   # record binding
        self.counts[server] += 1
        self.conn_to_server[connection_id] = server
        return f"{connection_id},{user_id},{server + self.index_base}"

    def disconnect(self, connection_id):             # Part 2
        server = self.conn_to_server.pop(connection_id, None)
        if server is None:
            return                                   # unknown id -> ignore
        self.counts[server] -= 1
        # NOTE: keep the objectId binding — it's permanent even after disconnect
```

### The pitfalls that actually fail submissions
- **Index base.** Some variants number servers from **1**, not 0. Don't hardcode — keep an `index_base` and set it from the prompt. Getting this wrong fails *every* line while your logic is perfect.
- **Sticky > load balancing.** Check the `objectId` binding **before** applying the least-loaded rule, not after.
- **Binding is permanent.** A `DISCONNECT` decrements the count but must **not** erase the `objectId → server` binding — a later request with that objectId still goes to the same server.
- **Disconnect must not corrupt state.** Unknown IDs are no-ops; never let one raise or push a count negative.
- **Exact output format.** `connectionId,userId,targetIndex`, no spaces, no trailing characters.

### Complexity note (mention it if asked, don't over-engineer)
The `_least_loaded` scan is O(number of servers) per connect. For OA scale that's fine and maximally clear — prefer it. Only if a later stage demands high throughput would you swap in a min-heap or a "buckets by connection-count" structure; flag the tradeoff rather than reaching for it preemptively, since clarity is what's being graded.

### Practice reps for this one
Rebuild the class from an empty file in under 20 minutes, then test: equal-load routing (ties go to index 0/1), repeated `objectId` (always same server even when overloaded), invalid `DISCONNECT` (ignored), and a sticky connection that disconnects then reconnects (same server). If you can do that cold, this problem is a free pass.
