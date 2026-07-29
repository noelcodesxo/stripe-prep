import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import pytest
import solution_p5 as sol

CASES = [
    ('part1_basic_normalization', 'part1',
     ['acct1|Llama, Inc.', 'acct2|LLAMA  Inc.', 'acct3|   ', 'acct4|Llama Inc'],
     ['acct1|Name Available', 'acct2|Name Not Available', 'acct3|Name Not Available', 'acct4|Name Available']),
    ('part1_ampersand_is_space', 'part1',
     ['a1|Ben & Jerry', 'a2|Ben  Jerry'],
     ['a1|Name Available', 'a2|Name Not Available']),
    ('part2_suffix_and_article', 'part2',
     ['a1|The Llama, Inc.', 'a2|Llama LLC', 'a3|Llama And Friend', 'a4|Llama Friend'],
     ['a1|Name Available', 'a2|Name Not Available', 'a3|Name Available', 'a4|Name Not Available']),
    ('part2_leading_and_is_distinct', 'part2',
     ['a1|And Llama Friend', 'a2|Llama Friend'],
     ['a1|Name Available', 'a2|Name Available']),
    ('part3_reclaim_frees_name', 'part3',
     ['a1|Llama Inc.', 'RECLAIM|a1|Llama Inc.', 'a2|Llama'],
     ['a1|Name Available', 'a2|Name Available']),
    ('part3_reclaim_requires_owner', 'part3',
     ['a1|Llama Inc.', 'RECLAIM|a2|Llama Inc.', 'a2|Llama'],
     ['a1|Name Available', 'a2|Name Not Available']),
    ('part4_whois_lookup', 'part4',
     ['a1|Llama Inc.', 'WHOIS|the llama', 'WHOIS|Acme', 'RECLAIM|a1|Llama Inc.', 'WHOIS|Llama'],
     ['a1|Name Available', 'a1', 'UNREGISTERED', 'UNREGISTERED']),
]

@pytest.mark.parametrize("name,fn,inp,expected", CASES, ids=[c[0] for c in CASES])
def test_part(name, fn, inp, expected):
    assert getattr(sol, fn)(inp) == expected
