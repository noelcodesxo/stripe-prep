"""
Problem 6 - Store Closing Time.  Full spec: ../../06_store_closing.md

An hourly log of 'Y' (customers) / 'N' (empty). For a closing_time t in 0..n,
penalty = (# empty hours while OPEN, i.e. in hours[:t]) + (# customer hours while
CLOSED, i.e. in hours[t:]). Parts 3-4 add parsing many logs out of noisy text.

Each function receives the input for that part as a list of lines and returns a
list of output lines.

PARTS
  part 1: input line 1 = space-separated Y/N log; line 2 = closing_time int.
          Output one line: the penalty.
  part 2: input line 1 = the log. Output one line: the best closing time (minimum
          penalty; on a tie, the SMALLEST closing time).
  part 3: input is an aggregate blob (any number of lines). Extract every valid
          log -- a run "BEGIN <Y/N>* END". BEGIN with no END is discarded; a nested
          BEGIN restarts the current log (no nesting); non-Y/N tokens are garbage.
          Output the best closing time for each valid log, in order, one per line.
  part 4: input line 1 = "WEIGHTS <a> <b>" (a = cost per empty-open hour, b = cost
          per closed-with-customers hour); the rest is an aggregate blob. Output
          "<best_time> <min_penalty>" per valid log under those weights.

Manual run against stdin:  python solution_p6.py 2 < input.txt
"""
from typing import List


def part1(lines: List[str]) -> List[str]:
    # Penalty for one log at one given closing time.
    raise NotImplementedError


def part2(lines: List[str]) -> List[str]:
    # Best closing time (min penalty; smallest time breaks ties). Aim for O(n).
    raise NotImplementedError


def part3(lines: List[str]) -> List[str]:
    # Parse valid BEGIN..END logs from noisy text; best closing time for each.
    raise NotImplementedError


def part4(lines: List[str]) -> List[str]:
    # Weighted penalty; output "<best_time> <min_penalty>" per valid log.
    raise NotImplementedError


if __name__ == "__main__":
    import sys
    part = sys.argv[1] if len(sys.argv) > 1 else "1"
    data = sys.stdin.read().splitlines()
    fn = {"1": part1, "2": part2, "3": part3, "4": part4}[part]
    print("\n".join(fn(data)))
