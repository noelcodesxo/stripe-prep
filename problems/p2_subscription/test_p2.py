import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import pytest
import solution_p2 as sol

CASES = [
    ('part1_basic', 'part1', ['PLAN basic 100', '5 SUBSCRIBE alice basic', '10 CANCEL alice', 'QUERY 20'], ['alice 500']),
    ('part1_still_active', 'part1', ['PLAN basic 100', 'PLAN pro 300', '0 SUBSCRIBE bob pro', 'QUERY 10'], ['bob 3000']),
    ('part2_change_proration', 'part2', ['PLAN basic 100', 'PLAN pro 300', '0 SUBSCRIBE bob basic', '4 CHANGE bob pro', '6 CANCEL bob', 'QUERY 10'], ['bob 1000']),
    ('part3_resub_and_refund', 'part3', ['PLAN basic 100', '0 SUBSCRIBE carol basic', '5 CANCEL carol', '10 SUBSCRIBE carol basic', '12 CANCEL carol', '15 REFUND carol 250', 'QUERY 20'], ['carol 450']),
    ('part4_invoice_windows', 'part4', ['PLAN basic 100', 'PLAN pro 300', '0 SUBSCRIBE carol basic', '4 CHANGE carol pro', 'INVOICE carol 3 8', 'INVOICE carol 0 4', 'INVOICE carol 100 200'], ['carol 1300', 'carol 400', 'carol 30000']),
]

@pytest.mark.parametrize("name,fn,inp,expected", CASES, ids=[c[0] for c in CASES])
def test_part(name, fn, inp, expected):
    assert sol.Solution().solve(inp, part=int(fn[-1])) == expected
