import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import pytest
import solution_p3 as sol

CASES = [
    ('part1_basic', 'part1', ['1 cardA 1000 shopX APPROVED', '2 cardA 500 shopY DECLINED', '3 cardB 200 shopX APPROVED', '4 cardA 700 shopX APPROVED'], ['cardA 2 1700 0.33', 'cardB 1 200 0.00']),
    ('part2_velocity', 'part2', ['VELOCITY 3 60', '10 cardA 100 m APPROVED', '10 cardB 100 m APPROVED', '30 cardA 100 m APPROVED', '65 cardA 100 m APPROVED', '66 cardA 100 m APPROVED', '200 cardB 100 m APPROVED'], ['cardA 4 400 0.00 Y', 'cardB 2 200 0.00 N']),
    ('part2_none', 'part2', ['VELOCITY 5 10', '1 cardA 100 m APPROVED', '2 cardA 100 m APPROVED'], ['cardA 2 200 0.00 N']),
    ('part3_testing_burst', 'part3', ['VELOCITY 3 60', 'BURST 3 100 60', '0 cardA 10 mtest APPROVED', '0 cardA 5000 mbig APPROVED', '1 cardA 5000 mbig APPROVED', '2 cardA 5000 mbig APPROVED', '5 cardA 20 mtest DECLINED', '10 cardA 30 mtest APPROVED'], ['cardA 5 15040 0.17 Y mtest']),
    ('part4_risk_ranking', 'part4', ['VELOCITY 3 60', 'BURST 3 100 60', 'TOPK 2', '0 cardB 20000 shop APPROVED', '1 cardB 100 shop DECLINED', '5 cardC 100 shop DECLINED', '10 cardA 100 mtest APPROVED', '30 cardA 50 mtest APPROVED', '65 cardA 40 mtest DECLINED', '66 cardA 30 mtest APPROVED'], ['cardA 3 220 0.25 Y mtest 30', 'cardB 1 20000 0.50 N - 7']),
]

@pytest.mark.parametrize("name,fn,inp,expected", CASES, ids=[c[0] for c in CASES])
def test_part(name, fn, inp, expected):
    assert sol.Solution().solve(inp, part=int(fn[-1])) == expected
