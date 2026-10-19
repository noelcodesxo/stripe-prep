"""Problem 6 - Store Closing Time.

Each request evaluates one Y/N log, and every stage returns a `<time> <penalty>` row.
The shared noisy-log parser and penalty calculation are intentionally left for the
learner.

Manual run against stdin:  python solution_p6.py 2 < input.txt
"""
from typing import List


class Solution:
    def solve(self, lines: List[str], part: int = 1) -> List[str]:
        """Read close/auto requests and evaluate logs through one shared flow."""
        if part not in (1, 2, 3, 4):
            raise ValueError(f"part must be between 1 and 4, got {part}")

        tokens = " ".join(lines).split()
        weighted = part == 4 and bool(tokens) and tokens[0] == "WEIGHTS"
        if tokens and tokens[0] == "WEIGHTS" and part < 4:
            raise ValueError("WEIGHTS is available from part 4")
        if weighted:
            weights = (int(tokens[1]), int(tokens[2]))
            tokens = tokens[3:]
        else:
            weights = (1, 1)

        records: list[tuple[list[str], str, int | None]] = []
        pending_request: tuple[str, int | None] | None = None
        current_log: list[str] | None = None

        # TODO: make one token pass to collect BEGIN/END records, preserving
        # pending_request while a BEGIN is restarted by another BEGIN. CLOSE t and
        # AUTO attach to the next completed record; unmarked records default to AUTO
        # from Part 3 onward. Ignore garbage and discard unfinished records.
        raise NotImplementedError("Implement the shared noisy-log and penalty flow")


if __name__ == "__main__":
    import sys

    part = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    data = sys.stdin.read().splitlines()
    print("\n".join(Solution().solve(data, part)))
