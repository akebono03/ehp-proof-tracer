"""R3-41A focused checks. These tests do not modify product modules."""
from pathlib import Path

from phase168_r3_41a_partial_model_gap_audit.audit import (
    ROOT,
    analyze_route_contract,
    audit_incomplete_statuses,
    markdown_report,
    run_audit,
)


def test_route_contract_finds_standard_model_and_explicit_partial_fallback():
    route = analyze_route_contract(ROOT)
    assert route["web_default_citation_source"] == "model"
    assert route["web_standard_uses_common_model"]
    assert route["flask_uses_standard_web"]
    assert route["flask_explicit_case_uses_adapter"]
    assert route["web_explicit_partial_uses_adapter"]
    assert route["adapter_fallback_calls"]
    assert route["adapter_common_calls"]


def test_three_incomplete_states_retain_the_existing_web_contract():
    rows = audit_incomplete_statuses()
    assert [row["case"] for row in rows] == [
        "not_searched", "partial", "search_failed",
    ]
    for row in rows:
        assert row["adapter_partial_result"]
        assert row["adapter_has_lines"]
        assert row["legacy_has_status"]
        assert row["legacy_has_open_goal_section"]
        assert not row["legacy_qed"]
    assert rows[1]["legacy_contains_observed_step"]
    assert rows[2]["legacy_has_diagnostic_section"]


def test_report_does_not_claim_mathematical_validity():
    report = {"routes": analyze_route_contract(ROOT),
              "cases": audit_incomplete_statuses()}
    text = markdown_report(report)
    assert "読み取り専用" in text
    assert "人工の不完全状態3ケース" in text
    assert "全体 pytest は Phase 168 の最後" in text


def test_audit_can_initialize_missing_output_directory(tmp_path: Path):
    output = tmp_path / "missing" / "output"
    assert not output.exists()
    report = run_audit(ROOT, output)
    assert report["status"] == "PASS"
    assert (output / "audit.md").is_file()
    assert (output / "audit.json").is_file()
    assert (output / "review_bundle.zip").is_file()
