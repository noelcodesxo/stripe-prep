import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import pytest
import solution_p8 as sol


CASES = [
    ("part1_example", "part1", ["userA,100,120,payg", "userB,150,100,payg", "userB,100,130,payg"], ["userA: $0.07", "userB: $0.14"]),
    ("part1_sort_and_zero", "part1", ["zoe,0,0,payg", "amy,99,99,payg", "Bob,100,100,payg"], ["Bob: $0.07", "amy: $0.00", "zoe: $0.00"]),
    ("part1_aggregate_before_floor", "part1", ["a,60,70,payg", "a,60,40,payg"], ["a: $0.07"]),
    ("part1_separate_directions", "part1", ["a,99,1,payg", "b,100,199,payg", "c,200,200,payg"], ["a: $0.00", "b: $0.07", "c: $0.14"]),
    ("part1_large_bill", "part1", ["a,10000000,10000000,payg"], ["a: $7000.00"]),
    ("part2_example", "part2", ["userA,100,100,payg", "userB,20000,10000,fixed", "userB,25000,12000,fixed"], ["userA: $0.07", "userB: $17.30"]),
    ("part2_fee_once", "part2", ["a,0,0,fixed", "a,0,0,fixed", "b,40000,20000,fixed"], ["a: $15.00", "b: $15.00"]),
    ("part2_overage_boundaries", "part2", ["a,40099,20099,fixed", "b,40100,20100,fixed"], ["a: $15.00", "b: $15.07"]),
    ("part2_allowances_separate", "part2", ["a,0,20200,fixed", "b,40200,0,fixed"], ["a: $15.08", "b: $15.06"]),
    ("part2_aggregate_fixed", "part2", ["a,20060,10060,fixed", "a,20060,10060,fixed"], ["a: $15.07"]),
    ("part3_example", "part3", ["userA,100,100,payg", "userA,100,100,payg", "userA,20000,10000,fixed", "userA,100,100,fixed", "userB,100,100,payg"], ["userA: $7.71", "userB: $0.07"]),
    ("part3_separate_plan_blocks", "part3", ["a,60,60,payg", "a,20060,10060,fixed"], ["a: $7.50"]),
    ("part3_payg_does_not_use_allowance", "part3", ["a,10000,5000,payg", "a,0,0,fixed"], ["a: $12.50"]),
    ("part3_per_user_ratios", "part3", ["a,0,0,fixed", "b,0,0,payg", "a,0,0,payg", "b,0,0,payg", "b,0,0,fixed"], ["a: $7.50", "b: $5.00"]),
    ("part3_fractional_allowance", "part3", ["a,13433,6766,fixed", "a,0,0,payg", "a,0,0,payg"], ["a: $5.00"]),
    ("part3_fractional_allowance_full_block", "part3", ["a,13434,6767,fixed", "a,0,0,payg", "a,0,0,payg"], ["a: $5.07"]),
    ("part3_fractional_fee", "part3", ["a,0,0,fixed"] + ["a,0,0,payg"] * 6, ["a: $2.14"]),
    ("part3_half_cent_up", "part3", ["a,0,0,fixed"] + ["a,0,0,payg"] * 7, ["a: $1.88"]),
    ("part3_single_plan_users", "part3", ["b,40100,20100,fixed", "a,200,100,payg"], ["a: $0.10", "b: $15.07"]),
]
CASES += [(f"{part}_empty", part, [], []) for part in ("part1", "part2", "part3")]


@pytest.mark.parametrize("name,fn,inp,expected", CASES, ids=[case[0] for case in CASES])
def test_part(name, fn, inp, expected):
    assert getattr(sol, fn)(inp) == expected
