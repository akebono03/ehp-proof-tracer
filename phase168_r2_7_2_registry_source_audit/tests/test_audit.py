from phase168_r2_7_2_registry_source_audit.audit import TARGETS, classify
from toda_literature_statement_boundary import TodaFixedStatementComponent


def test_target_count():
    assert len(TARGETS) == 2


def test_archive_classification():
    assert classify({"source_text": "example"}) == "SOURCE_ONLY"


def test_mathematical_classification():
    assert classify(object()) == "MATHEMATICAL_TYPED"


def test_metadata_classification():
    assert classify(object.__new__(TodaFixedStatementComponent)) == "METADATA_ONLY"
