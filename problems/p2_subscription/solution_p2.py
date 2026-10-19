"""Problem 2 - Subscription Billing Engine.

All events and output requests belong to one billing timeline. Later parts add event
and request types; they do not select a different billing program.

Manual run against stdin:  python solution_p2.py 4 < input.txt
"""
from typing import List


class Solution:
    def solve(self, lines: List[str], part: int = 1) -> List[str]:
        """Collect one cumulative plan, event, and request stream."""
        if part not in (1, 2, 3, 4):
            raise ValueError(f"part must be between 1 and 4, got {part}")

        plans: dict[str, int] = {}
        events: list[tuple[int, str, tuple[str, ...]]] = []
        requests: list[tuple[str, tuple[str, ...]]] = []
        in_requests = False

        for line in lines:
            tokens = tuple(line.split())
            if not tokens:
                continue
            if tokens[0] == "PLAN":
                if in_requests:
                    raise ValueError("PLAN definitions must precede requests")
                plans[tokens[1]] = int(tokens[2])
                continue
            if tokens[0] == "QUERY":
                in_requests = True
                requests.append(("QUERY", (tokens[1],)))
                continue
            if tokens[0] == "INVOICE":
                if part < 4:
                    raise ValueError("INVOICE is available from part 4")
                in_requests = True
                requests.append(("INVOICE", (tokens[1], tokens[2], tokens[3])))
                continue

            if in_requests:
                raise ValueError("Dated events must precede QUERY/INVOICE requests")
            day = int(tokens[0])
            event_type = tokens[1]
            if event_type == "CHANGE" and part < 2:
                raise ValueError("CHANGE is available from part 2")
            if event_type == "REFUND" and part < 3:
                raise ValueError("REFUND is available from part 3")
            events.append((day, event_type, tokens[2:]))

        # Implement accrual, snapshots, refunds, and invoice-window proration here.
        # Keep them in one processor over `plans`, `events`, and `requests` so every
        # later feature extends the same customer timeline.
        raise NotImplementedError("Implement the cumulative subscription billing processor")


if __name__ == "__main__":
    import sys

    part = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    data = sys.stdin.read().splitlines()
    print("\n".join(Solution().solve(data, part)))
