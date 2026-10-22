from phase168_r2_7_3_registration_preflight.audit import TARGETS, category
from toda_literature_statement_boundary import TodaFixedStatementComponent
from unified_statement_registry import AssertionOrigin


def test_expected_prop53_components():
    assert len(TARGETS["Proposition 5.3"]) == 4


def test_expected_prop56_components():
    assert len(TARGETS["Proposition 5.6"]) == 5


def test_metadata_type_origin():
    assert TodaFixedStatementComponent.__name__ == "TodaFixedStatementComponent"
    assert AssertionOrigin.SOURCE_ARCHIVE is not AssertionOrigin.FIXED_STATEMENT


def test_classifier_uses_real_type_not_dataclass_alone():
    from types import SimpleNamespace
    obj = SimpleNamespace(origin=AssertionOrigin.FIXED_STATEMENT, content=object())
    assert category(obj) == "MATHEMATICAL_TYPED"
