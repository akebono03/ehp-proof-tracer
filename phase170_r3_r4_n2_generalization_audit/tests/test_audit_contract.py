"""Focused offline contract tests for n=2 read-only proof and Web diagnostics."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest


def audit_module():
    path = Path(__file__).resolve().parents[1] / "audit.py"
    spec = importlib.util.spec_from_file_location("phase170_r3_r4_contract", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def example(*, search="search_failed", goal_count=1, web_error=None):
    result = {
        "group": "pi_5^2", "n": 2, "k": 3,
        "db_rows": [{"orders": "2", "generator": "eta cube"}],
        "typed_goal_count": goal_count,
        "search_status": search,
        "web": {"key": "generic-partial-proof", "partial_result": True},
    }
    if web_error is not None:
        result["web"]["error"] = web_error
    return result


def test_contract_accepted_defaults_and_range():
    module = audit_module()
    assert module.GROUP_SPHERE == 2
    assert (module.DEFAULT_MIN_K, module.DEFAULT_MAX_K) == (3, 10)


def test_integer_csv_cell_parsing_rejects_malformed_data():
    module = audit_module()
    assert module.cell_is_int("2", 2)
    assert module.cell_is_int("2.0", 2)
    assert not module.cell_is_int("NaN", 2)
    assert not module.cell_is_int("2.1", 2)
    assert not module.cell_is_int("", 2)


@pytest.mark.parametrize("diff", [
    (("M", "web_group_proof.py"),),
    (("A", "README.md"),),
    (("A", "tests/test_new.py"),),
    (("D", "phase170_r3_r4_n2_generalization_audit/audit.py"),),
    (("A", "phase170_r3_r4_n2_generalization_audit/../web_group_proof.py"),),
])
def test_unreviewed_changes_fail_closed(diff):
    assert not audit_module().acceptable_added_audit_changes(diff)


def test_later_audit_only_added_file_allowed():
    assert audit_module().acceptable_added_audit_changes(
        (("A", "phase170_r3_r4_n2_generalization_audit/tests/test_audit_contract.py"),)
    )


def test_git_name_status_parser_handles_nul_termination():
    assert audit_module().parse_changes_z(b"A\x00phase170_x/readme.md\x00") == (
        ("A", "phase170_x/readme.md"),
    )


@pytest.mark.parametrize("malformed", [b"A\x00file", b"A\x00", b"A\x00file\x00M\x00"])
def test_git_name_status_parser_rejects_malformed(malformed):
    with pytest.raises(RuntimeError):
        audit_module().parse_changes_z(malformed)


def test_empty_git_diff_is_valid():
    assert audit_module().parse_changes_z(b"") == ()


def test_failed_search_with_goal_is_not_reported_complete():
    assert audit_module().outcome_class(example()) == "GOAL_AVAILABLE_PROOF_UNFINISHED"


def test_missing_goal_is_classified_separately():
    assert audit_module().outcome_class(example(goal_count=0)) == "TYPED_GOAL_SELECTION_UNRESOLVED"


def test_missing_database_row_is_classified_separately():
    case = example()
    case["db_rows"] = []
    assert audit_module().outcome_class(case) == "NO_EXPLICIT_DB_ROW"


def test_complete_search_without_verified_web_is_not_complete():
    result = example(search="complete")
    assert audit_module().outcome_class(result) == "SEARCH_COMPLETE_WEB_NOT_VERIFIED"


def test_verified_web_required_for_complete_classification():
    result = example(search="complete")
    result["web"] = {"route": "standard_web_public_trust_gated", "key": "generic-complete-proof", "partial_result": False}
    assert audit_module().outcome_class(result) == "COMPLETE_AND_WEB_VERIFIED"


def test_renderer_error_does_not_imply_proven_group():
    assert audit_module().outcome_class(example(web_error="render failure")) == "SEARCH_INCOMPLETE_AND_RENDER_ERROR"


def test_shortened_repr_never_claims_completeness():
    value = audit_module().clipped("x" * 30, 5)
    assert value.endswith(" [TRUNCATED]")


def test_markdown_reports_contain_explicit_unfinished_result():
    report = {"git": {"head": "test"}, "cases": [
        {**example(), "outcome": "GOAL_AVAILABLE_PROOF_UNFINISHED",
         "structured_goal_count": 1, "simple_goal_count": 0,
         "zero_goal_count": 0, "source_assertion_id": None,
         "proven_step_count": 0, "open_goals": [], "diagnostics": []}
    ]}
    text = audit_module().to_markdown(report)
    assert "全体 pytest: 未実行" in text
    assert "GOAL_AVAILABLE_PROOF_UNFINISHED" in text
    assert "π" not in text or "pi_5^2" in text


def test_json_serialization_is_plain_data_only():
    payload = json.dumps(example(), ensure_ascii=False)
    assert json.loads(payload)["n"] == 2
