"""
Problem 3 - Streaming Transaction Fraud Detection.  Full spec: ../../03_transaction_fraud.md

Implement the Solution methods below. `solve` is the stable entry point for every
part: pass the input lines and the part number, then return the output lines.
Transactions are given already sorted by timestamp as:
  <timestamp> <card_id> <amount_cents> <merchant> <status>
with status in {APPROVED, DECLINED}. Config lines precede the transactions.

CONFIG LINES
  VELOCITY <N> <W>       part 2: N+ approvals within any W-second window
  BURST <M> <T> <W>      part 3: M+ txns within any W-second window, avg amount < T
  TOPK <K>               part 4: number of riskiest cards to output

Manual run against stdin:  python solution_p3.py 4 < input.txt
"""
from typing import List


class Solution:
    def solve(self, lines: List[str], part: int = 1) -> List[str]:
        """Run one stage of the problem against a list of input lines."""
        if part not in (1, 2, 3, 4):
            raise ValueError(f"part must be between 1 and 4, got {part}")
        return getattr(self, f"_part{part}")(lines)

    @staticmethod
    def _parse_transactions(lines: List[str]) -> dict[str, list[int, int, str, str]]:
        cards_transactions: dict[str, list[int, int, str, str]] = {}
        for line in lines:
            tokens = line.split(" ")
            timestamp = int(tokens[0])
            card = tokens[1]
            amount = int(tokens[2])
            merchant = tokens[3]
            status = tokens[4]
            cards_transactions.setdefault(card, []).append((amount, timestamp, merchant, status))
        return cards_transactions

    def _part1(self, lines: List[str]) -> List[str]:
        # Per card, sorted: "<card> <approved_count> <total_approved_cents> <decline_rate>"
        # decline_rate = declined/total, formatted to 2 decimals (e.g. 0.33).
        cards_transactions = self._parse_transactions(lines)
        # scores: dir[str, str] = {}
        # high_velocity_cards = set()

        def calculate_declined_rate():
            res = []
            for card, transactions in cards_transactions.items():
                approved_count = 0
                total_approved = 0
                decline_count = 0
                for transaction in transactions:
                    if transaction[3] == "APPROVED":
                        approved_count += 1
                        total_approved += transaction[0]
                    if transaction[3] != "APPROVED":
                        decline_count += 1

                res.append("{} {} {} {:.2f}".format(card, approved_count, total_approved, (decline_count / len(transactions))))
            return res

        print(cards_transactions)
        res = sorted(calculate_declined_rate(), key=lambda row: (row.split()[0]))

        return res

    def _part2(self, lines: List[str]) -> List[str]:
        # Flag cards with N+ APPROVED txns in any W-second window. Sorted, else "NONE".
        raise NotImplementedError

    def _part3(self, lines: List[str]) -> List[str]:
        # Flag (card, merchant) pairs: M+ txns in any W-second window with avg amount < T.
        # Output "<card> <merchant>" sorted by card then merchant, else "NONE".
        raise NotImplementedError

    def _part4(self, lines: List[str]) -> List[str]:
        # Risk score per card: +5/decline, +10 if high-velocity (part 2),
        # +15 per distinct burst merchant (part 3), +1 per full 10000 approved cents.
        # Output top K as "<card> <score>", score desc then card asc.
        raise NotImplementedError


if __name__ == "__main__":
    import sys

    part = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    data = sys.stdin.read().splitlines()
    print("\n".join(Solution().solve(data, part)))
