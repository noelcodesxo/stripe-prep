"""Problem 3 - Streaming Transaction Fraud Detection.

`solve` builds one per-card transaction history. Later parts add columns to the
Part 1 report using that same history; those added analyses are learner TODOs.
Config lines precede the timestamp-sorted transactions:
  VELOCITY <N> <W>
  BURST <M> <T> <W>
  TOPK <K>
The report begins `<card> <approved_count> <approved_cents> <decline_rate>`; later
parts append the velocity flag, burst merchants, and risk score.

Manual run against stdin:  python solution_p3.py 4 < input.txt
"""
from typing import List


class Solution:
    def solve(self, lines: List[str], part: int = 1) -> List[str]:
        """Aggregate the shared transaction stream and extend its report by part."""
        if part not in (1, 2, 3, 4):
            raise ValueError(f"part must be between 1 and 4, got {part}")

        config: dict[str, tuple[int, ...]] = {}
        transaction_lines: List[str] = []
        for line in lines:
            tokens = line.split(" ")
            if tokens[0] == "VELOCITY":
                config["VELOCITY"] = (int(tokens[1]), int(tokens[2]))
            elif tokens[0] == "BURST":
                config["BURST"] = (int(tokens[1]), int(tokens[2]), int(tokens[3]))
            elif tokens[0] == "TOPK":
                config["TOPK"] = (int(tokens[1]),)
            else:
                transaction_lines.append(line)

        cards_transactions = self._parse_transactions(transaction_lines)
        if part >= 2:
            required = ("VELOCITY",) if part == 2 else ("VELOCITY", "BURST")
            if part == 4:
                required += ("TOPK",)
            missing = [name for name in required if name not in config]
            if missing:
                raise ValueError("Missing config line(s): " + ", ".join(missing))
            # Keep the feature additions in one report flow. Implement the
            # high-velocity, burst, and ranking columns without replacing Part 1.
            self._base_rows(cards_transactions)
            raise NotImplementedError("Extend the per-card report with cumulative fraud fields")

        # Preserve the existing Part 1 debug output and row calculations exactly.
        print(cards_transactions)
        return self._base_rows(cards_transactions)

    @staticmethod
    def _parse_transactions(lines: List[str]) -> dict[str, list[tuple[int, int, str, str]]]:
        cards_transactions: dict[str, list[tuple[int, int, str, str]]] = {}
        for line in lines:
            tokens = line.split(" ")
            timestamp = int(tokens[0])
            card = tokens[1]
            amount = int(tokens[2])
            merchant = tokens[3]
            status = tokens[4]
            cards_transactions.setdefault(card, []).append((amount, timestamp, merchant, status))
        return cards_transactions

    @staticmethod
    def _base_rows(
        cards_transactions: dict[str, list[tuple[int, int, str, str]]]
    ) -> List[str]:
        """Return the unchanged Part 1 metric columns used by every later report."""
        rows = []
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
            rows.append(
                "{} {} {} {:.2f}".format(
                    card, approved_count, total_approved, decline_count / len(transactions)
                )
            )
        return sorted(rows, key=lambda row: row.split()[0])


if __name__ == "__main__":
    import sys

    part = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    data = sys.stdin.read().splitlines()
    print("\n".join(Solution().solve(data, part)))
