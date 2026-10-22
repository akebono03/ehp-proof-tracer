from types import SimpleNamespace

from phase168_r2_8_1_citation_mismatch_audit.audit import CASES
from phase168_r2_8_5_search_connection_audit.audit import summarize_result


def test_nine_target_cases_are_unique():
    assert len(CASES) == 9
    assert len({(n, k) for n, k, _ in CASES}) == 9


def test_status_is_reported_without_inferring_completion():
    result = SimpleNamespace(status=SimpleNamespace(value="partial"), structure_status=SimpleNamespace(value="known"), proven_steps=(), open_goals=("goal",), diagnostics=("missing",), references=(), conclusion=None)
    row = summarize_result(result)
    assert row["status"] == "partial"
    assert row["open_goal_count"] == 1
    assert row["conclusion"] == "None"


def test_complete_status_preserved_when_returned_by_search():
    result = SimpleNamespace(status=SimpleNamespace(value="complete"), structure_status=SimpleNamespace(value="known"), proven_steps=("step",), open_goals=(), diagnostics=(), references=("Proposition 5.3",), conclusion="verified")
    row = summarize_result(result)
    assert row["status"] == "complete"
    assert row["proven_step_count"] == 1
    assert row["references"] == ["Proposition 5.3"]


def test_missing_optional_fields_are_safe():
    row = summarize_result(SimpleNamespace())
    assert row["proven_step_count"] == 0
    assert row["open_goal_count"] == 0
