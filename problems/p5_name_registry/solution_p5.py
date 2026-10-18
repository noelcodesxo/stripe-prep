"""
Problem 5 - Company Name Registry.  Full spec: ../../05_name_registry.md

Normalize a proposed company name, then check it against everything registered so
far. The core is a normalize(name) method plus a dict registry that maps
normalized_name -> owning account. Later parts extend BOTH: richer normalization,
and an owner-only "undo" (reclaim). Store the owner, not just a set, so reclaim can
authorize.

Implement the Solution methods below. `solve` is the stable entry point for every
part: pass the input lines and the part number, then return the output lines.

LINE TYPES
  <account_id>|<proposed_name>   a registration request  -> emits a result line
  RECLAIM|<account_id>|<name>    part 3+: owner frees a name  -> emits nothing
  WHOIS|<name>                   part 4:  lookup            -> emits owner or UNREGISTERED

NORMALIZATION
  part 1 (basic): case-insensitive; '&' and ',' become spaces; collapse runs of
                  spaces; trim. A name that normalizes to empty is never available.
  part 2+ (full): also drop company suffixes {inc., corp., llc, l.l.c., llc.},
                  drop a single leading article {the, an, a}, and drop the word
                  "and" everywhere EXCEPT as the first token.

OUTPUT
  registration -> "<account_id>|Name Available"  or  "<account_id>|Name Not Available"
                  (once available, the name is registered and taken thereafter)
  WHOIS        -> the owning account_id, or "UNREGISTERED"

Manual run against stdin:  python solution_p5.py 3 < input.txt
"""
from typing import List


class Solution:
    def solve(self, lines: List[str], part: int = 1) -> List[str]:
        """Run one stage of the problem against a list of input lines."""
        if part not in (1, 2, 3, 4):
            raise ValueError(f"part must be between 1 and 4, got {part}")
        return getattr(self, f"_part{part}")(lines)

    def _part1(self, lines: List[str]) -> List[str]:
        # Basic normalization + registry. Empty-after-normalization => Not Available.
        raise NotImplementedError

    def _part2(self, lines: List[str]) -> List[str]:
        # Full normalization (suffixes, leading article, non-leading "and").
        raise NotImplementedError

    def _part3(self, lines: List[str]) -> List[str]:
        # Adds RECLAIM (owner-only): remove the normalized name so it frees up again.
        raise NotImplementedError

    def _part4(self, lines: List[str]) -> List[str]:
        # Adds WHOIS lookups interleaved with registrations and reclaims.
        raise NotImplementedError


if __name__ == "__main__":
    import sys

    part = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    data = sys.stdin.read().splitlines()
    print("\n".join(Solution().solve(data, part)))
