"""
Problem 7 - Payment Card Validation.  Full spec: ../../07_card_validation.md

Luhn + network detection, then two brute-force layers (redacted, corrupted).
Get the two primitives rock-solid first: luhn_ok(num) and network(num); every part
is built on them.

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
          one digit changed, OR two ADJACENT digits swapped. Output every distinct
          valid original as "<card>,<NETWORK>", sorted numerically ascending.

Manual run against stdin:  python solution_p7.py 2 < input.txt
"""
from typing import List


def part1(lines: List[str]) -> List[str]:
    # Visa-only Luhn check.
    raise NotImplementedError


def part2(lines: List[str]) -> List[str]:
    # Detect network first, THEN check Luhn.
    raise NotImplementedError


def part3(lines: List[str]) -> List[str]:
    # Redacted '*': count valids per network, alphabetical.
    raise NotImplementedError


def part4(lines: List[str]) -> List[str]:
    # Corrupted '?': one digit change OR one adjacent swap; dedup; numeric sort.
    raise NotImplementedError


if __name__ == "__main__":
    import sys
    part = sys.argv[1] if len(sys.argv) > 1 else "1"
    data = sys.stdin.read().splitlines()
    fn = {"1": part1, "2": part2, "3": part3, "4": part4}[part]
    print("\n".join(fn(data)))
