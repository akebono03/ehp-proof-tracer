"""R52-R11: proof forest reuses the shared Toda narrative step renderer."""
from expression import GeneratorSymbol, HomotopyElement
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase165_r52_partial_proof import (
    ProofSearchStatus, make_partial_proof_result,
    render_partial_proof_markdown,
)
from proof import ProofRule, ProofStep, Relation, RelationType
from toda_group_proof_narrative_renderer import (
    render_toda_partial_proof_narrative_markdown,
)


def _goal():
    eta3 = HomotopyElement(
        name="η₃", dimension=3, source=4, target=3,
        generator=GeneratorSymbol(family="η", index=3),
    )
    return Relation(
        TodaPrimaryGroup(4, 3), FiniteCyclicGroup(order=2, generator=eta3),
        RelationType.EQUALITY,
    )


def test_r11_partial_and_compatibility_are_one_renderer(monkeypatch):
    import toda_group_proof_narrative_renderer as common
    seen = []
    original = common._render_generic_narrative_step

    def check(step):
        seen.append(step)
        return original(step)

    monkeypatch.setattr(common, "_render_generic_narrative_step", check)
    step = ProofStep(conclusion=_goal(), premises=(), rule=ProofRule.GIVEN)
    result = make_partial_proof_result(
        n=3, k=1, status=ProofSearchStatus.PARTIAL,
        references=("Proposition 5.1",),
        proven_steps=(step,),
        open_goals=("unresolved premise",),
    )
    text = render_partial_proof_markdown(result)
    assert seen == [step]
    assert "unresolved premise" in text
    assert "参照情報を持つ ProofStep はありません。" in text
    assert "Proposition 5.1" not in text
    assert "## 証明" in text
    assert "□" not in text
    assert "Relation(lhs=" not in text


def test_r11_unresolved_typed_goal_is_math_not_python_repr():
    result = make_partial_proof_result(
        n=3, k=1, status=ProofSearchStatus.SEARCH_FAILED,
        open_goals=(_goal(),),
        diagnostics=("expected one registered derivation for _goal, found 0",),
    )
    text = render_toda_partial_proof_narrative_markdown(result)
    assert r"\pi_{4}^{3}" in text
    assert "FiniteCyclicGroup(" not in text
    assert "expected one registered derivation" not in text
    assert "□" not in text


def test_r11_given_step_does_not_certify_completed_proof():
    import pytest
    step = ProofStep(conclusion=_goal(), premises=(), rule=ProofRule.GIVEN)
    result = make_partial_proof_result(
        n=3, k=1, status=ProofSearchStatus.COMPLETE,
        proven_steps=(step,), conclusion=_goal(),
    )
    with pytest.raises(ValueError, match="exactly one derived root"):
        render_partial_proof_markdown(result)


def test_r11_rejects_non_partial_result():
    import pytest
    with pytest.raises(TypeError):
        render_toda_partial_proof_narrative_markdown(None)


def test_r11_web_adapter_calls_common_renderer(monkeypatch):
    import phase165_r52_r3_web_adapter as adapter
    import toda_group_proof_narrative_renderer as common
    calls = []
    original = common.render_toda_partial_proof_narrative_markdown

    def observed(result):
        calls.append(result)
        return original(result)

    monkeypatch.setattr(common, "render_toda_partial_proof_narrative_markdown", observed)
    result = make_partial_proof_result(
        n=3, k=1, status=ProofSearchStatus.SEARCH_FAILED,
        open_goals=(_goal(),), diagnostics=("no matching rule",),
    )
    view = adapter.build_partial_web_group_proof_view(result)
    assert calls == [result]
    assert view.rendered_lines
