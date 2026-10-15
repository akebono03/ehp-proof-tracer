"""R57-R11: target ordering is a proof-path constraint, not presentation."""
from __future__ import annotations

from phase165_r52_r12_component_bridge import expand_cited_given_components
from phase165_r52_r13_reference_registration import build_adopted_prop51_reference
from phase165_r52_r9_shared_math import shared_expansion_provider
from phase165_r57_r8_eta_specialization import (
    _fixed_typed_relations, specialize_eta_group_relation,
)
from phase165_r57_r11_proof_order_gate import (
    is_unordered_root_structure_specialization, retain_ordered_root_expansions,
)
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from proof import Relation


def _proof_fixture():
    source_bridge = build_adopted_prop51_reference()
    source, = _fixed_typed_relations(source_bridge)
    bridge = expand_cited_given_components(source_bridge)
    goal = specialize_eta_group_relation(source, 4)
    return source, bridge, goal


def test_r11_root_cannot_use_same_group_symbolic_structure():
    source, bridge, goal = _proof_fixture()
    expansions = shared_expansion_provider(bridge)(goal)
    direct = tuple(x for x in expansions if x.subgoals == (source,))
    assert len(direct) == 1
    assert is_unordered_root_structure_specialization(goal, goal, direct[0])
    assert retain_ordered_root_expansions(goal, goal, direct) == ()


def test_r11_proof_target_is_wired_to_shared_provider():
    source, bridge, goal = _proof_fixture()
    expansions = shared_expansion_provider(bridge, proof_target=goal)(goal)
    assert not any(x.subgoals == (source,) for x in expansions)


def test_r11_nonroot_goal_preserves_generic_specialization_mechanism():
    source, bridge, goal = _proof_fixture()
    other = Relation(goal.lhs, goal.rhs)
    # No proof root supplied: the generic mathematical inference remains usable.
    assert any(x.subgoals == (source,) for x in shared_expansion_provider(bridge)(other))


def test_r11_public_target_does_not_claim_unordered_direct_proof():
    result = search_group_from_registered_goal(n=4, k=1)
    assert result.status is not ProofSearchStatus.COMPLETE
    assert result.conclusion is None
    assert result.open_goals
    assert not any("higher-eta specialization" in str(s.inference_rule) for s in result.proven_steps)


def test_r11_pi32_prerequisite_path_survives():
    result = search_group_from_registered_goal(n=2, k=1)
    assert result.status is ProofSearchStatus.COMPLETE
    assert result.conclusion is not None
