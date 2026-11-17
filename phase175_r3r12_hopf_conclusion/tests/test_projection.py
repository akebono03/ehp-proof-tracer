"""Live public model and fail-closed cyclic Hopf-lift narrative contracts."""
from __future__ import annotations

from dataclasses import replace

import pytest

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative
from phase175_r3r12_hopf_conclusion.projection import (
    _certified_hopf_lift,
    project_verified_hopf_lift_conclusion,
)


@pytest.fixture(scope="module")
def pi73_verified():
    bridge = build_shared_typed_bridge()
    contexts = []
    result = search_group_from_registered_goal(
        n=3, k=4, bridge=bridge, context_sink=contexts.append,
    )
    assert result.status is ProofSearchStatus.COMPLETE
    assert not result.open_goals
    assert len(contexts) == 1
    citing_id = resolve_specialized_goal_citing_id(bridge, result.conclusion)
    assert citing_id is not None
    verify_proof_tree_for_narrative(
        result, contexts[0], citing_assertion_id=citing_id,
    )
    model = build_linked_proof_narrative_model(result, contexts[0])
    return result, model


def test_pi73_single_final_conclusion_and_hopf_isomorphism(pi73_verified) -> None:
    result, model = pi73_verified
    before = tuple(id(step) for step in model.steps)
    assert _certified_hopf_lift(model) is not None
    markdown = render_model_backed_narrative_markdown(result, model)
    references, body = markdown.split("\n証明\n", 1)
    summary = (
        r"[R5], [R6], [R7]より, $H(\nu'\eta_{6})=H(\nu'E\eta_{5})"
        r"=H(\nu')E\eta_{5}=\eta_{5}E\eta_{5}=\eta_{5}^{2}$."
    )
    conclusion = r"$\pi_{7}^{3} = \mathbb{Z}/2\{\nu'\eta_{6}\}$."
    assert body.count(summary) == 1
    assert body.count(conclusion) == 1, (
        "Duplicated root conclusion; root and cyclic generator renderers may differ",
        body,
    )
    assert "以上より, " + conclusion in body
    assert "\n" + conclusion + "\n" not in body
    assert r"[R4]より, $\eta_{5}^{2}$ は $\pi_{7}^{5}$ の生成元" in body
    assert "$H$ は全射." in body
    assert "すでに $H$ は単射なので, $H$ は同型." in body
    assert body.index(summary) < body.index("$H$ は全射.") < body.index("以上より, " + conclusion)
    assert "**[R2] Lemma 5.7.**" in references
    assert "**[R6] Proposition 2.2.**" in references
    assert len(model.citations) == 7
    assert before == tuple(id(step) for step in model.steps)


def test_public_generator_and_source_anchors_match_verified_image(pi73_verified) -> None:
    """The public generator is allowed a different internal source spelling."""
    from phase175_r3r12_hopf_conclusion.projection import _source_numbers
    from toda_human_readable_renderer import render_toda_public_group_generator_latex

    result, model = pi73_verified
    certificate = _certified_hopf_lift(model)
    assert certificate is not None
    scope, _, cyclic_step, positions = certificate
    codomain = cyclic_step.premises[1].conclusion
    generator = render_toda_public_group_generator_latex(codomain.rhs.generator)
    numbers = _source_numbers(model, positions[2], scope)
    markdown = render_model_backed_narrative_markdown(result, model)
    _, body = markdown.split("\n証明\n", 1)
    prefix = ", ".join(f"[R{number}]" for number in numbers) + "より, $H("
    assert len(numbers) >= 2, (numbers, generator)
    assert any(
        line.startswith(prefix) and line.endswith(f"={generator}$.")
        for line in body.splitlines()
    ), (prefix, generator, body)


