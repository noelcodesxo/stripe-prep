"""
Problem 9 — Request Routing System. Full spec: ../../09_request_routing.md

Implement one function accepting the complete newline-separated command string.
Return one output string per nonblank command. Commands:
  REGISTER name latitude longitude capacity
  SET_HEALTHY name true|false
  DISTANCE latitude1 longitude1 latitude2 longitude2
  ROUTE latitude longitude

Use the spec's validation, distance, capacity, health, and output rules.
Each call has independent state. Unlike P1–P8, this exercise has no part functions.

Manual run: python solution_p9.py < input.txt
"""
from typing import List


def solveRequestRoutingSystem(input_text: str) -> List[str]:
    raise NotImplementedError


if __name__ == "__main__":
    import sys
    print("\n".join(solveRequestRoutingSystem(sys.stdin.read())))
