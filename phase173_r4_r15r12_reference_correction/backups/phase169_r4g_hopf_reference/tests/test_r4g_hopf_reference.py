"""R4G: pre-Proposition 4.4 fibration is an explicitly verified Reference source."""
from __future__ import annotations

import re
from dataclasses import replace
from pathlib import Path

import pytest

from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import MapInjective
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r27_r5_literature import (
    TodaProp44UniversalStatement,
    verify_prop44_hopf_fibration_source,
)
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative
from phase169_r4b_prop44_injectivity.rule import expand_cited_prop44_injectivity
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
    citing = resolve_specialized_goal_citing_id(bridge, result.conclusion)
    assert citing is not None
    verify_proof_tree_for_narrative(result, contexts[0], citing_assertion_id=citing)
    model = build_linked_proof_narrative_model(result, contexts[0])
    text = render_model_backed_narrative_markdown(result, model)
    assert "\n証明\n" in text
    reference, body = text.split("\n証明\n", 1)
    return result, model, reference, body


def test_r4g_source_position_and_verified_hopf_prelude():
    verify_prop44_hopf_fibration_source()
    source = (Path(__file__).resolve().parents[2] / "sources" / "toda" / "Toda_04_2.tex")
    content = source.read_text(encoding="utf-8")
    prelude = content.index("$n=2,4,8$ のとき, Hopf fibration")
    proposition = content.index(r"\begin{proposition}\label{prop:4.4}")
    assert prelude < proposition
    assert r"\cite{Steenrod1951}" in content[prelude:proposition]
    assert TodaProp44UniversalStatement().preceding_hopf_fibration_dimensions == (2, 4, 8)


def test_r4g_refuses_edited_chapter_iv(tmp_path):
    source = (Path(__file__).resolve().parents[2] / "sources" / "toda" / "Toda_04_2.tex")
    changed = tmp_path / "Toda_04_2.tex"
    changed.write_bytes(source.read_bytes().replace(b"Hopf fibration", b"missing fibration", 1))
    with pytest.raises(ValueError, match="unverified Toda Chapter IV"):
        verify_prop44_hopf_fibration_source(changed)


def test_r4g_fibration_is_in_same_source_bound_reference(pi64):
    _, model, reference, body = pi64
    assert len(model.citations) == 5
    prop44 = [c for c in model.citations
              if (c.reference.locator or c.reference.label) == "Proposition 4.4"]
    assert len(prop44) == 1
    citation = prop44[0]
    assert len(citation.assertion_ids) == 1
    assert len(citation.statement_bodies) == 1  # existing R4E model API preserved
    text = citation.statement_bodies[0]
    assert "Proposition 4.4 直前の記述" in text
    assert r"$n=2,4,8$" in text
    assert r"$h:S^{2n-1}\to S^n$" in text
    assert r"$H(\alpha)=\pm\iota_{2n-1}$" in text
    assert text in reference
    assert f"[R{citation.number}]より" in body
    assert r"$h:S^7\to S^4$" in body
    assert "Lemma 5.4" not in reference + body
    assert body.rstrip().endswith("□")


def test_r4g_typed_prop44_cannot_accept_fake_fibration_metadata():
    correct = TodaProp44UniversalStatement()
    counterfeit = replace(correct, preceding_hopf_fibration_dimensions=())
    group_map = TodaSuspensionMap(TodaPrimaryGroup(5, 3), TodaPrimaryGroup(6, 4))
    assert len(expand_cited_prop44_injectivity(MapInjective(group_map), (correct,))) == 1
    assert expand_cited_prop44_injectivity(MapInjective(group_map), (counterfeit,)) == ()


def test_r4g_web_and_pi53_existing_route_unchanged(pi64):
    _, model, reference, body = pi64
    all_numbers = {c.number for c in model.citations}
    reference_numbers = {int(x) for x in re.findall(r"\*\*\[R(\d+)\]", reference)}
    body_numbers = {int(x) for x in re.findall(r"\[R(\d+)\]", body)}
    assert all_numbers == reference_numbers == body_numbers == {1, 2, 3, 4, 5}
    view = build_standard_web_group_proof_view(4, 2, mode="narrative")
    assert view.key == "generic-complete-proof"
    assert view.partial_result is False
    assert len(view.steps) == 18
    lines = ["".join(s.value for s in line.segments) for line in view.rendered_lines]
    assert any("Proposition 4.4 直前" in line for line in lines)
    bridge = build_shared_typed_bridge()
    contexts = []
    previous = search_group_from_registered_goal(n=3, k=2, bridge=bridge, context_sink=contexts.append)
    assert previous.status is ProofSearchStatus.COMPLETE
    assert len(previous.proven_steps) == 28
    model53 = build_linked_proof_narrative_model(previous, contexts[0])
    markdown53 = render_model_backed_narrative_markdown(previous, model53)
    assert "Hopf fibration" not in markdown53
