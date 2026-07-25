"""
Problem 2 - Subscription Billing Engine.  Full spec: ../../02_subscription_billing.md

Implement the four functions below. Each receives the input for that part as a
list of lines and returns a list of output lines. Time is whole-day integers;
charges accrue from the start day inclusive to the end day exclusive.

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


def part1(lines: List[str]) -> List[str]:
    # PLAN/SUBSCRIBE/CANCEL + one QUERY cutoff. Output "<cust> <cents>" per
    # customer that ever subscribed, sorted by customer.
    raise NotImplementedError


def part2(lines: List[str]) -> List[str]:
    # Adds CHANGE with proration (change day billed at the new rate).
    raise NotImplementedError


def part3(lines: List[str]) -> List[str]:
    # Adds re-subscription (intervals add up) and REFUND (subtract; may go negative).
    raise NotImplementedError


def part4(lines: List[str]) -> List[str]:
    # Output gross charges per INVOICE window (proration at edges), in input order.
    raise NotImplementedError


if __name__ == "__main__":
    import sys
    part = sys.argv[1] if len(sys.argv) > 1 else "1"
    data = sys.stdin.read().splitlines()
    fn = {"1": part1, "2": part2, "3": part3, "4": part4}[part]
    print("\n".join(fn(data)))
