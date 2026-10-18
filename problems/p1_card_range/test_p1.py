import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import pytest
import solution_p1 as sol

CASES = [
    ('part1_basic', 'part1', ['400000 499999 visa', '510000 559999 mastercard', '340000 349999 amex', 'QUERIES', '411111', '340012', '600000'], ['visa', 'amex', 'UNKNOWN']),
    ('part1_boundaries', 'part1', ['100 200 a', '201 300 b', 'QUERIES', '100', '200', '201', '99'], ['a', 'a', 'b', 'UNKNOWN']),
    ('part2_override', 'part2', ['400000 499999 visa', '450000 459999 visa_debit', 'QUERIES', '455000', '411111'], ['visa_debit', 'visa']),
    ('part2_partial_override', 'part2', ['10 50 a', '20 30 b', '30 40 c', 'QUERIES', '25', '30', '35', '15'], ['b', 'c', 'c', 'a']),
    ('part3_gap', 'part3', ['100 200 a', '400 500 b'], ['201 399']),
    ('part3_adjacent_nogap', 'part3', ['100 200 a', '201 300 b'], ['NONE']),
    ('part3_single_none', 'part3', ['100 200 a'], ['NONE']),
    ('part4_merge_same_bank', 'part4', ['100 150 visa', '151 200 visa', '300 400 amex'], ['100 200 visa', '300 400 amex']),
    ('part4_nested_same_bank', 'part4', ['0 100 visa', '50 60 visa', '40 70 visa'], ['0 100 visa']),
]

@pytest.mark.parametrize("name,fn,inp,expected", CASES, ids=[c[0] for c in CASES])
def test_part(name, fn, inp, expected):
    assert sol.Solution().solve(inp, part=int(fn[-1])) == expected
