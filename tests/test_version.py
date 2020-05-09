import re

import mario


def is_valid_version(s: str):
    match = re.fullmatch(r'(\d+\.\d+.\d+(-rc\.[0-9/.]+)?)', s)
    return match is not None


def test_version_is_valid():
    assert is_valid_version(mario.__version__)
