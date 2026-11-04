"""R4E: bibliography and body citations are owned by genuine ProofSteps."""
from __future__ import annotations

import re

import pytest

from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import MapInjective
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative
from phase165_r52_r27_r5_literature import TodaProp44UniversalStatement
from phase165_r12_r11_prop42_unified import TodaProp42GeneralExactnessStatement
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from proof import ProofRule
from web_group_proof import build_standard_web_group_proof_view


@pytest.fixture(scope="module")
def pi64():
    bridge = build_shared_typed_bridge()
    contexts = []
    result = search_group_from_registered_goal(
        n=4, k=2, bridge=bridge, context_sink=contexts.append,
    )
    assert result.status is ProofSearchStatus.COMPLETE
    assert len(result.proven_steps) == 18
    assert result.open_goals == ()
    assert len(contexts) == 1
    citing_id = resolve_specialized_goal_citing_id(bridge, result.conclusion)
    assert citing_id is not None
    verify_proof_tree_for_narrative(
        result, contexts[0], citing_assertion_id=citing_id,
    )
    model = build_linked_proof_narrative_model(result, contexts[0])
    markdown = render_model_backed_narrative_markdown(result, model)
    assert "\n証明\n" in markdown
    reference, body = markdown.split("\n証明\n", 1)
    return result, model, reference, body


def test_r4e_reference_proposition_44_has_source_bound_content(pi64):
    _, model, reference, _ = pi64
    prop44 = [c for c in model.citations
              if (c.reference.locator or c.reference.label) == "Proposition 4.4"]
    assert len(prop44) == 1
    citation = prop44[0]
    assert len(citation.assertion_ids) == 1
    assert len(citation.statement_bodies) == 1
    assert r"H(\alpha)=\pm\iota_{2n-1}" in citation.statement_bodies[0]
    assert r"E:\pi_{i-1}^{n-1}\to\pi_i^{n}" in citation.statement_bodies[0]
    assert "は単射" in citation.statement_bodies[0]
    assert citation.statement_bodies[0] in reference


def test_r4e_injectivity_tags_genuine_prop44_ancestor(pi64):
    _, model, _, body = pi64
    citation = next(c for c in model.citations
                    if (c.reference.locator or c.reference.label) == "Proposition 4.4")
    target_map = TodaSuspensionMap(TodaPrimaryGroup(5, 3), TodaPrimaryGroup(6, 4))
    injectivity = [step for step in model.steps
                   if step.rule is ProofRule.INFERENCE
                   and isinstance(step.conclusion, MapInjective)
                   and step.conclusion.map == target_map]
    assert len(injectivity) == 1
    assert any(p.rule is ProofRule.GIVEN
               and type(p.conclusion) is TodaProp44UniversalStatement
               for p in injectivity[0].premises)
    assert re.search(
        rf"\[R{citation.number}\]より, \$E: \\pi_\{{5\}}\^\{{3\}}\\to \\pi_\{{6\}}\^\{{4\}}\$ は単射",
        body,
    )


def test_r4e_ehp_window_has_proposition42_citation(pi64):
    _, model, _, body = pi64
    citation = next(c for c in model.citations
                    if (c.reference.locator or c.reference.label) == "Proposition 4.2 (4.4)")
    assert any(step.rule is ProofRule.GIVEN
               and type(step.conclusion) is TodaProp42GeneralExactnessStatement
               for step in model.steps)
    assert f"[R{citation.number}]より, " in body
    assert re.search(rf"\[R{citation.number}\]より, \$\\pi_\{{5\}}\^\{{3\}}", body)
    assert "は完全." in body


def test_r4e_reference_and_body_citation_sets_coincide(pi64):
    _, model, reference, body = pi64
    numbers = {c.number for c in model.citations}
    assert len(numbers) == 5
    reference_numbers = [int(value) for value in re.findall(r"\*\*\[R(\d+)\]", reference)]
    body_numbers = {int(value) for value in re.findall(r"\[R(\d+)\]", body)}
    assert set(reference_numbers) == body_numbers == numbers
    assert len(reference_numbers) == len(numbers)
    assert body.rstrip().endswith("□")
    assert "未解決 Goal" not in body


def test_r4e_standard_web_path_remains_verified_and_complete():
    view = build_standard_web_group_proof_view(4, 2, mode="narrative")
    assert view.key == "generic-complete-proof"
    assert view.partial_result is False
    assert len(view.steps) == 18
    assert len(view.rendered_lines) >= 20
    rendered = ["".join(segment.value for segment in line.segments)
                for line in view.rendered_lines]
    assert any("[R2]より" in text and "単射" in text for text in rendered)
    assert any("[R3]より" in text and "は完全" in text for text in rendered)
