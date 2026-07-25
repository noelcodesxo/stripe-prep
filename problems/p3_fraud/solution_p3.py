"""
Problem 3 - Streaming Transaction Fraud Detection.  Full spec: ../../03_transaction_fraud.md

Implement the four functions below. Transactions are given already sorted by
timestamp as:  <timestamp> <card_id> <amount_cents> <merchant> <status>
with status in {APPROVED, DECLINED}. Config lines precede the transactions.

CONFIG LINES
  VELOCITY <N> <W>       part 2: N+ approvals within any W-second window
  BURST <M> <T> <W>      part 3: M+ txns within any W-second window, avg amount < T
  TOPK <K>               part 4: number of riskiest cards to output

Manual run against stdin:  python solution_p3.py 4 < input.txt
"""
from typing import List


def part1(lines: List[str]) -> List[str]:
    # Per card, sorted: "<card> <approved_count> <total_approved_cents> <decline_rate>"
    # decline_rate = declined/total, formatted to 2 decimals (e.g. 0.33).
    raise NotImplementedError


def part2(lines: List[str]) -> List[str]:
    # Flag cards with N+ APPROVED txns in any W-second window. Sorted, else "NONE".
    raise NotImplementedError


def part3(lines: List[str]) -> List[str]:
    # Flag (card, merchant) pairs: M+ txns in any W-second window with avg amount < T.
    # Output "<card> <merchant>" sorted by card then merchant, else "NONE".
    raise NotImplementedError


def part4(lines: List[str]) -> List[str]:
    # Risk score per card: +5/decline, +10 if high-velocity (part 2),
    # +15 per distinct burst merchant (part 3), +1 per full 10000 approved cents.
    # Output top K as "<card> <score>", score desc then card asc.
    raise NotImplementedError


if __name__ == "__main__":
    import sys
    part = sys.argv[1] if len(sys.argv) > 1 else "1"
    data = sys.stdin.read().splitlines()
    fn = {"1": part1, "2": part2, "3": part3, "4": part4}[part]
    print("\n".join(fn(data)))
