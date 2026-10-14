"""Regression checks for the pi3^2 source used by the public proposition proof."""
from pathlib import Path

from homotopy_groups import FreeCyclicGroup, TodaPrimaryGroup
from hopf_facts import ETA_2
from phase165_r14_r38_direct_registry import build_adopted_typed_reference_registry
from phase165_r52_r9_shared_math import build_shared_typed_bridge, search_shared_group_goal
from phase165_r52_partial_proof import ProofSearchStatus
from proof import ProofRule, Relation


def test_r26_r1_shared_pi32_generates_inferred_proofstep():
    root = Path(__file__).resolve().parent.parent
    bridge = build_shared_typed_bridge(sources=(
        build_adopted_typed_reference_registry(root / 'phase165_r14_r39_toda51.tex'),
    ))
    result = search_shared_group_goal(
        n=2, k=1, group_structure=FreeCyclicGroup(ETA_2), bridge=bridge,
    )
    assert result.status is ProofSearchStatus.COMPLETE
    matching = [step for step in result.proven_steps if step.conclusion == Relation(
        TodaPrimaryGroup(3, 2), FreeCyclicGroup(ETA_2)
    )]
    assert len(matching) == 1
    assert matching[0].rule is ProofRule.INFERENCE


def test_r26_r1_public_narrative_restored():
    from web_group_proof import build_standard_web_group_proof_view
    view = build_standard_web_group_proof_view(2, 1, 2, 'narrative')
    body = '\n'.join(
        line.prefix + ' ' + ' '.join(segment.value for segment in line.segments)
        for line in view.rendered_lines
    )
    assert '証明対象' in body
    assert '使用する結果' in body
    assert '証明' in body
