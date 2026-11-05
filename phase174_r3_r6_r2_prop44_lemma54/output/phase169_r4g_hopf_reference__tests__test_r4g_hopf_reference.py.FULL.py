"""The pre-Proposition-4.4 source is a separately cited remark, not Proposition 4.4."""
from __future__ import annotations

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
from phase173_r4_r1_lemma54_source_bridge.source import TodaLemma54TypedSource
from phase174_r3_r6_r2_prop44_lemma54.source import (
    PRELUDE_LOCATOR,
    TodaPreProp44SplittingStatement,
    build_cited_preprop44_splitting,
    expand_cited_preprop44_splitting,
)
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
    assert result.open_goals == ()
    assert len(contexts) == 1
    citing = resolve_specialized_goal_citing_id(bridge, result.conclusion)
    assert citing is not None
    verify_proof_tree_for_narrative(result, contexts[0], citing_assertion_id=citing)
    model = build_linked_proof_narrative_model(result, contexts[0])
    markdown = render_model_backed_narrative_markdown(result, model)
    assert "\n証明\n" in markdown
    reference, body = markdown.split("\n証明\n", 1)
    return result, model, reference, body


def test_r4g_source_position_and_distinct_prelude():
    verify_prop44_hopf_fibration_source()
    root = Path(__file__).resolve().parents[2]
    text = (root / "sources/toda/Toda_04_2.tex").read_text(encoding="utf-8")
    assert text.index("$n=2,4,8$ のとき, Hopf fibration") < text.index(
        r"\begin{proposition}\label{prop:4.4}",
    )
    bridge = build_cited_preprop44_splitting()
    assert len(bridge.proof_links) == 1
    assert bridge.proof_links[0].step.conclusion == TodaPreProp44SplittingStatement()
    reference = next(iter(bridge.registry._references.values()))
    assert reference.publication_position == 7250
    assert reference.locator == PRELUDE_LOCATOR
    assert not hasattr(TodaProp44UniversalStatement(), "preceding_hopf_fibration_dimensions")


def test_r4g_refuses_edited_chapter_iv(tmp_path):
    source = Path(__file__).resolve().parents[2] / "sources/toda/Toda_04_2.tex"
    edited = tmp_path / "Toda_04_2.tex"
    edited.write_bytes(source.read_bytes().replace(b"Hopf fibration", b"changed fibration", 1))
    with pytest.raises(ValueError, match="unverified Toda Chapter IV"):
        verify_prop44_hopf_fibration_source(edited)


def test_r4g_earlier_prelude_is_cited_separately(pi64):
    _, model, reference, body = pi64
    prelude = tuple(c for c in model.citations
                    if (c.reference.locator or c.reference.label) == PRELUDE_LOCATOR)
    assert len(prelude) == 1
    assert len(prelude[0].statement_bodies) == 1
    assert r"$n=2,4,8$" in prelude[0].statement_bodies[0]
    assert "E+h_*" in prelude[0].statement_bodies[0]
    assert PRELUDE_LOCATOR in reference
    assert r"$h:S^7\to S^4$" not in body
    assert "Proposition 4.4 直前の記述" not in reference
    assert body.rstrip().endswith("□")


def test_r4g_conditional_proposition_requires_independent_hopf_witness():
    proposition = TodaProp44UniversalStatement()
    assert not hasattr(proposition, "preceding_hopf_fibration_dimensions")
    goal = MapInjective(TodaSuspensionMap(TodaPrimaryGroup(5, 3), TodaPrimaryGroup(6, 4)))
    assert expand_cited_prop44_injectivity(goal, (proposition,)) == ()
    assert len(expand_cited_prop44_injectivity(
        goal, (proposition, TodaLemma54TypedSource()),
    )) == 1
    assert expand_cited_prop44_injectivity(
        goal, (replace(proposition, includes_suspension_injectivity=False),
               TodaLemma54TypedSource()),
    ) == ()
    assert len(expand_cited_preprop44_splitting(
        goal, (TodaPreProp44SplittingStatement(),),
    )) == 1


def test_r4g_web_and_prior_pi53_still_complete(pi64):
    result, _, reference, body = pi64
    view = build_standard_web_group_proof_view(4, 2, mode="narrative")
    assert view.key == "generic-complete-proof"
    assert view.partial_result is False
    assert len(view.steps) == len(result.proven_steps)
    assert "Chapter IV" in reference
    bridge = build_shared_typed_bridge()
    contexts = []
    earlier = search_group_from_registered_goal(
        n=3, k=2, bridge=bridge, context_sink=contexts.append,
    )
    assert earlier.status is ProofSearchStatus.COMPLETE
    model = build_linked_proof_narrative_model(earlier, contexts[0])
    earlier_narrative = render_model_backed_narrative_markdown(earlier, model)
    assert r"$h:S^7\to S^4$" not in earlier_narrative
