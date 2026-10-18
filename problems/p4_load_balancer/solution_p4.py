"""
Problem 4 - Multi-Stage Load Balancer (OOD).  Full spec: ../../04_load_balancer.md

Implement the Solution methods below. `solve` is the stable entry point for every
part: pass the input lines and the part number, then return the output lines.

This one is object-oriented by nature: model ONE class that holds the shared state
(per-server connection counts, connectionId->server, objectId->server) and let each
part add a small method on top of it. Parts 2-4 should be additions, not rewrites --
if you find yourself rewriting Part 1, restructure.

Each line is one of:
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


class LoadBalancer:
    def __init__(self, server_count: int, capacity: int | None = None):
        self.connection_count_per_server = [0] * server_count
        self.connection_id_to_server = {}
        self.capacity = capacity
        self.object_id_to_server = {}

    def find_server_with_least_connections(self) -> int:
        server = 0
        min_conn_count: int = self.connection_count_per_server[0]

        for idx in range(1, len(self.connection_count_per_server)):
            if self.connection_count_per_server[idx] < min_conn_count:
                server = idx
                min_conn_count = self.connection_count_per_server[idx]
        return server

    def establish_new_connection(self, conn_id: int, user_id: str, object_id: int = None) -> str:
        if conn_id in self.connection_id_to_server:
            return None

        # Extend method to support the object id to server logic
        server = self.object_id_to_server[object_id] if object_id is not None and object_id in self.object_id_to_server else self.find_server_with_least_connections()

        if self.capacity is not None and self.connection_count_per_server[server] >= self.capacity:
            return "{},{},REJECTED".format(conn_id, user_id)
        else:
            self.connection_id_to_server[conn_id] = server
            self.connection_count_per_server[server] += 1
            if object_id is not None:
                self.object_id_to_server[object_id] = server
            return "{},{},{}".format(conn_id, user_id, server)

    def disconnect(self, conn_id: int) -> None:
        if conn_id not in self.connection_id_to_server:
            return None

        # Find server to reduce count from.
        server = self.connection_id_to_server[conn_id]
        self.connection_count_per_server[server] -= 1

        # Check how to delete a key from a map if this is the correct way.
        del self.connection_id_to_server[conn_id]


class Solution:
    def solve(self, lines: List[str], part: int = 1) -> List[str]:
        """Run one stage of the problem against a list of input lines."""
        if part not in (1, 2, 3, 4):
            raise ValueError(f"part must be between 1 and 4, got {part}")

        loadbalancer = None
        responses: list[str] = []
        for line in lines:
            tokens = line.split(" ")

            if tokens[0] == "SERVERS":
                server_count: int = int(tokens[1])
                if part < 4:
                    loadbalancer = LoadBalancer(capacity=10, server_count=server_count)
                else:
                    loadbalancer = LoadBalancer(server_count=server_count)
            elif part == 4 and tokens[0] == "CAPACITY":
                capacity: int = int(tokens[1])
                loadbalancer.capacity = capacity
            elif tokens[0] == "CONNECT":
                conn_id = tokens[1]
                user_id = tokens[2]
                if part >= 3:
                    object_id = tokens[3] if len(tokens) >= 4 else None
                    responses.append(loadbalancer.establish_new_connection(
                        conn_id=conn_id,
                        user_id=user_id,
                        object_id=object_id,
                    ))
                else:
                    responses.append(loadbalancer.establish_new_connection(
                        conn_id=conn_id,
                        user_id=user_id,
                    ))
            elif part == 4 and tokens[0] == "DISCONNECT":
                conn_id = tokens[1]
                loadbalancer.disconnect(conn_id=conn_id)

        return responses


if __name__ == "__main__":
    import sys

    part = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    data = sys.stdin.read().splitlines()
    print("\n".join(Solution().solve(data, part)))
