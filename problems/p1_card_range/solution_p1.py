"""
Problem 1 - Card Range Registry.  Full spec: ../../01_card_range_registry.md

Implement the Solution methods below. `solve` is the stable entry point for every
part: pass the input lines and the part number, then return the output lines.

INPUT FORMATS
  part1 / part2:
      <low> <high> <bank>     one or more range lines
      QUERIES                 literal separator
      <prefix>                one or more integer query lines
  part3 / part4:
      <low> <high> <bank>     range lines only (no QUERIES section)

Manual run against stdin:  python solution_p1.py 2 < input.txt
"""
from typing import List


class Solution:
    def solve(self, lines: List[str], part: int = 1) -> List[str]:
        """Run one stage of the problem against a list of input lines."""
        if part not in (1, 2, 3, 4):
            raise ValueError(f"part must be between 1 and 4, got {part}")
        return getattr(self, f"_part{part}")(lines)

    @staticmethod
    def _parse_ranges_and_queries(lines: List[str]):
        separator = lines.index('QUERIES')
        return lines[:separator], lines[separator + 1:]

    def _part1(self, lines: List[str]) -> List[str]:
        # Non-overlapping lookup. Output the owning bank per query, or "UNKNOWN".
        ranges, queries = self._parse_ranges_and_queries(lines)
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

    def _part2(self, lines: List[str]) -> List[str]:
        # Overlapping ranges allowed; the LATER range in input order wins on overlap.
        # first thing to do: set it up such that the ranges are set up with the ranges cleaned up
        ranges, queries = self._parse_ranges_and_queries(lines)
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

    def _part3(self, lines: List[str]) -> List[str]:
        # Report coverage gaps within [min low, max high], ascending. "NONE" if none.
        raise NotImplementedError

    def _part4(self, lines: List[str]) -> List[str]:
        # Resolve overrides, then merge adjacent/overlapping ranges of the same bank.
        raise NotImplementedError


if __name__ == "__main__":
    import sys

    part = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    data = sys.stdin.read().splitlines()
    print("\n".join(Solution().solve(data, part)))
