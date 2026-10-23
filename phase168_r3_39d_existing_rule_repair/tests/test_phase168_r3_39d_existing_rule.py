from pathlib import Path

from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
from phase165_r12_r15_toda51 import build_adopted_toda51_zero_reference
from phase165_r57_r20_general_specialization import specialize_typed_statement
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from proof import ProofRule


def test_circle_general_specialization_has_guard():
    bridge = build_adopted_toda51_zero_reference(Path(__file__).resolve().parents[2] / 'phase165_r14_r39_toda51.tex')
    general = next(a.content for a in bridge.registry._assertions.values()
                   if isinstance(a.content, TodaPrimaryGroupZeroStatement)
                   and not isinstance(a.content.group.group_dimension, int))
    assert specialize_typed_statement(general, TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(2, 1))) == (('i', 2),)
    assert specialize_typed_statement(general, TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(1, 1))) is None


def test_legacy_direct_given_links_suppressed():
    bridge = build_shared_typed_bridge()
    forbidden = {f'shared:1:adopted:assertion:{i}' for i in (1, 2, 4, 6)}
    assert forbidden.isdisjoint({l.assertion_id for l in bridge.proof_links if l.step is not None and l.step.rule is ProofRule.GIVEN})
    assert forbidden.issubset(set(bridge.registry._assertions))


def test_three_group_search_still_complete():
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase165_r52_partial_proof import ProofSearchStatus
    for n, k in ((2, 1), (3, 1), (4, 1)):
        result = search_group_from_registered_goal(n=n, k=k)
        assert result.status is ProofSearchStatus.COMPLETE, (n, k, result.status)
