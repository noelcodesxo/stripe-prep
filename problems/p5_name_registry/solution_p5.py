"""Problem 5 - Company Name Registry.

Registrations, reclaims, and lookups share one registry for the whole input stream.
The normalization and registry operations are intentionally left for the learner.

Manual run against stdin:  python solution_p5.py 3 < input.txt
"""
from typing import List


class Solution:
    def solve(self, lines: List[str], part: int = 1) -> List[str]:
        """Process one interleaved stream of registration commands."""
        if part not in (1, 2, 3, 4):
            raise ValueError(f"part must be between 1 and 4, got {part}")

        registry: dict[str, str] = {}
        output: List[str] = []
        for line in lines:
            if line.startswith("RECLAIM|"):
                if part < 3:
                    raise ValueError("RECLAIM is available from part 3")
                _, account_id, name = line.split("|", 2)
                command = ("RECLAIM", account_id, name)
            elif line.startswith("WHOIS|"):
                if part < 4:
                    raise ValueError("WHOIS is available from part 4")
                _, name = line.split("|", 1)
                command = ("WHOIS", name)
            else:
                account_id, name = line.split("|", 1)
                command = ("REGISTER", account_id, name)

            # Apply this command to the shared registry, using basic normalization
            # in Part 1 and the extended rules from Part 2 onward.
            # RECLAIM mutates this same registry; WHOIS reads it at this point in
            # the stream. Registration output stays in the original pipe format.
            raise NotImplementedError("Implement normalization and registry commands")

        return output


if __name__ == "__main__":
    import sys

    part = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    data = sys.stdin.read().splitlines()
    print("\n".join(Solution().solve(data, part)))
