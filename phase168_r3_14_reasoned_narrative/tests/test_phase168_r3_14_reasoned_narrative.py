from dataclasses import replace

import pytest

from phase165_r52_partial_proof import ProofSearchStatus, make_partial_proof_result
from phase168_r3_3_proof_narrative_model import build_proof_narrative_model
from phase168_r3_14_reasoned_narrative import (
    build_reasoned_narrative_lines,
    render_reasoned_narrative_markdown,
)
from proof import InferenceRule, LiteratureReference, ProofRule, ProofStep


def _case():
    given = ProofStep("A", (), ProofRule.GIVEN)
    rule = InferenceRule(
        name="sample", literature_reference=LiteratureReference(
            label="Toda (5.2)", locator="(5.2)",
        ),
    )
    root = ProofStep("B", ("A",), ProofRule.INFERENCE, inference_rule=rule)
    result = make_partial_proof_result(
        n=2, k=2, status=ProofSearchStatus.COMPLETE,
        proven_steps=(given, root), conclusion="B",
    )
    return result, build_proof_narrative_model(result)


def test_dependency_is_preserved():
    result, model = _case()
    lines = build_reasoned_narrative_lines(result, model)
    assert len(lines) == 2
    assert lines[1].premise_indices == (0,)
    assert lines[1].citation_numbers == (1,)
    assert lines[1].role == "root"


def test_render_does_not_invent_mathematical_text():
    result, model = _case()
    markdown = render_reasoned_narrative_markdown(result, model)
    assert "[R1] (5.2)" in markdown
    assert "ステップ1を前提として" in markdown
    assert "数式表示未対応" in markdown
    assert "完全性より" not in markdown


def test_missing_premise_fails_closed():
    result, model = _case()
    wrong_step = replace(result.proven_steps[1], premises=("UNKNOWN",))
    changed = replace(result, proven_steps=(result.proven_steps[0], wrong_step))
    with pytest.raises(ValueError, match="unresolved premise"):
        render_reasoned_narrative_markdown(changed, build_proof_narrative_model(changed))


def test_inconsistent_model_fails_closed():
    result, model = _case()
    changed = replace(result, proven_steps=tuple(reversed(result.proven_steps)))
    with pytest.raises(ValueError, match="must match"):
        build_reasoned_narrative_lines(changed, model)
