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
