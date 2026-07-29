import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import pytest
import solution_p7 as sol

CASES = [
    ('part1_visa_valid', 'part1', ['4532015112830366'], ['VISA']),
    ('part1_visa_bad_checksum', 'part1', ['4242424242424243'], ['INVALID_CHECKSUM']),
    ('part2_mixed_networks', 'part2',
     ['4532015112830366', '5555555555554444', '378282246310005', '562523343010901', '4242424242424243'],
     ['VISA', 'MASTERCARD', 'AMEX', 'UNKNOWN_NETWORK', 'INVALID_CHECKSUM']),
    ('part3_one_wildcard', 'part3', ['453201511283036*'], ['VISA,1']),
    ('part3_two_wildcards', 'part3', ['42424242424242**'], ['VISA,10']),
    ('part4_corrupted_amex', 'part4', ['340000000000009?'],
     ['340000000000009,AMEX', '340000000000090,AMEX']),
]

@pytest.mark.parametrize("name,fn,inp,expected", CASES, ids=[c[0] for c in CASES])
def test_part(name, fn, inp, expected):
    assert getattr(sol, fn)(inp) == expected
