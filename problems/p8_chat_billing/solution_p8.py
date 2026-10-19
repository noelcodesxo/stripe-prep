"""
Problem 8 — Chat Token Billing. Full spec: ../../08_chat_billing.md

Each function takes CSV session strings: user_id,input_tokens,output_tokens,plan.
Return sorted "user_id: $xx.xx" lines, including zero bills; [] for empty input.
Aggregate tokens per user, plan, and direction before flooring 100-token blocks.
PAYG rates: 3 input / 4 output cents per block.
Fixed: $15 once, includes 40000 input / 20000 output tokens; same overage rates.
Part 3 prorates fixed fee and allowances by fixed_sessions / total_sessions.
Preserve exact fractions; floor blocks after allowance subtraction; round final
bill once to cents, half up. These are explicit practice conventions.

Manual run: python solution_p8.py 3 < sessions.txt
"""
from typing import List


def part1(sessions: List[str]) -> List[str]:
    # PAYG only.
    raise NotImplementedError


def part2(sessions: List[str]) -> List[str]:
    # PAYG or fixed; each user has one plan for the whole month.
    raise NotImplementedError


def part3(sessions: List[str]) -> List[str]:
    # Users may mix plans; prorate using each user's own session counts.
    raise NotImplementedError


if __name__ == "__main__":
    import sys
    part = sys.argv[1] if len(sys.argv) > 1 else "1"
    data = sys.stdin.read().splitlines()
    fn = {"1": part1, "2": part2, "3": part3}[part]
    print("\n".join(fn(data)))
