"""
Problem 1 - Card Range Registry.  Full spec: ../../01_card_range_registry.md

Implement the four functions below. Each receives the input for that part as a
list of lines (trailing newlines already stripped) and returns a list of output
lines. The test suite calls these functions directly.

INPUT FORMATS
  part1 / part2:
      <low> <high> <bank>     one or more range lines
      QUERIES                 literal separator
      <prefix>                one or more integer query lines
  part3 / part4:
      <low> <high> <bank>     range lines only (no QUERIES section)

Manual run against stdin:  python solution_p1.py 2 < input.txt
"""
from operator import indexOf
from typing import List


def part1(lines: List[str]) -> List[str]:
    # Non-overlapping lookup. Output the owning bank per query, or "UNKNOWN".
    ranges, queries = lines[:lines.index('QUERIES')], lines[lines.index('QUERIES')+1:]
    ans = []
    for q in queries:
        cur_bank = 'UNKNOWN'
        for r in ranges:
            lo, hi, bank = r.split(' ')
            if lo <= q <= hi:
                cur_bank = bank
                break
        ans.append(cur_bank)
    return ans


def part2(lines: List[str]) -> List[str]:
    # Overlapping ranges allowed; the LATER range in input order wins on overlap.
    # first thing to do: set it up such that the ranges are set up with the ranges cleaned up
    ranges, queries = lines[:lines.index('QUERIES')], lines[lines.index('QUERIES')+1:]
    ans = []
    for q in queries:
        cur_bank = 'UNKNOWN'
        cur_start = -1
        for r in ranges:
            lo, hi, bank = r.split(' ')
            if lo <= q <= hi:
                if int(lo) > cur_start:
                    cur_bank = bank
                    cur_start = int(lo)
        ans.append(cur_bank)
    return ans


def part3(lines: List[str]) -> List[str]: 
    # Report coverage gaps within [min low, max high], ascending. "NONE" if none.
    
    raise NotImplementedError


def part4(lines: List[str]) -> List[str]:
    # Resolve overrides, then merge adjacent/overlapping ranges of the same bank.
    raise NotImplementedError


if __name__ == "__main__":
    import sys
    part = sys.argv[1] if len(sys.argv) > 1 else "1"
    data = sys.stdin.read().splitlines()
    fn = {"1": part1, "2": part2, "3": part3, "4": part4}[part]
    print("\n".join(fn(data)))
