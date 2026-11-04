"""Actual source-first Proof Tree to canonical Narrative Model to Web regressions."""
from __future__ import annotations

import pytest

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from web_group_proof import build_standard_web_group_proof_view


@pytest.fixture(scope='module')
def verified_pi74():
    bridge = build_shared_typed_bridge()
    contexts = []
    result = search_group_from_registered_goal(
        n=4, k=3, bridge=bridge, context_sink=contexts.append,
    )
    assert result.status is ProofSearchStatus.COMPLETE
    assert result.conclusion is not None and not result.open_goals
    assert contexts
    model = build_linked_proof_narrative_model(result, contexts[-1])
    return result, model


def test_prop44_reference_displays_full_isomorphism_not_prelude(verified_pi74) -> None:
    result, model = verified_pi74
    prop = tuple(c for c in model.citations
                 if (c.reference.locator or c.reference.label) == 'Proposition 4.4')
    assert len(prop) == 1
    body = '\n'.join(prop[0].statement_bodies)
    assert r'\alpha\in\pi_{2n-1}^{n}' in body
    assert r'H(\alpha)=\pm\iota_{2n-1}' in body
    assert r'\pi_{i-1}^{n-1}\oplus\pi_i^{2n-1}' in body
    assert r'\xrightarrow{\;\cong\;}' in body
    assert r'(\beta,\gamma)\longmapsto E\beta+\alpha\circ\gamma' in body
    assert r'E:\pi_{i-1}^{n-1}\to\pi_i^{n}' in body
    markdown = render_model_backed_narrative_markdown(result, model)
    assert 'Steenrod1951' not in markdown
    assert 'Proposition 4.4 直前の記述' not in markdown


def test_verified_lemma54_reference_body_is_visible(verified_pi74) -> None:
    result, model = verified_pi74
    lemma = tuple(c for c in model.citations
                  if (c.reference.locator or c.reference.label) == 'Lemma 5.4')
    assert len(lemma) == 1
    text = '\n'.join(lemma[0].statement_bodies)
    assert r'\nu_4\in\pi_7^4' in text
    assert r'H(\nu_4)=\iota_7' in text
    assert r"2E\nu_4=E^2\nu'" in text
    assert text in render_model_backed_narrative_markdown(result, model)


def test_verified_prior_database_latex_is_inline_math(verified_pi74) -> None:
    result, model = verified_pi74
    view = build_standard_web_group_proof_view(
        n=4, k=3, mode='narrative', citation_source='model',
    )
    assert view.key == 'generic-complete-proof' and not view.partial_result
    refs = tuple(line for line in view.rendered_lines if
                 any('先行データベース結果' in seg.value for seg in line.segments))
    assert refs
    assert any(any(seg.kind == 'inline_math' and r'\pi_{6}^{3}' in seg.value
                   for seg in line.segments) for line in refs)
    assert result.open_goals == model.open_goals == ()


@pytest.mark.parametrize('n,k', ((3, 3), (4, 4), (4, 7)))
def test_other_completed_groups_not_promoted_or_downgraded(n: int, k: int) -> None:
    view = build_standard_web_group_proof_view(
        n=n, k=k, mode='narrative', citation_source='model',
    )
    assert view.key == 'generic-complete-proof'
    assert not view.partial_result
    assert view.rendered_lines


@pytest.mark.parametrize('k', (8, 31))
def test_abstract_only_groups_remain_partial(k: int) -> None:
    goal = exact_prior_database_result(4, k)
    assert goal is not None
    result = search_group_from_registered_goal(n=4, k=k, goal=goal)
    view = build_standard_web_group_proof_view(
        n=4, k=k, goal=goal, mode='narrative', citation_source='model',
    )
    assert result.conclusion is None and result.open_goals
    assert result.abstract_structure is not None
    assert view.key == 'generic-partial-proof' and view.partial_result
    headings = [line.prefix for line in view.rendered_lines if line.kind == 'heading']
    assert headings.count("使用する結果") == 1
    assert headings.count("証明済みの抽象群構造") == 0
    assert headings.count("検証済みの途中経過") == 0
    assert headings.count("未解決 Goal") == 1
    assert view.abstract_structure_certified
    assert any(r"\cong" in segment.value
               for line in view.rendered_lines for segment in line.segments)
