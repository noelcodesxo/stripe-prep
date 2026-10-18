"""Problem 7 - Payment Card Validation.

Plain cards, redacted cards, and corrupted cards share one stable row format. The
Luhn/network checks and candidate generation are intentionally learner TODOs.

Manual run against stdin:  python solution_p7.py 2 < input.txt
"""
from typing import List


class Solution:
    def solve(self, lines: List[str], part: int = 1) -> List[str]:
        """Classify every card request into the cumulative output schema."""
        if part not in (1, 2, 3, 4):
            raise ValueError(f"part must be between 1 and 4, got {part}")

        requests: list[tuple[str, str]] = []
        for card in lines:
            if "?" in card:
                if part < 4:
                    raise ValueError("Corrupted-card requests are available from part 4")
                requests.append(("CORRUPTED", card))
            elif "*" in card:
                if part < 3:
                    raise ValueError("Redacted-card requests are available from part 3")
                requests.append(("REDACTED", card))
            else:
                requests.append(("PLAIN", card))

        # TODO: use shared Luhn/network helpers and return
        # `<source>|<outcome>|<count>|<details>` for every request.
        raise NotImplementedError("Implement card classification and candidate search")


if __name__ == "__main__":
    import sys

    part = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    data = sys.stdin.read().splitlines()
    print("\n".join(Solution().solve(data, part)))
