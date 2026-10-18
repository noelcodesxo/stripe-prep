"""
Problem 2 - Subscription Billing Engine.  Full spec: ../../02_subscription_billing.md

Implement the Solution methods below. `solve` is the stable entry point for every
part: pass the input lines and the part number, then return the output lines.
Time is whole-day integers; charges accrue from the start day inclusive to the end
day exclusive.

LINE TYPES
  PLAN <name> <daily_rate_cents>
  <day> SUBSCRIBE <customer> <plan>
  <day> CANCEL <customer>
  <day> CHANGE <customer> <new_plan>        (part 2+)
  <day> REFUND <customer> <cents>           (part 3+)
  QUERY <day>                               (parts 1-3: cutoff for totals)
  INVOICE <customer> <start_day> <end_day>  (part 4: half-open window)

Manual run against stdin:  python solution_p2.py 4 < input.txt
"""
from typing import List


class Solution:
    def solve(self, lines: List[str], part: int = 1) -> List[str]:
        """Run one stage of the problem against a list of input lines."""
        if part not in (1, 2, 3, 4):
            raise ValueError(f"part must be between 1 and 4, got {part}")
        return getattr(self, f"_part{part}")(lines)

    def _part1(self, lines: List[str]) -> List[str]:
        # PLAN/SUBSCRIBE/CANCEL + one QUERY cutoff. Output "<cust> <cents>" per
        # customer that ever subscribed, sorted by customer.
        raise NotImplementedError

    def _part2(self, lines: List[str]) -> List[str]:
        # Adds CHANGE with proration (change day billed at the new rate).
        raise NotImplementedError

    def _part3(self, lines: List[str]) -> List[str]:
        # Adds re-subscription (intervals add up) and REFUND (subtract; may go negative).
        raise NotImplementedError

    def _part4(self, lines: List[str]) -> List[str]:
        # Output gross charges per INVOICE window (proration at edges), in input order.
        raise NotImplementedError


if __name__ == "__main__":
    import sys

    part = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    data = sys.stdin.read().splitlines()
    print("\n".join(Solution().solve(data, part)))
