"""R4F: no post-Prop5.3 ν4 lemma used to explain cited Prop4.4."""
from __future__ import annotations

import re
from pathlib import Path

import pytest

from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import MapInjective
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase165_r52_r27_r5_literature import TodaProp44UniversalStatement
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative
from proof import ProofRule
from web_group_proof import build_standard_web_group_proof_view


@pytest.fixture(scope="module")
def pi64_narrative():
    bridge = build_shared_typed_bridge()
    screened = []
    result = search_group_from_registered_goal(
        n=4, k=2, bridge=bridge, context_sink=screened.append,
    )
    assert result.status is ProofSearchStatus.COMPLETE
    assert len(result.proven_steps) == 18
    assert result.open_goals == ()
    assert len(screened) == 1
    citing = resolve_specialized_goal_citing_id(bridge, result.conclusion)
    assert citing is not None
    verify_proof_tree_for_narrative(
        result, screened[0], citing_assertion_id=citing,
    )
    model = build_linked_proof_narrative_model(result, screened[0])
    text = render_model_backed_narrative_markdown(result, model)
    assert "\n証明\n" in text
    return result, model, *text.split("\n証明\n", 1)


def test_r4f_source_order_fibration_precedes_prop44_and_nu4_lemma_follows_prop53():
    root = Path(__file__).resolve().parents[2]
    chapter4 = (root / "sources/toda/Toda_04_2.tex").read_text(encoding="utf-8")
    chapter5 = (root / "sources/toda/Toda_05_2.tex").read_text(encoding="utf-8")
    before = chapter4.index("$n=2,4,8$ のとき, Hopf fibration")
    theorem = chapter4.index(r"\begin{proposition}\label{prop:4.4}")
    assert before < theorem
    prior_text = chapter4[before:theorem]
    assert "Hopf 不変量" in prior_text
    assert "S^{2n-1}" in prior_text
    lemma = re.search(
        r"\\begin\{lemma\}(?:\[[^\]]*\])?\s*\\label\{lem:5\.4\}", chapter5,
    )
    assert lemma is not None
    assert chapter5.index(r"\begin{proposition}\label{prop:5.3}") < lemma.start()


def test_r4f_hopf_fibration_application_is_explicit_and_citation_bound(pi64_narrative):
    _, model, reference, body = pi64_narrative
    prop44 = [c for c in model.citations
              if (c.reference.locator or c.reference.label) == "Proposition 4.4"]
    assert len(prop44) == 1
    number = prop44[0].number
    expected_map = TodaSuspensionMap(TodaPrimaryGroup(5, 3), TodaPrimaryGroup(6, 4))
    injectivity = [s for s in model.steps
                   if s.rule is ProofRule.INFERENCE
                   and isinstance(s.conclusion, MapInjective)
                   and s.conclusion.map == expected_map]
    assert len(injectivity) == 1
    assert len(injectivity[0].premises) == 1
    assert injectivity[0].premises[0].rule is ProofRule.GIVEN
    assert type(injectivity[0].premises[0].conclusion) is TodaProp44UniversalStatement
    assert f"[R{number}]" in reference
    assert r"$h:S^7\to S^4$" in body
    assert r"$\alpha=h\in\pi_7^4$" in body
    assert r"$H(\alpha)=\pm\iota_7$" in body
    assert f"[R{number}]を $(n,i)=(4,6)$ に適用できる" in body
    assert re.search(
        rf"\[R{number}\]より, \$E: \\pi_\{{5\}}\^\{{3\}}\\to \\pi_\{{6\}}\^\{{4\}}\$ は単射",
        body,
    )
    assert "nu_4" not in body and "\\nu_4" not in body
    assert "Lemma 5.4" not in body
    assert body.rstrip().endswith("□")


def test_r4f_standard_web_view_is_complete_with_application(pi64_narrative):
    result, model, reference, body = pi64_narrative
    assert len(model.citations) == 5
    all_refs = {citation.number for citation in model.citations}
    used_refs = {int(x) for x in re.findall(r"\[R(\d+)\]", body)}
    assert all_refs == used_refs
    assert "以上より" in body
    view = build_standard_web_group_proof_view(4, 2, mode="narrative")
    assert view.key == "generic-complete-proof"
    assert view.partial_result is False
    assert len(view.steps) == 18
    rendered = "\n".join(
        "".join(segment.value for segment in line.segments)
        for line in view.rendered_lines
    )
    assert r"\alpha=h\in\pi_7^4" in rendered
    assert "Hopf fibration" in rendered
    assert "(4,6)" in rendered


def test_r4f_pi53_existing_completed_narrative_unchanged():
    bridge = build_shared_typed_bridge()
    contexts = []
    result = search_group_from_registered_goal(
        n=3, k=2, bridge=bridge, context_sink=contexts.append,
    )
    assert result.status is ProofSearchStatus.COMPLETE
    assert len(result.proven_steps) == 28
    assert len(contexts) == 1
    model = build_linked_proof_narrative_model(result, contexts[0])
    markdown = render_model_backed_narrative_markdown(result, model)
    assert "Hopf fibration" not in markdown
    assert "\n証明\n" in markdown
    assert markdown.rstrip().endswith("□")
