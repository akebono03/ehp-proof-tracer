"""Real source and verified tree used only as a base for rejection tests."""
from __future__ import annotations

import pytest

from homotopy_groups import DirectSumGroup
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_29_order_projection import project_narrative_order
from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative
from phase169_r10ed_direct_sum_generality_audit.adversarial import rejection_checks
from phase169_r10ec_direct_sum_narrative_projection.projection import (
    project_verified_direct_sum_transport,
)
from proof import Relation


@pytest.fixture(scope="module")
def real_two_suspension_case():
    """Use a screened, replayed R10EC case without adding a new GIVEN."""
    bridge = build_shared_typed_bridge()
    contexts = []
    result = search_group_from_registered_goal(
        n=13, k=9, bridge=bridge, context_sink=contexts.append,
    )
    assert result.status is ProofSearchStatus.COMPLETE
    assert result.open_goals == () and len(contexts) == 1
    assert isinstance(result.conclusion, Relation)
    assert isinstance(result.conclusion.rhs, DirectSumGroup)
    citing_id = resolve_specialized_goal_citing_id(bridge, result.conclusion)
    verify_proof_tree_for_narrative(
        result, contexts[0], citing_assertion_id=citing_id,
        derived_target_without_citing_id=(citing_id is None),
    )
    model = build_linked_proof_narrative_model(result, contexts[0])
    order = tuple(entry.step_index for entry in project_narrative_order(model))
    return result, model, order


def test_r10ed_all_real_model_mutations_are_refused(real_two_suspension_case):
    _, model, order = real_two_suspension_case
    baseline = project_verified_direct_sum_transport(model, order)
    assert baseline is not None
    checks = rejection_checks(model, order)
    assert len(checks) == 9
    assert all(checks.values()), [name for name, ok in checks.items() if not ok]


def test_r10ed_rejection_checks_never_change_real_proof_tree(real_two_suspension_case):
    result, model, order = real_two_suspension_case
    step_ids = tuple(id(step) for step in model.steps)
    root_premises = tuple(id(step) for step in model.steps[model.root_index].premises)
    before_citations = model.step_citation_numbers
    assert all(rejection_checks(model, order).values())
    assert step_ids == tuple(id(step) for step in model.steps)
    assert root_premises == tuple(id(step) for step in model.steps[model.root_index].premises)
    assert before_citations == model.step_citation_numbers
    assert result.status is ProofSearchStatus.COMPLETE
