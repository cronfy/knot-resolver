from typing import Any

import pytest
from jinja2 import Template

from knot_resolver_manager.datamodel.types import EscapedStr
from knot_resolver_manager.utils.modelling import SchemaNode

str_template = Template("'{{ string }}'")


@pytest.mark.parametrize(
    "val,exp",
    [
        ("string", "string"),
        (2000, "2000"),
        ('"\a\b\f\n\r\t\v\\"', r"\"\x07\x08\x0c\n\r\t\x0b\\\""),
        ('""', r"\"\""),
        ("''", r"\'\'"),
        # fmt: off
        ('\"\"', r'\"\"'),
        ("\'\'", r'\'\''),
        # fmt: on
    ],
)
def test_escaped_str(val: Any, exp: str):
    class TestSchema(SchemaNode):
        pattern: EscapedStr

    d = TestSchema({"pattern": val})
    assert str_template.render(string=d.pattern) == f"'{exp}'"
