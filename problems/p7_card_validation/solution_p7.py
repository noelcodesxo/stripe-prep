"""
Problem 7 - Payment Card Validation.  Full spec: ../../07_card_validation.md

Luhn + network detection, then two brute-force layers (redacted, corrupted).
Get the two primitives rock-solid first: luhn_ok(num) and network(num).

Implement the Solution methods below. `solve` is the stable entry point for every
part: pass the input lines and the part number, then return the output lines.

NETWORKS
  VISA        16 digits, starts with 4
  MASTERCARD  16 digits, first two digits 51..55
  AMEX        15 digits, starts with 34 or 37

LUHN: from the rightmost digit, double every 2nd digit; if a doubled value > 9
      subtract 9; sum all; valid iff sum % 10 == 0.

PARTS (one input card per line unless noted)
  part 1: 16-digit numbers starting with 4. Output "VISA" or "INVALID_CHECKSUM".
  part 2: any number. Output the network if Luhn passes; "INVALID_CHECKSUM" if a
          network matches but Luhn fails; "UNKNOWN_NETWORK" if no network matches.
  part 3: ONE line, a card with '*' wildcards (1-5 of them). Try all digit fills;
          output "<NETWORK>,<count>" for each network with >=1 valid fill, sorted
          alphabetically by network. (No valid fills -> no output lines.)
  part 4: ONE line, a card ending with '?', meaning exactly one error occurred:
          one digit changed, OR two adjacent digits swapped. Output every distinct
          valid original as "<card>,<NETWORK>", sorted numerically ascending.

Manual run against stdin:  python solution_p7.py 2 < input.txt
"""
from typing import List


class Solution:
    def solve(self, lines: List[str], part: int = 1) -> List[str]:
        """Run one stage of the problem against a list of input lines."""
        if part not in (1, 2, 3, 4):
            raise ValueError(f"part must be between 1 and 4, got {part}")
        return getattr(self, f"_part{part}")(lines)

    def _part1(self, lines: List[str]) -> List[str]:
        # Visa-only Luhn check.
        raise NotImplementedError

    def _part2(self, lines: List[str]) -> List[str]:
        # Detect network first, THEN check Luhn.
        raise NotImplementedError

    def _part3(self, lines: List[str]) -> List[str]:
        # Redacted '*': count valids per network, alphabetical.
        raise NotImplementedError

    def _part4(self, lines: List[str]) -> List[str]:
        # Corrupted '?': one digit change OR one adjacent swap; dedup; numeric sort.
        raise NotImplementedError


if __name__ == "__main__":
    import sys

    part = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    data = sys.stdin.read().splitlines()
    print("\n".join(Solution().solve(data, part)))