def test_internal_cyclic_latex_is_not_a_second_proof_requirement(
    pi73_verified, monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Typed Hopf-lift certificate, not an internal string, owns generator identity."""
    from phase165_r12_r2_quotient_rules import CyclicStructureStatement
    from phase175_r3r12_hopf_conclusion import projection

    result, model = pi73_verified
    original_renderer = projection._group_proof_statement_latex

    def internal_cyclic_unrenderable(statement):
        if isinstance(statement, CyclicStructureStatement):
            return None, "internal cyclic spelling intentionally unavailable"
        return original_renderer(statement)

    monkeypatch.setattr(
        projection, "_group_proof_statement_latex", internal_cyclic_unrenderable,
    )
    content = render_model_backed_narrative_markdown(result, model)
    _, body = content.split("\n証明\n", 1)
    conclusion = r"$\pi_{7}^{3} = \mathbb{Z}/2\{\nu'\eta_{6}\}$."
    assert body.count(conclusion) == 1, body
    assert "すでに $H$ は単射なので, $H$ は同型." in body


def test_partial_or_missing_source_citations_are_unchanged(pi73_verified) -> None:
    _, model = pi73_verified
    text = ["使用する結果", "", "証明", "", "確認済み", "", "□"]
    assert project_verified_hopf_lift_conclusion(
        text, replace(model, status=ProofSearchStatus.PARTIAL),
    ) == text
    assert project_verified_hopf_lift_conclusion(
        text, replace(model, citations=()),
    ) == text
    assert project_verified_hopf_lift_conclusion(
        text, replace(model, root_index=None),
    ) == text
    assert _certified_hopf_lift(replace(model, citations=())) is None


def test_injectivity_line_matches_the_real_typed_renderer(pi73_verified) -> None:
    """The actual renderer emits a space after H:, unlike an old hand-coded guard."""
    from phase168_r3_27_typed_statement_projection import typed_sentence

    result, model = pi73_verified
    certificate = _certified_hopf_lift(model)
    assert certificate is not None
    _, _, cyclic_step, _ = certificate
    injective_step = cyclic_step.premises[0]
    sentence = typed_sentence(injective_step.conclusion, injective_step)
    assert sentence is not None
    assert r"$H: \pi_{7}^{3}\to \pi_{7}^{5}$ は単射." in sentence
    markdown = render_model_backed_narrative_markdown(result, model)
    _, body = markdown.split("\n証明\n", 1)
    assert sentence in body.splitlines()
    assert "すでに $H$ は単射なので, $H$ は同型." in body


def test_missing_injectivity_line_preserves_original(pi73_verified) -> None:
    """A genuinely missing injectivity display must not invent an isomorphism."""
    from phase168_r3_27_typed_statement_projection import typed_sentence

    result, model = pi73_verified
    certificate = _certified_hopf_lift(model)
    assert certificate is not None
    injective_step = certificate[2].premises[0]
    sentence = typed_sentence(injective_step.conclusion, injective_step)
    assert sentence is not None
    markdown = render_model_backed_narrative_markdown(result, model)
    # Drop only the sentence to check the fail-closed presentation contract.
    before = markdown.splitlines()
    assert before.count(sentence) == 1
    damaged = [line for line in before if line != sentence]
    assert project_verified_hopf_lift_conclusion(damaged, model) == damaged


def test_missing_rendered_summary_does_not_infer_surjectivity(pi73_verified) -> None:
    _, model = pi73_verified
    text = [
        "使用する結果", "", "証明", "",
        r"完全性より, $H:\pi_{7}^{3}\to\pi_{7}^{5}$ は単射.", "",
        r"[R4]より, $\pi_{7}^{5} = \mathbb{Z}/2\{\eta_{5}^{2}\}$.", "",
        r"$\pi_{7}^{3} = \mathbb{Z}/2\{\nu'\eta_{6}\}$.", "",
        r"以上より, $\pi_{7}^{3} = \mathbb{Z}/2\{\nu'\eta_{6}\}$.",
        "", "□",
    ]
    assert project_verified_hopf_lift_conclusion(text, model) == text


def test_pi63_old_narrative_remains_unchanged() -> None:
    bridge = build_shared_typed_bridge()
    contexts = []
    result = search_group_from_registered_goal(
        n=3, k=3, bridge=bridge, context_sink=contexts.append,
    )
    assert result.status is ProofSearchStatus.COMPLETE
    citing_id = resolve_specialized_goal_citing_id(bridge, result.conclusion)
    assert citing_id is not None
    verify_proof_tree_for_narrative(
        result, contexts[0], citing_assertion_id=citing_id,
    )
    model = build_linked_proof_narrative_model(result, contexts[0])
    markdown = render_model_backed_narrative_markdown(result, model)
    _, body = markdown.split("\n証明\n", 1)
    assert r"[R3]より, $E(\eta_{5})=\eta_{6}$." in body
    assert "[R4]より, " in body
    assert "[R3], [R4], [R5]より, " in body
    assert "すでに $H$ は単射なので, $H$ は同型." not in body
