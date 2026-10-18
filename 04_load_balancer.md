# Problem 4 — Multi-Stage Load Balancer

*An original problem in the shape of Stripe's most frequently reported OA. Do not treat the wording as the real assessment.*

You are implementing a connection load balancer. This is an **object-oriented design** problem: the win is a single clean class that holds the shared state, with each stage adding a small, well-ordered rule on top. If you're rewriting Part 1 to do Part 3, stop and restructure.

Use one `Solution.solve(lines, part=...)` call over the full command stream. The part
argument enables the latest stage's commands, but it never switches to a separate
output mode. All `CONNECT` requests continue to share the same connection counts and
bindings, and every `CONNECT` continues to emit the same row format.

The input is a list of lines. The first line is always `SERVERS <n>`, declaring `n` servers indexed `0 .. n-1`. Every `CONNECT` produces exactly one output line; `DISCONNECT` produces none.

## Part 1 — Basic load balancing

Line type: `CONNECT <connectionId> <userId>`

Assign each new connection to the server with the **fewest active connections**. If several servers tie, pick the **smallest index**. Track a per-server active-connection count.

Output per CONNECT: `<connectionId>,<userId>,<targetIndex>` (0-indexed), format exact — no spaces.

```
Input:  SERVERS 3 / CONNECT c1 u1 / CONNECT c2 u2 / CONNECT c3 u3 / CONNECT c4 u4
Output: c1,u1,0 / c2,u2,1 / c3,u3,2 / c4,u4,0
```

## Part 2 — Disconnect

New line type: `DISCONNECT <connectionId>`

Free the connection: find which server it was on, decrement that server's count, and forget the mapping. An **unknown / already-freed connectionId is silently ignored** (no error, no output). A freed slot must be reusable by later CONNECTs.

You'll want a `connectionId -> serverIndex` map to support this.

## Part 3 — Sticky routing by objectId

Extended CONNECT: `CONNECT <connectionId> <userId> <objectId>` (a 4th token).

All requests sharing an `objectId` must always route to the **same server**, even if that server is currently more loaded than others. Order of logic is the whole problem:

1. If the `objectId` is already bound, reuse its server.
2. Otherwise apply the Part 1 least-loaded rule.
3. Record the `objectId -> server` binding.

The binding is **permanent** — it must survive a `DISCONNECT` of a connection that used it. (CONNECTs may still arrive without an objectId; those behave like Part 1.)

## Part 4 — Capacity limits

New config line: `CAPACITY <c>` — each server may hold at most `c` active connections.

On CONNECT, if the intended target would exceed capacity, **reject** the connection instead of placing it (count unchanged):

- Sticky target already at capacity → reject.
- Otherwise choose the least-loaded server **that is below capacity**; if every server is full → reject.

Output for a rejected connection: `<connectionId>,<userId>,REJECTED`.

## Traps to watch

- Index base — this variant is **0-indexed**; some real variants number from 1. Read the spec, keep it a parameter.
- Sticky is checked **before** load balancing, and the binding is permanent across disconnects.
- Unknown DISCONNECT is a no-op; never let a count go negative.
- Exact output format, including the literal `REJECTED`.
