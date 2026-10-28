"""Focused regression of existing eta-only route and unrelated stable transport."""
from __future__ import annotations

import pytest

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import (
    registered_group_goal_candidates,
    search_group_from_registered_goal,
)
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase168_r3_41p13_trust_boundary.verification import verify_proof_tree_for_narrative
from phase169_r10e1_general_group_transport.transport import (
    expand_prior_general_group_transport,
)
from proof import ProofRule


@pytest.fixture(scope="module")
def shared_bridge():
    return build_shared_typed_bridge()


@pytest.mark.parametrize("n", (4, 5, 6, 30))
def test_r10eg_proved_eta_one_stem_complete(n, shared_bridge):
    """Canonical eta goals must recover independently proved original paths."""
    contexts = []
    result = search_group_from_registered_goal(
        n=n, k=1, bridge=shared_bridge, context_sink=contexts.append,
    )
    assert result.status is ProofSearchStatus.COMPLETE, result.diagnostics
    assert result.open_goals == () and result.conclusion is not None
    assert len(contexts) == 1
    root = [step for step in result.proven_steps
            if step.conclusion == result.conclusion and step.rule is ProofRule.INFERENCE]
    assert len(root) == 1
    citing = resolve_specialized_goal_citing_id(shared_bridge, result.conclusion)
    inferred, given = verify_proof_tree_for_narrative(
        result, contexts[0], citing_assertion_id=citing,
        derived_target_without_citing_id=citing is None,
    )
    assert inferred > 0 and given > 0
    if n == 4:
        assert len(result.proven_steps) == 10


@pytest.mark.parametrize("n,k", ((8, 2), (15, 8), (13, 9)))
def test_r10eg_non_one_stem_regression_stays_complete(n, k, shared_bridge):
    """Do not interfere with the independently demonstrated other-stem proofs."""
    contexts = []
    result = search_group_from_registered_goal(
        n=n, k=k, bridge=shared_bridge, context_sink=contexts.append,
    )
    assert result.status is ProofSearchStatus.COMPLETE, result.diagnostics
    assert result.open_goals == () and result.conclusion is not None
    assert len(contexts) == 1
    citing = resolve_specialized_goal_citing_id(shared_bridge, result.conclusion)
    inferred, given = verify_proof_tree_for_narrative(
        result, contexts[0], citing_assertion_id=citing,
        derived_target_without_citing_id=citing is None,
    )
    assert inferred > 0 and given > 0


def test_r10eg_source_specific_root_suppression_is_not_a_proof(shared_bridge):
    """Only the verified symbolic eta target's generic proposals are withheld."""
    from dataclasses import replace
    from homotopy_groups import FiniteCyclicGroup
    from expression import HomotopyElement

    goal, = registered_group_goal_candidates(shared_bridge, n=4, k=1)
    assert expand_prior_general_group_transport(
        goal, (), shared_bridge, proof_target=goal,
    ) == ()
    unknown_generator = replace(goal.rhs.generator, name="unregistered_eta_spelling")
    unknown = replace(goal, rhs=FiniteCyclicGroup(2, unknown_generator))
    assert unknown != goal
    # A malformed alias must not pass the eta-family shape guard. This test
    # checks the guard's precise type/identity contract, not source eligibility.
    from phase165_r12_r28_presentation_connection import _matching_eta_name
    from toda_rules import toda_eta_family_definition_statement
    assert not _matching_eta_name(
        unknown_generator, toda_eta_family_definition_statement(4).element,
    )
    assert not isinstance(goal.rhs.generator, type(None))
