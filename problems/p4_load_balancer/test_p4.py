import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import pytest
import solution_p4 as sol

CASES = [
    ('part1_basic', 'part1',
     ['SERVERS 3', 'CONNECT c1 u1', 'CONNECT c2 u2', 'CONNECT c3 u3', 'CONNECT c4 u4'],
     ['c1,u1,0', 'c2,u2,1', 'c3,u3,2', 'c4,u4,0']),
    ('part1_ties_lowest_index', 'part1',
     ['SERVERS 2', 'CONNECT a ua', 'CONNECT b ub', 'CONNECT c uc'],
     ['a,ua,0', 'b,ub,1', 'c,uc,0']),
    ('part2_disconnect_rebalances', 'part2',
     ['SERVERS 2', 'CONNECT a ua', 'CONNECT b ub', 'DISCONNECT a', 'CONNECT c uc'],
     ['a,ua,0', 'b,ub,1', 'c,uc,0']),
    ('part2_invalid_disconnect_ignored', 'part2',
     ['SERVERS 2', 'CONNECT a ua', 'DISCONNECT zzz', 'CONNECT b ub'],
     ['a,ua,0', 'b,ub,1']),
    ('part3_sticky_overrides_load', 'part3',
     ['SERVERS 3', 'CONNECT c1 u1 o1', 'CONNECT c2 u2 o2', 'CONNECT c3 u3 o1', 'CONNECT c4 u4 o1'],
     ['c1,u1,0', 'c2,u2,1', 'c3,u3,0', 'c4,u4,0']),
    ('part3_binding_survives_disconnect', 'part3',
     ['SERVERS 2', 'CONNECT c1 u1 o1', 'CONNECT c2 u2 o2', 'DISCONNECT c1', 'CONNECT c3 u3 o1'],
     ['c1,u1,0', 'c2,u2,1', 'c3,u3,0']),
    ('part4_capacity_reject', 'part4',
     ['SERVERS 2', 'CAPACITY 1', 'CONNECT a ua', 'CONNECT b ub', 'CONNECT c uc'],
     ['a,ua,0', 'b,ub,1', 'c,uc,REJECTED']),
    ('part4_sticky_target_full_rejects', 'part4',
     ['SERVERS 2', 'CAPACITY 1', 'CONNECT a ua o1', 'CONNECT b ub o1'],
     ['a,ua,0', 'b,ub,REJECTED']),
]

@pytest.mark.parametrize("name,fn,inp,expected", CASES, ids=[c[0] for c in CASES])
def test_part(name, fn, inp, expected):
    assert sol.Solution().solve(inp, part=int(fn[-1])) == expected
