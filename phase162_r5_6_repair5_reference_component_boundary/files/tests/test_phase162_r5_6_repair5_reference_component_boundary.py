"""Phase 162 R5-6 Repair 5: fixed reference component presentation boundary."""

from phase162_validated_proof_presentation import (
    _fixed_statement_reuse_visible_ids,
    _reference_component_reuse_boundary_ids,
    _render_validated_reference_section,
    _validated_proof_body_step_lines,
    build_validated_backward_proof_presentation,
    render_validated_backward_proof_markdown,
)
from tests.test_phase162_r2_validated_proof_presentation import _validated_fixture


def _fixture():
    presentation = build_validated_backward_proof_presentation(_validated_fixture())
    _, fixed_ids = _render_validated_reference_section(presentation)
    return presentation, fixed_ids


def test_phase162_repair5_component_boundary_hides_exclusive_bridge():
    presentation, fixed_ids = _fixture()
    boundaries = _reference_component_reuse_boundary_ids(presentation, fixed_ids)
    assert len(boundaries) == 1
    anchor = next(step for step in presentation.nodes if id(step) in boundaries)
    bridge = next(
        step for step in anchor.premises
        if getattr(step.inference_rule, "name", None)
        == "Toda 5.3 eta_5 iterated suspension bridge"
    )
    visible = _fixed_statement_reuse_visible_ids(presentation, fixed_ids)
    assert id(anchor) in visible
    assert id(bridge) not in visible
    assert any(step is anchor for step, _ in _validated_proof_body_step_lines(presentation, fixed_ids))
    assert all(step is not bridge for step, _ in _validated_proof_body_step_lines(presentation, fixed_ids))
    assert bridge in anchor.premises


def test_phase162_repair5_unregistered_component_does_not_suppress(monkeypatch):
    import phase162_validated_proof_presentation as module

    presentation, fixed_ids = _fixture()
    original = module.get_general_reference_statement
    monkeypatch.setattr(
        module,
        "get_general_reference_statement",
        lambda locator: None if locator == "(5.3)" else original(locator),
    )
    assert not _reference_component_reuse_boundary_ids(presentation, fixed_ids)
    baseline = _fixed_statement_reuse_visible_ids(presentation, fixed_ids)
    assert any(
        getattr(step.inference_rule, "name", None)
        == "Toda 5.3 eta_5 iterated suspension bridge"
        and id(step) in baseline
        for step in presentation.nodes
    )


def test_phase162_repair5_render_preserves_dag_and_applications():
    presentation, fixed_ids = _fixture()
    snapshot = tuple(
        (id(step), tuple(id(p) for p in step.premises))
        for step in presentation.nodes
    )
    text = render_validated_backward_proof_markdown(presentation)
    assert r"$E^{2}\eta_{3} = \eta_{5}$" not in text
    assert r"$H(\nu')=\eta_{5}$" in text
    assert "Proposition 5.1 の $n=5$" in text
    assert "### 単射性" in text and "### 全射性" in text
    assert text.rstrip().endswith("□")
    assert tuple(
        (id(step), tuple(id(p) for p in step.premises))
        for step in presentation.nodes
    ) == snapshot
