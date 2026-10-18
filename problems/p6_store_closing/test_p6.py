import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import pytest
import solution_p6 as sol

CASES = [
    ('part1_penalty_midday', 'part1', ['CLOSE 3 BEGIN Y Y N Y END'], ['3 2']),
    ('part1_penalty_open_all_day', 'part1', ['CLOSE 4 BEGIN Y Y N Y END'], ['4 1']),
    ('part2_best_time', 'part2', ['AUTO BEGIN Y Y N Y END'], ['2 1']),
    ('part2_all_empty_never_open', 'part2', ['AUTO BEGIN N N N END'], ['0 0']),
    ('part3_aggregate_two_logs', 'part3',
     ['garbage BEGIN Y Y N END trash BEGIN N Y END un', 'finished BEGIN Y Y'],
     ['2 0', '0 1']),
    ('part3_nested_begin_resets', 'part3', ['BEGIN Y BEGIN N N END'], ['0 0']),
    ('part4_weighted', 'part4', ['WEIGHTS 1 5', 'BEGIN Y N Y END'], ['3 1']),
    ('part4_preserves_explicit_auto_and_noisy_requests', 'part4',
     ['WEIGHTS 1 5', 'CLOSE 1 BEGIN N Y END',
      'AUTO BEGIN Y N Y END', 'garbage BEGIN Y BEGIN N Y END'],
     ['1 6', '3 1', '2 1']),
]

@pytest.mark.parametrize("name,fn,inp,expected", CASES, ids=[c[0] for c in CASES])
def test_part(name, fn, inp, expected):
    assert sol.Solution().solve(inp, part=int(fn[-1])) == expected
