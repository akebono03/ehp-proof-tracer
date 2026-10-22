from phase167_r4_6_specialization_route_audit.audit import inspect_sources, focus_lines


def test_existing_specialization_and_order_functions_present():
    data = inspect_sources()
    renderer = data["toda_group_proof_narrative_renderer.py"]
    assert "_phase159_r1_6d_toda_51_diagonal_specialization_lines" in renderer
    assert "_phase159_r1_6d_finalize_reference_and_linkage" in renderer
    contribution = data["toda_group_proof_narrative_contribution_renderer.py"]
    assert "order_toda_group_proof_narrative_visible_step_dependencies" in contribution


def test_focus_selects_reference_and_diagonal_lines():
    data = {"lines": [
        {"prefix": "[R1]より, ", "statement_latex": r"\pi_{5}^{5}=\mathbb{Z}",
         "suffix": ""},
        {"prefix": "証明対象", "statement_latex": None, "suffix": ""},
    ]}
    selected = focus_lines(data)
    assert len(selected) == 1
    assert selected[0]["prefix"] == "[R1]より, "
