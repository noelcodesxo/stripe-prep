"""
Problem 4 - Multi-Stage Load Balancer (OOD).  Full spec: ../../04_load_balancer.md

This one is object-oriented by nature: model ONE class that holds the shared
state (per-server connection counts, connectionId->server, objectId->server) and
let each part be a small method on top of it. Parts 2-4 should be additions, not
rewrites -- if you find yourself rewriting Part 1, restructure.

Each function receives the input for that part as a list of lines and returns a
list of output lines (one per CONNECT). DISCONNECT emits nothing.

LINE TYPES
  SERVERS <n>                 first line: number of servers, indexed 0..n-1
  CONNECT <cid> <uid>         part 1+: assign to least-loaded (tie -> smallest index)
  DISCONNECT <cid>            part 2+: free that connection; unknown cid is ignored
  CONNECT <cid> <uid> <oid>   part 3+: sticky -- same oid always same server
  CAPACITY <c>                part 4: max connections per server (a config line)

OUTPUT (per CONNECT):  "<cid>,<uid>,<targetIndex>"   (0-indexed)
  part 4: if no eligible server (sticky target full, or all servers full),
          output "<cid>,<uid>,REJECTED" and drop the connection.

Manual run against stdin:  python solution_p4.py 3 < input.txt
"""
from typing import List


def part1(lines: List[str]) -> List[str]:
    # SERVERS + CONNECT only. Route to fewest active connections; tie -> lowest index.
    raise NotImplementedError


def part2(lines: List[str]) -> List[str]:
    # Adds DISCONNECT (decrement that server; unknown connection id is a no-op).
    raise NotImplementedError


def part3(lines: List[str]) -> List[str]:
    # Adds sticky routing: a 4th CONNECT token (objectId) pins all its requests to
    # one server permanently -- checked BEFORE load balancing, kept across disconnect.
    raise NotImplementedError


def part4(lines: List[str]) -> List[str]:
    # Adds CAPACITY: reject (don't place) a CONNECT when its target would exceed cap.
    raise NotImplementedError


if __name__ == "__main__":
    import sys
    part = sys.argv[1] if len(sys.argv) > 1 else "1"
    data = sys.stdin.read().splitlines()
    fn = {"1": part1, "2": part2, "3": part3, "4": part4}[part]
    print("\n".join(fn(data)))
