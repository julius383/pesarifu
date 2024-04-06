import re

import lark
import pytest
from toolz import pipe

from pesarifu.etl.safaricom.transform import parse_details


def example_details():
    lines = []
    with open("examples/mpesa_details.txt", "r", encoding="utf-8") as fp:
        lines = fp.readlines()
    return list(
        filter(
            bool,
            map(
                lambda x: pipe(
                    x,
                    lambda y: re.sub(r"\s{2,}", "", y),
                    str.strip,
                ),
                lines,
            ),
        )
    )



@pytest.mark.parametrize("example", example_details())
def test_parse_details(example):
    assert isinstance(parse_details(example), dict)
