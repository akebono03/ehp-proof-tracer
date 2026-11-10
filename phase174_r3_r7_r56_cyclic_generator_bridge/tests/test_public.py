"""Verify independent source-first proof searches under real production sources."""
from __future__ import annotations

from homotopy_groups import TodaPrimaryGroupZeroStatement, TodaPrimaryGroup
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from proof import ProofRule


def _public_search(*, n: int, k: int, bridge):
    contexts = []
    result = search_group_from_registered_goal(
        n=n, k=k, bridge=bridge, context_sink=contexts.append,
    )
    assert result.status is ProofSearchStatus.COMPLETE
    assert not result.open_goals
    assert len(contexts) == 1
    verify_proof_tree_for_narrative(
        result, contexts[0], citing_assertion_id=None,
        derived_target_without_citing_id=True,
    )
    model = build_linked_proof_narrative_model(result, contexts[0])
    return result, model


def test_pi11_6_is_independently_proved_with_certified_generator() -> None:
    bridge = build_shared_typed_bridge()
    result, model = _public_search(n=6, k=5, bridge=bridge)
    expected = exact_prior_database_result(6, 5)
    assert expected is not None
    assert result.conclusion == expected
    assert result.proven_steps
    assert model.steps[model.root_index].rule is ProofRule.INFERENCE
    assert model.steps[model.root_index].conclusion == expected
    assert any(item.reference.locator == "Proposition 2.7"
               for item in model.citations)


def test_pi12_7_remains_source_first_complete() -> None:
    bridge = build_shared_typed_bridge()
    result, model = _public_search(n=7, k=5, bridge=bridge)
    assert isinstance(result.conclusion, TodaPrimaryGroupZeroStatement)
    assert result.conclusion.group == TodaPrimaryGroup(12, 7)
    assert model.steps[model.root_index].rule is ProofRule.INFERENCE
    assert any(item.reference.locator == "Proposition 4.2 (4.4)"
               for item in model.citations)


def test_earlier_db_result_is_not_promoted_as_same_group_given() -> None:
    from phase169_r10e4_ordered_db_prior.db_prior import admitted_db_step

    prior = exact_prior_database_result(6, 5)
    assert prior is not None
    assert admitted_db_step(prior, proof_target=prior) is None
    from homotopy_groups import TodaPrimaryGroupZeroStatement, TodaPrimaryGroup
    later = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    adopted = admitted_db_step(prior, proof_target=later)
    assert adopted is not None
    assert adopted.rule is ProofRule.GIVEN
    assert adopted.conclusion == prior
