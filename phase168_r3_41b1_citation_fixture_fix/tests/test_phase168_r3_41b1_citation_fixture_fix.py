"""Only test-fixture maintenance; no production citation semantics change."""
from phase168_r3_41b1_citation_fixture_fix.fix_test import (
    AFTER, BEFORE, patched_bytes, verify_test_source,
)


_SAMPLE = 'from dataclasses import replace\nimport pytest\n\ndef test_unknown_citation_number_is_rejected():\n    result, model = _case()\n    wrong = replace(model, step_citation_numbers=((2,),))\n    with pytest.raises(ValueError, match="missing or unrelated"):\n        build_narrative_body_lines(result, wrong)\n\ndef test_reverse_citation_mapping_is_checked():\n    result, model = _case()\n    wrong = replace(model, step_citation_numbers=((),))\n    with pytest.raises(ValueError, match="disagree"):\n        build_narrative_body_lines(result, wrong)\n'


def test_unknown_citation_fixture_changes_only_citation_list():
    repaired = patched_bytes(_SAMPLE.encode("utf-8")).decode("utf-8")
    assert BEFORE not in repaired
    assert AFTER in repaired
    assert 'match="missing or unrelated"' in repaired
    assert 'match="disagree"' in repaired
    verify_test_source(repaired)


def test_unknown_citation_fixture_repair_is_idempotent():
    original = _SAMPLE.encode("utf-8")
    fixed = patched_bytes(original)
    assert patched_bytes(fixed) == fixed


def test_unknown_citation_fixture_keeps_reverse_mapping_test():
    repaired = patched_bytes(_SAMPLE.encode("utf-8")).decode("utf-8")
    assert "def test_reverse_citation_mapping_is_checked():" in repaired
    assert "wrong = replace(model, step_citation_numbers=((),))" in repaired
