import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import pytest
import solution_p6 as sol

CASES = [
    ('part1_penalty_midday', 'part1', ['Y Y N Y', '3'], ['2']),
    ('part1_penalty_open_all_day', 'part1', ['Y Y N Y', '4'], ['1']),
    ('part2_best_time', 'part2', ['Y Y N Y'], ['2']),
    ('part2_all_empty_never_open', 'part2', ['N N N'], ['0']),
    ('part3_aggregate_two_logs', 'part3',
     ['garbage BEGIN Y Y N END trash BEGIN N Y END un', 'finished BEGIN Y Y'],
     ['2', '0']),
    ('part3_nested_begin_resets', 'part3', ['BEGIN Y BEGIN N N END'], ['0']),
    ('part4_weighted', 'part4', ['WEIGHTS 1 5', 'BEGIN Y N Y END'], ['3 1']),
]

@pytest.mark.parametrize("name,fn,inp,expected", CASES, ids=[c[0] for c in CASES])
def test_part(name, fn, inp, expected):
    assert getattr(sol, fn)(inp) == expected
