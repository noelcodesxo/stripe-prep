"""
Problem 5 - Company Name Registry.  Full spec: ../../05_name_registry.md

Normalize a proposed company name, then check it against everything registered so
far. The core is a normalize(name) function plus a dict registry that maps
normalized_name -> owning account. Later parts extend BOTH: richer normalization,
and an owner-only "undo" (reclaim). Store the owner, not just a set, so reclaim can
authorize.

Each function receives the input for that part as a list of lines and returns a
list of output lines. Not every line produces output (see below).

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


def part1(lines: List[str]) -> List[str]:
    # Basic normalization + registry. Empty-after-normalization => Not Available.
    raise NotImplementedError


def part2(lines: List[str]) -> List[str]:
    # Full normalization (suffixes, leading article, non-leading "and").
    raise NotImplementedError


def part3(lines: List[str]) -> List[str]:
    # Adds RECLAIM (owner-only): remove the normalized name so it frees up again.
    raise NotImplementedError


def part4(lines: List[str]) -> List[str]:
    # Adds WHOIS lookups interleaved with registrations and reclaims.
    raise NotImplementedError


if __name__ == "__main__":
    import sys
    part = sys.argv[1] if len(sys.argv) > 1 else "1"
    data = sys.stdin.read().splitlines()
    fn = {"1": part1, "2": part2, "3": part3, "4": part4}[part]
    print("\n".join(fn(data)))
