"""Read-only R3-40F checks; no production files are modified."""

from pathlib import Path

from phase168_r3_40f_residual_route_audit.audit import analyze_structure

ROOT = Path(__file__).resolve().parents[2]


def test_renderer_has_no_active_deferred_loop():
    info = analyze_structure(ROOT)
    assert info["renderer_after_indices_reads"] == []
    assert info["projection_after_indices_reads"] == []
    assert info["renderer_uses_shared_order"]
    assert info["renderer_uses_shared_citation_model"]


def test_legacy_order_entry_api_is_still_compatible():
    info = analyze_structure(ROOT)
    assert info["retains_compatibility_field"]
    assert info["historical_focused_test_reads_after_indices"]
    assert info["order_emits_narrative_order_entries"]
    assert info["order_has_dependency_graph"]


def test_web_model_is_default_but_compatibility_routes_remain():
    info = analyze_structure(ROOT)
    assert info["web_defaults"]["mode"] == "narrative"
    assert info["web_defaults"]["citation_source"] == "model"
    assert info["standard_web_has_explicit_legacy_branch"]
    assert info["adapter_has_model_renderer"]
    assert info["adapter_has_no_model_fallback"]


def test_four_existing_narratives_have_no_deferred_entries(tmp_path, monkeypatch):
    from phase168_r3_40f_residual_route_audit import audit

    output = tmp_path / "missing_output_directory"
    assert not output.exists()
    monkeypatch.setattr(audit, "OUTPUT", output)
    cases = audit.audit_four_cases(ROOT)
    assert output.is_dir()
    assert len(cases) == 4
    for case in cases:
        assert (output / (case["case"] + "_current.md")).is_file()
        assert case["complete_coverage"]
        assert case["all_after_indices_empty"]
        assert case["no_dependency_inversions"]
        assert case["matches_r3_40e_snapshot"] is not False
        assert case["web_narrative_route"] == "generic-complete-proof"
