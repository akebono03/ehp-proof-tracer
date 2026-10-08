"""Phase 162 R5-6 Repair 4: fixed statement reuse and visibility boundary."""

from phase162_validated_proof_presentation import (
    _fixed_statement_reuse_visible_ids,
    _render_validated_reference_section,
    _validated_proof_body_step_lines,
    build_validated_backward_proof_presentation,
    render_validated_backward_proof_markdown,
)
from proof import ProofRule
from tests.test_phase162_r2_validated_proof_presentation import _validated_fixture


def _fixture_and_boundary():
    presentation = build_validated_backward_proof_presentation(_validated_fixture())
    _, fixed_ids = _render_validated_reference_section(presentation)
    return presentation, fixed_ids


def test_phase162_r5_6_repair4_fixed_ancestry_suppressed_only_when_exclusive():
    presentation, fixed_ids = _fixture_and_boundary()
    visible_ids = _fixed_statement_reuse_visible_ids(presentation, fixed_ids)
    expected = set()

    def visit(step):
        if id(step) in expected:
            return
        expected.add(id(step))
        if id(step) in fixed_ids:
            return
        for premise in step.premises:
            visit(premise)

    visit(presentation.root_step)
    assert visible_ids == frozenset(expected)
    assert id(presentation.root_step) in visible_ids
    # Only fixed statements reached from the final goal are visibility leaves.
    # Other referenced source statements can be present in the reference
    # catalog without belonging to the truncated path from the root.
    assert visible_ids.intersection(fixed_ids)
    assert visible_ids.intersection(fixed_ids).issubset(fixed_ids)
    assert visible_ids.issubset({id(step) for step in presentation.nodes})
    hidden = {id(step) for step in presentation.nodes} - visible_ids
    assert hidden, "Fixture must exercise actual fixed-source ancestry suppression"
    assert all(id(step) in visible_ids for step, _ in _validated_proof_body_step_lines(presentation, fixed_ids))


def test_phase162_r5_6_repair4_preserves_reachable_nonfixed_inferences():
    presentation, fixed_ids = _fixture_and_boundary()
    visible = _fixed_statement_reuse_visible_ids(presentation, fixed_ids)
    records = _validated_proof_body_step_lines(presentation, fixed_ids)
    emitted_ids = {id(step) for step, _ in records}
    assert emitted_ids.issubset(visible - fixed_ids)
    for step in presentation.nodes:
        if id(step) not in visible or id(step) in fixed_ids:
            assert id(step) not in emitted_ids
    assert any(step.rule is ProofRule.INFERENCE for step, _ in records)


def test_phase162_r5_6_repair4_dag_unchanged_and_application_retained():
    presentation, fixed_ids = _fixture_and_boundary()
    before = tuple((id(step), tuple(id(premise) for premise in step.premises)) for step in presentation.nodes)
    text = render_validated_backward_proof_markdown(presentation)
    assert "Proposition 5.1 の $n=5$" in text
    assert r"$H(\nu')=\eta_{5}$" in text
    assert r"$\Delta(\iota_{5})=\pm2\eta_{2}$" in text
    assert "### 単射性" in text and "### 全射性" in text
    assert text.rstrip().endswith("□")
    assert tuple((id(step), tuple(id(premise) for premise in step.premises)) for step in presentation.nodes) == before
