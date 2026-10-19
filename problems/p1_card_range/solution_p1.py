"""Problem 1 - Card Range Registry. Full spec: ../../01_card_range_registry.md

`solve` is the single entry point. Ranges are followed by one `QUERIES` section;
later parts add request types to that section rather than replacing earlier ones.
The algorithms for GAPS and CANONICAL are intentionally left for the learner.

Manual run against stdin:  python solution_p1.py 2 < input.txt
"""
from typing import List


class Solution:
    def solve(self, lines: List[str], part: int = 1) -> List[str]:
        """Process lookups and (in later parts) additional registry requests."""
        if part not in (1, 2, 3, 4):
            raise ValueError(f"part must be between 1 and 4, got {part}")

        try:
            separator = lines.index("QUERIES")
        except ValueError:
            # A registry without requests is a valid empty request stream.
            return []

        ranges = lines[:separator]
        answers: List[str] = []
        for request in lines[separator + 1:]:
            if request == "GAPS":
                if part < 3:
                    raise ValueError("GAPS is available from part 3")
                raise NotImplementedError("Implement the cumulative coverage-gap report")
            if request == "CANONICAL":
                if part < 4:
                    raise ValueError("CANONICAL is available from part 4")
                raise NotImplementedError("Implement the cumulative canonical-range report")
            answers.append(self._lookup(ranges, request, part))
        return answers

    @staticmethod
    def _lookup(ranges: List[str], query: str, part: int) -> str:
        """Preserve the implemented lookup behavior for Parts 1 and 2."""
        cur_bank = "UNKNOWN"
        if part == 1:
            for r in ranges:
                lo, hi, bank = r.split(" ")
                if lo <= query <= hi:
                    cur_bank = bank
                    break
            return cur_bank

        cur_start = -1
        for r in ranges:
            lo, hi, bank = r.split(" ")
            if lo <= query <= hi:
                if int(lo) > cur_start:
                    cur_bank = bank
                    cur_start = int(lo)
        return cur_bank


if __name__ == "__main__":
    import sys

    part = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    data = sys.stdin.read().splitlines()
    print("\n".join(Solution().solve(data, part)))
