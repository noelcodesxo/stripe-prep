import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import pytest
import solution_p7 as sol

CASES = [
    ('part1_visa_valid', 'part1', ['4532015112830366'], ['4532015112830366|VISA|1|-']),
    ('part1_visa_bad_checksum', 'part1', ['4242424242424243'], ['4242424242424243|INVALID_CHECKSUM|0|-']),
    ('part2_mixed_networks', 'part2',
     ['4532015112830366', '5555555555554444', '378282246310005', '562523343010901', '4242424242424243'],
     ['4532015112830366|VISA|1|-', '5555555555554444|MASTERCARD|1|-',
      '378282246310005|AMEX|1|-', '562523343010901|UNKNOWN_NETWORK|0|-',
      '4242424242424243|INVALID_CHECKSUM|0|-']),
    ('part3_one_wildcard', 'part3', ['453201511283036*'], ['453201511283036*|REDACTED|1|VISA=1']),
    ('part3_two_wildcards', 'part3', ['42424242424242**'], ['42424242424242**|REDACTED|10|VISA=10']),
    ('part4_corrupted_amex', 'part4', ['340000000000009?'],
     ['340000000000009?|CORRUPTED|1|340000000000090:AMEX']),
    ('part4_plain_redacted_and_corrupted', 'part4',
     ['4532015112830366', '453201511283036*', '340000000000009?'],
     ['4532015112830366|VISA|1|-',
      '453201511283036*|REDACTED|1|VISA=1',
      '340000000000009?|CORRUPTED|1|340000000000090:AMEX']),
]

@pytest.mark.parametrize("name,fn,inp,expected", CASES, ids=[c[0] for c in CASES])
def test_part(name, fn, inp, expected):
    assert sol.Solution().solve(inp, part=int(fn[-1])) == expected
