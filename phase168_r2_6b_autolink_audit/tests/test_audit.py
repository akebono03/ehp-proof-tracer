from dataclasses import dataclass

from phase168_r2_6b_autolink_audit.audit import classify_content


@dataclass(frozen=True)
class ExampleMathematicalContent:
    value: int


class TodaFixedStatementComponent:
    pass


def test_source_archive_is_not_mathematical_typed_content():
    assert classify_content({"source_text": "formula"}) == "SOURCE_ONLY"


def test_boundary_component_is_metadata():
    assert classify_content(TodaFixedStatementComponent()) == "METADATA_ONLY"


def test_dataclass_math_is_typed():
    assert classify_content(ExampleMathematicalContent(1)) == "TYPED_REGISTERED"


def test_scalar_is_not_typed():
    assert classify_content("metadata") == "OTHER"
